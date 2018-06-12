import time
import socket
import threading
import atexit



#
# Config
#
base_port = 56000
start_msg = "<19853732 start>"
end_msg = "<19853732 end>"
stop_msg = "<19853732 stop>"

#
# Create sockets
#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', base_port))
s.listen(5)

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.bind(('', base_port+1))
s2.listen(5)

def exit_handler():
    global s, s2
    s.close()
    s2.close()

atexit.register(exit_handler)


#
# Main loop program side
#
def program_worker():
    global web_output, s2, running
    while True:
        conn, addr = s2.accept()
        msg = conn.recv(10240)
        if msg == start_msg.encode('utf-8'):
            web_output = b'Executing program...\n'
            running = True
        elif msg == end_msg.encode('utf-8'):
            web_output = web_output + b'Terminated'
            running = False
        else:
            web_output = web_output + msg
        conn.close()

running = False
web_output = b'No program executed'
t = threading.Thread(target=program_worker)
t.start()


#
# Main loop web side
#
while True:
    conn, addr = s.accept()
    msg = conn.recv(3)
    
    if msg == b'get':
        if running:
            answer = web_output
        else:
            answer = web_output + stop_msg.encode('utf-8')
        try:
            totalsent = 0
            while totalsent < len(answer):
                sent = conn.send(answer[totalsent:])
                if sent == 0:
                    break
                totalsent = totalsent + sent
        except BrokenPipeError:
            pass

    conn.close()


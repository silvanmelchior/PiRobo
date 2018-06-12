import time
import socket
import threading
import atexit



#
# Config
#
base_port = 56000


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
    global web_output, s2
    while True:
        conn, addr = s2.accept()
        msg = conn.recv(102400) # TODO
        web_output = web_output + msg
        conn.close()

web_output = b''
t = threading.Thread(target=program_worker)
t.start()


#
# Main loop web side
#
while True:
    conn, addr = s.accept()
    msg = conn.recv(3)
    
    if msg == b'get':
        answer = web_output
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


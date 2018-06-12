import sys
import atexit
import socket


base_port = 56000
start_msg = "<19853732 start>"
end_msg = "<19853732 end>"


def send_msg(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', base_port+1))
    msg_new = msg.encode('utf-8')
    totalsent = 0
    while totalsent < len(msg_new):
        sent = s.send(msg_new[totalsent:])
        if sent == 0:
            break
        totalsent = totalsent + sent
    s.close()



send_msg(start_msg)

def exit_handler():
    send_msg(end_msg)

atexit.register(exit_handler)

for line in sys.stdin:
    send_msg(line)

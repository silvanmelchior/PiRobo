import sys
import atexit
import socket


base_port = 56000
start_msg = "<19853732 start>"
end_msg = "<19853732 end>"


def send_msg(msg, offset):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', base_port+offset))
    msg_new = msg.encode('utf-8')
    totalsent = 0
    while totalsent < len(msg_new):
        sent = s.send(msg_new[totalsent:])
        if sent == 0:
            break
        totalsent = totalsent + sent
    s.close()



send_msg(start_msg, 1)

def exit_handler():
    send_msg(end_msg, 1)
    send_msg("motor 0 0", 10)

atexit.register(exit_handler)

for line in sys.stdin:
    send_msg(line, 1)

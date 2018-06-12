import sys
import atexit
import socket


base_port = 56000
start_msg = "Executing program...\n"
end_msg = "Terminated\n"


def send_msg(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', base_port+1))
    msg_new = msg.encode('utf-8')
    s.send(msg_new) # TODO
    s.close()



send_msg(start_msg)

def exit_handler():
    send_msg(end_msg)

atexit.register(exit_handler)

for line in sys.stdin:
    send_msg(line)

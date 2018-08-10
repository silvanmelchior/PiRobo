import os
import socket

#
# Config
#
base_port = 56000
discovery_msg = b'PiRobo discover'
halt_msg = b'PiRobo halt'
reboot_msg = b'PiRobo reboot'
sw_file = "/../VERSION.txt"
hw_file = "/../ID.txt"



#
# Read Versions
#
def file_get_contents(filename):
    with open(filename) as f:
        return f.read()
directory = os.path.dirname(os.path.realpath(__file__))
sw_version = file_get_contents(directory + sw_file).split()[0]
hw_version = file_get_contents(directory + hw_file).split()[0]
answer_msg = 'v1 ' + sw_version + ' ' + hw_version


#
# Create Sockets
#
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',base_port+100))


#
# Main Loop
#
while True:
    m = s.recvfrom(1024)
    if m[0] == discovery_msg:
        s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s2.sendto(answer_msg.encode('utf-8') ,m[1])
    elif m[0] == halt_msg:
        os.system('halt')
    elif m[0] == reboot_msg:
        os.system('reboot')


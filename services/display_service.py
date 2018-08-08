import os
import time
import smbus
import subprocess
import psutil
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from wifi import Cell, Scheme


#
# Config
#
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
padding = -2
x = 0
sw_file = "/../VERSION.txt"
hw_file = "/../ID.txt"
PCF8574 = 0x20
js_empty = 0xff
js_up = 0xfe
js_left = 0xfb
js_down = 0xfd
js_right = 0xf7
js_enter = 0xef
line_len = 11


#
# PWD chars
#
pwd_chars = [chr(a) for a in range(65, 91)]
pwd_chars += [chr(a) for a in range(97, 123)]
pwd_chars += [chr(a) for a in range(48, 58)]
pwd_chars += [chr(a) for a in range(32, 48)]
pwd_chars += [chr(a) for a in range(58, 65)]
pwd_chars += [chr(a) for a in range(91, 97)]
pwd_chars += [chr(a) for a in range(123, 127)]


#
# Init HW
#
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
top = padding
bottom = height-padding
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
font = ImageFont.load_default()
joystick = smbus.SMBus(1)
joystick.write_byte(PCF8574, 0xff)


#
# Read Versions
#
def file_get_contents(filename):
    with open(filename) as f:
        return f.read()
directory = os.path.dirname(os.path.realpath(__file__))
sw_version = file_get_contents(directory + sw_file).split()[0]
hw_version = file_get_contents(directory + hw_file).split()[0]


#
# Display Functions
#
def main_screen():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    cmd = "iwgetid -r"
    try:
        SSID = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        SSID = "<no wifi>"
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    draw.text((x, top),    "SSID: " + SSID, font=font, fill=255)
    draw.text((x, top+8),  "IP: " + IP.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top+16), "CPU Usage: " + str(psutil.cpu_percent()) + "%",  font=font, fill=255)
    draw.text((x, top+25), "V " + sw_version + "  ID " + hw_version,  font=font, fill=255)
    disp.image(image)
    disp.display()


def main_menu(item):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top),    "MAIN MENU", font=font, fill=255)
    draw.text((x, top+9),  (">" if item == 0 else " ") + " Shutdown", font=font, fill=255)
    draw.text((x, top+17), (">" if item == 1 else " ") + " Reboot", font=font, fill=255)
    draw.text((x, top+25), (">" if item == 2 else " ") + " Change Wifi", font=font, fill=255)
    disp.image(image)
    disp.display()


def scanning_screen():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), "SCANNING...", font=font, fill=255)
    disp.image(image)
    disp.display()


def ssid_menu(cell, item):
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), "CHOOSE SSID", font=font, fill=255)
    start = item-2 if item > 2 else 0
    if start+0 < len(cell):
        draw.text((x, top+9),  ("> " if item == 0 else "  ") + cell[start+0].ssid, font=font, fill=255)
    if start+1 < len(cell):
        draw.text((x, top+17), ("> " if item == 1 else "  ") + cell[start+1].ssid, font=font, fill=255)
    if start+2 < len(cell):
        draw.text((x, top+25), ("> " if item >= 2 else "  ") + cell[start+2].ssid, font=font, fill=255)
    disp.image(image)
    disp.display()


def pwd_menu_top(item, pwd):
    sel_x = item%line_len
    sel_y = int(item/line_len)
    start = sel_y-1 if sel_y > 1 else 0
    block = sel_y if sel_y <= 1 else 1
    
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), "PWD: " + pwd[-15:], font=font, fill=255)
    if item == 0:
        draw.text((x, top+7), "> DEL    OK    EXIT", font=font, fill=255)
    elif item == 1:
        draw.text((x, top+7), "  DEL  > OK    EXIT", font=font, fill=255)
    elif item == 2:
        draw.text((x, top+7), "  DEL    OK  > EXIT", font=font, fill=255)
    offset = [15, 23]
    for i in range(2):
        line = ""
        for j in range(line_len):
            line += " " if j != 0 else ""
            line += pwd_chars[i*line_len + j]
        draw.text((1, top+offset[i]),  line, font=font, fill=255)
    disp.image(image)
    disp.display()


def pwd_menu(item, pwd):
    sel_x = item%line_len
    sel_y = int(item/line_len)
    start = sel_y-1 if sel_y > 1 else 0
    block = sel_y if sel_y <= 1 else 1
    
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), "PWD: " + pwd[-15:], font=font, fill=255)
    draw.text((x, top+7), "  DEL    OK    EXIT", font=font, fill=255)
    offset = [15, 23, height]
    for i in range(2):
        line = ""
        end = line_len if start+i != int(len(pwd_chars)/line_len) else len(pwd_chars) % line_len
        for j in range(end):
            line += " " if j != 0 else ""
            line += pwd_chars[(start+i)*line_len + j]
        draw.text((1, top+offset[i]),  line, font=font, fill=255)
    draw.rectangle((sel_x*11.8-0.5,offset[block]-1,sel_x*11.8+8.7,offset[block+1]), outline=0, fill=255)
    draw.text((1+sel_x*12,top+offset[block]), pwd_chars[sel_y*line_len + sel_x], font=font, fill=0)
    disp.image(image)
    disp.display()


def update_wifi(ssid, pwd):
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f: 
        f.write('ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n') 
        f.write('update_config=1\n') 
        f.write('\n') 
        f.write('network={\n') 
        f.write('  ssid="' + ssid + '"\n') 
        f.write('  psk="' + pwd + '"\n') 
        f.write('}\n') 


def shutdown():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), "SHUTING DOWN...", font=font, fill=255)
    draw.text((x, top+9), "Please wait > 15s,", font=font, fill=255)
    draw.text((x, top+17), "then turn off the", font=font, fill=255)
    draw.text((x, top+25), "robot.", font=font, fill=255)
    disp.image(image)
    disp.display()
    os.system('halt')


def reboot():
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), "Rebooting...", font=font, fill=255)
    draw.text((x, top+17), "Please wait", font=font, fill=255)
    disp.image(image)
    disp.display()
    os.system('reboot')


#
# Main Loop
#
loop_cnt = 10000
state = 0
state_bak = 0
pins_bak = js_empty
cell = []
pwd = ""
while True:

    # check input
    pins = joystick.read_byte(PCF8574)
    if state == 0:
        if pins != js_empty:
            state = 10
    elif state >= 10 and state <= 12:
        if pins == js_enter:
            if state == 10:
                state = 10000
            if state == 11:
                state = 10001
            if state == 12:
                state = 100
        elif pins == js_left:
            state = 0
            loop_cnt = 1000
        elif pins == js_down and pins_bak != js_down:
            state = state + 1 if state < 12 else 10
        elif pins == js_up and pins_bak != js_up:
            state = state - 1 if state > 10 else 12
    elif state >= 200 and state <= 199+len(cell):
        if pins == js_enter:
            sel_wifi = state-200
            pwd = ""
            state = 1000
        elif pins == js_left:
            state = 10
        elif pins == js_down and pins_bak != js_down:
            state = state + 1 if state < 199+len(cell) else 200
        elif pins == js_up and pins_bak != js_up:
            state = state - 1 if state > 200 else 199+len(cell)
    elif state >= 1000 and state <= 999+len(pwd_chars):
        if pins == js_enter and pins_bak != js_enter:
            sel_x = (state-1000)%line_len
            sel_y = int((state-1000)/line_len)
            pwd += pwd_chars[sel_y*line_len + sel_x]
            pwd_menu(state-1000, pwd)
        elif pins == js_left:
            state = state - 1 if state > 1000 else 999+len(pwd_chars)
        elif pins == js_down:
            state = state + line_len
            if state > 999+len(pwd_chars):
                state = 2000
        elif pins == js_up:
            state -= line_len
            if state < 1000:
                state = 2000
        elif pins == js_right:
            state = state + 1 if state < 999+len(pwd_chars) else 1000
    elif state >= 2000 and state <= 2002:
        if pins == js_enter and pins_bak != js_enter:
            if state == 2000:
                pwd = pwd[:-1]
                pwd_menu_top(state-2000, pwd)
            elif state == 2001:
                update_wifi(cell[sel_wifi].ssid, pwd)
                state = 10001
            elif state == 2002:
                state = 10
        elif pins == js_left:
            state = state - 1 if state > 2000 else 2002
        elif pins == js_down:
            state = 1000
        elif pins == js_up:
            state = 999+len(pwd_chars)
        elif pins == js_right:
            state = state + 1 if state < 2002 else 2000
    
    # show screens
    if state == 0:
        loop_cnt += 1
        if loop_cnt >= 40:
            main_screen()
            loop_cnt = 0
    elif state >= 10 and state <= 12 and state_bak != state:
        main_menu(state-10)
    elif state == 100 and state_bak != 100:
        scanning_screen()
        cell = list(Cell.all('wlan0'))
        state = 200
        ssid_menu(cell, state-200)
    elif state >= 200 and state <= 199+len(cell) and state_bak != state:
        ssid_menu(cell, state-200)
    elif state >= 1000 and state <= 999+len(pwd_chars) and state != state_bak:
        pwd_menu(state-1000, pwd)
    elif state >= 2000 and state <= 2002 and state != state_bak:
        pwd_menu_top(state-2000, pwd)
    elif state == 10000 and state != state_bak:
        shutdown()
    elif state == 10001 and state != state_bak:
        reboot()
    
    # wait
    pins_bak = pins
    state_bak = state
    time.sleep(0.05)



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
    SSID = subprocess.check_output(cmd, shell=True)
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    draw.text((x, top),    "SSID: " + SSID.decode('utf-8'), font=font, fill=255)
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
    print(item)
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    draw.text((x, top), "CHOOSE SSID", font=font, fill=255)
    start = item-2 if item > 2 else 0
    # TODO: if exists
    if start+0 < len(cell):
        draw.text((x, top+9),  ("> " if item == 0 else "  ") + cell[start+0].ssid, font=font, fill=255)
    if start+1 < len(cell):
        draw.text((x, top+17), ("> " if item == 1 else "  ") + cell[start+1].ssid, font=font, fill=255)
    if start+2 < len(cell):
        draw.text((x, top+25), ("> " if item >= 2 else "  ") + cell[start+2].ssid, font=font, fill=255)
    disp.image(image)
    disp.display()


#
# Main Loop
#
loop_cnt = 10000
state = 0
state_bak = 0
pins_bak = js_empty
while True:

    # check input
    pins = joystick.read_byte(PCF8574)
    if state == 0:
        if pins != js_empty:
            state = 10
    elif state >= 10 and state <= 12:
        if pins == js_enter:
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
            ...
        elif pins == js_left:
            state = 10
        elif pins == js_down and pins_bak != js_down:
            state = state + 1 if state < 199+len(cell) else 200
        elif pins == js_up and pins_bak != js_up:
            state = state - 1 if state > 200 else 199+len(cell)
    
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
        print(cell)
        state = 200
        ssid_menu(cell, state-200)
    elif state >= 200 and state <= 199+len(cell) and state_bak != state:
        ssid_menu(cell, state-200)
    
    # wait
    pins_bak = pins
    state_bak = state
    time.sleep(0.05)



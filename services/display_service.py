import os
import time
import subprocess
import psutil
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


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


#
# Init Display
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
# Main Loop
#
while True:

    # Clear image
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Get data
    cmd = "iwgetid -r"
    SSID = subprocess.check_output(cmd, shell=True)
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)

    # Draw data
    draw.text((x, top),    "SSID: " + SSID.decode('utf-8'), font=font, fill=255)
    draw.text((x, top+8),  "IP: " + IP.decode('utf-8'),  font=font, fill=255)
    draw.text((x, top+16), "CPU Usage: " + str(psutil.cpu_percent()) + "%",  font=font, fill=255)
    draw.text((x, top+25), "V " + sw_version + "  ID " + hw_version,  font=font, fill=255)

    # Display data
    disp.image(image)
    disp.display()
    time.sleep(2)


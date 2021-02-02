  
# updated for python3, Russ Feb 1, 2021
# https://github.com/rottenoasis
# use python3 to exexute!
import os, json, datetime
from urllib.request import urlopen
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from gpiozero import CPUTemperature, LoadAverage, DiskUsage

inky_display = InkyPHAT("red") # RED because thats the color I have
inky_display.set_border(inky_display.WHITE)

# get the current time. Runs every 10 minutes from crontab
current_time = datetime.datetime.now()

# Set current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load graphic. Not used here because the screen is all text
# UNcomment the next line to show a graphic. Be sure to comment OUT the one after that
#img = Image.open("./logo.png")
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img) 

# get the api data
try:
  f = urlopen('http://pi.hole/admin/api.php')
  json_string = f.read()
  parsed_json = json.loads(json_string)
  adsblocked = parsed_json['ads_blocked_today']
  ratioblocked = parsed_json['ads_percentage_today']
  dnsqueries = parsed_json['dns_queries_today']
  clients = parsed_json['unique_clients']
  f.close()
except:
  adsblocked = 'wtf?'
  ratioblocked = 'something wrong'
  # have not seen an exception yet

# Get the temperature
cpu = CPUTemperature()
cpu_temp = str(round(cpu.temperature,1)) + chr(176) + "C"

# Get the load average
load = LoadAverage(min_load_average = 0, max_load_average = 1.0)
cpu_load = str(load.value)

# Get the disk usage percentage
du = DiskUsage()
disk_use = str(round(du.usage,1))

# Set the font
font = ImageFont.truetype(FredokaOne, 19)
# draw the display
draw.text((20,0), str(current_time.strftime("%Y-%m-%d %H:%M:%S")),inky_display.RED, font)
draw.text((20,17), "CPU:" + str(cpu_load) + " DSK:" + str(disk_use) + "%", inky_display.BLACK, font)
draw.text((20,34), "BLOCKED: " + str(adsblocked), inky_display.RED, font)
draw.text((20,51), str(round(ratioblocked,2)) + "% " + str(cpu_temp), inky_display.BLACK, font)
draw.text((20,68), "QUERIES: " + str(dnsqueries), inky_display.RED, font)
draw.text((20,85), "CLIENTS: " + str(clients), inky_display.BLACK, font)
inky_display.set_image(img)

# rotate the display
flipped = img.rotate(180)
inky_display.set_image(flipped)

inky_display.show()

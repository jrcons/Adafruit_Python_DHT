#!/usr/bin/python
# Copyright (c) 2017 Rolls-Royce plc
# Author: Adrian Rotaru
# 
# htout.py : Get DHT11 sensor readings (humidity and temperature); 
#   create/update CSV file with readings; post readings to a Maximo dev instance using REST API

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import sys
import Adafruit_DHT
import csv
import socket
import time, os, fnmatch, shutil

#DHT sensor variables
sensor = Adafruit_DHT.DHT11
pin = 4
#Hostname variable
hostname = socket.gethostname()
#Get current humidity and temperature from sensor
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
#Timestamp variable - used for file name and TimeStamp CSV column
t = time.localtime()
timestamp = time.strftime('%Y-%m-%d_%H%M', t)
#path of csv file
csv_path = '/home/pi/bpc_temp_humidity/readings/'
#csv file name - unique
csv_name_unique      = (csv_path + "bpc_hum_temp_" + hostname + ".csv")
#csv file name - timestamped
csv_name_timestamped = (csv_path + "bpc_hum_temp_" + hostname + "_" + timestamp + ".csv")
#asset number
asset="BRI-MO-01"
#URLs for Maximo REST API request
url_humidity    = ('https://cns-mx76av.cfms.org.uk/maxrest/rest/os/mxmeterdata?_actio=AddChange&ASSETNUM='+asset+'&METERNAME=HUMIDITY&_lid=rotarua&_lpwd=Rollsroyce1&SITEID=BEDFORD')
url_temperature = ('https://cns-mx76av.cfms.org.uk/maxrest/rest/os/mxmeterdata?_actio=AddChange&ASSETNUM='+asset+'&METERNAME=TEMP-C&_lid=rotarua&_lpwd=Rollsroyce1&SITEID=BEDFORD')


#Create and write into CSV file - new file at each script run
with open(csv_name_timestamped, 'w') as csvfile:
    fieldnames = ['Humidity','Temperature','Hostname','TimeStamp']
    writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
    writer.writeheader()
    writer.writerow({'Humidity': humidity, 'Temperature': temperature, 'Hostname': hostname,'TimeStamp': timestamp})

#Open unique csv file name and append
writearg = [humidity,temperature,hostname,timestamp]
with open (csv_name_unique, 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(writearg)
    
#Post readings into Maximo using REST API request
r_humidity=requests.post(url_humidity,data={'NEWREADING': humidity})
r_temperature=requests.post(url_temperature,data={'NEWREADING': temperature})

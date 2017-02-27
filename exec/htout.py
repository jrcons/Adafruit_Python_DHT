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

#set path of csv file
csv_path = '/home/pi/bpc_temp_humidity/readings/'
#set csv file name - unique
csv_name_unique      = (csv_path + "bpc_hum_temp_" + hostname + ".csv")
#set csv file name - timestamped
csv_name_timestamped = (csv_path + "bpc_hum_temp_" + hostname + "_" + timestamp + ".csv")

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

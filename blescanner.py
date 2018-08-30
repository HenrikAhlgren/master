#import bluetooth
from bluepy.btle import Scanner
import time
import paho.mqtt.publish as publish
MQTT_SERVER = "192.168.1.6"
#:1883
sleep_time = 60
known_devices = [['1','54:60:09:60:06:0D','away',0],['2','54:60:09:60:06:0D','away',0],['3','FF:FF:C2:00:1A:E0','away',0],['4','FF:FF:C4:00:52:36','away',0]]
first = 'true'
while True:
   device_found = "N"
   time.sleep(sleep_time)
   scanner = Scanner()
   devices = scanner.scan(10.0)
   #for color, value in known_devices.items():
   for x in range(0, 4):
      device_found = "N"
      for dev in devices:
        if known_devices[x][1] ==  dev.addr:
           device_found = "Y"
           break
      if device_found == "Y" and known_devices[x][2] == 'away':
         publish.single("location/"+known_devices[x][0], "home", hostname=MQTT_SERVER)
         known_devices[x][2] = 'home'
         known_devices[x][3] = 0
      if device_found == "N" and known_devices[x][2] == 'home':
         known_devices[x][3] = known_devices[x][3] +1
         if known_devices[x][3] == 4:
            known_devices[x][2] = 'away'
            known_devices[x][3] = 0
            publish.single("location/"+known_devices[x][0], "away", hostname=MQTT_SERVER)
            
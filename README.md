# PiHoleOledDisplay

Inspired by willdurand/pihole-oled, I updated to work with the newest version of the Adafruit lib and other updates

## Hardware

- Oled display 0,96" 128x32
- Raspberry pi 

### How to connect the Oled and the Raspberry pi

![alt text](https://github.com/inonoob/PiHoleOledDisplay/blob/master/res/Oled-Pi-connection_Steckplatine.png)

### Connect oled display with the Rasperberry Pi:  

## Software 

## Prerequisite 

Have a Raspberry Pi with the lastest Raspbian installed

## Installation of needed packages

Download the following packages

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install i2c-tools
sudo apt-get install pip3
sudo apt install python3-pip
sudo pip3 install Pillow
sudo apt-get install libopenjp2-7 libtiff5
pip3 install adafruit-circuitpython-ssd1306
pip3 install humanize
pip3 install psutil
pip3 install requests
```


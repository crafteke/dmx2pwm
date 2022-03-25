# README #

Bridge between OLA daemon and GPIO softPWM.
### Dependencies

* python > 3.6
* pip3 install ola RPi.GPIO
* install OLA daemon first (see snippets rpi dmx)

### service installation

 Copy dmx2pwm.service to /etc/systemd/system/dmx2pwm.service  
   
Content:
  
```
[Unit]
Description=PWM DMX bridge
After=olad.service
[Service]
ExecStart=/usr/bin/python3 -u lightDMXcontroller.py
WorkingDirectory=/home/pi/dmx2pwm/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
### Service control
```
sudo sytemctl reload-daemon
sudo systemctl start dmx2pwm
sudo systemctl status dmx2pwm (check status)
sudo systemctl enable dmx2pwm
```
### OLA config
For reference see: https://www.openlighting.org/ola/advanced-topics/patch-persistency/#ola-portconf

#create universe in /etc/ola/ola-universe.conf 
uni_X_merge = LTP
uni_X_name = Universe X

#patch port to universe in /etc/ola/ola-port.conf 
2-1-I-0 = X # X is universe 
2-1-I-0_priority_value = 100

#run for test
olad --config-dir /etc/ola

#listing devices
ola_device_info

### OLA python patching (workaround for issue with comparators)
#update apt
sudo apt update
sudo apt upgrade
sudo apt-get install ola
sudo apt-get install ola-rdm-tests
#check if http://[hostname].local:9090 is reachable
#install ola python wrapper
pip3 install ola
#patch ola if version 0.10.7
wget https://bitbucket.org/oxykube/workspace/snippets/B9B7dK
/home/pi/.local/lib/python3.7/site-packages/ola/ClientWrapper.py
#install pip3
sudo apt install python3-pip 

### Hostname & DMX node autoconfig
Add `/home/pi/hostname_config.sh` in /etc/rc.local
Set the config file dmx.config in /boot
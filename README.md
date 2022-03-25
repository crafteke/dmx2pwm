# README #

Bridge between OLA daemon and GPIO softPWM.
## Dependencies

* python > 3.6
* pip3, RPi.GPIO, olad, ola (python wrapper)
* install OLA daemon first (see below)

## OLA setup and config

For reference see: https://www.openlighting.org/ola/advanced-topics/patch-persistency/#ola-portconf

create universe in /etc/ola/ola-universe.conf  (not working, TODO find the static config file of olad)
```
uni_X_merge = LTP
uni_X_name = Universe X
```
patch port to universe in /etc/ola/ola-port.conf (not working, TODO find the static config file of olad)
```
2-1-I-0 = X # X is universe 
2-1-I-0_priority_value = 100
```
run for test
```
olad --config-dir /etc/ola
```

listing devices
```
ola_device_info
```
Fix the usb device bug(see in logs: common/io/Serial.cpp:151: Device /dev/ttyUSB0 doesn't exist, so there's no point trying to acquire a lock)
```
sudo rm /etc/ola/ola-stageprofi.conf;sudo echo -e 'device = /dev/ttyUSB0\nenabled = false\n' > /etc/ola/ola-stageprofi.conf 

```
Activate the USB FTDI / DMX plugin (if needed)
```
disable USB serial
/etc/ola/ola-usbserial.conf
disable enttec open DMX
/etc/ola/ola-opendmx.conf
enable FTDI
/etc/ola/ola-ftdidmx.conf
```

### OLA python patching (workaround for issue with comparators)
update apt and install ola
```
sudo apt update
sudo apt upgrade
sudo apt-get install ola
sudo apt-get install ola-rdm-tests

pip3 install ola

```
check if http://[hostname].local:9090 is reachable.

### Patch ola if version 0.10.7
```
cp ClientWrapper.py /home/pi/.local/lib/python3.7/site-packages/ola/ClientWrapper.py
```

## service installation

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

### Hostname (to move to vanillaPi) & DMX node autoconfig TODO:Split dmx and rpi config (for name, device, sio server...)
Add `/home/pi/hostname_config.sh` in /etc/rc.local
Set the config file dmx.config in /boot
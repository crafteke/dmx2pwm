# README #

Bridge between OLA daemon and GPIO softPWM.
### Dependencies

* python > 3.6
* pip3 install ola RPi.GPIO
* install OLA daemon first (see snippets rpi dmx)

### service installation

* create /etc/systemd/system/dmx2pwm.service
Content:
[Unit]
Description=PWM DMX bridge
After=olad.service

[Service]
ExecStart=/usr/bin/python3 -u lightDMXcontroller.py
WorkingDirectory=/home/pi/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target

### Service control

sudo sytemctl reload-daemon
sudo systemctl start dmx2pwm
sudo systemctl status dmx2pwm (check status)
sudo systemctl enable dmx2pwm

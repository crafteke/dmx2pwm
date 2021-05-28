#!/bin/bash

### BEGIN INIT INFO
# Provides:          setting hostname from boot config file
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Changing hostname
# Description:       Changing hostname to config
### END INIT INFO


old=$(cat /etc/hostname)
new=$(cat /boot/dmx.config | grep name | awk '{print $2}')
if [ $new != $old ]
then
  echo "Hostname setup..."
  service network-manager stop
  sed -i "s/$old/$new/g" /etc/hosts
  sed -i "s/$old/$new/g" /etc/hostname
  hostname "$new"
  service network-manager start
  echo "Done." 
fi
exit 0

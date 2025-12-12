#!/bin/bash

# Intro

# actual_version=$( cat /etc/os-release | grep "VERSION" | head -n 2 | tail -n 1 | sed 's/[^0-9.]//g' )

latest_os_upgrade=$( grep "upgrade linux-image" /var/log/dpkg.log | tail -n 1 | sed "s/ .*//" )
current_os=$( uname -a )

echo "-- System Status --"
echo "Your system was last updated on $latest_os_upgrade."
echo "Current OS : $current_os."
echo
echo "-- sudo users --"
getent group sudo

# EOF

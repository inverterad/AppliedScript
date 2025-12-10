#!/bin/bash
# Detta script samlar in systeminformation - RECON
#
# Author: Fredrik Karlsson
# Last Update: 2025-12-09
datum=$( date "+%F" )

exec > >(tee -a logg_$datum.txt) 2>&1
date	
echo "Välkommen till mitt RECON script för att kontrollera en Linux-miljö"
echo
echo "=== SYSTEMINFO ==="
uname -a

echo
echo "=== AKTUELL ANVÄNDARE ==="
echo $USER

echo
echo "=== ANVÄNDARE MED SHELL ==="
grep "sh$" /etc/passwd

echo
echo "=== NÄTVERK ==="
ip a | grep inet
echo
netstat -t -u

echo
echo "=== HÅRDVARA ==="
echo 
lscpu | grep "CPU(s):" | head -1
lscpu | grep "Model name"
echo
free -h
echo
df -h | grep -v "tmpfs"
echo
echo "=== PLATS ==="
echo

country=$( curl -s https://ipapi.co/json/ | grep "country_code_iso3" | sed -e "s/[^ a-zA-Z']//g" -e 's/country.[^[:space:]]*//' -e 's/ \+/ /' )
city=$( curl -s https://ipapi.co/json/ | grep "city" | sed -e "s/[^ a-zA-Z']//g" -e 's/ci.[^[:space:]]*//' -e 's/ \+/ /' )

echo "Land: $country"
echo "Stad: $city"
echo


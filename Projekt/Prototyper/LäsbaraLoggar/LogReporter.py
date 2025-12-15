#!/usr/bin/env python3

#“Human-Readable Security Reports” from Raw Data
# Many logs are unreadable.
# Your script could take messy input (e.g., firewall logs, SSH logs) and convert it into:
# A simple table
# A daily HTML summary
# A CSV timeline
# Real use: SOC analysts and admins depend on small conversion utilities daily.

import subprocess

def ssh_extraction():
    # Läs in SSH-logg med hjälp av biblioteket subprocess, text=True levererar all data i en lång sträng. 
    raw_ssh_data = subprocess.check_output(["journalctl", "-u", "ssh.service", "--no-pager"], text=True)

    # ssh_success_count = 0
    # ssh_failure_count = 0
    ssh_examples = []

    # Loop för att gå genom varje logg-inlägg, eftersom det är sparat som en enda strängen så delar vi upp strängen här också.
    for line in raw_ssh_data.splitlines():
        if "Accepted password" in line:
            # ssh_success_count += 1
            if len(ssh_examples) < 5:
                ssh_examples.append(line.strip())
        elif "Failed password" in line:
            # ssh_failure_count += 1
            if len(ssh_examples) < 5:
                ssh_examples.append(line.strip())

    if len(ssh_examples) == 0:
        return("No SSH attempts since yesterday.")
    else:
        print("SSH logins: ")
        for line in ssh_examples:
            return(line)

###

raw_sudo_data = subprocess.check_output(["journalctl", "-t", "sudo", "--since", "yesterday", "--no-pager"], text=True)

sudo_examples = []

for line in raw_sudo_data.splitlines():
    if "COMMAND=" in line:
        sudo_examples.append(line.strip())

if len(sudo_examples) == 0:
    print("No sudo usage since yesterday.")
else:
    print("Sudo usage: ")
    for line in sudo_examples:
        print(line)

###

raw_login_data = subprocess.check_output(["journalctl", "_SYSTEMD_UNIT=systemd-logind.service", "--since", "yesterday", "--no-pager"], text=True)

raw_su_data = subprocess.check_output(["journalctl", "_COMM=su", "--since", "yesterday", "--no-pager"], text=True)

# print(ssh_extraction())

# print(ssh_examples)
# print(ssh_success_count)
# print(ssh_failure_count)
# print(raw_sudo_data)
# print(raw_login_data)
# print(raw_su_data)

# Skriva till en txt-fil för framtida undersökningar.

# with open("dagens.txt", "w") as log_file:
#    log_file.write(ssh_examples)
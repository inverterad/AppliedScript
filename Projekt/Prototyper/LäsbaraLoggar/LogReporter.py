#!/usr/bin/env python3

#“Human-Readable Security Reports” from Raw Data
# Many logs are unreadable.
# Your script could take messy input (e.g., firewall logs, SSH logs) and convert it into:
# A simple table
# A daily HTML summary
# A CSV timeline
# Real use: SOC analysts and admins depend on small conversion utilities daily.

import subprocess
import re
from tabulate import tabulate

def ssh_extraction():
    # Läs in SSH-logg med hjälp av biblioteket subprocess, text=True levererar all data i en lång sträng. 
    raw_ssh_data = subprocess.check_output(["journalctl", "-u", "ssh.service", "--no-pager"], text=True)

    # Använder re-modulen för att få in regex så jag kan hitta mönster.
    pattern = re.compile(
        r'^(?P<date>\w{3}\s+\d{1,2})\s+'
        r'(?P<time>\d{2}:\d{2}:\d{2})\s+'
        r'\S+\s+\S+:\s+'
        r'(?P<password>Accepted\s+password|Failed\s+password)\s+'
        r'for\s+(?P<user>\w+|invalid\s+user\s+\w+)\s+'
        r'from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})'
    )

    ssh_examples = []
    ssh_parsed = []

    # Loop för att gå genom varje logg-inlägg, eftersom det är sparat som en enda strängen så delar vi upp strängen här också.
    for line in raw_ssh_data.splitlines():
        if "Accepted password" in line:
            # if len(ssh_examples) < 5:
            ssh_examples.append(line.strip())
        elif "Failed password" in line:
            # if len(ssh_examples) < 5:
            ssh_examples.append(line.strip())

    # Fyll på dictionaries med datan för varje incident.
    for line in ssh_examples:
        match = pattern.search(line)
        if match:
            ssh_parsed.append(match.groupdict())

    return(ssh_parsed)

###

def sudo_extraction():
    # Använder subprocess för att extrahera sudo-data sedan igår.
    raw_sudo_data = subprocess.check_output(["journalctl", "-t", "sudo", "--since", "yesterday", "--no-pager"], text=True)

    # Använder re-modulen för att få in regex så jag kan hitta mönster.
    pattern = re.compile(
        r'^(?P<date>\w{3}\s+\d{1,2})\s+'
        r'(?P<time>\d{2}:\d{2}:\d{2})\s+'
        r'\S+\s+sudo\[\d+\]:\s+'
        r'\w+\s+:\s+'
        r'TTY=\S+\s+;\s+'
        r'PWD=(?P<working_directory>\S+)\s+\;\s+'
        r'USER=(?P<user>\w+)\s+\S+\s+'
        r'COMMAND=(?P<command>.+)'
    )

    sudo_examples = []
    sudo_parsed = []

    # Spara endast relevanta inlägg.
    for line in raw_sudo_data.splitlines():
        if "COMMAND=" in line:
            sudo_examples.append(line.strip())

    # Fixa dictionaries med pattern från regex.
    for line in sudo_examples:
        match = pattern.search(line)
        if match:
            sudo_parsed.append(match.groupdict())

    # Om inga inlägg finns så ska man kunna ta emot det, annars levereras dictionaries.
    if len(sudo_parsed) == 0:
        return("empty")
    else:
        return(sudo_parsed)

###

def login_data_extraction():

    raw_login_data = subprocess.check_output(["journalctl", "_SYSTEMD_UNIT=systemd-logind.service", "--since", "yesterday", "--no-pager"], text=True)

    # Använder re-modulen för att få in regex så jag kan hitta mönster.
    pattern_new = re.compile(
        r"^(?P<date>\w{3}\s+\d{1,2})\s+"
        r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"\S+\s+systemd-logind\[\d+\]:\s+"
        r"(?P<session>New\s+session)\s+"
        r"'(?P<session_id>[a-zA-Z0-9]+)'\s+\S+\s+\S+\s+"
        r"'(?P<user>\S+)'\s+with\s+class\s+"
        r"'(?P<class>\S+)'\s+and\s+type\s+"
        r"'(?P<interface>\S+)'"
    )

    pattern_removed = re.compile(
        r"^(?P<date>\w{3}\s+\d{1,2})\s+"
        r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"\S+\s+systemd-logind\[\d+\]:\s+"
        r"(?P<session>Removed\s+session)\s+"
        r"(?P<session_id>[a-zA-Z0-9]+)"
    )

    login_data = []

    # Itererar över login-datan och går genom båda mönstren för att kolla efter logins.
    # Sedan fyller vi på login_data med varje inlägg som matchar.
    for line in raw_login_data.splitlines():
        match1 = pattern_new.search(line)
        match2 = pattern_removed.search(line)

        if match1:
            login_data.append(match1.groupdict())
        
        elif match2:
            login_data.append(match2.groupdict())

    
    return(login_data)

raw_su_data = subprocess.check_output(["journalctl", "_COMM=su", "--since", "yesterday", "--no-pager"], text=True)


print("SSH Logins")
print("----------")
print(tabulate(ssh_extraction(), headers="keys"))
print()
print("Sudo usage")
print("----------")
print(tabulate(sudo_extraction(), headers="keys"))
print()
print("Login data")
print("----------")
print(tabulate(login_data_extraction(), headers="keys"))


# print(ssh_examples)
# print(ssh_success_count)
# print(ssh_failure_count)
# print(raw_sudo_data)
# print(raw_login_data)
# print(raw_su_data)

# Skriva till en txt-fil för framtida undersökningar.

# with open("dagens.txt", "w") as log_file:
#    log_file.write(ssh_examples)
#!/usr/bin/env python3

import argparse
import datetime
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
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

    # Om inga inlägg finns.
    if len(ssh_parsed) == 0:
        return("empty")
    else:
        # Här används tabulate för att göra det snyggt och prydligt i och med att vi levererar datan.
        return(tabulate(ssh_parsed, headers="keys"))

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
        # Här används tabulate för att göra det snyggt och prydligt i och med att vi levererar datan.
        return(tabulate(sudo_parsed, headers="keys"))

def login_data_extraction():

    # Använd subprocess för att extrahera login-data genom journalctl sedan igår.
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

    # Om inga inlägg finns.
    if len(login_data) == 0:
        return("empty")
    else:
        # Här används tabulate för att göra det snyggt och prydligt i och med att vi levererar datan.
        return((tabulate(login_data, headers="keys")))

def su_data_extraction():

    # Här tar vi in den råa datan från journalctl med rätt flaggor.
    raw_su_data = subprocess.check_output(["journalctl", "_COMM=su", "--since", "yesterday", "--no-pager"], text=True)

    # Använder re-modulen för att få in regex så jag kan hitta ett mönster för su misslyckas.
    pattern_failed = re.compile(
        r"^(?P<date>\w{3}\s+\d{1,2})\s+"
        r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"\S+\s+su\[\d+\]:\s+FAILED\s+SU\s+"
        r"\(to\s+(?P<to_user>\S+)\)\s+"
        r"(?P<from_user>\S+)\s+on\s+\S+"
    )

    # Använder re-modulen för att få in regex så jag kan hitta ett mönster för su lyckas.
    pattern_success = re.compile(
        r"^(?P<date>\w{3}\s+\d{1,2})\s+"
        r"(?P<time>\d{2}:\d{2}:\d{2})\s+"
        r"\S+\s+su\[\d+\]:\s+"
        r"\(to\s+(?P<to_user>\S+)\)\s+"
        r"(?P<from_user>\S+)\s+on\s+\S+"
    )

    # Initierar en lista för framtida dictionaries med korrekt data.
    su_data = []

    # Går genom varje rad i den råa datan för att sedan kolla om det stämmer överens med något av mönstrena.
    for line in raw_su_data.splitlines():
        match_fail = pattern_failed.search(line)
        match_success = pattern_success.search(line)

        # Här snyggar jag till dictionaryn och lägger till en login-key med värde "failed" så att man kan se det i the output.
        if match_fail:
            match_fail_updated = match_fail.groupdict()
            match_fail_updated["login"] = "failed"
            su_data.append(match_fail_updated)

        # Här snyggar jag till dictionaryn och lägger till en login-key med värde "success" så att man kan se det i the output.
        elif match_success:
            match_success_updated = match_success.groupdict()
            match_success_updated["login"] = "success"
            su_data.append(match_success_updated)

    # Om inga inlägg finns.
    if len(su_data) == 0:
        return("empty")
    else:
        # Här används tabulate för att göra det snyggt och prydligt i och med att vi levererar datan.
        return((tabulate(su_data, headers="keys")))

def log_export():
    
    # Datum och tid för framtida loggfilens namn.
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d_%H:%M")
    logfile_name = str(current_time_str) + "_log.txt"

    # Här skapar jag en katalog för loggfiler om den inte redan finns.
    folder = Path("log")
    folder.mkdir(parents=True, exist_ok=True)

    # Här nedan skriver vi samma information som skrivs ut i terminalen men till en loggfil.
    with open(folder / logfile_name, "w") as log_file:
        log_file.write("\nSSH Logins\n")
        log_file.write("----------\n")
        log_file.write(ssh_extraction())
        log_file.write("\nSudo Usage\n")
        log_file.write("----------\n")
        log_file.write(sudo_extraction())
        log_file.write("\nLogin Data\n")
        log_file.write("----------\n")
        log_file.write(login_data_extraction())
        log_file.write("\nSu Data\n")
        log_file.write("----------\n")
        log_file.write(su_data_extraction())

def argument_flaggor():
    
    flaggor = argparse.ArgumentParser(add_help=False)
    flaggor.add_argument("-h", "--help", action="store_true", help="Visa hjälptext")
    flaggor.add_argument("-v", "--version", action="store_true", help="Visa versionnummer")
    args = flaggor.parse_args()

    if args.help:
        print("Användning: sudo ./LogReporter [-h] [-v]\n")
        print("Undersöker SSHloggar, sudoanvändning, logindata och suanvändning och visar resultatet i ett läsbart format i standard output.")
        print("Resultatet skrivs även till en txt-fil i log-katalogen.")
        sys.exit()
    
    if args.version:
        print("Version 0.9")
        sys.exit()

# Kolla om vi kör Linux, om inte så avslutar vi och meddelar användaren.
if platform.system() != "Linux":
    print("Scriptet fungerar inte på andra operativsystem än Linux, tyvärr. Avslutar.")
    sys.exit()

# Kolla så att scriptet körs som sudo
# if os.geteuid() != 0:
    # print("Detta script kräver sudo-behörighet.")
    # sys.exit()

argument_flaggor()

# Skriv ut allt till standardoutput
print("SSH Logins")
print("----------")
print(ssh_extraction())
print()
print("Sudo usage")
print("----------")
print(sudo_extraction())
print()
print("Login data")
print("----------")
print(login_data_extraction())
print()
print("Su data")
print("-------")
print(su_data_extraction())
# log_export()

# Firewallloggar?

# Nätverksloggar?
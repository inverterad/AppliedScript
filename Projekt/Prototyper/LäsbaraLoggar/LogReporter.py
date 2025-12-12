#“Human-Readable Security Reports” from Raw Data
# Many logs are unreadable.
# Your script could take messy input (e.g., firewall logs, SSH logs) and convert it into:
# A simple table
# A daily HTML summary
# A CSV timeline
# Real use: SOC analysts and admins depend on small conversion utilities daily.

import subprocess

# Läs in loggen

raw_ssh_data = subprocess.check_output(["journalctl", "-u", "ssh.service", "--no-pager", "--boot"], text=True)

print(raw_ssh_data)
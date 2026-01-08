# LogReporter
Python-script som används för att undersöka diverse loggfiler på ett Linux-system med syfte att informera om någon har loggat in på systemet senaste dygnet och då ge information om när och hur.

Scriptet ska fungera på alla Linuxbaserade system som använder sig av journalctl.

## Systemkrav
- Linux
- Python 3.10+
- sudo-rättigheter (kontrolleras automatiskt av scriptet)

## Beroenden
Scriptet kräver externa Python-bibliotek som listas i `requirements.txt`.

Notera att beroenden installeras för aktuell Python-miljö. Om scriptet inte hittar tabulate vid körning med sudo, använd:

    sudo -H python3 -m pip install -r requirements.txt



## Instruktion för användning

    git clone https://github.com/inverterad/AppliedScript.git
    cd AppliedScript/Projekt/LogReporter
    chmod +x LogReporter.py
    python3 -m pip install -r requirements.txt
    sudo ./LogReporter.py

## Flaggor
- -h, --help : Visar hjälpsida.
- -v, --version : Visar vilken version av scriptet du använder.

## Funktion
Samlar in information via journalctl om:

    SSH logins
    Sudo-användning
    Login-data
    Kommandot su

Sedan omvandlar vi loggarna till ett mer läsbart format och visar upp i standard output och i samma veva skapas en loggfil i katalogen:

    LogReporter/log/

## Screenshot / Video
WIP

## Flödesschema

[Temporär tidig version](Projekt_Loggläsningsrapport_Flowchart.pdf)
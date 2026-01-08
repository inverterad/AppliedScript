# LogReporter
Python-script som används för att undersöka diverse loggfiler på ett Linux-system med syfte att informera om någon har loggat in på systemet senaste dygnet och då ge information om när och hur.

Scriptet ska fungera på alla Linuxbaserade system som använder sig av journalctl.

## Systemkrav
Scriptet kontrollerar automatiskt att du har sudo-rättighet då detta är ett krav.

Biblioteket tabulate är ett krav för att scriptet ska fungera.

## Instruktion för användning

    git clone https://github.com/inverterad/AppliedScript.git
    cd AppliedScript/Projekt/LogReporter
    chmod +x LogReporter.py
    pip install tabulate
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
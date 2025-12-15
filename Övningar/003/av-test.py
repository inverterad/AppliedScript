#!/usr/bin/env python3

import platform
import time

this_system = platform.system()

if this_system == "Windows":
    # Fortsätt med Windows-specifik kod
    print("Windows upptäckt. Scriptet fortsätter..")

elif this_system == "Linux":
    print("Linux upptäckt. Detta script är avsett för Windows.")
    exit()

elif this_system == "Darwin":
    print("macOS upptäckt. Detta script är avsett för Windows.")
    exit()

else:
    print(f"Okänt operativsystem ({this_system}). Detta script är avsett för Windows. Avbryter körning.")
    exit()


# Skriv AV test signaturen baserad på EICAR-testfil, innehållet är helt ofarligt och kommer inte att skada systemet.
eicar_str = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

print("Skapar ofarlig EICAR-fil för att testa antivirus.")
with open("test.txt", "w", encoding="utf-8") as text_f:
    text_f.write(eicar_str)


print("Avvaktar för att antivirus ska få tid att göra sitt jobb..")
time.sleep(3)

try:
    with open("test.txt", "r") as test_f:
        file_content = test_f.read()
        
    # Kontrollera om innehållet matchar EICAR-signaturen
    if file_content == eicar_str:
        print("Filen finns kvar, antivirus har inte gjort sitt jobb.")

except Exception as e:
    # Om ett fel uppstår här pga att filen har tagits bort eller flyttats
    print("[!!!] Filen kunde inte läsas!")
    print("[!!!] AV har tagit bort/karantänat filen.")
    print("[---] Din AV/EDR-lösning är helt fungerande och skyddar mot kända virus-signaturer.")


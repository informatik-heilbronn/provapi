import time
import datetime
import logging
import keys

# ----------------------------------------------------------------------------------------------------------
# Allgemein
# ----------------------------------------------------------------------------------------------------------

# setup für logging
logging.basicConfig(filename='comparison.log', level=logging.INFO)


# ----------------------------------------------------------------------------------------------------------
# Funktionen
# ----------------------------------------------------------------------------------------------------------

def compare(upper_bauschein, lower_bauschein, tank, leitung):
    """vergleicht Kennziffern"""

    # timestamp
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    # Vergleich
    if upper_bauschein == tank and lower_bauschein == leitung:
        print('Check Erfolgreich')
        logging.info(st + " - Vergleich Erfolgreich - " + upper_bauschein + lower_bauschein + tank + leitung)
        return 1
    elif upper_bauschein == tank and lower_bauschein != leitung:
        print('Check Fehlgeschlagen: Kennziffer des Tanks auf dem Bauschein stimmt nicht mit dem entsprechenden '
              'DMC-Code überein!')
        logging.info(st + " - Vergleich fehlgeschlagen - " + upper_bauschein + lower_bauschein + tank + leitung)
        return 2
    elif upper_bauschein != tank and lower_bauschein == leitung:
        print('Check Fehlgeschlagen: Kennziffer der Leitung auf dem Bauschein stimmt nicht mit dem entsprechenden '
              'DMC-Code überein!')
        logging.info(st + " - Vergleich fehlgeschlagen - " + upper_bauschein + lower_bauschein + tank + leitung)
        return 3
    else:
        print('Check Fehlgeschlagen: Kennziffer der Leitung und des Tanks auf dem Bauschein stimmt nicht mit dem '
              'entsprechenden DMC-Code überein!')
        logging.info(st + " - Vergleich fehlgeschlagen - " + upper_bauschein + lower_bauschein + tank + leitung)
        return 4


def start_comparison(upper_bauschein, lower_bauschein, tank, leitung):
    """überprüft Kennziffern und startet Vergleich"""

    # lädt Listen aus 'keys'-Modul
    tank_list = keys.get_tank_keys()
    leitung_list = keys.get_leitung_keys()

    # hier wird überprüft, ob die Kennziffern registriert sind
    upper_bauschein_check = check(upper_bauschein, tank_list)
    lower_bauschein_check = check(lower_bauschein, leitung_list)
    tank_check = check(tank, tank_list)
    leitung_check = check(leitung, leitung_list)

    # falls alle checks erfolgreich sind wird verglichen
    if upper_bauschein_check and lower_bauschein_check and tank_check and leitung_check:
        return compare(upper_bauschein, lower_bauschein, tank, leitung)
    else:
        print("Bitte überprüfen Sie Ihre Eingabe.")
        logging.info("Ungültige Kennziffer - " + upper_bauschein + lower_bauschein + tank + leitung)
        return 5


def check(key, key_list):
    """überprüft, ob Kennziffern registriert sind"""
    # schaut ob ein Format vorliegt, das in einen String gewandelt werden kann
    if isinstance(key, int) or isinstance(key, float):
        key = str(key)
    # entfernt alle whitespaces und Kommas
    if isinstance(key, str):
        key = key.replace(" ", "")
        key = key.replace(",", "")
    # überprüft, ob String leer ist
    if isinstance(key, str) and not len(key) == 0:
        for i in key_list:
            if key in i[len(i)-1]:
                return True
    return False

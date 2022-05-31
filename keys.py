import configparser
import re

config = configparser.RawConfigParser()
config.read('keys.properties')

# Variablen für tank_keys und leitung_keys, die von allen Klassen und Modulen genutzt werden
tank_keys = config.get("KEYS", "tank_keys")
leitung_keys = config.get("KEYS", "leitung_keys")

# wandelt String in Liste um und trennt Elemente durch ','
tank_keys = tank_keys.split(',')
leitung_keys = leitung_keys.split(',')


# ----------------------------------------------------------------------------------------------------------
# Funktionen
# ----------------------------------------------------------------------------------------------------------

def add_tank_key(key):
    """eine Kennziffer der Tank-Liste hinzufügen"""
    # überprüft, ob key in String gewandelt werden kann
    if isinstance(key, int) or isinstance(key, float):
        key = str(key)
    # regex
    key = re.sub(r"[^A-Za-z0-9\s]", "", key)
    key = key.replace(" ", "")
    # überprüft, ob String leer ist
    if isinstance(key, str) and len(key) > 0:
        tank_keys.append(key)
        config.set("KEYS", "tank_keys", clear_string(str(tank_keys)))
        with open("keys.properties", "w") as props:
            config.write(props)
    else:
        raise Exception


def remove_tank_key(key):
    """eine Kennziffer von der Tank-Liste entfernen"""
    # überprüft, ob key in String gewandelt werden kann
    if isinstance(key, int) or isinstance(key, float):
        key = str(key)
    # regex
    key = re.sub(r"[^A-Za-z0-9\s]", "", key)
    key = key.replace(" ", "")
    # überprüft, ob String leer ist
    if isinstance(key, str) and len(key) > 0:
        tank_keys.remove(key)
        config.set("KEYS", "tank_keys", clear_string(str(tank_keys)))
        print(config.get("KEYS", "tank_keys"))
        with open("keys.properties", "w") as props:
            config.write(props)
    else:
        raise Exception


def add_leitung_key(key):
    """eine Kennziffer der leitung-Liste hinzufügen"""
    # überprüft, ob key in String gewandelt werden kann
    if isinstance(key, int) or isinstance(key, float):
        key = str(key)
    # regex
    key = re.sub(r"[^A-Za-z0-9\s]", "", key)
    key = key.replace(" ", "")
    # überprüft, ob String leer ist
    if isinstance(key, str) and len(key) > 0:
        leitung_keys.append(key)
        config.set("KEYS", "leitung_keys", clear_string(str(leitung_keys)))
        with open("keys.properties", "w") as props:
            config.write(props)
    else:
        raise Exception


def remove_leitung_key(key):
    """eine Kennziffer von der Leitung-Liste entfernen"""
    # überprüft, ob key in String gewandelt werden kann
    if isinstance(key, int) or isinstance(key, float):
        key = str(key)
    # regex
    key = re.sub(r"[^A-Za-z0-9\s]", "", key)
    key = key.replace(" ", "")
    # überprüft, ob String leer ist
    if isinstance(key, str) and len(key) > 0:
        leitung_keys.remove(key)
        config.set("KEYS", "leitung_keys", clear_string(str(leitung_keys)))
        print(config.get("KEYS", "leitung_keys"))
        with open("keys.properties", "w") as props:
            config.write(props)
    else:
        raise Exception


def clear_string(string):
    string = string.replace("\"", "")
    string = string.replace("\'", "")
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.replace(" ", "")
    return string


def get_tank_keys():
    return tank_keys


def get_leitung_keys():
    return leitung_keys

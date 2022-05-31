import configparser

config = configparser.RawConfigParser()
config.read('admin.properties')
usrnm = config.get("USERDATA", "username")
pw = config.get("USERDATA", "password")


# ----------------------------------------------------------------------------------------------------------
# Funktionen
# ----------------------------------------------------------------------------------------------------------

def check_userinfo(username, password):
    """überprüft, ob 'username' und 'password' valide sind"""
    return True if username == usrnm and password == pw else False

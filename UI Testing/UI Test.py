import pyautogui




"""Test to see whether the Abgleichbutton does something"""
def abgleichbutton():
    r = pyautogui.locateOnScreen('Abgleich.png', grayscale=False, confidence=.5)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        print('Found and clicked Abgleich')
        t=pyautogui.locateOnScreen('Suche.png', grayscale=False, confidence=.5)
        if(t != None):
            print('Test Abgleich Successful')
        else:
            print ('Test Abgleich Unsuccesful')

##Bei den Folgenden 3 Tests sind wir echt unsicher wie wir das testen sollen

"""Test to see whether the Leitungbutton does something"""
def leitungbutton():
    r = pyautogui.locateOnScreen('Leitung auswaehlen.png', grayscale=False, confidence=.9)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t=pyautogui.locateOnScreen('selectafile.png', grayscale=False, confidence=.5)
        x=pyautogui.locateOnScreen('selectafiledark.png', grayscale=False, confidence=.5)
        if(t!= None or x!= None):
            print('Test Leitung Successful')
            z = pyautogui.locateOnScreen('abbrechen.png', grayscale=False, confidence=.5)
            s = pyautogui.locateOnScreen('abbrechendark.png', grayscale=False, confidence=.5)
            if (z != None):
                x, y = pyautogui.center(z)
                pyautogui.click(x, y)
            if (s != None):
                x, y = pyautogui.center(s)
                pyautogui.click(x, y)
        else:
            print('Test Leitung Unsuccesful')

"""Test to see whether the Bauscheinbutton does something"""
def bauscheinbutton():
    r = pyautogui.locateOnScreen('Bauschein auswaehlen.png', grayscale=False, confidence=.9)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('selectafile.png', grayscale=False, confidence=.5)
        x = pyautogui.locateOnScreen('selectafiledark.png', grayscale=False, confidence=.5)
        if (t != None or x != None):
            print('Test Bauschein Successful')
            z=pyautogui.locateOnScreen('abbrechen.png', grayscale=False, confidence=.5)
            s=pyautogui.locateOnScreen('abbrechendark.png', grayscale=False, confidence=.5)
            if(z != None):
                x, y = pyautogui.center(z)
                pyautogui.click(x, y)
            if(s != None):
                x,y =pyautogui.center(s)
                pyautogui.click(x, y)


        else:
            print('Test Bauschein Unsuccesful')

"""Test to see whether the Tankbutton does something"""
def tankbutton():
    r = pyautogui.locateOnScreen('Tank auswaehlen.png', grayscale=False, confidence=.9)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('selectafile.png', grayscale=False, confidence=.5)
        x = pyautogui.locateOnScreen('selectafiledark.png', grayscale=False, confidence=.5)
        if (t != None or x != None):
            print('Test Tank Successful')
            z = pyautogui.locateOnScreen('abbrechen.png', grayscale=False, confidence=.5)
            s = pyautogui.locateOnScreen('abbrechendark.png', grayscale=False, confidence=.5)
            if (z != None):
                x, y = pyautogui.center(z)
                pyautogui.click(x, y)
            if (s != None):
                x, y = pyautogui.center(s)
                pyautogui.click(x, y)
        else:
            print('Test Tank Unsuccesful')

"""Test to see whether the Tankfeld does something,controlled by erfolgAbgleich"""
def tankfeld():
    r = pyautogui.locateOnScreen('TankText.png', grayscale=False, confidence=.98)

    if (r != None):

        x, y = pyautogui.center(r)
        pyautogui.click(x, y+5)
        pyautogui.write('K')

"""Test to see whether the Leitungfeld does something,controlled by erfolgAbgleich"""
def leitungfeld():
    r = pyautogui.locateOnScreen('LeitungText.png', grayscale=False, confidence=.98)

    if (r != None):

        x, y = pyautogui.center(r)
        pyautogui.click(x, y+5)
        pyautogui.write('A')

"""Test to see whether the Bauscheinupfeld does something,controlled by erfolgAbgleich"""
def bauscheinupfeld():
    r = pyautogui.locateOnScreen('BauscheinUp.png', grayscale=False, confidence=.98)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y + 5)
        pyautogui.write('K')

"""Test to see whether the Bauscheinlowfeld does something,controlled by erfolgAbgleich"""
def bauscheinlowfeld():
    r = pyautogui.locateOnScreen('BauscheinLow.png', grayscale=False, confidence=.98)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y + 5)
        pyautogui.write('A')

"""Controlls whether the four field elements above do something """
def erfolgAbgleich():
    r = pyautogui.locateOnScreen('Abgleich.png', grayscale=False, confidence=.5)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        print('Found and clicked Abgleich')
        t = pyautogui.locateOnScreen('Erfolg.png', grayscale=False, confidence=.5)
        if (t != None):
            print('Test Felder Successful')
        else:
            print('Test Felder Unsuccesful')

"""Test to see whether the pageswap to the LoginPage works"""
def einstellungen():
    r = pyautogui.locateOnScreen('setting.png', grayscale=False, confidence=.95)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('LoginPage.png', grayscale=False, confidence=.5)
        if (t!= None):
            print('Login Page Found Successful')
        else: print('Login Page Found Unsuccessful')

"""Test to see whether the pageswap to the StartPage works"""
def zurueck():
    r = pyautogui.locateOnScreen('zurueck.png', grayscale=False, confidence=.95)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('Abgleich.png', grayscale=False, confidence=.5)
        if (t != None):
            print('Got back to StartPage Successful')
        else:
            print('Got back to StartPage Unsuccessful')

"""Test to see whether the Loginfelder work"""
def loginfelder():
    r = pyautogui.locateOnScreen('Username.png', grayscale=False, confidence=.98)
    t = pyautogui.locateOnScreen('Passwort.png', grayscale=False, confidence=.98)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        pyautogui.write('admin')
        if (t != None):
            x, y= pyautogui.center(t)
            pyautogui.click(x, y)
            pyautogui.write('123')
        else:
            print('FAILED TO FIND PASSWORD')
    else:print('FAILED TO FIND USERNAME')

"""Test to see whether the Loginbutton works"""
def login():
    r = pyautogui.locateOnScreen('Login.png', grayscale=False, confidence=.9)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('AddPage.png', grayscale=False, confidence=.9)
        if (t != None):
            print('Got to AddPage Successful')
    else:
        print('Got to AddPage Unsuccessful')

"""Test to see whether the Loginoutbutton works"""
def logout():
    r = pyautogui.locateOnScreen('Logout.png', grayscale=False, confidence=.9)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('Abgleich.png', grayscale=False, confidence=.9)
        if (t != None):
            print('Got to StartPage Successful')
    else:
        print('Got to StartPage Unsuccessful')


def main():
    abgleichbutton()

    bauscheinbutton()

    tankbutton()

    leitungbutton()

    tankfeld()

    leitungfeld()

    bauscheinupfeld()

    bauscheinlowfeld()

    erfolgAbgleich()

    einstellungen()

    loginfelder()

    login()

    logout()

    einstellungen()

    zurueck()

if __name__ == "__main__":
    main()

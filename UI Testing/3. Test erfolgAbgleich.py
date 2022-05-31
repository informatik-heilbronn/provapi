import pyautogui

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


if __name__ == "__main__":
    erfolgAbgleich()
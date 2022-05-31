import pyautogui

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

if __name__ == "__main__":
    loginfelder()
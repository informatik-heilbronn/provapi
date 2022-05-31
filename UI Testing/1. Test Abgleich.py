import pyautogui

def abgleichbutton():
    r = pyautogui.locateOnScreen('Abgleich.png', grayscale=False, confidence=.5)
    print(r)
    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        print('Found and clicked Abgleich')
        t=pyautogui.locateOnScreen('Suche.png', grayscale=False, confidence=.5)
        if(t != None):
            print('Test Abgleich Successful')
        else:
            print ('Test Abgleich Unsuccesful')

if __name__ == "__main__":
    abgleichbutton()
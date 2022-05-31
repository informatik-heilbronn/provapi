import time
import pyautogui

def einstellungen():
    r = pyautogui.locateOnScreen('setting.png', grayscale=False, confidence=.95)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('LoginPage.png', grayscale=False, confidence=.5)
        if (t!= None):
            print('Login Page Found Successful')
        else: print('Login Page Found Unsuccessful')




def zurueck():
    time.sleep(3)
    r = pyautogui.locateOnScreen('zurueck.png', grayscale=False, confidence=.95)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        t = pyautogui.locateOnScreen('Abgleich.png', grayscale=False, confidence=.5)
        if (t != None):
            print('Got back to StartPage Successful')
        else:
            print('Got back to StartPage Unsuccessful')

if __name__ == "__main__":
    einstellungen()
    zurueck()
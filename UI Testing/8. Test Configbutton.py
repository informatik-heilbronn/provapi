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

if __name__ == "__main__":
    einstellungen()
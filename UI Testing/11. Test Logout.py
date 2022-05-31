import pyautogui

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

if __name__ == "__main__":
    logout()
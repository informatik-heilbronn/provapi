import pyautogui


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


if __name__ == "__main__":
    login()
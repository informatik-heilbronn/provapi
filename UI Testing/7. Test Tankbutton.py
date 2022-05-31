import time
import pyautogui

def tankbutton():
    time.sleep(1)
    r = pyautogui.locateOnScreen('Tank auswaehlen.png', grayscale=False, confidence=.9)
    print(r)
    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y)
        time.sleep(1)
        t = pyautogui.locateOnScreen('selectafile.png', grayscale=False, confidence=.9)
        x = pyautogui.locateOnScreen('selectafiledark.png', grayscale=False, confidence=.9)
        if (t != None or x != None):
            print('Test Tank Successful')
            z = pyautogui.locateOnScreen('abbrechen.png', grayscale=False, confidence=.9)
            s = pyautogui.locateOnScreen('abbrechendark.png', grayscale=False, confidence=.9)
            if (z != None):
                x, y = pyautogui.center(z)
                pyautogui.click(x, y)
            if (s != None):
                x, y = pyautogui.center(s)
                pyautogui.click(x, y)
        else:
            print('Test Tank Unsuccesful')

if __name__ == "__main__":
    tankbutton()
import time
import pyautogui

def tankfeld():
    time.sleep(1)
    r = pyautogui.locateOnScreen('TankText.png', grayscale=False, confidence=.98)

    if (r != None):

        x, y = pyautogui.center(r)
        pyautogui.click(x, y+5)
        pyautogui.write('K')

"""Test to see whether the Leitungfeld does something,controlled by erfolgAbgleich"""
def leitungfeld():
    time.sleep(1)
    r = pyautogui.locateOnScreen('LeitungText.png', grayscale=False, confidence=.98)

    if (r != None):

        x, y = pyautogui.center(r)
        pyautogui.click(x, y+5)
        pyautogui.write('A')

"""Test to see whether the Bauscheinupfeld does something,controlled by erfolgAbgleich"""
def bauscheinupfeld():
    time.sleep(1)
    r = pyautogui.locateOnScreen('BauscheinUp.png', grayscale=False, confidence=.98)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y + 5)
        pyautogui.write('K')

"""Test to see whether the Bauscheinlowfeld does something,controlled by erfolgAbgleich"""
def bauscheinlowfeld():
    time.sleep(1)
    r = pyautogui.locateOnScreen('BauscheinLow.png', grayscale=False, confidence=.98)

    if (r != None):
        x, y = pyautogui.center(r)
        pyautogui.click(x, y + 5)
        pyautogui.write('A')


if __name__ == "__main__":
    tankfeld()
    leitungfeld()
    bauscheinupfeld()
    bauscheinlowfeld()
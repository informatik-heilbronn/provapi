import cv2
import threading
import time

# ----------------------------------------------------------------------------------------------------------
# Allgemein
# ----------------------------------------------------------------------------------------------------------

# globale Variablen
active = True
frame = None
frame2 = None
scan_rdy = False


# ----------------------------------------------------------------------------------------------------------
# Funktionen
# ----------------------------------------------------------------------------------------------------------

def take_photo(name):
    global frame, active
    img_name = ("current_" + name + ".png").format()
    cv2.imwrite(img_name, frame)
    return img_name


def bauschein_img():
    """macht alle X Sekunden eine Momentaufnahme des Kamerabilds"""
    while active:
        time.sleep(4)
        img_name = "bauschein.png".format()
        cv2.imwrite(img_name, frame)


def main_camera1():
    """startet Kamera1"""
    global frame, active

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while active:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
    cam.release()


def main_camera2():
    """startet Kamera2"""
    global frame, active

    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while active:
        ret, frame2 = cam.read()
        if not ret:
            print("failed to grab frame")
            break
    cam.release()

import cv2
import math
import keys
import re
import pytesseract as ptsr
from PIL import Image, ImageChops
from matplotlib import pyplot as plt
import numpy as np
from blend_modes import divide
from difflib import SequenceMatcher
from typing import Tuple, Union
from deskew import determine_skew
import camera

# Set Tesseract and Image Path
ptsr.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
path = "./Bauschein LB Varianten/workImage.png"

# Function for MainApp
def readImage(file_path):
    img = cv2.imread(file_path)

    cv2.imwrite("current_bauschein.png", img)

    image = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    image = de_shadow(image)

    image = thick_font(image)

    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, (0, 0, 0))
    image = rotated

    image = invertImage(image)

    image = grayscaleIm(image)
    cv2.imwrite(path, image)

    im = Image.open(path)
    im = trim(im)
    im.save(path)
    image = cv2.imread(path)

    imageBeforeThresh = image
    image = threshold(image, 110)

    image = blur(image, 3)

    # [60: 140, 530: 650]
    h, w, c = image.shape
    h2 = int(h / 7)
    h1 = h2 * 2
    w2 = int(w / 2 - (h2 * 2.5))
    w1 = int(w2 + (h2 * 2.5))
    cutout = image[h2:h1, w2:w1]

    cv2.imwrite("fahrzeugnummer.png", cutout)

    string = ""
    list = []
    found = False
    counter = 0
    threshValue = 70

    # try Reading the Image
    while counter < 12 and not found:
        try:
            string = ptsr.image_to_string(cutout)
        except:
            print("An error has occurred while Reading!")

        # regex
        string = re.sub(r"[^0-9\n]", "", string)
        list = string.split("\n")
        list.remove("")

        # Checking if something could be read and get the last Characters
        if len(list) > 0:
            found = True

        # If nothing was found try checking some more
        # maybe rotate 180 degree
        if not found and counter == 0:
            image = rotate(image, 180, (0, 0, 0))
            cutout = image[h2:h - 100, 50:w2 + 20]
        # check different area
        if not found and counter == 1:
            cutout = image[h - h:h - 100, w - w:w2 + 50]
        # check different area with other thresh and blur
        if not found and counter == 2:
            image = threshold(imageBeforeThresh, 110)
            image = blur(image, 5)
            cutout = image[h2:h, w - w:w2 + 50]
        # try decreasing thresh multiple times
        if not found and 6 > counter > 2:
            image = threshold(imageBeforeThresh, threshValue)
            image = blur(image, 7)
            cutout = image[h2:h - 100, 50:w2 + 50]
            threshValue -= 5
        # try increasing thresh multiple times
        if not found and 11 > counter >= 6:
            image = threshold(imageBeforeThresh, threshValue)
            image = blur(image, 5)
            cutout = image[h2:h - 100, 50:w2 + 50]
            threshValue += 10
        counter += 1

    # Give back solution
    print(string)
    if found:
        return string
    else:
        print("fail")
        return ""


# ==================================================#
###  Functions for increasing the Image Quality  ###
# ==================================================#
def invertImage(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image


def grayscaleIm(image):
    newImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return newImg


def threshold(image, threshValue):
    thresh, img_bw = cv2.threshold(image, threshValue, 230, cv2.THRESH_BINARY)
    return img_bw


def blur(image, blur):
    bluredImage = cv2.GaussianBlur(image, (blur, blur), 0)
    return bluredImage


def thick_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=2)
    image = cv2.bitwise_not(image)
    return image


# function to remove shadows from the image
def de_shadow(image):
    # splitting the image into channels
    bA = image[:, :, 0]
    gA = image[:, :, 1]
    rA = image[:, :, 2]

    # dialting the image channels individually to spead the text to the background
    dilated_image_bB = cv2.dilate(bA, np.ones((7, 7), np.uint8))
    dilated_image_gB = cv2.dilate(gA, np.ones((7, 7), np.uint8))
    dilated_image_rB = cv2.dilate(rA, np.ones((7, 7), np.uint8))

    # blurring the image to get the backround image
    bB = cv2.medianBlur(dilated_image_bB, 21)
    gB = cv2.medianBlur(dilated_image_gB, 21)
    rB = cv2.medianBlur(dilated_image_rB, 21)

    # blend_modes library works with 4 channels, the last channel being the alpha channel
    # so we add one alpha channel to our image and the background image each
    image = np.dstack((image, np.ones((image.shape[0], image.shape[1], 1)) * 255))
    image = image.astype(float)
    dilate = [bB, gB, rB]
    dilate = cv2.merge(dilate)
    dilate = np.dstack((dilate, np.ones((image.shape[0], image.shape[1], 1)) * 255))
    dilate = dilate.astype(float)

    # now we divide the image with the background image
    # without rescaling i.e scaling factor = 1.0
    blend = divide(image, dilate, 1.0)
    blendb = blend[:, :, 0]
    blendg = blend[:, :, 1]
    blendr = blend[:, :, 2]
    blend_planes = [blendb, blendg, blendr]
    blend = cv2.merge(blend_planes)
    # blend = blend*0.85
    blend = np.uint8(blend)

    # returning the shadow-free image
    return blend


def trim(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)


def rotate(
           image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
           ) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)
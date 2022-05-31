from pylibdmtx.pylibdmtx import decode
import cv2
import re
import keys


# ----------------------------------------------------------------------------------------------------------
# Funktionen
# ----------------------------------------------------------------------------------------------------------

def decode_dmc(filepath, pattern_list):
    """versucht eine gültige Kennziffer aus dem DMC-Code auszulesen"""
    dmc_image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    dmc_msg = str(decode(dmc_image))

    if dmc_msg.__eq__("[]"):
        thresh = 145
        blur_val = -1

        while dmc_msg.__eq__("[]") and blur_val <= 5:
            blur_val += 2
            thresh_offset = 0

            while dmc_msg.__eq__("[]") and thresh_offset <= 50:
                thresh_offset += 5

                dmc_image = incr_quality(dmc_image, int(thresh + thresh_offset), blur_val)
                dmc_msg = str(decode(dmc_image))

                print("Current Thresh: " + str(thresh + thresh_offset) + " Current Blur: " + str(
                    blur_val) + " DMC Message: " + str(dmc_msg))

    if dmc_msg.__eq__("[]"):
        extracted_index = "Can't decode DMC Code"
    else:
        extracted_index = extract_num(str(dmc_msg), pattern_list)

    return extracted_index


def incr_quality(image, threshold_val, blur):
    """Bildaufbereitung"""
    new_image = cv2.threshold(image, threshold_val, 255, cv2.THRESH_BINARY_INV)[1]
    new_image = cv2.GaussianBlur(new_image, (blur, blur), 0)
    new_image = 255 - new_image
    return new_image


def extract_num(string, patterns):
    """trennt Kennziffer von String"""
    string = "".join(string.split())
    print(string)

    # regex
    string = re.sub(r"[^A-Za-z0-9\n]", "", string)
    print(string)

    for pattern in patterns:
        match = re.search(pattern, string)
        if match is not None:
            string = match.group()
            return string[len(string) - 1:]

    return "?"


def get_dmc_from_file(file_path, property):
    """startet den gesamten DMCR-Vorgang"""
    # Liste gültiger Kennziffern zum Abgleichen
    if property=="tank":
        pattern_list = keys.get_tank_keys()
    else:
        pattern_list = keys.get_leitung_keys()

    return str(decode_dmc(file_path, pattern_list))

import pyautogui
import pytesseract
from PIL import Image
import keyboard
import time

    # for i in range(1, 6):
    # if 'Départ' not in text:




# Indiquez le chemin de votre exécutable Tesseract-OCR ici
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ruben\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Change this to your Tesseract-OCR installation location

def get_indice():
    global indice
    screenshot = pyautogui.screenshot()

    if indice == 1:
        region = screenshot.crop((52, 816, 279, 840)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        indice += 1
        text = pytesseract.image_to_string(region)
        return text
    elif indice == 2:
        region = screenshot.crop((52, 845, 279, 869)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        indice += 1
        text = pytesseract.image_to_string(region)
        return text
    elif indice == 3:
        region = screenshot.crop((52, 874, 279, 898)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        indice += 1
        text = pytesseract.image_to_string(region)
        return text
    elif indice == 4:
        region = screenshot.crop((52, 903, 279, 927)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        indice += 1
        text = pytesseract.image_to_string(region)
        return text
    elif indice == 5:
        region = screenshot.crop((52, 932, 279, 956)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        indice += 1
        text = pytesseract.image_to_string(region)
        return text
    elif indice == 6:
        region = screenshot.crop((52, 961, 279, 985)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        indice = 1
        text = pytesseract.image_to_string(region)
        return text

def remplir_indice():
    text = ""
    while not text or 'Départ' in text:
        text = get_indice()
        print("BOUCLE")

    time.sleep(0.2)
    pyautogui.click(2513, 249)  
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.write(text)

indice = 1
# Lorsque la touche 'f' est pressée, exécute la fonction extract_and_type
keyboard.add_hotkey('f', remplir_indice)

# This line is necessary to keep the script running
keyboard.wait()

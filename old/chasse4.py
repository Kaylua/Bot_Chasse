import pyautogui
import pytesseract
from PIL import Image
import keyboard
import time
import re
import pyperclip

# Setup pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ruben\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Change this to your Tesseract-OCR installation location

#Check si on a déjà validé un indice
def find_green_flag():
     # Fournir le chemin vers l'image à trouver
    location = pyautogui.locateOnScreen('green_flag.png')
    if location:
        print(f"Found the image at {location}")
        return True
    else:
        print("Image not found")
        return False
    
#Remplis les coordonnées dans dofusdb
def fill_coordinates(coordinates):
    # Split the coordinates into two variables
    x, y = map(int, coordinates[0].split(','))
    # Click on the input field
    pyautogui.click(2266, 261)
    # Select all existing text and delete it
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    # Wait a bit before typing
    time.sleep(0.2)
    # Type the extracted text into the field
    pyautogui.write(str(x))
    # Click on the input field
    pyautogui.click(2513, 249)  
    # Select all existing text and delete it
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    # Wait a bit before typing
    time.sleep(0.2)
    # Type the extracted text into the field
    pyautogui.write(str(y))

#Récuperes les coordonnées de la map sur laquelle on se trouve
def get_coordinates():
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    # You might need to adjust the region parameters according to your needs
    region = screenshot.crop((0, 43, 310, 103))
    region.save('region.png')
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(region)
    # Find coordinates in the text
    coordinates = re.findall(r'[-\d]+,[-\d]+', text)
    return coordinates

def check_and_fill_coordinates():
    # Find coordinates in the text
    coordinates = get_coordinates()
    time.sleep(0.2)
    fill_coordinates(coordinates)

#----------------------------------------------------------------------------------     
def indice_right():
    pyautogui.click(2439, 405)
def indice_up():
    pyautogui.click(2397, 374) 
def indice_down():
    pyautogui.click(2401, 443)
def indice_left():
    pyautogui.click(2365, 410)   
#----------------------------------------------------------------------------------
def move_left():
    pyautogui.click(345, 528)       
def move_right():
    pyautogui.click(1574, 526)  
def move_up():
    pyautogui.click(978, 30)  
def move_down():
    pyautogui.click(962, 922)  
#----------------------------------------------------------------------------------

#Lance une nouvelle chasse
def new_hunt():
    pyautogui.hotkey('h')
    time.sleep(2)
    pyautogui.click(553, 422)
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(3)
    move_right()
    time.sleep(4)
    move_right()
    time.sleep(5)
    pyautogui.click(950, 463)
    time.sleep(5)
    pyautogui.click(1429, 482)
    time.sleep(5)
    pyautogui.click(1035, 479)
    pyautogui.click(1090, 519)    
    time.sleep(5)
    pyautogui.click(374, 838)
    time.sleep(5)
    pyautogui.click(539, 818)
    time.sleep(5)
    pyautogui.hotkey('h')
    time.sleep(3)
    pyautogui.click(553, 416)

#Récupère le nom de l'indice recherché
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

#Récupère la phrase qui donne la direction indiquée par la fleche
def get_fleche():
    global indice
    
    if indice == 1:
        new_indice = 6
    else:
        new_indice = indice - 1

    if new_indice == 1:
        pyautogui.moveTo(37, 834)
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 758, 398, 804)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleche.png')
        text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 2:
        pyautogui.moveTo(37, 860)
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 787, 398, 833)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleche.png')
        text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 3:
        pyautogui.moveTo(37, 890)
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 816, 398, 862)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleche.png')
        text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 4:
        pyautogui.moveTo(37, 918)
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 845, 398, 891)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleche.png')
        text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 5:
        pyautogui.moveTo(37, 946)
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 874, 398, 920)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleche.png')
        text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 6:
        pyautogui.moveTo(37, 976)
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 903, 398, 949)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleche.png')
        text = pytesseract.image_to_string(region)
        return get_direction(text)

#Récupère la direction indiquée par la fleche
def get_direction(text):
    directions = ['est', 'ouest', 'nord', 'sud']
    found_direction = None
    for direction in directions:
        if re.search(r'\b' + direction + r'\b', text, re.IGNORECASE):
            found_direction = direction
            break
    return found_direction

#Cherche la direction et l'indice et remplis les champs dans dofusdb
def remplir_indice():
    #Cherche la direction et l'indice
    text = ""
    while not text or 'Départ' in text:
        text = get_indice()

    direction = get_fleche()

    if direction == 'nord':
        indice_up()
    elif direction == 'sud':
        indice_down()
    elif direction == 'ouest':
        indice_left()
    elif direction == 'est':
        indice_right()
    else:
        print("AUCUNE DIRECTION TROUVEE")

    # Remplis les champs dans dofusdb
    time.sleep(0.2)
    pyautogui.click(2255, 541)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.write(text)
    time.sleep(0.7)
    pyautogui.press('down')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.2)
    clipboard_content = pyperclip.paste()

#Actions de l'utilisateur
keyboard.add_hotkey('q', move_left)
keyboard.add_hotkey('d', move_right)
keyboard.add_hotkey('z', move_up)
keyboard.add_hotkey('s', move_down)
keyboard.add_hotkey('²', new_hunt)
keyboard.add_hotkey('f', remplir_indice)

#variables
indice = 1

#Attends une action clavier de l'utilisateur
keyboard.wait()

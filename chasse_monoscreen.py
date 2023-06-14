import pyautogui
import pytesseract
from PIL import Image
import keyboard
import time
import re
import pyperclip
import os 
import string
import sys

# Setup pytesseract
os.environ['TESSDATA_PREFIX'] = r'C:\Users\ruben\AppData\Local\Programs\Tesseract-OCR\tessdata'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ruben\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Change this to your Tesseract-OCR installation location

class TerminateExecution(Exception):
    pass

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
    
#Corrige les mots avec accent qui sont mal interprétés
def correction_text(text):
    # Définition des corrections
    corrections = {
        "qte": "quete",
        "qute": "quete",
        # ajoutez d'autres mots problématiques ici
    }
    
    # Suppression de la ponctuation et mise en minuscule du texte
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Division du texte en mots
    words = text.split()

    # Parcours de tous les mots et remplacement si nécessaire
    corrected_words = [corrections[word] if word in corrections else word for word in words]

    # Rassemblement des mots corrigés en une seule chaîne de caractères
    corrected_text = ' '.join(corrected_words)

    return corrected_text

#Récuperes les coordonnées de la map sur laquelle on se trouve
def get_coordinates():
    try:
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        # You might need to adjust the region parameters according to your needs
        region = screenshot.crop((0, 43, 155, 103))
        region.save('autres_images/map_coordinates.png')
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(region)
        # Verification si il a bien ramassé des chiffres
        digit_count = sum(char.isdigit() for char in text)
        if digit_count is None or digit_count < 2:
            screenshot = pyautogui.screenshot()
            region = screenshot.crop((2, 71, 171, 100))
            region.save('autres_images/map_coordinates2.png')
            text = pytesseract.image_to_string(region)
            digit_count = sum(char.isdigit() for char in text)
        # Si on a bien des chiffres, on continue
        text = text.replace('~', '-') # parfois tesseract lis ~ au lieu de - du coup je remplace ~ par - dans le text
        text = text.replace('(', ',').replace(')', ',') #remplace les parentheses par des virgules au cas ou tesseract lit une parenthese a la place d'une virgule
        # Find coordinates in the text
        coordinates = re.findall(r'[-\d]+,[-\d]+', text)
        # Split the coordinates into two variables
        x, y = map(int, coordinates[0].split(','))
        if check_zone_image(0.8, "autres_images/archimonstre.png", 324, 23, 1593, 927):
            print("******************* Archimonstre trouvé en [",x,",",y,"] *******************")
        return x,y
    except Exception:
        time.sleep(0.2)
        pyautogui.click(430, 1027)
        pyautogui.write("%pos%")
        pyautogui.press('enter')
        time.sleep(0.3)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((341, 986, 633, 1005)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        text = pytesseract.image_to_string(region)
        text = text.replace('~', '-')
        coordinates = re.findall(r'[-\d]+,[-\d]+', text)
        x, y = map(int, coordinates[0].split(','))
        recenter_mouse()
        return x,y

#Récuperes les coordonnées de la map sur laquelle on se trouve
def get_start_coordinates_old():
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    # You might need to adjust the region parameters according to your needs
    region = screenshot.crop((16, 776, 322, 985))
    region.save('autres_images/start_coordinates.png')
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(region)
    text = text.replace('~', '-') # parfois tesseract lis ~ au lieu de - du coup je remplace ~ par - dans le text
    print("TEXT : ",text)
    # Find coordinates in the text
    coordinates = re.findall(r'[-\d]+,[-\d]+', text)
    if coordinates:
        x, y = map(int, coordinates[0].split(','))
    else:
        print("Erreur : 'coordinates' est vide. Dans le doute on met les coord du zaap Tainela car c'est le seul qui pose probleme.")
        x, y = 1,-32
    return x,y

def get_start_coordinates():
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    # You might need to adjust the region parameters according to your needs
    region = screenshot.crop((16, 776, 322, 985))
    region.save('autres_images/start_coordinates.png')
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(region)
    text = text.replace('~', '-') # parfois tesseract lis ~ au lieu de - du coup je remplace ~ par - dans le text
    # Find coordinates in the text
    coordinates = re.findall(r'[-\d]+,[-\d]+', text)
    if coordinates:
        x, y = map(int, coordinates[0].split(','))
    else:
        # Try to find two pairs of digits without a comma
        coordinates = re.findall(r'(\d+)-(\d+)', text)
        if coordinates:
            x, y = int(coordinates[0][0]), -int(coordinates[0][1])
        else:
            print("Erreur : 'coordinates' est vide. Dans le doute on met les coord du zaap Tainela car c'est le seul qui pose probleme.")
            x, y = 1,-32
    return x, y

def alt_tab():
    time.sleep(0.2)
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.2)

def check_and_fill_coordinates():
    # Find coordinates in the text
    x,y = get_coordinates()
    time.sleep(0.2)
    alt_tab()
    # Click on the input field
    pyautogui.click(756, 251)
    # Select all existing text and delete it
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    # Wait a bit before typing
    time.sleep(0.2)
    # Type the extracted text into the field
    pyautogui.write(str(x))
    # Click on the input field
    pyautogui.click(1116, 251)  
    # Select all existing text and delete it
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    # Wait a bit before typing
    time.sleep(0.2)
    # Type the extracted text into the field
    pyautogui.write(str(y))
    alt_tab()

#----------------------------------------------------------------------------------     
def indice_right():
    pyautogui.click(997, 406)
def indice_up():
    pyautogui.click(959, 370) 
def indice_down():
    pyautogui.click(960, 447)
def indice_left():
    pyautogui.click(923, 408)   
#----------------------------------------------------------------------------------
def move_left():
    pyautogui.click(345, 528)       
def move_right():
    pyautogui.click(1574, 526)  
def move_up():
    pyautogui.click(962, 30)  
def move_down():
    pyautogui.click(962, 922)  
#----------------------------------------------------------------------------------

#Lance une nouvelle chasse
def new_hunt():
    global canal_chat_set
    if not canal_chat_set:
        set_canal_guilde()
        canal_chat_set = True

    time.sleep(0.3)
    recenter_mouse()
    time.sleep(0.3)
    pyautogui.hotkey('r')
    time.sleep(2.5)
    move_to_destination(-25, -36)
    time.sleep(0.8)
    pyautogui.click(950, 463)
    time.sleep(4.5)
    pyautogui.click(1429, 482)
    time.sleep(5.5)
    pyautogui.click(1035, 479)
    pyautogui.click(1090, 519)    
    time.sleep(5.5)
    move_fenetre_chasse()
    time.sleep(0.8)
    pyautogui.click(371, 848)
    time.sleep(5.5)
    pyautogui.click(539, 818)
    time.sleep(5)
    pyautogui.hotkey('h')
    time.sleep(2.5)
    global bool_new_hunt
    bool_new_hunt = True
    global hunt_count
    hunt_count += 1
    print("Départ de la chasse N°",hunt_count)
    time.sleep(0.2)
    move_to_depart_chasse()

# Clean une string de tout ce qui n'est pas une lettre, un accent ou un apostrophe
def clean_string(input_string):
    # '[^a-zA-ZÀ-ÿ\''œŒ']' signifie 'tout caractère qui n'est pas une lettre, un accent, une apostrophe, œ ou Œ'
    cleaned_string = re.sub('[^a-zA-ZÀ-ÿ\'œŒ]', ' ', input_string)
    # Remplacer "comne" par "corne" et "comnes" par "cornes"
    cleaned_string = cleaned_string.replace("comne", "corne").replace("comnes", "cornes").replace("comes", "cornes")
    # Supprimer les espaces de fin
    cleaned_string = cleaned_string.rstrip()
    return cleaned_string

#Récupère le nom de l'indice recherché
def get_indice():
    global indice
    screenshot = pyautogui.screenshot()

    if indice == 1:
        print("Go Indice N°1")
        region = screenshot.crop((52, 816, 279, 840)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save("indices/indice1.png")
        indice += 1
        text = pytesseract.image_to_string(region, lang='fra')
        text = clean_string(text)
        return text
    elif indice == 2:
        print("Go Indice N°2")
        region = screenshot.crop((52, 845, 279, 869)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save("indices/indice2.png")
        indice += 1
        text = pytesseract.image_to_string(region, lang='fra')
        text = clean_string(text)
        return text
    elif indice == 3:
        print("Go Indice N°3")
        region = screenshot.crop((52, 874, 279, 898)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save("indices/indice3.png")
        indice += 1
        text = pytesseract.image_to_string(region, lang='fra')
        text = clean_string(text)
        return text
    elif indice == 4:
        print("Go Indice N°4")
        region = screenshot.crop((52, 903, 279, 927)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save("indices/indice4.png")
        indice += 1
        text = pytesseract.image_to_string(region, lang='fra')
        text = clean_string(text)
        return text
    elif indice == 5:
        print("Go Indice N°5")
        region = screenshot.crop((52, 932, 279, 956)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save("indices/indice5.png")
        indice += 1
        text = pytesseract.image_to_string(region, lang='fra')
        text = clean_string(text)
        return text
    elif indice == 6:
        print("Go Indice N°6")
        region = screenshot.crop((52, 961, 279, 985)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save("indices/indice6.png")
        indice = 1
        text = pytesseract.image_to_string(region, lang='fra')
        text = clean_string(text)
        return text

#Récupère la phrase qui donne la direction indiquée par la fleche
def get_fleche2():
    global indice
    direction = None
    confidence = 0.98

    if indice == 1:
        new_indice = 6
    else:
        new_indice = indice - 1

    if new_indice == 1: 
        if check_zone_image(confidence, "fleches/fleche_haut.png", 25, 817, 56, 844):
            direction = "nord"
        elif check_zone_image(confidence, "fleches/fleche_bas.png", 25, 817, 56, 844):
            direction = "sud"
        elif check_zone_image(confidence, "fleches/fleche_droite.png", 25, 817, 56, 844):
            direction = "est"
        elif check_zone_image(confidence, "fleches/fleche_gauche.png", 25, 817, 56, 844):
            direction = "ouest"
    elif new_indice == 2: 
        if check_zone_image(confidence, "fleches/fleche_haut.png", 28, 847, 50, 872):
            direction = "nord"
        elif check_zone_image(confidence, "fleches/fleche_bas.png", 28, 847, 50, 872):
            direction = "sud"
        elif check_zone_image(confidence, "fleches/fleche_droite.png", 28, 847, 50, 872):
            direction = "est"
        elif check_zone_image(confidence, "fleches/fleche_gauche.png", 28, 847, 50, 872):
            direction = "ouest"
    elif new_indice == 3: 
        if check_zone_image(confidence, "fleches/fleche_haut.png", 25, 874, 48, 902):
            direction = "nord"
        elif check_zone_image(confidence, "fleches/fleche_bas.png", 25, 874, 48, 902):
            direction = "sud"
        elif check_zone_image(confidence, "fleches/fleche_droite.png", 25, 874, 48, 902):
            direction = "est"
        elif check_zone_image(confidence, "fleches/fleche_gauche.png", 25, 874, 48, 902):
            direction = "ouest"
    elif new_indice == 4: 
        if check_zone_image(confidence, "fleches/fleche_haut.png", 25, 907, 50, 931):
            direction = "nord"
        elif check_zone_image(confidence, "fleches/fleche_bas.png", 25, 907, 50, 931):
            direction = "sud"
        elif check_zone_image(confidence, "fleches/fleche_droite.png", 25, 907, 50, 931):
            direction = "est"
        elif check_zone_image(confidence, "fleches/fleche_gauche.png", 25, 907, 50, 931):
            direction = "ouest"
    elif new_indice == 5: 
        if check_zone_image(confidence, "fleches/fleche_haut.png", 23, 933, 49, 960):
            direction = "nord"
        elif check_zone_image(confidence, "fleches/fleche_bas.png", 23, 933, 49, 960):
            direction = "sud"
        elif check_zone_image(confidence, "fleches/fleche_droite.png", 23, 933, 49, 960):
            direction = "est"
        elif check_zone_image(confidence, "fleches/fleche_gauche.png", 23, 933, 49, 960):
            direction = "ouest"
    elif new_indice == 6: 
        if check_zone_image(confidence, "fleches/fleche_haut.png", 23, 962, 51, 987):
            direction = "nord"
        elif check_zone_image(confidence, "fleches/fleche_bas.png", 23, 962, 51, 987):
            direction = "sud"
        elif check_zone_image(confidence, "fleches/fleche_droite.png", 23, 962, 51, 987):
            direction = "est"
        elif check_zone_image(confidence, "fleches/fleche_gauche.png", 23, 962, 51, 987):
            direction = "ouest"

    print(direction)
    indice += 1
    return direction

#Récupère la phrase qui donne la direction indiquée par la fleche
def get_fleche():
    global indice
    
    if indice == 1:
        new_indice = 6
    else:
        new_indice = indice - 1

    if new_indice == 1:
        pyautogui.click(37, 834)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 759, 380, 804)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche1.png')
        text = pytesseract.image_to_string(region)
        text = get_direction(text)
        #print("fleche : ",text)
        if text is None or any(character.isdigit() for character in text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            pyautogui.click(38, 830)
            time.sleep(0.5)
            screenshot = pyautogui.screenshot()
            region = screenshot.crop((33, 768, 380, 804))
            text = pytesseract.image_to_string(region)
            text = get_direction(text)
            region.save('fleches/fleche1_bis.png')
            if indice_fleche_text_check(text):
                print("Aucune direction trouvée. Lancement d'une nouvelle chasse.")
                relancer_chasse()
        return get_direction(text)
    elif new_indice == 2:
        pyautogui.click(37, 860)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 788, 380, 833)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche2.png')
        text = pytesseract.image_to_string(region)
        text = get_direction(text)
        #print("fleche : ",text)
        if text is None or any(character.isdigit() for character in text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            pyautogui.click(38, 859)
            time.sleep(0.5)
            screenshot = pyautogui.screenshot()
            region = screenshot.crop((33, 797, 380, 833))
            text = pytesseract.image_to_string(region)
            text = get_direction(text)
            region.save('fleches/fleche2_bis.png')
            if indice_fleche_text_check(text):
                print("Aucune direction trouvée. Lancement d'une nouvelle chasse.")
                relancer_chasse()
        return get_direction(text)
    elif new_indice == 3:
        pyautogui.click(37, 890)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 817, 380, 862)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche3.png')
        text = pytesseract.image_to_string(region)
        text = get_direction(text)
        #print("fleche : ",text)
        if text is None or any(character.isdigit() for character in text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            pyautogui.click(38, 887)
            time.sleep(0.5)
            screenshot = pyautogui.screenshot()
            region = screenshot.crop((33, 826, 380, 862))
            text = pytesseract.image_to_string(region)
            text = get_direction(text)
            region.save('fleches/fleche3_bis.png')
            if indice_fleche_text_check(text):
                print("Aucune direction trouvée. Lancement d'une nouvelle chasse.")
                relancer_chasse()
        return get_direction(text)
    elif new_indice == 4:
        pyautogui.click(37, 918)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 846, 380, 891)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice 846:large vs 853:petit (+7)
        region.save('fleches/fleche4.png')
        text = pytesseract.image_to_string(region)
        text = get_direction(text)
        #print("fleche : ",text)
        if text is None or any(character.isdigit() for character in text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            pyautogui.click(38, 916)
            time.sleep(0.5)
            screenshot = pyautogui.screenshot()
            region = screenshot.crop((33, 855, 380, 891))
            text = pytesseract.image_to_string(region)
            text = get_direction(text)
            region.save('fleches/fleche4_bis.png')
            if indice_fleche_text_check(text):
                print("Aucune direction trouvée. Lancement d'une nouvelle chasse.")
                relancer_chasse()
        return get_direction(text)
    elif new_indice == 5:
        pyautogui.click(37, 946)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 875, 380, 920)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche5.png')
        text = pytesseract.image_to_string(region)
        text = get_direction(text)
        #print("fleche : ",text)
        if text is None or any(character.isdigit() for character in text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            pyautogui.click(38, 946)
            time.sleep(0.5)
            screenshot = pyautogui.screenshot()
            region = screenshot.crop((33, 884, 380, 920))
            text = pytesseract.image_to_string(region)
            text = get_direction(text)
            region.save('fleches/fleche5_bis.png')
            if indice_fleche_text_check(text):
                print("Aucune direction trouvée. Lancement d'une nouvelle chasse.")
                relancer_chasse()
        return get_direction(text)
    elif new_indice == 6:
        pyautogui.click(37, 976)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 904, 380, 949)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche6.png')
        text = pytesseract.image_to_string(region)
        text = get_direction(text)
        #print("fleche : ",text)
        if text is None or any(character.isdigit() for character in text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            pyautogui.click(38, 973)
            time.sleep(0.5)
            screenshot = pyautogui.screenshot()
            region = screenshot.crop((33, 913, 380, 949))
            text = pytesseract.image_to_string(region)
            text = get_direction(text)
            region.save('fleches/fleche6_bis.png')
            if indice_fleche_text_check(text):
                print("Aucune direction trouvée. Lancement d'une nouvelle chasse.")
                relancer_chasse()
        return text

#Récupère la direction indiquée par la fleche
def get_direction(text):
    directions = ['est', 'ouest', 'nord', 'sud']
    special_cases = {'louest': 'ouest', 'lest': 'est', 'Fest' : 'est', 'Fouest' : 'ouest', 'fouest' : 'ouest', 'fest' : 'est', 'su' : 'sud', 'oues' : 'ouest', 'Vest' : 'est', 'Vouest' : 'ouest'}
    found_direction = None
    for direction in directions:
        if re.search(r'\b' + direction + r'\b', text, re.IGNORECASE):
            found_direction = direction
            break
    if found_direction is None:  # si aucune direction standard n'a été trouvée, vérifier les cas spéciaux
        for case, direction in special_cases.items():
            if re.search(r'\b' + case + r'\b', text, re.IGNORECASE):
                found_direction = direction
                break
    return found_direction

def indice_fleche_text_check(text): # check le text retourné en lisant un indice ou une direction
    # si text est None alors return False
    if text is None:
        return True

    # Chercher des mots de trois lettres ou plus (si yen a pas alors c'est probablement pas un indice, donc return False)
    matches = re.findall(r'\b\w{2,}\b', text, re.UNICODE)
    # Cherche si y'a pas un un chiffre dans la String (si y'en a, alors c'est probablement pas un indice donc return False)
    # Cherche d'autres trucs qui fait que c pas un indice
    if any(character.isdigit() for character in text) or not matches or not text or 'Départ' in text:
        return True
    else:
        return False


#Cherche la direction et l'indice et remplis les champs dans dofusdb
def remplir_indice():
    global indice_fill
    #Cherche la direction et l'indice
    text = ""
    # Pleins de vérifs pour etre sur que la string recue est bien un indice, si c'est pas un indice, alors on passe à l'indice suivant
    if(indice_fill == False):
        while indice_fleche_text_check(text):
            text = get_indice()
        pyperclip.copy(text)
    indice_fill = False
    direction = get_fleche()

    if "Phorreur" in text:
        print("Phorreur détécté !")
        move_to_phorreur(direction)
        time.sleep(0.5)
        tick_flag()
        time.sleep(0.5)
        check_and_fill_coordinates()
        raise TerminateExecution() #stop l'execution de cette fonction ainsi que celle d'avant
    time.sleep(0.5)
    alt_tab()
    if direction == 'nord':
        indice_up()
    elif direction == 'sud':
        indice_down()
    elif direction == 'ouest':
        indice_left()
    elif direction == 'est':
        indice_right()
    else:
        print("AUCUNE DIRECTION TROUVEE ",direction)
    time.sleep(1)
    # Remplis les champs dans dofusdb
    pyautogui.click(1015, 535)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.8)
    pyautogui.press('down')
    time.sleep(0.2)
    pyautogui.press('enter')
    alt_tab()

def verif_indice_dofusdb():
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    # Crop the image to the area of interest
    region = screenshot.crop((2245, 991, 2553, 1018))
    region.save("DOSKDOPQSD.png")
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(region)
    # Check if the words "copiée" and "dans" are in the text
    if "copiée" in text and "dans" in text:
        return True
    else:
        return False

# Récupère la coordonnée du prochain indice
def get_coord_destination():
    # Récupère le contenu du presse-papiers
    clipboard_content = pyperclip.paste()
    # Utilise une expression régulière pour trouver les coordonnées dans la chaîne
    matches = re.findall(r'-?\d+', clipboard_content)
    # Si deux coordonnées ont été trouvées...
    if len(matches) == 2:
        # ...stocke les dans x et y
        x, y = map(int, matches)
        return x, y
    else:
        return None, None

def determine_direction_and_distance():
    # Décompresse les coordonnées de départ et d'arrivée
    start_coordinates = get_coordinates()
    end_coordinates = get_coord_destination()
    # Si une des deux fonctions n'a pas trouvé de coordonnées, on renvoie None
    if start_coordinates is None:
        print("Echec lors de la récupération des coordonnées de départ : ",start_coordinates)
        return None, 0
    # Si une des deux fonctions n'a pas trouvé de coordonnées, on renvoie None
    if end_coordinates is None:
        print("Echec lors de la récupération des coordonnées d'arrivée : ",end_coordinates)
        return None, 0
    
    start_x, start_y = start_coordinates
    end_x, end_y = end_coordinates
    # Calcule la différence entre les coordonnées de départ et d'arrivée
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    # Détermine la direction et la distance du déplacement
    if delta_x != 0:
        # Si delta_x n'est pas 0, le mouvement est horizontal
        direction = 'right' if delta_x > 0 else 'left'
        distance = abs(delta_x)
    elif delta_y != 0:
        # Si delta_y n'est pas 0, le mouvement est vertical
        direction = 'down' if delta_y > 0 else 'up'
        distance = abs(delta_y)
    else:
        # Si ni delta_x ni delta_y ne sont pas 0, il n'y a pas de mouvement
        direction = None
        distance = 0
    return direction, distance

def move_to_destination(destination_x, destination_y):
    stuck_test = 0
    actual_x, actual_y = get_coordinates()
    time.sleep(0.2)
    pyautogui.click(531, 1028)
    time.sleep(0.2)
    pyautogui.write(get_autopilot_command(destination_x, destination_y))
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    while(actual_x != destination_x or actual_y != destination_y):
        time.sleep(1)
        stuck_test += 1
        actual_x, actual_y = get_coordinates()
        if(stuck_test > 120):
            print("Personnage bloqué lors d'un déplacement. Lancement d'une nouvelle chasse.")
            relancer_chasse()
    time.sleep(0.3)

def move_to_phorreur2(direction):
    # Create a mapping of directions to coordinates changes
    directions_to_coordinates_changes = {
        'nord': (0, -1),
        'sud': (0, 1),
        'est': (1, 0),
        'ouest': (-1, 0),
    }

    for i in range(11):
        x, y = get_coordinates()
        if x is None or y is None:
            print("Erreur dans la récupération des coordonnées. (get_coordinates) Lancement d'une nouvelle chasse")
            relancer_chasse()
            return

        dx, dy = directions_to_coordinates_changes.get(direction, (0, 0))
        destination_x, destination_y = x + dx, y + dy
        move_to_destination(destination_x, destination_y)

        # After moving to a new map, try to spot the phorreur
        if spot_phorreur():
            print("Phorreur trouvé !")
            return
    print("Le bot n'a pas trouvé de phorreur après 10 tentatives. Lancement d'une nouvelle chasse.")
    relancer_chasse()
#La v2 ci apres gere les doublons des phorreurs
def move_to_phorreur(direction):
    # Création d'une correspondance entre les directions et les changements de coordonnées
    directions_to_coordinates_changes = {
        'nord': (0, -1),
        'sud': (0, 1),
        'est': (1, 0),
        'ouest': (-1, 0),
    }

    for i in range(11):
        x, y = get_coordinates()
        if x is None or y is None:
            print("Erreur dans la récupération des coordonnées. (get_coordinates) Lancement d'une nouvelle chasse")
            relancer_chasse()
            return

        dx, dy = directions_to_coordinates_changes.get(direction, (0, 0))
        destination_x, destination_y = x + dx, y + dy
        move_to_destination(destination_x, destination_y)

        # Après avoir bougé sur une nouvelle carte, essayer de repérer le phorreur
        # Skip la recherche de phorreur si la carte a déjà été visitée
        if (destination_x, destination_y) in phorreur_visited_maps:
            continue

        if spot_phorreur():
            print("Phorreur trouvé !")
            phorreur_visited_maps.append((destination_x, destination_y))  # Ajoute la carte à la liste des cartes visitées
            return

    print("Le bot n'a pas trouvé de phorreur après 10 tentatives. Lancement d'une nouvelle chasse.")
    relancer_chasse()

def get_autopilot_command(destination_x, destination_y):
    return "/travel {} {}".format(destination_x, destination_y)

def get_autopilot_coord(autopilot_command):
    try:
        # Divisez la chaîne à chaque espace pour obtenir une liste de "mots"
        words = autopilot_command.split()

        # Les coordonnées devraient être le deuxième et troisième "mots"
        x = int(words[1])
        y = int(words[2])

        return x, y
    except Exception:
        print("Récupération de la destionation échouée (get_autopilot_coord). Lancement d'une nouvelle chasse.")
        relancer_chasse()

def custom_autopilot(destination_x, destination_y):
    stuck_test = 0
    actual_x, actual_y = get_coordinates()
    pyautogui.click(531, 1028)
    pyautogui.write(get_autopilot_command(destination_x, destination_y))
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    while(actual_x != destination_x or actual_y != destination_y):
        time.sleep(1)
        stuck_test += 1
        actual_x, actual_y = get_coordinates()
        if(stuck_test > 120):
            print("Personnage bloqué lors de l'autopilotage. Lancement d'une nouvelle chasse.")
            relancer_chasse()
    time.sleep(0.5)
    check_and_fill_coordinates()
    time.sleep(0.5)
    letsgo()

def tick_flag():
    time.sleep(0.2)
    global indice
    
    if indice == 1:
        new_indice = 6
    else:
        new_indice = indice - 1

    if new_indice == 1:
        pyautogui.click(308, 834)
        time.sleep(0.2)
        return
    elif new_indice == 2:
        pyautogui.click(308, 860)
        time.sleep(0.2)
        return
    elif new_indice == 3:
        pyautogui.click(308, 890)
        time.sleep(0.2)
        return
    elif new_indice == 4:
        pyautogui.click(308, 918)
        time.sleep(0.2)
        return
    elif new_indice == 5:
        pyautogui.click(308, 946)
        time.sleep(0.2)
        return
    elif new_indice == 6:
        pyautogui.click(308, 976)
        time.sleep(0.2)
        return

def valider_etape():
    global phorreur_visited_maps  # Vide la liste des phorreurs déjà rencontrés
    phorreur_visited_maps = []

    pyautogui.click(292, 1013)
    time.sleep(0.5)
    move_fenetre_chasse()

# DETECTIONS D'IMAGES ---------------------------------------------------------------------------------------------------------
def check_image(image_name):
    # localisation de l'image sur l'écran
    location = pyautogui.locateOnScreen(image_name)
    # Si l'image est détectée sur l'écran
    if location:
        return True
    else:
        return False

def check_and_click_image(image_name):
    # localisation de l'image sur l'écran
    location = pyautogui.locateOnScreen(image_name)
    # Si l'image est détectée sur l'écran
    if location:
        # on calcule le point central de l'image
        center = pyautogui.center(location)
        # on clique sur le point central de l'image
        pyautogui.click(center)
        return True
    else:
        return False

def check_and_click_zone_image(confidence, image_name, x, y, x2, y2):
    # localisation de l'image sur l'écran
    location = pyautogui.locateOnScreen(image_name, confidence=confidence, region=(x, y, x2, y2))
    # Si l'image est détectée sur l'écran
    if location:
        # on calcule le point central de l'image
        center = pyautogui.center(location)
        # on clique sur le point central de l'image
        pyautogui.click(center)
        return True
    else:
        return False

def check_zone_image(confidence, image_name, x, y, x2, y2):
    # localisation de l'image dans une zone spécifique de l'écran
    location = pyautogui.locateOnScreen(image_name, confidence=confidence, region=(x, y, x2, y2))
    
    # Si l'image est détectée dans la zone spécifique
    if location:
        return True, location
    else:
        return False

# DETECTIONS D'IMAGES ---------------------------------------------------------------------------------------------------------

def move_fenetre_chasse():
    #variables
    image_path = "autres_images/fenetre.png"
    new_location = (62, 970)
    # Attend que l'image soit à l'écran
    location = pyautogui.locateOnScreen(image_path)
    while location is None:
        time.sleep(1)
        location = pyautogui.locateOnScreen(image_path)
    # Calcule le point central de l'image
    point = pyautogui.center(location)
    # Déplace la souris vers l'image, fait un clic gauche et le maintient
    pyautogui.moveTo(point)
    pyautogui.mouseDown()
    # Déplace l'image vers la nouvelle localisation
    pyautogui.moveTo(new_location)
    # Relâche le clic gauche pour déposer l'image
    pyautogui.mouseUp()
    pyautogui.moveTo(892, 527) # recentre la souris pour pas qu'elle gene la vue du programme

def recenter_mouse():
    pyautogui.click(1300, 1017)

def attaque_good_coffre2():
    coffre_found, location = check_zone_image(0.75, "combats/GOOD_COFFRE.png", 1546, 811, 1886, 895)
    if coffre_found:
        # Calculer le centre du rectangle
        center_x = location.left + location.width / 2
        center_y = location.top + location.height / 2
        # Cliquer au centre du rectangle
        pyautogui.click(center_x, center_y)
        return True
    else:
        return False

def attaque_good_coffre():
    pyautogui.moveTo(1619, 852)
    time.sleep(0.5)
    if not check_image('combats/BAD_COFFRE.png'):
        pyautogui.click(1619, 852)
        recenter_mouse()
        return
    pyautogui.moveTo(1664, 853)
    time.sleep(0.5)
    if not check_image('combats/BAD_COFFRE.png'):
        pyautogui.click(1664, 853)
        recenter_mouse()
        return
    pyautogui.moveTo(1714, 852)
    time.sleep(0.5)
    if not check_image('combats/BAD_COFFRE.png'):
        pyautogui.click(1714, 852)
        recenter_mouse()
        return
    pyautogui.moveTo(1763, 852)
    time.sleep(0.5)
    if not check_image('combats/BAD_COFFRE.png'):
        pyautogui.click(1763, 852)
        recenter_mouse()
        return

def spot_good_coffre():
    coffre_found, location = check_zone_image("combats/GOOD_COFFRE.png", 1546, 811, 1886, 895)
    if coffre_found:
        return True
    else:
        return False

def check_debut_combat():
    time.sleep(0.5)
    if check_zone_image(0.90, "combats/condition_fermer_cbt.png", 1303, 887, 1475, 1037):
        pyautogui.click(1374, 916)
    time.sleep(0.5)
    if check_zone_image(0.98, "combats/condition_mode_crea.png", 1303, 887, 1475, 1037):
        pyautogui.click(1358, 1018)
    time.sleep(0.5)
    if check_zone_image(0.95, "combats/condition_spectateur.png", 1303, 887, 1475, 1037):
        pyautogui.click(1389, 1018)
    time.sleep(0.5)

def combat():
    global conditions_combat_valides
    # Phase de début de combat
    while not check_zone_image(0.95, "combats/bouton_pret.png", 1303, 887, 1475, 1037):
        time.sleep(0.2)
    if not conditions_combat_valides:
        check_debut_combat()
        conditions_combat_valides = True
    pyautogui.click(1384, 968) #Click prêt
    time.sleep(5)
    while(check_image('combats/check_combat.png')): # while en combat...
        if(check_image('combats/check_tour_personnage.png')): # si c'est le tour du joueur...
            pyautogui.click(1188, 953) #Fleche harcelante
            time.sleep(0.8)
            attaque_good_coffre()
            time.sleep(0.8)
            pyautogui.click(1188, 953) #Fleche harcelante
            time.sleep(0.8)
            attaque_good_coffre()
            time.sleep(0.8)
            pyautogui.press('f1') #Pass turn
            time.sleep(1.3)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(0.8)
    pyautogui.press('enter')

def go_zaap(zaap_name):
    pyautogui.click(553, 416)
    time.sleep(1)
    keyboard.write(zaap_name)
    pyautogui.press('enter')

def move_to_depart_chasse():
    # Get Départ coordinates
    start_x, start_y = get_start_coordinates()

    # Define the zones to check
    zones = [
        {'name': 'Cite d\'Astrub', 'min_x': -2, 'min_y': -28, 'max_x': 15, 'max_y': -8},
        {'name': 'Plaine des Porkass', 'min_x': -8, 'min_y': -35, 'max_x': -2, 'max_y': -9},
        {'name': 'Plaine des Porkass', 'min_x': -17, 'min_y': -18, 'max_x': -3, 'max_y': -8},
        {'name': 'Routes Rocailleuses', 'min_x': -29, 'min_y': -34, 'max_x': -16, 'max_y': -11},
        {'name': 'Massif de Cania', 'min_x': -16, 'min_y': -34, 'max_x': -10, 'max_y': -19},
        {'name': 'Lac de cania', 'min_x': -10, 'min_y': -60, 'max_x': 1, 'max_y': -35},
        {'name': 'Plaines Rocheuses', 'min_x': -25, 'min_y': -65, 'max_x': -11, 'max_y': -37},
        {'name': 'Champs de Cania', 'min_x': -40, 'min_y': -50, 'max_x': -14, 'max_y': -35},
        {'name': 'Bonta', 'min_x': -37, 'min_y': -62, 'max_x': -26, 'max_y': -50},
        {'name': 'La Bourgade', 'min_x': -89, 'min_y': -76, 'max_x': -49, 'max_y': -27},
        {'name': 'Pandala', 'min_x': 13, 'min_y': -41, 'max_x': 29, 'max_y': -18},
        {'name': 'Village cotier', 'min_x': -64, 'min_y': -11, 'max_x': -42, 'max_y': 28},
        {'name': 'Plage de la tortue', 'min_x': 28, 'min_y': 2, 'max_x': 38, 'max_y': 13},
        {'name': 'Sufokia', 'min_x': 6, 'min_y': 23, 'max_x': 25, 'max_y': 29},
        {'name': 'Plaine des scarafeuilles', 'min_x': -7, 'min_y': 23, 'max_x': 12, 'max_y': 36},
        {'name': 'Rivage sufokien', 'min_x': 1, 'min_y': 11, 'max_x': 15, 'max_y': 22},
        {'name': 'Chateau d\'Amakna', 'min_x': 2, 'min_y': -7, 'max_x': 7, 'max_y': -5},
        {'name': 'Port de madrestam', 'min_x': 6, 'min_y': -4, 'max_x': -13, 'max_y': -1},
        {'name': 'Coin des bouftous', 'min_x': -3, 'min_y': -5, 'max_x': 15, 'max_y': 13},
        {'name': 'Route des roulottes', 'min_x': -29, 'min_y': -4, 'max_x': -22, 'max_y': 28},
        {'name': 'Village des eleveurs', 'min_x': -23, 'min_y': -11, 'max_x': -7, 'max_y': 18},
        {'name': 'Brakmar', 'min_x': -37, 'min_y': 18, 'max_x': -8, 'max_y': 49},
        {'name': 'Dunes des ossements', 'min_x': 3, 'min_y': -76, 'max_x': 22, 'max_y': -55},
        {'name': 'Futaie Enneigee', 'min_x': 19, 'min_y': -91, 'max_x': 42, 'max_y': -75},
        {'name': 'Tainela', 'min_x': -3, 'min_y': -35, 'max_x': 4, 'max_y': -28},

        # Add more zones as needed
    ]

    # Check each zone
    for zone in zones:
        if zone['min_x'] <= start_x <= zone['max_x'] and zone['min_y'] <= start_y <= zone['max_y']:
            print(f"La chasse se situe dans la zone : {zone['name']}.")
            go_zaap(zone['name'])
            time.sleep(3.5)

            if(zone['name'] == 'Pandala'): #sors de la map du zaap pandala
                pyautogui.click(586, 740)
                time.sleep(4)
            x,y = get_start_coordinates()
            custom_autopilot(x,y)
            break  # Stop checking if we find a match
    else:
        print("Aucune zone n'a été trouvée.")
        relancer_chasse()

def spot_phorreur():
    # Path to the directory with images
    directory_path = 'phorreurs/'  # replace with actual path

    # Define the region where to look for the character
    region = (294, 26, 1636, 925)  # replace with actual values

    # Get list of all files in the directory
    image_files = os.listdir(directory_path)

    for image_file in image_files:
        # Construct full image path
        image_path = os.path.join(directory_path, image_file)
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.73, region=region)
            if location:
                print(f"Phorreur trouvé grâce à l'image : ",image_file)
                pyautogui.moveTo(location)
                return True
        except Exception as e:
            print(f"Error while locating image: {image_path}. Error: {e}")
            relancer_chasse()

def letsgo():
    global indice

    if not check_and_click_image('combats/bagar.png'):
        try:
            remplir_indice()
            travel_command = pyperclip.paste()
            if not any(character.isdigit() for character in travel_command):
                print("-------------------------------------------ERREUR AVEC L'INDICE, ESSAI NUMERO 2.-------------------------------------------")
                global indice_fill
                indice_fill = True
                #indice -= 1
                check_and_fill_coordinates()
                pyautogui.click(1280, 1015) #renvois le focus sur la page dofus
                remplir_indice()
        except TerminateExecution:
            if(indice == 1): #C'est si le phorreur est sur l'indice 6, alors on valide l'étape avant de relancer letsgo()
                valider_etape()
            return letsgo()# Si l'exception est lancée, mettre fin à l'exécution de letsgo() et en lancer un nouveau
        destination_x, destination_y = get_autopilot_coord(pyperclip.paste())
        move_to_destination(destination_x, destination_y)
        tick_flag()
        # si apres toutes ces actions on est à indice == 1, ca veut dire qu'on a débloqué une nouvelle étape, faut donc valider
        if(indice == 1):
            valider_etape()
    else:
        indice = 1
        combat()
        new_hunt()
        return
    time.sleep(0.5)
    letsgo()

def hotkey_autopilot():
    x,y = get_start_coordinates()
    custom_autopilot(x,y)

def relancer_chasse():
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')
    global chasses_echouees
    chasses_echouees += 1
    print("Chasse échouée N°", chasses_echouees)
    check_and_click_zone_image(0.8, "autres_images/end_hunt.png", 0, 660, 340, 1030)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    screenshot = pyautogui.screenshot()
    region = screenshot.crop((341, 986, 633, 1005)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
    text = pytesseract.image_to_string(region)
    if "Impossible" in text or "finissez" in text:
        time.sleep(120)
        relancer_chasse()
    new_hunt()

def set_canal_guilde():
    time.sleep(0.5)
    pyautogui.click(702,981)
    time.sleep(0.5)
    pyautogui.click(336,1028)
    time.sleep(0.5)
    pyautogui.click(395,1018)
    time.sleep(0.5)

# Pour faire marcher, mettre @exception_handler au dessus d'une fonction
def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Une erreur est survenue dans la fonction {func.__name__}: {str(e)}")
            # Vous pouvez également décider de renvoyer une valeur par défaut en cas d'erreur
            return None
    return wrapper

#variables
indice = 1
# indice de départ (laisser à 1 si tu fais pas de tests)
bool_new_hunt = False # pour savoir si faut rentrer de nouvelles coord dans dofusdb
hunt_count = 0 # compteur de chasse
indice_fill = False
chasses_echouees = 0
conditions_combat_valides = False
phorreur_visited_maps = []  # Liste globale pour garder une trace des cartes visitées 
canal_chat_set = False

#Actions de l'utilisateur
# keyboard.add_hotkey('q', move_left)
# keyboard.add_hotkey('d', move_right)
# keyboard.add_hotkey('z', move_up) 
# keyboard.add_hotkey('s', move_down)
keyboard.add_hotkey('p', new_hunt)
keyboard.add_hotkey('f', letsgo)
keyboard.add_hotkey('v', check_and_fill_coordinates)

keyboard.add_hotkey('*', combat)

#Attends une action clavier de l'utilisateur
keyboard.wait()
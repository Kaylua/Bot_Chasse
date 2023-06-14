import pyautogui
import pytesseract
from PIL import Image
import keyboard
import time
import re
import pyperclip
import os 
import string

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

#Remplis les coordonnées dans dofusdb
def fill_coordinates(x, y):
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
    pyautogui.click(2475, 270)  
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
    region.save('map_coordinates.png')
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(region)
    # Verification si il a bien ramassé des chiffres
    digit_count = sum(char.isdigit() for char in text)
    if digit_count is None or digit_count < 2:
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((2, 71, 171, 100))
        region.save('map_coordinates2.png')
        text = pytesseract.image_to_string(region)
        digit_count = sum(char.isdigit() for char in text)
        if digit_count is None or digit_count < 2:
            input("Echec lors de la récupération des coordonnées de la map.")
    # Si on a bien des chiffres, on continue
    text = text.replace('~', '-') # parfois tesseract lis ~ au lieu de - du coup je remplace ~ par - dans le text
    # Find coordinates in the text
    coordinates = re.findall(r'[-\d]+,[-\d]+', text)
    # Split the coordinates into two variables
    x, y = map(int, coordinates[0].split(','))
    return x,y

#Récuperes les coordonnées de la map sur laquelle on se trouve
def get_start_coordinates():
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    # You might need to adjust the region parameters according to your needs
    region = screenshot.crop((16, 776, 322, 985))
    region.save('DEPART_COORDONNEES.png')
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(region)
    text = text.replace('~', '-') # parfois tesseract lis ~ au lieu de - du coup je remplace ~ par - dans le text
    # Find coordinates in the text
    coordinates = re.findall(r'[-\d]+,[-\d]+', text)
    # Split the coordinates into two variables
    # Assuming coordinates[0] is a string like "4,-9"
    x, y = map(int, coordinates[0].split(','))
    return x,y

def check_and_fill_coordinates():
    # Find coordinates in the text
    x,y = get_coordinates()
    time.sleep(0.2)
    fill_coordinates(x,y)

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
    pyautogui.click(962, 30)  
def move_down():
    pyautogui.click(962, 922)  
#----------------------------------------------------------------------------------

#Lance une nouvelle chasse
def new_hunt():
    pyautogui.hotkey('h')
    time.sleep(1)
    pyautogui.click(553, 422)
    time.sleep(0.2)
    pyautogui.hotkey('enter')
    time.sleep(1.3)
    move_right()
    time.sleep(3.5)
    move_right()
    time.sleep(4.8)
    pyautogui.click(950, 463)
    time.sleep(3.2)
    pyautogui.click(1429, 482)
    time.sleep(4)
    pyautogui.click(1035, 479)
    pyautogui.click(1090, 519)    
    time.sleep(4)
    move_fenetre_chasse()
    time.sleep(0.5)
    pyautogui.click(371, 848)
    time.sleep(4.5)
    pyautogui.click(539, 818)
    time.sleep(4.2)
    pyautogui.hotkey('h')
    time.sleep(1.5)
    pyautogui.click(553, 416)
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
    cleaned_string = cleaned_string.replace("comne", "corne").replace("comnes", "cornes")
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
def get_fleche():
    global indice
    
    if indice == 1:
        new_indice = 6
    else:
        new_indice = indice - 1

    if new_indice == 1:
        pyautogui.moveTo(37, 834)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 759, 380, 804)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche1.png')
        text = pytesseract.image_to_string(region)
        #print(text)
        if indice_fleche_text_check(text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            region = screenshot.crop((33, 766, 380, 804))
            text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 2:
        pyautogui.moveTo(37, 860)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 788, 380, 833)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche2.png')
        text = pytesseract.image_to_string(region)
        #print(text)
        if indice_fleche_text_check(text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            region = screenshot.crop((33, 795, 380, 833))
            text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 3:
        pyautogui.moveTo(37, 890)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 817, 380, 862)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche3.png')
        text = pytesseract.image_to_string(region)
        #print(text)
        if indice_fleche_text_check(text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            region = screenshot.crop((33, 824, 380, 862))
            text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 4:
        pyautogui.moveTo(37, 918)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 846, 380, 891)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice 846:large vs 853:petit (+7)
        region.save('fleches/fleche4.png')
        text = pytesseract.image_to_string(region)
        #print(text)
        if indice_fleche_text_check(text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            region = screenshot.crop((33, 853, 380, 891))
            text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 5:
        pyautogui.moveTo(37, 946)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 875, 380, 920)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche5.png')
        text = pytesseract.image_to_string(region)
        #print(text)
        if indice_fleche_text_check(text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            region = screenshot.crop((33, 882, 380, 920))
            text = pytesseract.image_to_string(region)
        return get_direction(text)
    elif new_indice == 6:
        pyautogui.moveTo(37, 976)
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        region = screenshot.crop((33, 904, 380, 949)) # 898 si je met plus ca descends si je met moins ca monte , +29 ou -29 pour monter d'un indice
        region.save('fleches/fleche6.png')
        text = pytesseract.image_to_string(region)
        #print(text)
        if indice_fleche_text_check(text): # Si ca retourne pas une bonne direction, ré essayer avec une autre prise de vue du screen (car certaines directions sont sur 2 lignes et d'autres 1)
            region = screenshot.crop((33, 911, 380, 949))
            text = pytesseract.image_to_string(region)
        return get_direction(text)

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
    #check si on viens de commencer la chasse, si oui alors on rentre les coordonnées dans dofusdb
    global bool_new_hunt
    if(bool_new_hunt == True):
        check_and_fill_coordinates()
        bool_new_hunt = False
    #Cherche la direction et l'indice
    text = ""
    # Pleins de vérifs pour etre sur que la string recue est bien un indice, si c'est pas un indice, alors on passe à l'indice suivant
    while indice_fleche_text_check(text):
        text = get_indice()
    pyperclip.copy(text)
    direction = get_fleche()

    if "Phorreur" in text:
        print("Phorreur détécté !")
        move_to_phorreur(direction)
        time.sleep(0.5)
        tick_flag()
        time.sleep(0.5)
        check_and_fill_coordinates()
        raise TerminateExecution() #stop l'execution de cette fonction ainsi que celle d'avant
    time.sleep(0.2)
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
    time.sleep(0.2)
    
    # Remplis les champs dans dofusdb
    pyautogui.click(2255, 541)
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('down')
    time.sleep(0.2)
    pyautogui.press('enter')

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

# Réalise les deplacements, sans temps de latence prédéfini grace a la boucle why qui test tous le temps les coordonnées
# Si le bot n'a pas changé de map au bout de 10 secondes, il est alors stoppé car considéré comme bloqué
def move_to_destination():
    direction, distance = determine_direction_and_distance()
    if(direction == 'right'):
        for i in range(distance):
            x,y = get_coordinates()
            new_x = 999
            stuck_test = 0
            move_right()
            while new_x!=x+1:
                time.sleep(0.5)
                new_x,y = get_coordinates()
                stuck_test += 1
                if stuck_test > 10:
                    input("Personnage bloqué!")

    elif(direction == 'left'):
        for i in range(distance):
            x,y = get_coordinates()
            new_x = 999
            stuck_test = 0
            move_left()
            while new_x!=x-1:
                time.sleep(0.5)
                new_x,y = get_coordinates()
                stuck_test += 1
                if stuck_test > 10:
                    input("Personnage bloqué!")
    elif(direction == 'up'):
        for i in range(distance):
            x,y = get_coordinates()
            new_y = 999
            stuck_test = 0
            move_up()
            while new_y!=y-1:
                time.sleep(0.5)
                x,new_y = get_coordinates()
                stuck_test += 1
                if stuck_test > 10:
                    input("Personnage bloqué!")
    elif(direction == 'down'):
        for i in range(distance):
            x,y = get_coordinates()
            new_y = 999
            stuck_test = 0
            move_down()
            while new_y!=y+1:
                time.sleep(0.5)
                x,new_y = get_coordinates()
                stuck_test += 1
                if stuck_test > 10:
                    input("Personnage bloqué!")

def move_to_destination_v2():
    # Create a mapping of directions to functions
    directions_functions = {
        'right': move_right,
        'left': move_left,
        'down': move_down,
        'up': move_up
    }

    direction, distance = determine_direction_and_distance()

    for i in range(distance):
        x, y = get_coordinates()
        new_x, new_y = x, y
        stuck_test = 0
        directions_functions[direction]()
        while (new_x != x + 1 if direction == 'right' else new_x != x - 1 if direction == 'left' else new_y != y - 1 if direction == 'up' else new_y != y + 1):
            time.sleep(1)
            new_x, new_y = get_coordinates()
            stuck_test += 1
            if stuck_test == 10:
                print("Personnage bloqué, tentative de contournement.")
                alternative_direction = 'up' if direction in ['right', 'left'] else 'right'
                directions_functions[alternative_direction]()
                time.sleep(6)
                # Check if the move was successful
                new_x, new_y = get_coordinates()
                if (new_x != x + 1 if alternative_direction == 'right' else new_x != x - 1 if alternative_direction == 'left' else new_y != y - 1 if alternative_direction == 'up' else new_y != y + 1):
                    input("Détournement échoué, personnage bloqué.")
                    return
                directions_functions[direction]()
                time.sleep(6)
                # Check if the move was successful
                new_x, new_y = get_coordinates()
                if (new_x != x + 1 if direction == 'right' else new_x != x - 1 if direction == 'left' else new_y != y - 1 if direction == 'up' else new_y != y + 1):
                    input("Détournement échoué, personnage bloqué.")
                    return
                alternative_direction = 'down' if direction in ['right', 'left'] else 'left'
                directions_functions[alternative_direction]()
                time.sleep(6)
                stuck_test = 0

def move_to_phorreur(direction):
    if(direction == 'nord'):
        direction = 'up'
    elif(direction == 'sud'):
        direction = 'down'
    elif(direction == 'est'):
        direction = 'right'
    elif(direction == 'ouest'):
        direction = 'left'

    # Create a mapping of directions to functions
    directions_functions = {
        'right': move_right,
        'left': move_left,
        'down': move_down,
        'up': move_up
    }

    for i in range(11):
        x, y = get_coordinates()
        if x is None or y is None:
            print("Erreur dans la récupération des coordonnées.")
            return
        new_x, new_y = x, y
        stuck_test = 0
        directions_functions[direction]()
        while (new_x != x + 1 if direction == 'right' else new_x != x - 1 if direction == 'left' else new_y != y - 1 if direction == 'up' else new_y != y + 1):
            time.sleep(1)
            new_x, new_y = get_coordinates()
            stuck_test += 1
            if stuck_test == 10:
                print("Personnage bloqué, tentative de contournement.")
                alternative_direction = 'up' if direction in ['right', 'left'] else 'right'
                directions_functions[alternative_direction]()
                time.sleep(6)
                # Check if the move was successful
                new_x, new_y = get_coordinates()
                if (new_x != x + 1 if alternative_direction == 'right' else new_x != x - 1 if alternative_direction == 'left' else new_y != y - 1 if alternative_direction == 'up' else new_y != y + 1):
                    input("Détournement échoué, personnage bloqué.")
                    return
                directions_functions[direction]()
                time.sleep(6)
                # Check if the move was successful
                new_x, new_y = get_coordinates()
                if (new_x != x + 1 if direction == 'right' else new_x != x - 1 if direction == 'left' else new_y != y - 1 if direction == 'up' else new_y != y + 1):
                    input("Détournement échoué, personnage bloqué.")
                    return
                alternative_direction = 'down' if direction in ['right', 'left'] else 'left'
                directions_functions[alternative_direction]()
                time.sleep(6)
                stuck_test = 0

        # After moving to a new map, try to spot the phorreur
        if spot_phorreur():
            print("Phorreur trouvé !")
            return
    input("Le bot n'a pas trouvé de phorreur après 10 tentatives.")

def custom_autopilot():
    # Get Départ coordinates
    destination_x, destination_y = get_start_coordinates()

    print("Direction : [",destination_x,",",destination_y,"]")
    # Get current coordinates
    x, y = get_coordinates()
    # Determine direction and distance
    x_direction = 'right' if destination_x > x else 'left'
    y_direction = 'down' if destination_y > y else 'up'
    x_distance = abs(destination_x - x)
    y_distance = abs(destination_y - y)
    # Create a mapping of directions to functions
    directions_functions = {
        'right': move_right,
        'left': move_left,
        'down': move_down,
        'up': move_up
    }
    # Calculate the maximum distance to travel in either direction
    max_distance = max(x_distance, y_distance)
    for i in range(max_distance):
        for direction, distance in [(x_direction, x_distance), (y_direction, y_distance)]:
            if i < distance:  
                x, y = get_coordinates()
                new_x, new_y = x, y
                stuck_test = 0
                directions_functions[direction]() 
                while (new_x != x + 1 if direction == 'right' else new_x != x - 1 if direction == 'left' else new_y != y - 1 if direction == 'up' else new_y != y + 1):
                    time.sleep(1)
                    new_x, new_y = get_coordinates()
                    stuck_test += 1
                    if stuck_test == 10:
                        print("Personnage bloqué, tentative de contournement.")
                        alternative_direction = 'up' if direction in ['right', 'left'] else 'right'
                        directions_functions[alternative_direction]()
                        time.sleep(6)
                        # Check if the move was successful
                        new_x, new_y = get_coordinates()
                        if (new_x != x + 1 if alternative_direction == 'right' else new_x != x - 1 if alternative_direction == 'left' else new_y != y - 1 if alternative_direction == 'up' else new_y != y + 1):
                            input("Détournement échoué, personnage bloqué.")
                        directions_functions[direction]()
                        time.sleep(6)
                        # Check if the move was successful
                        new_x, new_y = get_coordinates()
                        if (new_x != x + 1 if direction == 'right' else new_x != x - 1 if direction == 'left' else new_y != y - 1 if direction == 'up' else new_y != y + 1):
                            input("Détournement échoué, personnage bloqué.")
                        alternative_direction = 'down' if direction in ['right', 'left'] else 'left'
                        directions_functions[alternative_direction]()
                        time.sleep(6)
                        stuck_test = 0

    time.sleep(0.5)
    check_and_fill_coordinates
    time.sleep(0.5)
    letsgo()

def tick_flag():
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

def check_and_click_zone_image(image_name, x, y, x2, y2):
    # localisation de l'image sur l'écran
    location = pyautogui.locateOnScreen(image_name, region=(x, y, x2, y2))
    # Si l'image est détectée sur l'écran
    if location:
        # on calcule le point central de l'image
        center = pyautogui.center(location)
        # on clique sur le point central de l'image
        pyautogui.click(center)
        return True
    else:
        return False

def check_zone_image(image_name, x, y, x2, y2):
    # localisation de l'image dans une zone spécifique de l'écran
    location = pyautogui.locateOnScreen(image_name, region=(x, y, x2, y2))
    # Si l'image est détectée dans la zone spécifique
    if location:
        return True
    else:
        return False
# DETECTIONS D'IMAGES ---------------------------------------------------------------------------------------------------------

def move_fenetre_chasse():
    #variables
    image_path = "TEMPORAIRE_CHASSE_LEGENDAIRE.png"
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
    pyautogui.moveTo(1744, 1010)

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
    
def combat():
    # Phase de début de combat
    time.sleep(2)
    pyautogui.click(1384, 968) #Click prêt
    time.sleep(5)
    # pyautogui.click(894, 995) #Tir eloigne
    # time.sleep(0.5)
    # pyautogui.click(1822, 851) #Click personnage
    # recenter_mouse()
    # time.sleep(0.5)
    # pyautogui.click(1188, 953) #Fleche harcelante
    # time.sleep(0.5)
    # attaque_good_coffre()
    # time.sleep(0.5)
    # pyautogui.click(1188, 953) #Fleche harcelante
    # time.sleep(0.5)
    # attaque_good_coffre()
    # time.sleep(0.5)
    # pyautogui.press('f1') #Pass turn
    # time.sleep(0.5)
    #Loop
    while(check_image('combats/check_combat.png')): # while en combat...
        if(check_image('combats/check_tour_personnage.png')): # si c'est le tour du joueur...
            pyautogui.click(1188, 953) #Fleche harcelante
            time.sleep(0.5)
            attaque_good_coffre()
            time.sleep(0.5)
            pyautogui.click(1188, 953) #Fleche harcelante
            time.sleep(0.5)
            attaque_good_coffre()
            time.sleep(0.5)
            pyautogui.click(1188, 953) #Fleche harcelante
            time.sleep(0.5)
            attaque_good_coffre()
            time.sleep(0.5)
            pyautogui.press('f1') #Pass turn
            time.sleep(1)
    time.sleep(3)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('enter')

def go_zaap(zaap_name):
    pyautogui.click(1080, 241)
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
        {'name': 'Port de madrestam', 'min_x': 6, 'min_y': -4, 'max_x': -13, 'max_y': -2},
        {'name': 'Coin des bouftous', 'min_x': -3, 'min_y': -5, 'max_x': 15, 'max_y': 13},
        {'name': 'Route des roulottes', 'min_x': -29, 'min_y': -4, 'max_x': -22, 'max_y': 28},
        {'name': 'Village des eleveurs', 'min_x': -23, 'min_y': -11, 'max_x': -7, 'max_y': 18},
        {'name': 'Brakmar', 'min_x': -37, 'min_y': 18, 'max_x': -8, 'max_y': 49},
        {'name': 'Dunes des ossements', 'min_x': 3, 'min_y': -76, 'max_x': 22, 'max_y': -55},
        # Add more zones as needed
    ]

    # Check each zone
    for zone in zones:
        if zone['min_x'] <= start_x <= zone['max_x'] and zone['min_y'] <= start_y <= zone['max_y']:
            print(f"La chasse se situe dans la zone : {zone['name']}.")
            go_zaap(zone['name'])
            time.sleep(2)

            if(zone['name'] == 'Pandala'): #sors de la map du zaap pandala
                pyautogui.click(586, 740)
                time.sleep(2)
            custom_autopilot()
            break  # Stop checking if we find a match
    else:
        print("Aucune zone n'a été trouvée.")

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
            location = pyautogui.locateOnScreen(image_path, confidence=0.7, region=region)
            if location:
                print(f"Phorreur trouvé grâce à l'image : ",image_file)
                pyautogui.moveTo(location)
                return True
        except Exception as e:
            print(f"Error while locating image: {image_path}. Error: {e}")

def letsgo():
    global indice

    if not check_and_click_image('combats/bagar.png'):
        try:
            remplir_indice()
        except TerminateExecution:
            if(indice == 1): #C'est si le phorreur est sur l'indice 6, alors on valide l'étape avant de relancer letsgo()
                valider_etape()
            return letsgo()# Si l'exception est lancée, mettre fin à l'exécution de letsgo() et en lancer un nouveau
        move_to_destination()
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

#variables
indice = 1 # indice de départ (laisser à 1 si tu fais pas de tests)
bool_new_hunt = False # pour savoir si faut rentrer de nouvelles coord dans dofusdb
hunt_count = 0 # compteur de chasse

#Actions de l'utilisateur
# keyboard.add_hotkey('q', move_left)
# keyboard.add_hotkey('d', move_right)
# keyboard.add_hotkey('z', move_up) 
# keyboard.add_hotkey('s', move_down)
keyboard.add_hotkey('²', new_hunt)
keyboard.add_hotkey('f', letsgo)
keyboard.add_hotkey('v', check_and_fill_coordinates)

keyboard.add_hotkey('*', custom_autopilot)
# keyboard.add_hotkey('c', custom_autopilot)

#Attends une action clavier de l'utilisateur
keyboard.wait()

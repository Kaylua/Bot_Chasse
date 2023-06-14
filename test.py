import pytesseract
from PIL import Image
import pyautogui
# Chemin vers l'image à traiter
image_path = 'map_coordinates.png'

# Charger l'image avec PIL (Pillow)
image = Image.open(image_path)

# Utiliser Tesseract pour reconnaître le texte dans l'image
text = pytesseract.image_to_string(image)

# Afficher le texte extrait
print(text)

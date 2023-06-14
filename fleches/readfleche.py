from PIL import Image
import pytesseract
import os

# Setup pytesseract
os.environ['TESSDATA_PREFIX'] = r'C:\Users\ruben\AppData\Local\Programs\Tesseract-OCR\tessdata'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\ruben\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Change this to your Tesseract-OCR installation location

# Charger une image à partir d'un fichier
image = Image.open('fleche3.png')

# Utiliser tesseract pour extraire le texte de l'image
text = pytesseract.image_to_string(image, lang='fra')

# Imprimer le texte extrait
print(text)

from PIL import Image
from pytesseract import *

image = Image.open('image_04.jpg')

print_image = image_to_string(image, lang='eng')
print(print_image)
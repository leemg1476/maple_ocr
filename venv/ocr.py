from PIL import Image
from pytesseract import *
import matplotlib.pylab as plt

image = Image.open('image_05.jpg')
size = image.size
image = image.resize((size[0]*3,size[1]*3))

plt.imshow(image)
plt.show()

print_image = image_to_string(image, lang='kor')
print(print_image)
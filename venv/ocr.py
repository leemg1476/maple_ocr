from PIL import Image
from pytesseract import *
import matplotlib.pylab as plt
import os
import sqlite3
import pandas as pd


def ITT(image):
    image = Image.open('image_05.jpg')
    size = image.size
    image = image.resize((size[0]*3,size[1]*3))

    plt.imshow(image)
    plt.show()

    img_string = image_to_string(image, lang='kor')

    return img_string

#
# conn = sqlite3.connect('maple_daily_quest.db',isolation_level=None)
# c = conn.cursor()

# c.execute("CREATE TABLE IF NOT EXISTS table1 \
#         (id integer PRIMARY KEY, name text, birthday text)")
#
# c.execute("INSERT INTO table1 \
#         VALUES(1, 'LEE','1987-00-00')")


file = pd.read_excel('maple_daily_quest_index.xlsx')

print(file)



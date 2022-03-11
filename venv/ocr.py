from PIL import Image
from PIL import ImageFilter as imgfilter
from pytesseract import *
import matplotlib.pylab as plt
import os
import sqlite3
import pandas as pd
from difflib import SequenceMatcher as sm


def ITT(image_path,mode):
    image = Image.open('image_07.jpg').convert('L')
    size = image.size
    image = image.resize((size[0]*3,size[1]*3))

    image = image.filter(imgfilter.GaussianBlur)
    image = image.filter(imgfilter.SHARPEN)
    image = image.filter(imgfilter.GaussianBlur)

    plt.imshow(image)
    plt.show()

    img_string = image_to_string(image, lang=mode)
    img_string = img_string.split('\n')
    return img_string[:-1]

def find_quest_index(string_kor,string_eng):
    file = pd.read_csv('maple_daily_quest_index.csv')
    file = file.dropna(axis=0)
    file = file.dropna(axis=1)

    maxs = 0
    max_tmp = ''
    for i in range(len(file)):
        a,name,level = file.iloc[i]
        x = round(sm(None,string_kor,name).ratio(),3)
        if x > maxs:
            maxs = x
            max_tmp = name

        elif x == maxs:
            eng_ratio_name = round(sm(None,string_eng,name).ratio(),3)
            eng_ratio_maxs = round(sm(None,string_eng,max_tmp).ratio(),3)
            if eng_ratio_name > eng_ratio_maxs:
                max_tmp = name
                maxs = x

            continue

    tmp = file.loc[file['일퀘이름'] == max_tmp]
    area = tmp['지역'].values[0]
    # print(area)#이름으로 지역 추출


    quest_index = file.loc[file['지역'] == area]
    # print(quest_index)#지역으로 퀘스트 목록 추출

    tmp_index = file[file['일퀘이름'] == max_tmp].index
    quest_index = quest_index.drop(tmp_index)#인식된 목록을 제외한 퀘스트 목록 추출

# conn = sqlite3.connect('maple_daily_quest.db',isolation_level=None)
# c = conn.cursor()

# c.execute("CREATE TABLE IF NOT EXISTS table1 \
#         (id integer PRIMARY KEY, name text, birthday text)")
#
# c.execute("INSERT INTO table1 \
#         VALUES(1, 'LEE','1987-00-00')")







from PIL import Image
from PIL import ImageFilter as imgfilter
from pytesseract import *
from difflib import SequenceMatcher as sm

from itertools import combinations as comb
from collections import defaultdict
import base64
import sys
import numpy as np
from io import BytesIO

def ITT(img,mode):
    image = img.convert('L')
    size = image.size
    image = image.resize((size[0]*3,size[1]*3))

    image = image.filter(imgfilter.GaussianBlur)
    image = image.filter(imgfilter.SHARPEN)
    image = image.filter(imgfilter.GaussianBlur)

    # plt.imshow(image)
    # plt.show()

    img_string_kor = image_to_string(image, lang='kor')
    img_string_kor = img_string_kor.split('\n')

    img_string_eng = image_to_string(image, lang='eng')
    img_string_eng = img_string_eng.split('\n')

    d = image_to_data(image,output_type=Output.DICT)
    n_boxes = len(d['level'])

    location = []
    for i in range(n_boxes):
        x, y, w, h = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        location.append([x,y,w,h])

    location.sort(key = lambda x: x[1])
    location_y = [[y,h] for _,y,_,h in location[1:]]

    return img_string_kor[:-1],img_string_eng[:-1],location_y



def find_quest_index(string_kors,string_engs):
    file = pd.read_csv('maple_daily_quest_index.csv')
    file = file.dropna(axis=0)
    file = file.dropna(axis=1)

    tmp = [[] for _ in range(len(string_kors))]
    maxs = [0 for _ in range(len(string_kors))]

    for i in range(len(file)):
        a,name,level = file.iloc[i]

        for j,(string_kor, string_eng) in enumerate(zip(string_kors, string_engs)):

            x = round(sm(None,string_kor,name).ratio(),3)

            if x > maxs[j]:
                maxs[j] = x
                tmp[j] = [name,level,j]

            elif x == maxs[j]:
                eng_ratio_name = round(sm(None,string_eng,name).ratio(),3)
                eng_ratio_maxs = round(sm(None,string_eng,tmp[j]).ratio(),3)
                if eng_ratio_name > eng_ratio_maxs:
                    tmp[j] = [name,level,j]
                    maxs[j] = x


    tmp_quest_index = file.loc[file['일퀘이름'] == tmp[0][0]]
    area = tmp_quest_index['지역'].values[0]
    # print(area)#이름으로 지역 추출


    quest_index = file.loc[file['지역'] == area]
    # print(quest_index)#지역으로 퀘스트 목록 추출

    for _,i,_ in tmp:
        tmp_index = quest_index[quest_index['일퀘이름'] == i].index
        quest_index = quest_index.drop(tmp_index)#인식된 목록을 제외한 퀘스트 목록 추출


    sorted_raw_quest = sorted(tmp, key = lambda x: -x[1])
    n = len(quest_index)


    result = []
    result_maxs = 0

    for i in range(1,len(sorted_raw_quest)+1):

        x = sorted_raw_quest[:i]
        total_x = 0
        for _,j,_ in x:
            total_x += j

        quest_list = quest_index.values.tolist()
        quest_comb = list(comb(quest_list,i))

        upper_case = 0
        lower_case = 0
        for x_tmp in quest_comb:

            total_comb = 0
            for _,_,j in x_tmp:
                total_comb += int(j)

            if total_comb > total_x:

                upper_case += 1

            elif total_comb < total_x:

                lower_case += 1

        if upper_case >= lower_case:
            break

        else:

            if result_maxs < round(lower_case/(upper_case+lower_case),3):

                result.append(sorted_raw_quest[i-1])
                result_maxs = round(lower_case/(upper_case+lower_case),3)

            else:
                break

    res_index = [i for _,_,i in result]
    return res_index




def get_rect_from_image(image,location_y,result_index):


    dic = defaultdict(int)

    for y,h in location_y:
        if dic[y] == 0:
            dic[y] = h
        elif dic[y] > h:
            dic[y] = h
    for i in range(image.size[0]):
        for j in range(image.size[1]):

            for k,y in enumerate(dic):
                h = dic[y]

                if not(k in result_index):
                    continue

                rgb = image.getpixel((i, j))
                if y <= j <= y+h:
                    if rgb != (255,255,255):
                        image.putpixel((i,j),(rgb[2],rgb[1],rgb[0]))
                        break
                else:
                    continue
    image = image.resize((image.size[0]//3,image.size[1]//3))

    return image


def main(base_stirng):

    img = Image.open(BytesIO(base64.b64decode(base_string)))
    size = img.size
    img = img.resize((size[0]*3,size[1]*3))

    string_kor,string_eng,location_y = ITT(img,'kor')

    result_index = find_quest_index(string_kor,string_eng)

    imgs = get_rect_from_image(x,location_y,result_index)

    buffer = BytesIO()
    imgs.save(buffer,format = 'jpg')
    img_string = base64.b64encode(buffer.getvalue())

    return img_string




# string_kors = ITT('image_07.jpg','kor')
# string_engs = ITT('image_07.jpg','eng')
#
# # print(string_kor,string_eng)
#
# print(string_kors,string_engs)
# find_quest_index(string_kors,string_engs)



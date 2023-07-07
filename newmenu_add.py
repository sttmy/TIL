from utils.Preprocess import Preprocess
from tensorflow.keras import preprocessing
import pickle


import re
from re import search, findall, match, sub

try:
    new_menu = input('새로운 메뉴를 입력하세요: ')
    ##### ① user_dic 단어, 품사정보에 추가
    num = 0
    with open('../utils/user_dic.tsv', 'a', encoding='utf-8') as f:
        add = '\n'+new_menu+'\t'+'NNG'
        f.write(add)
        num += 1
    print('num-->', num)

    ##### ② corpus 말뭉치에 추가
    txt1 = open('../train_tools/dict/corpus2add.txt', mode='r', encoding='UTF8')
    txt2 = txt1.readlines()
    num = 0
    with open('../train_tools/dict/corpus2add.txt', 'a', encoding='utf-8') as f:
        for i in txt2:
            if search('짜장면', i) and i:
                i = re.sub("짜장면", new_menu, i)
                num += 1
                f.write(i)
            else:
                pass
    print('num-->', num)

    ##### ③ intent 의도분류 데이터에 추가
    txt1 = open('../models/intent/total_train_data2.csv', mode='r', encoding='UTF8')
    txt2 = txt1.readlines()
    num = 0
    with open('../models/intent/total_train_data2.csv', 'a', encoding='utf-8') as f:
        for i in txt2:
            if search('짜장면', i) and i:
                i = re.sub("짜장면", new_menu, i)
                num += 1
                f.write(i)
            else:
                pass
    print('num-->', num)

    ##### ④ ner_train 개체명 인식데이터에 추가
    file_name = '../models/ner/ner_train2add.txt'
    num = 0
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(file_name, 'a', encoding='utf-8') as f:
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx + 1][0] == '$':
                this_sent = []
                this_sent.append(l)
            elif l[0] == '$' and lines[idx - 1][0] == ';':
                this_sent.append(l)
            elif l[0] == '\n':
                menu = '짜장면'
                if menu in this_sent[0]:
                    sents = []
                    for i in this_sent:
                        if menu in i:
                            i = re.sub(menu, new_menu, i)
                        sents.append(i)
                    for j in sents:
                        num += 1
                        f.writelines(j)
                else:
                    pass
            else:
                this_sent.append(l)
    print('num: ', num)
except Exception as e:
    print("오류 발생 : ", e)
finally:
    print('종료되었습니다')
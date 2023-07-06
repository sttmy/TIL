# /test 디렉터리 model_ner_test.py

from utils.Preprocess import Preprocess
from models.ner.NerModel import NerModel

p = Preprocess(word2index_dic='chatbot_dict2.bin',
               userdic = '../../utils/user_dic.tsv')    # 인자 추가!!!

ner = NerModel(model_name = '../models/ner/ner_model.h5', preprocess = p)
query = '오늘 오전 13시 2분에 탕수육 주문하고 싶어요'
predicts = ner.predict(query)
print(predicts)
# -*- utf-8 -*-
from wordcloud import WordCloud
from os import path
import numpy as np
from PIL import Image
import jieba
import json

file = open('items.json')
companyLabel = ''
for eachline in file:
    d = json.loads(eachline)
    if(d.has_key('companyLabelList')):
        companyLabel += ','.join(d['companyLabelList'])+','

cut_str = jieba.cut(companyLabel)
result = '/'.join(cut_str)

background = np.array(Image.open(path.join("money.jpg")))
wc = WordCloud(font_path='./msyh.ttf', mask=background, background_color='black', width=800, height=600, max_font_size=100, max_words=2000, min_font_size=20,
               mode='RGBA', colormap='pink')

wc.generate(result)
wc.to_file(r"./companyLabelList.png")

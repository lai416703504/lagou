# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.sans-serif'] = ['SimHei']
custom_font = mpl.font_manager.FontProperties(fname='msyh.ttf')

file = open('items.json')
joblist = []
for eachline in file:
    joblist.append(json.loads(eachline))

df = DataFrame(joblist)

education = df.education.value_counts()

edu_list = list(education.index)

edu_map = dict(education)

plt.figure('quyu')

# plt.add_subplot(121)
plt.title(u'学历对应数量', fontproperties=custom_font)

xticks = np.arange(len(edu_map))

quyuName = edu_map.keys()

number = [x for x in edu_map.values()]

bar_width = 0.5

bars = plt.bar(xticks, number, width=bar_width, edgecolor='none')

for x, y in zip(xticks, number):
    plt.text(x, y + 20, '%d' % y, ha='center', va='top')

plt.ylabel(u'数量（个）', fontproperties=custom_font)
plt.xticks(xticks + bar_width / 2, quyuName)

# plt.(quyuName, fontproperties=custom_font)

plt.xlim(([bar_width / 2 - 0.5, len(edu_map) - bar_width / 2]))

plt.ylim([0, 500])


plt.savefig("edu.png",dpi=100)

plt.show()
# plt.show()

# district

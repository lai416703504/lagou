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

district = df.district.value_counts()

quyu_list = list(district.index)

quyu_map = dict(district)

plt.figure('quyu')

# plt.add_subplot(121)
plt.title(u'区域对应职位数量', fontproperties=custom_font)

xticks = np.arange(len(quyu_map))

quyuName = quyu_map.keys()

number = [x for x in quyu_map.values()]

bar_width = 0.5

bars = plt.bar(xticks, number, width=bar_width, edgecolor='none')

for x, y in zip(xticks, number):
    plt.text(x, y + 20, '%d' % y, ha='center', va='top')

plt.ylabel(u'数量（个）', fontproperties=custom_font)
plt.xticks(xticks + bar_width / 2, quyuName)

# plt.(quyuName, fontproperties=custom_font)

plt.xlim(([bar_width / 2 - 0.5, len(quyu_map) - bar_width / 2]))

plt.ylim([0, 500])


plt.savefig("quyu.png",dpi=100)

plt.show()
# plt.show()

# district

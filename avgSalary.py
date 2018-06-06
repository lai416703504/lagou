# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import re

mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.sans-serif'] = ['SimHei']
custom_font = mpl.font_manager.FontProperties(fname='msyh.ttf')

file = open('items.json')
joblist = []
for eachline in file:
    joblist.append(json.loads(eachline))

df = DataFrame(joblist)

df1 = df[['salary', 'district']]
minList = []
maxList = []
avgList = []

for index in df1.index:
    temp = re.sub('[Kk]', '', df1.loc[index].salary)
    salaryList = re.split('-', temp)
    # print salaryList
    minList.append(salaryList[0])
    maxList.append(salaryList[1])
    avgList.append((int(salaryList[0]) + int(salaryList[1])) / 2.)

df1.insert(2, 'min', minList)
df1.insert(3, 'max', maxList)
df1.insert(4, 'avg', avgList)

avgSalarys =  df1.groupby(['district'])['avg'].mean()


avg_map = dict(avgSalarys)


avg_list = list(avgSalarys.index)


plt.figure('quyu')

# plt.add_subplot(121)
plt.title(u'薪资', fontproperties=custom_font)

xticks = np.arange(len(avg_map))

quyuName = avg_map.keys()

number = [x for x in avg_map.values()]

bar_width = 0.5

bars = plt.bar(xticks, number, width=bar_width, edgecolor='none')

for x, y in zip(xticks, number):
    plt.text(x, y + 0.5, '%.02f' % y, ha='center', va='top')

plt.ylabel(u'平均月薪（K）', fontproperties=custom_font)
plt.xlabel(u'行政区', fontproperties=custom_font)
plt.xticks(xticks + bar_width / 2, quyuName)

# plt.(quyuName, fontproperties=custom_font)

plt.xlim(([bar_width / 2 - 0.5, len(avg_map)]))

plt.ylim([0.0, 10.0])

plt.savefig("avg_salary.png", dpi=100)

plt.show()
# plt.show()

# district

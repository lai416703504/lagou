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

salarys = list(df.salary)

temp = []
for salarymix in salarys:
    temp = temp + re.split('-', salarymix)

salaryList = []
for salarymix in temp:
    salaryList.append(re.sub('[Kk]', '', salarymix))

salarySeries = Series(salaryList)
salary = salarySeries.value_counts()

salary_list = list(salary.index)

salary_map = dict(salary)

plt.figure('quyu')

# plt.add_subplot(121)
plt.title(u'薪资', fontproperties=custom_font)

xticks = np.arange(len(salary_map))

quyuName = salary_map.keys()

number = [x for x in salary_map.values()]

bar_width = 0.5

bars = plt.bar(xticks, number, width=bar_width, edgecolor='none')

for x, y in zip(xticks, number):
    plt.text(x, y + 20, '%d' % y, ha='center', va='top')

plt.ylabel(u'数量（个）', fontproperties=custom_font)
plt.xlabel(u'月薪（K）', fontproperties=custom_font)
plt.xticks(xticks + bar_width / 2, quyuName)

# plt.(quyuName, fontproperties=custom_font)

plt.xlim(([bar_width / 2 - 0.5, len(salary_map)]))

plt.ylim([0, 256])

plt.savefig("salary.png", dpi=100)

plt.show()
# plt.show()

# district

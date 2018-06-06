# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from pandas import DataFrame
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import re

mpl.rcParams['font.size'] = 8
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
custom_font = mpl.font_manager.FontProperties(fname='msyh.ttf')

file = open('items.json')
joblist = []
for eachline in file:
    try:
        temp = json.loads(eachline)
    except Exception as e:
        temp = {}

    temp1 = {}
    if temp.has_key('salary'):
        minSalary = re.sub('[Kk]', '', temp['salary'].split('-')[0])
        maxSalary = re.sub('[Kk]', '', temp['salary'].split('-')[-1])

        avgSalary = (int(maxSalary) + int(minSalary)) / 2.
        pattern = r'(1-3)|(3-5)'
        if re.match(pattern, temp['workYear'].encode('utf-8')):
            temp1['district'] = temp['district']
            temp1['avgSalary'] = avgSalary
            temp1['workYear'] = temp['workYear']
            joblist.append(temp1)

sns.set(style='whitegrid', color_codes=True, font=custom_font.get_name())

df = DataFrame(joblist)

df['avgSalary'] = df.avgSalary.astype(float)
df['district'] = df.district.astype(object)
df['workYear'] = df.workYear.astype(object)

sns.boxplot(x="district", y="avgSalary", hue='workYear', data=df)

plt.savefig("areaSalary.png", dpi=100)

plt.show()

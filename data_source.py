#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 * @Author       : Yan
 * @Date         : 2021/12/22
 * @Description  : linuxyan.github.io
 * @LastEditTime : 2021/12/22
 """
import pandas as pd
import numpy as np
import json

data = pd.read_excel(u'data_source/金额数据.xlsx')
data['总金额'] = data['金额'].cumsum()
data['总持仓'] = data['数量'].cumsum()
data['总市值'] = np.round(data['当前价格'] * data['总持仓'], 4)
data['盈亏比例'] = np.round((data['总市值'] / data['总金额'] - 1) * 100, 2)
print(data)

# 填充数据
df = pd.DataFrame({'dt_str': pd.date_range(data['日期'].max(), '2032-12-30', freq='30D')})
df['日期'] = df['dt_str'].dt.strftime('%Y.%m.%d')
data = pd.concat([data, df[['日期']]])
data = data.fillna(axis=0, method='ffill')

# 初次买入价格和当前价格
json_data, json_data_name = {}, 'index_data.json'
json_data['日期'] = data['日期'].values.tolist()
json_data['当前价格'] = data['当前价格'].values.tolist()
json_data['初始价格'] = data['初始价格'].values.tolist()
with open('data_json/' + json_data_name, 'w') as file_obj:
    json.dump(json_data, file_obj, indent=4)

# 定投金额 当前市值
json_data, json_data_name = {}, 'market_value_data.json'
json_data['日期'] = data['日期'].values.tolist()
json_data['总金额'] = data['总金额'].values.tolist()
json_data['总市值'] = data['总市值'].values.tolist()
with open('data_json/' + json_data_name, 'w') as file_obj:
    json.dump(json_data, file_obj, indent=4)

# 利润比例
json_data, json_data_name = {}, 'profit_data.json'
json_data['日期'] = data['日期'].values.tolist()
json_data['盈亏比例'] = data['盈亏比例'].values.tolist()
with open('data_json/' + json_data_name, 'w') as file_obj:
    json.dump(json_data, file_obj, indent=4)

# 投资记录
json_data_name = 'record_data.json'
json_data = data.values.tolist()
with open('data_json/' + json_data_name, 'w') as file_obj:
    json.dump(json_data, file_obj, indent=4)

# create README.md
with open("README.md", "w") as file_obj:
    data.to_markdown(file_obj)

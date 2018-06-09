#coding:utf-8
"""
author:C-YC
target:将爬取的演职信息导入mongodb
finish date：2018,06,08
"""
import sys
import os
import json
import collections
import time
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding("utf-8")


def data_storage(movie_year, movie_name):
    dict0 = collections.OrderedDict()
    with open("../data/"+movie_year+"/"+movie_name, "r")as f:
        lines = f.readlines()
    for line in lines:
        dict_key = line.replace("\n", "").split("：")[0]
        # print dict_key,
        dict_values = line.replace("\n", "").split("：")[1]
        dict_value = dict_values.replace("\"", "\'")
        # print dict_value
        dict0[dict_key] = dict_value
    print json.dumps(dict0, ensure_ascii=False, encoding='UTF-8', indent=1)
    try:
        time.sleep(0.5)
        my_set.insert(dict0)
    except:
        pass



def main():
    # 按路径取电影名
    year = u'2012'
    path = "../data/2012"
    files = os.listdir(path)
    for f in files:
        print f
        data_storage(year, f)
    time.sleep(2)
    year = u'2013'
    path = "../data/2013"
    files = os.listdir(path)
    for f in files:
        print f
        data_storage(year, f)


if __name__ == '__main__':
    # 连接mongodb
    conn = MongoClient('192.168.235.55', 27017)
    db = conn['admin']
    db.authenticate("admin", "123456")
    db = conn['team_behind_sc']
    my_set = db['Filmmaker_page']
    main()
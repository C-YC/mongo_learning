#coding:utf-8
import sys
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding("utf-8")


dict0 = {}
conn = MongoClient('192.168.235.55', 27017)  # 连接mongodb
db = conn['admin']
db.authenticate("admin", "123456")
db = conn['team_behind_sc']    # use team_behind_sc（数据库）
table = db['Filmmaker_page']   # 连接要导入的表
table.insert(dict0)            # 将字典导入


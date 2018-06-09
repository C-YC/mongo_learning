#coding:utf-8
"""
author:C-YC
target:根据电影名爬取时光网电影演职信息
finish date：2018,06,08
"""
import sys
import os
import time
import re
import json
import urllib
from selenium import webdriver
reload(sys)
sys.setdefaultencoding("utf-8")
driver = webdriver.PhantomJS(executable_path='./phantomjs')


def get_credits(url, movie_name, movie_id, movie_year):
    print '函数调用成功！'
    # 取得电影的演职页面url
    movie_url = url+'fullcredits.html'
    time.sleep(1)
    driver.get(movie_url)
    time.sleep(2)
    html = driver.page_source
    time.sleep(1)
    dict0 = {}
    # 先将简单信息存入文件， ：中文的冒号作为切片的标志符号，用于存字典存数据库
    with open("../data/"+movie_year+"/"+movie_name+".txt", "w")as fl:
        fl.write("_id："+movie_id+"\n"+"year："+movie_year+"\n"+"movie_name："+movie_name+"\n")
    # 采用正则匹配获取所要信息
    with open("../data/demo.html", "w+")as s:
        s.write(html)
    time.sleep(2)
    with open("../data/demo.html", "r")as m:
        fp = m.read().replace('\n', '')
    # 获取演员列表
    all_actors = re.findall('<dd>.*?</dd>', fp)
    print type(all_actors)
    print len(all_actors)
    time.sleep(1)
    for r in range(1, len(all_actors)):
        actor_namess = re.findall('<h3><a href=".*?" target="_blank">(.*?)</a></h3>', all_actors[r])
        # print type(actor_names)
        # print len(actor_names)
        actor_url = re.findall('<h3><a href="(.*?)" target="_blank">.*?</a></h3>', all_actors[r])
        print actor_url,
        for actor_names in actor_namess:
            actor_name = actor_names
            print actor_name
            dict0[actor_name] = actor_url[0]
    print json.dumps(dict0, ensure_ascii=False, encoding='UTF-8')
    q = open("../data/"+movie_year+"/"+movie_name+".txt", "a+")
    q.write('演员：'+json.dumps(dict0, ensure_ascii=False, encoding='UTF-8')+'\n')
    time.sleep(1)
    q.close()
    # 获取职员列表
    all_credits = re.findall('<div class="credits_list">(.*?)</div>', fp)
    print len(all_credits)
    time.sleep(1)
    for r in range(len(all_credits)):
        dict1 = {}
        credit_lists = re.findall('<h4>(.*?)</h4>', all_credits[r])
        for credit_list in credit_lists:
            credit_type = credit_list.split(" ")[0]
            print credit_type
        credit_name_0 = re.findall('<a target="_blank" href=".*?">(.*?)</a>', all_credits[r])
        credit_url_0 = re.findall('<a target="_blank" href="(.*?)">.*?</a>', all_credits[r])
        credit_name_1 = re.findall('<a href=".*?" target="_blank">(.*?)</a>', all_credits[r])
        credit_url_1 = re.findall('<a href="(.*?)" target="_blank">.*?</a>', all_credits[r])
        if len(credit_name_0) > 0:
            for r in range(len(credit_name_0)):
                credit_name = credit_name_0[r]
                credit_url = credit_url_0[r]
                time.sleep(0.2)
                dict1[credit_name] = credit_url
        else:
            for r in range(len(credit_name_1)):
                credit_name = credit_name_1[r]
                credit_url = credit_url_1[r]
                time.sleep(0.2)
                dict1[credit_name] = credit_url
        global credit_type
        w = open("../data/"+movie_year+"/" + movie_name + ".txt", "a+")
        time.sleep(1)
        w.write(credit_type + '：' + json.dumps(dict1, ensure_ascii=False, encoding='UTF-8') + '\n')
        w.close()
        dict.clear(dict1)


def info_judge(movie_year):
    # 定义一个列表，用于存放已爬的电影名
    # 当再次运行时可以直接从未爬取的电影开始爬取
    judge_names = []
    with open("../data/finish.txt", "a+")as fls:
        flines = fls.readlines()
    for fline in flines:
        judge_name = fline.replace("\n", "")
        judge_names.append(judge_name)
    # 打开电影名文件，开始爬取
    with open("../data/"+movie_year+".txt", 'r')as f:
        lines = f.readlines()
    for line in lines:
        pr_name = line.replace('\n', '').split('')[0]
        print pr_name
        # 判断该电影是否在已爬取列表里面
        # 是，则跳过；否，则继续
        if pr_name in judge_names:
            pass
        else:
            # 将str型改成unicode型，与接下来的电影名和年份做匹配
            movie_name = unicode(line.replace('\n', '').split('')[0])
            movie_id = unicode(line.replace('\n', '').split('')[1])
            time.sleep(1)
            print movie_name,
            print type(movie_name)
            # 将电影名的编码转化成与时光网搜索网址一致的编码
            pre_url = 'http://search.mtime.com/search/?q=' + urllib.quote(pr_name)
            print pre_url
            # 搜索电影
            driver.get(pre_url)
            time.sleep(1)
            # 拿取搜索页面所有电影的url，存成列表
            urls = driver.find_elements_by_xpath("//div[@class='main']/ul/li/h3/a")
            time.sleep(2)
            print len(urls)
            all_urls = [i.get_attribute("href") for i in urls]
            time.sleep(1)
            # 从列表中取url，匹配url的电影名和年份是否与所要爬取的一致
            for url in all_urls:
                driver.get(url)
                time.sleep(1)
                try:
                    name = driver.find_element_by_xpath("//div[@class='clearfix']/h1").text
                    year = driver.find_element_by_xpath("//div[@class='clearfix']/p[@class='db_year']/a").text
                    time.sleep(0.5)
                    print type(name),
                    print name
                    print type(year),
                    print year
                    # 如果一致则调用get_credits函数否则跳过
                    if name == movie_name and year == movie_year:
                        time.sleep(1)
                        get_credits(url, movie_name, movie_id, movie_year)
                        time.sleep(1)
                        break
                    else:
                        pass
                except:
                    pass
            time.sleep(1)
            try:
                # 如果存在该电影的文件，则说明已经成功爬取
                p = open("../data/" + movie_year + "/" + movie_name + ".txt", "r")
                p.close()
                time.sleep(0.5)
                # 将爬取成功的电影名加入文件，进而加入列表
                with open("../data/finish.txt", "a+")as n:
                    n.write(movie_name + '\n')
            except:
                # 如果不存在该电影文件，则说明电影爬取失败，将电影信息写入错误文件
                with open("../data/wrong.txt", "a+")as m:
                    m.write(movie_id + " " + movie_name + " " + movie_year + "\n")
                time.sleep(0.5)


def main():
    # 主函数
    year0 = u'2012'
    info_judge(year0)
    time.sleep(2)
    year1 = u'2013'
    info_judge(year1)


if __name__ == '__main__':
    # 创建文件夹和错误文档
    if not os.path.exists("../data/2012"):
        os.mkdir("../data/2012")
    if not os.path.exists("../data/2013"):
        os.mkdir("../data/2013")
    with open("../data/wrong.txt", "w+")as f:
        f.write("")
    main()
# -*- coding:utf-8 -*-
__author__ ="豆豆嗯嗯"

import urllib.request
from bs4 import BeautifulSoup
import threading
import time
import random


# 获取期号列表
def getIssueNumberList():
    url = "http://apply.sztb.gov.cn/apply/app/status/norm/person"
    # 访问页面
    response = urllib.request.urlopen(url)
    response = response.read().decode("utf-8")
    soup = BeautifulSoup(response, "html.parser")
    options = soup.select("select > option")
    monthlist = []
    for option in options:
        monthlist.append(option.get_text())
    del monthlist[0]
    return monthlist


# 获取当前期号总页数
def getpageCount(IssueNumber):
    url2 = "http://apply.sztb.gov.cn/apply/app/status/norm/person?pageNo=1" + "&issueNumber=" + IssueNumber+ "&applyCode=";
    # print(url2)
    # 访问页面
    response2 = urllib.request.urlopen(url2)
    response2 = response2.read().decode("utf-8")
    # print(response2)
    soup = BeautifulSoup(response2, "html.parser")
    head = soup.head
    script = head.select("link[rel='shortcut icon'] + script")
    # print(script)
    pageCount = str(script).split("pageCount = window.parseInt('")[1].split("'")[0]
    return pageCount



# 获取当前页页面申请编码和姓名信息
def getUserInfo(pageNo,issueNumber):
    page_url = "http://apply.sztb.gov.cn/apply/app/status/norm/person?pageNo="+pageNo+"&issueNumber="+issueNumber+"&applyCode=";
    # 访问页面
    response3 = urllib.request.urlopen(page_url)
    response3 = response3.read().decode("utf-8")
    # print(response3)
    soup = BeautifulSoup(response3, "html.parser")
    '''
    table = soup.select("table[class='ge2_content']")
    # print(table)
    content_header = soup.select("tr[class='content_header']")
    # print(content_header)
    '''

    content_datalist = soup.select("tr[class='content_data']")
    # print(content_datalist)
    for tr in content_datalist:
        tdlist = tr.find_all("td")
        num = tdlist[0].get_text()
        name = tdlist[1].get_text()
        print(num,"-----------------",name)



class MyThread(threading.Thread):
    def __init__(self,pageCount,issueNumber):
        threading.Thread.__init__(self)
        self.pageCount = pageCount
        self.issueNumber = issueNumber

    def run(self):
        for num in range(1,int(pageCount)):
            # print(self.issueNumber,"-----------------",num)
            getUserInfo(str(num),self.issueNumber)
            time.sleep(random.randint(0, 3))  # 暂停0~3秒的整数秒，时间区间：[0,3]






    
print("urlib爬取深圳市小汽车增量指标数据示例")


IssueNumberlist = getIssueNumberList()

threads = []
for IssueNumer in IssueNumberlist:
    # print(IssueNumer)
    pageCount = getpageCount(IssueNumer)
    threads.append(MyThread(pageCount,IssueNumer))
    # mythread.run()

for thread in threads:
    thread.start()











# -*- coding:utf-8 -*-
from builtins import range
from pip._vendor.requests.packages.urllib3 import response
__author__ ="豆豆嗯嗯"

import urllib.request
import re
import xlwt
import  threading
import time
import random


# 获取月份列表
def getIssueNumberList(applyInfo):
    issueNumber = applyInfo.split("<option value=\"000000\">最近六个月</option>")[1].split("</select>")[0]
    issueNumberList = re.findall(r">[0-9]+", issueNumber)
    return issueNumberList


# 获取当月总页数
def getpageCount(issueNumber):
    page_url = "http://apply.sztb.gov.cn/apply/app/status/norm/person?pageNo=1"+"&issueNumber="+issueNumber+"&applyCode=";
    response = urllib.request.urlopen(page_url)
    applyInfo = response.read().decode("utf-8")
    pageCount = applyInfo.split("pageCount = window.parseInt('")[1].split("'")[0]
    return pageCount


# 获取某页有效信息
def getPageInfo(pageNo,issueNumber):
    page_url = ""    
    if(pageNo==""  or issueNumber=="" ):
        page_url = "http://apply.sztb.gov.cn/apply/app/status/norm/person";
    else:
        page_url = "http://apply.sztb.gov.cn/apply/app/status/norm/person?pageNo="+str(pageNo)+"&issueNumber="+issueNumber+"&applyCode=";
    applyInfo = ""
    try:
        response = urllib.request.urlopen(page_url)
        applyInfo = response.read().decode("utf-8")
    except :
        print("数据获取异常")
    return applyInfo


# 截取当页效信息----申请用户信息
def getApplyInfo(applyInfo):
    if applyInfo !="":
        applyInfo = applyInfo.replace("\n", "")
        applyInfo = applyInfo.replace("\r", "")
        applyInfo = applyInfo.replace("\t", "")
        applyInfo = applyInfo.split("<tbody><tr class=\"content_header\"><th>申请编码</th><th>姓名</th></tr>")[1].split(
            "</tbody></table><div style=\"height: 10px;\">")[0]
        applyInfo = "".join(applyInfo)
        applyInfo = applyInfo.replace("<tr  class=\"content_data\"><td >", "")
        applyInfo = applyInfo.replace("</td><td >", ":")
        applyInfo = applyInfo.replace("</td></tr>", ",")
        applyInfo = applyInfo.split(",")
        applyInfo.remove('')
#     applyInfo.pop()
    return applyInfo


class Mythread(threading.Thread):
    def __init__(self,pageCount,issueNumber,sheet):
        threading.Thread.__init__(self)
        self.pageCount = pageCount
        self.issueNumber = issueNumber
        self.sheet = sheet
        
    def run(self):
#         获取每一页的数据
        rowNum = 1
        for pageNo in range(1,int(self.pageCount)+1):
            applyInfo = getPageInfo(pageNo, self.issueNumber)
            queryresult = getApplyInfo(applyInfo)
            for info in queryresult:
#                 print(rowNum)
                appNum = info.split(":")[0]
                appName = info.split(":")[1]
#                 print("编号:%s   姓名:%s    月份:%s" % (appNum, appName,self.issueNumber))
                self.sheet.write(rowNum, 0, appNum)
                self.sheet.write(rowNum, 1, appName)
                rowNum = rowNum+1
            
            time.sleep(random.randint(0,3))  # 暂停0~3秒的整数秒，时间区间：[0,3]
        xls.save('sample2.xls')
            
            



# 获取月份信息
applyInfo = getPageInfo("", "")
issueNumberList = getIssueNumberList(applyInfo)
xls = xlwt.Workbook()
threads = []
for issueNumbe in issueNumberList:
    issueNo = issueNumbe.replace(">","")
    sheet = xls.add_sheet(issueNo) 
    sheet.write(0, 0, '编号')
    sheet.write(0, 1, '姓名')
    pageCount = getpageCount(issueNo)
    threads.append(Mythread(pageCount,issueNo,sheet))
    
for thread in threads:
    thread.start()
    




   
     

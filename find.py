# -*- coding:utf-8 -*-
__author__ ="豆豆嗯嗯"

import urllib.request
import re
import xlwt

def getPageCount(applyInfo):
    
    pageCount = applyInfo.split("pageCount = window.parseInt('")[1].split("'")[0]
    return pageCount

def getIssueNumberList(applyInfo):
    issueNumber = applyInfo.split("<option value=\"000000\">最近六个月</option>")[1].split("</select>")[0]
    issueNumberList = re.findall(r">[0-9]+", issueNumber)
    print(issueNumberList)
    return issueNumberList

def getApplyInfo(applyInfo):
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
    applyInfo.pop()
    return applyInfo


def WriteExcel(sheet,pageurl,rowNum):
    
    response = urllib.request.urlopen(pageurl)
    applyInfo = response.read().decode("utf-8")  
    applyInfo = getApplyInfo(applyInfo)
    for info in applyInfo:
        appNum = info.split(":")[0]
        appName = info.split(":")[1]
        #print("编号:%s   姓名:%s" % (appNum, appName))
        sheet.write(rowNum, 0, appNum)
        sheet.write(rowNum, 1, appName)
        rowNum = rowNum+1
    xls.save('sample.xls')
    return rowNum
    

if __name__=="__main__":

    print("urlib爬取深圳市小汽车增量指标数据示例")
   
    url = "http://apply.sztb.gov.cn/apply/app/status/norm/person"

    # 访问页面
    response = urllib.request.urlopen(url)

    # 打印下状态码
    #print(response.status)
    # 打印下状态码对应的可读性文字说明，例如在http协议里，200 对应 OK
    #print(response.reason)
    # 打印下请求返回的header
    #print(response.headers)
    
    # 打印下请求返回的数据
    applyInfo = response.read().decode("utf-8")
    issueNumberList = getIssueNumberList(applyInfo)
    
    xls = xlwt.Workbook()
    
    
    for number in issueNumberList:
        rowNum = 1
        print(number.replace(">",""))
        sheet = xls.add_sheet(number.replace(">","")) 
        sheet.write(0, 0, '编号')
        sheet.write(0, 1, '姓名')
        
#         获取每个月份的分页数
        page_url = "http://apply.sztb.gov.cn/apply/app/status/norm/person?pageNo=1"+"&issueNumber="+number.replace(">","")+"&applyCode=";
#         print(page_url)
        response = urllib.request.urlopen(page_url)
        applyInfo = response.read().decode("utf-8")
        pageCount = getPageCount(applyInfo)
        
#         获取每个月的申请人信息  
        for i in range(1,int(pageCount)+1): 
#             print(i)
            page_url = "http://apply.sztb.gov.cn/apply/app/status/norm/person?pageNo="+str(i)+"&issueNumber="+number.replace(">","")+"&applyCode=";   
            rowNum = WriteExcel(sheet,page_url,rowNum)
            
        
        
           


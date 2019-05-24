 # coding:utf-8
#! /usr/bin/python

import  unittest,requests,HTMLTestRunner,time,os
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from feng_test_method.feng_test_MethodCode import *
from appium import webdriver
import smtplib, os, re  # 发送库
from email.mime.text import MIMEText  # 构建文本邮件库
from email.mime.multipart import MIMEMultipart
PATH = lambda  p:os.path.abspath(
       os.path.join(os.path.dirname(__file__),p)
)
print(PATH)
def allCase():
    #待执行用例的目录
    case_dir=os.path.dirname(os.path.dirname(__file__))+'/feng_test_case'
    #构造测试集合
    #suite=unittest.TestSuite()
    #获取到一个list集合
    allTest = unittest.defaultTestLoader.discover(case_dir,pattern="test*.py",top_level_dir=None)
    #pattern————匹配脚本名称规则，test*.py是匹配所有test开头的所有脚本
    #top_level_dir 这个是顶层目录的名称 ，一般为空就可以了
    # for test_suite in allTest:
    #     for test_case in test_suite:
    #         suite.addTests(test_case)
    return  allTest
#pathCode = 'C:\\Users\\feng\Desktop\python01\\fengfan_unittest\\feng_test_result\\'
#cuitime=time.strftime('%Y%m%d%H%M%S',time.localtime())
#report_path = pathCode+cuitime+'.html'
#report_set = open(report_path, 'wb')
#runner = HTMLTestRunner.HTMLTestRunner(stream=report_set,title=u'自动化测试报告',description=u'用例执行情况：')
if __name__=="__main__":
    pathCode =os.path.dirname(os.path.dirname(__file__))+'/feng_test_result/'
    curtime=time.strftime('%Y%m%d%H%M%S',time.localtime())
    report_path = pathCode+curtime+'.html'
    report_set = open(report_path, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=report_set,title=u'自动化测试报告',description=u'用例执行情况：')
    runner.run(allCase())
    report_set.close()
    def smtp_mail(choocemail, sendmail, receivemail):  # choocemail选择163还是qq,sendmail发件人，receivemail收件人
        path =os.path.dirname(os.path.dirname(__file__))+'/feng_test_result/'
        lists = os.listdir(path)
        filepath = path + lists[-1]
        with open(filepath, "rb") as fp:
            mail_body = fp.read()
        if choocemail == '163':  # 选择是163之后，所有的参数都是163的
            smtpserver = "smtp.163.com"  # 163邮箱服务器地址
            port = 0  # 端口号163邮箱为0，腾讯邮箱为 465 或者587
            mailtext = "您好:</br><p>　　　　请下载附件之后，由谷歌打开查看测试报告详情！</p>"  # 邮件内容

            mailCode = MIMEMultipart("alternative") #可以构造一个MIMEMultipart对象代表邮件本身，然后往里面加上一个MIMEText作为邮件正文，再继续往里面加上表示附件的MIMEBase对象
            # 使用MUMEText构造文本邮件字典
            mailCode['from'] = sendmail  # 添加发件人键值对
            mailCode['to'] = receivemail  # 添加收件人键值对
            mailCode['subject'] = '冯凡—自动化测试报告'  # 添加文本主题键值对

            body = MIMEText(mailtext, "html", "utf-8")
            mailCode.attach(body)
            # 添加附件
            att = MIMEText(mail_body, "base64", "utf-8")
            att["Content-Type"] = "application/octet-stream"
            att["Content-Disposition"] = 'attachment; filename="test_report.html"'
            mailCode.attach(att)

            smtp = smtplib.SMTP()  # 使用该方法发送邮件
            smtp.connect(smtpserver)  # 链接服务器
            smtp.login(sendmail, 'ff123456789')  # 登录
            smtp.sendmail(sendmail, receivemail, mailCode.as_string())  # 发送
            smtp.quit()  # 关闭
        if choocemail == 'qq':
            smtpserver = "smtp.qq.com"  # qq邮箱服务器地址
            port = 465
            mailtext = "您好:</br><p>　　　　请下载附件之后，由谷歌打开查看测试报告详情！</p>"  # 邮件内容
            mailCode = MIMEMultipart()

            mailCode['from'] = sendmail
            mailCode['to'] = receivemail
            mailCode['subject'] = '冯凡—自动化测试报告'

            text = MIMEText(mailtext, 'html', 'utf-8')  # 构造邮件
            mailCode.attach(text)

            # 添加附件
            att = MIMEText(mail_body, "base64", "utf-8")
            att["Content-Type"] = "application/octet-stream"
            att["Content-Disposition"] = 'attachment; filename="test_report.html"'
            mailCode.attach(att)

            smtp = smtplib.SMTP_SSL(smtpserver, port)
            smtp.login(sendmail, "fhezvfffbbvvbfgb")  # 登录
            smtp.sendmail(sendmail, receivemail, mailCode.as_string())  # 发送
            smtp.quit()  # 关闭


    smtp_mail('qq', '930690755@qq.com', '328353369@qq.com')
    smtp_mail('qq', '930690755@qq.com', '496851723@qq.com')
    # smtp_mail('163', '17688986015@163.com', '930690755@qq.com')








import unittest,unittest,requests,HTMLTestRunner,random,json,pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from feng_test_method.H5_Method import H5Method
from feng_test_log.feng_test_logmethod import Log
from feng_test_method.feng_test_MethodCode import MyMethod
from feng_test_conf.feng_test_env.feng_test_config import MustCode
import time

time = time.strftime('%d%H%M%S', time.localtime())
class  Test_login(unittest.TestCase):
    def setUp(self):
        self.logger = Log()
        self.logger.info('_______start_______')
    def tearDown(self):
        self.logger.info('________over_______\n')
    def test01(self):
        '''未注册手机号码第一次注册'''

        msg_=MyMethod().duQu_Excel('H5商城','注册',1,8)
        response=H5Method().Post_register('H5商城','注册',1,4,3,2)

        self.assertEqual(msg_,response.json()['msg'],msg='短信验证码未发送成功')

    def test02(self):
        '''已注册手机号码'''
        response = H5Method().Post_register('H5商城', '注册', 2, 4, 3, 2)
        msg_ = MyMethod().duQu_Excel('H5商城', '注册', 2, 8)
        self.assertEqual(response.json()['msg'], msg_, msg='短信验证码未发送成功')

    def test03(self):
        '''验证一分种内只能申请一次'''
        a=H5Method().Excel_Dict('H5商城', '注册', 3, 4, 3, 2)
        self.logger.info('注册登录/注册-Excel表格获取内容为：\n%s'%a)
        phoneNum=MyMethod().createPhone()
        self.logger.info('随机生成手机号码为：%s'%phoneNum)
        data={'phoneNum':phoneNum,'shopId':str(a['data'])}
        data=json.dumps(data)
        self.logger.info('待传入json格式内容data是：%s'%data)

        msg_ = MyMethod().duQu_Excel('H5商城', '注册', 3, 8)
        H5Method().Post_H5(a['url'],a['headers'],data)
        response1 = H5Method().Post_H5(a['url'],a['headers'],data)
        self.assertEqual(msg_,response1.json()['msg'],msg='连续发送验证码存在异常')



    def test04(self):
        '''注册验证验证码'''
        response=H5Method().set_password()
        self.assertEqual('验证成功!',response.json()['msg'],msg='注册--验证码无法验证')

    def test05(self):
        '''设置密码ff123456'''
        response=H5Method().set_password()
        key=response.json()['data']['key']
        a=H5Method().Excel_Dict('H5商城', '注册', 5, 4, 3, 2)
        data=a['data']
        data['key']=key
        data=json.dumps(data)
        print(type(data),data)
        response=H5Method().Post_H5(a['url'],a['headers'],data)
        self.assertEqual(MyMethod().duQu_Excel('H5商城','注册',5,8),response.json()['msg'],msg='注册不成功')

    def test06(self):
        '''输入密码为纯数字'''
        response=H5Method().set_password()
        key=response.json()['data']['key']
        a=H5Method().Excel_Dict('H5商城', '注册', 6, 4, 3, 2)
        data=a['data']
        data['key']=key
        data=json.dumps(data)
        print(type(data),data)
        response=H5Method().Post_H5(a['url'],a['headers'],data)
        self.assertEqual(MyMethod().duQu_Excel('H5商城','注册',6,8),response.json()['msg'],msg='注册不成功')
    def test07(self):
        '''输入密码为纯英文'''
        response = H5Method().set_password()
        key = response.json()['data']['key']
        a = H5Method().Excel_Dict('H5商城', '注册', 7, 4, 3, 2)
        data = a['data']
        data['key'] = key
        data = json.dumps(data)
        print(type(data), data)
        response = H5Method().Post_H5(a['url'], a['headers'], data)
        self.assertEqual(MyMethod().duQu_Excel('H5商城', '注册', 7, 8), response.json()['msg'], msg='注册不成功')

    def test08(self):
        '''输入密码低于六位'''
        response = H5Method().set_password()
        key = response.json()['data']['key']
        a = H5Method().Excel_Dict('H5商城', '注册', 8, 4, 3, 2)
        data = a['data']
        data['key'] = key
        data = json.dumps(data)
        print(type(data), data)
        response = H5Method().Post_H5(a['url'], a['headers'], data)
        self.assertEqual(MyMethod().duQu_Excel('H5商城', '注册', 8, 8), response.json()['msg'], msg='注册不成功')
    def test09(self):
        '''设置密码大于二十位'''
        response = H5Method().set_password()
        key = response.json()['data']['key']
        a = H5Method().Excel_Dict('H5商城', '注册', 9, 4, 3, 2)
        data = a['data']
        data['key'] = key
        data = json.dumps(data)
        print(type(data), data)
        response = H5Method().Post_H5(a['url'], a['headers'], data)
        self.assertEqual(MyMethod().duQu_Excel('H5商城', '注册', 9, 8), response.json()['msg'], msg='注册不成功')




























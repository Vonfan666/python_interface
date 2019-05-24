import unittest,time,unittest,requests,HTMLTestRunner,random,json,pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from feng_test_method.H5_Method import H5Method
from feng_test_log.feng_test_logmethod import Log
from feng_test_method.feng_test_MethodCode import MyMethod

time = time.strftime('%d%H%M%S', time.localtime())




class  Test_login(unittest.TestCase):
    def setUp(self):
        self.logger = Log()
        self.logger.info('_______start_______')
    def tearDown(self):
        self.logger.info('________over_______\n')

    def test01(self):
        '''账号密码正确登录'''
        url=MyMethod().duQu_Excel('H5商城','登录',1,4)
        headers=MyMethod().duQu_Excel('H5商城','登录',1,3)
        json=MyMethod().duQu_Excel('H5商城','登录',1,2)
        response=H5Method.login_H5(url,eval(headers),json)  #eval  执行字符串表达式，并返回值！
        self.logger.info('登录返回：%s'%response.json())
        self.assertEqual(MyMethod().duQu_Excel('H5商城','登录',1,8),response.json()['msg'],
                         msg='正确账号密码、shop_id，登录失败')

    def  test02(self):
        '''账号密码正确,shopid不正确'''
        url = MyMethod().duQu_Excel('H5商城', '登录', 2, 4)
        headers = MyMethod().duQu_Excel('H5商城', '登录', 2, 3)
        json = MyMethod().duQu_Excel('H5商城', '登录', 2, 2)
        response = H5Method.login_H5(url, eval(headers), json)  # eval  执行字符串表达式，并返回值！
        self.logger.info('登录返回：%s' % response.json())
        self.assertEqual(MyMethod().duQu_Excel('H5商城', '登录', 2, 8), response.json()['msg'],
                         msg='账号跨店铺登录--异常')
    def  test03(self):
        '''账号正确、密码错误，shopid正确'''
        url = MyMethod().duQu_Excel('H5商城', '登录', 3, 4)
        headers = MyMethod().duQu_Excel('H5商城', '登录', 3, 3)
        json = MyMethod().duQu_Excel('H5商城', '登录', 3, 2)
        response = H5Method.login_H5(url, eval(headers), json)  # eval  执行字符串表达式，并返回值！
        self.logger.info('登录返回：%s' % response.json())
        self.assertEqual(MyMethod().duQu_Excel('H5商城', '登录', 3, 8), response.json()['msg'],
                         msg='账号正确、密码错误，shopid正确--登录异常')

    def test04(self):
        '''密码为空'''
        url = MyMethod().duQu_Excel('H5商城', '登录', 4, 4)
        headers = MyMethod().duQu_Excel('H5商城', '登录', 4, 3)
        json = MyMethod().duQu_Excel('H5商城', '登录', 4, 2)
        response = H5Method.login_H5(url, eval(headers), json)  # eval  执行字符串表达式，并返回值！
        self.logger.info('登录返回：%s' % response.json())
        self.assertIn(MyMethod().duQu_Excel('H5商城', '登录', 4, 8), response.json()['msg'],
                         msg='*********Test_login—test04-密码为空--登录异常********')

    def test05(self):
        '''账号密码为空'''
        url = MyMethod().duQu_Excel('H5商城', '登录', 5, 4)
        headers = MyMethod().duQu_Excel('H5商城', '登录', 5, 3)
        json = MyMethod().duQu_Excel('H5商城', '登录', 5, 2)
        response = H5Method.login_H5(url, eval(headers), json)  # eval  执行字符串表达式，并返回值！
        self.logger.info('登录返回：%s' % response.json())
        self.assertIn(MyMethod().duQu_Excel('H5商城', '登录', 5, 8), response.json()['msg'],
                      msg='*********Test_login—test05-账号密码为空--登录异常********')

    def test06(self):
        '''账号错误，密码正确'''
        url = MyMethod().duQu_Excel('H5商城', '登录', 6, 4)
        headers = MyMethod().duQu_Excel('H5商城', '登录', 6, 3)
        json = MyMethod().duQu_Excel('H5商城', '登录', 6, 2)
        response = H5Method.login_H5(url, eval(headers), json)  # eval  执行字符串表达式，并返回值！
        self.logger.info('登录返回：%s' % response.json())
        self.assertEqual(MyMethod().duQu_Excel('H5商城', '登录', 6, 8), response.json()['msg'],
                      msg='*********Test_login—test05-账号错误，密码正确--登录异常********')



import unittest,requests,HTMLTestRunner,random,json,pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from feng_test_method.H5_Method import H5Method
from feng_test_log.feng_test_logmethod import Log
from feng_test_method.feng_test_MethodCode import MyMethod
from feng_test_conf.feng_test_env.feng_test_config import MustCode
import time
from feng_test_log.feng_test_logmethod import *
time = time.strftime('%d%H%M%S', time.localtime())



class  Test_banner(unittest.TestCase):
    def setUp(self):
        Log()
        self.logger = logging.getLogger()
    def tearDown(self):
        pass
    def test_01(self):
        '''发送验证码'''
        response=H5Method().Post_register('H5商城','忘记密码',1,4,3,2)
        print(response.json()['msg'])
        self.assertEqual(MyMethod().duQu_Excel('H5商城','忘记密码',1,8),response.json()['msg'],msg='忘记密码，无法发送验证码')

    def test_02(self):
        '''发送验证码,并校验'''
        phone='13152637543'
        # print(phone)
        # H5Method().H5_Post_register(phone,'ff123456') #注册成功
        # self.logger.info('------------注册成功-----------')
        # print(phone)
        H5Method().reset_post_password(phone) #发送验证码
        code=MyMethod().redisCode_key('mall:shoppingmall:smsVeriCode:FIND_BACK_LOGIN_PWD:',phone)
        # print(code,type(code))
        # print(eval(code),type(eval(code)))
        # response=H5Method().reset_password(phone,eval(code))
        # key=response.json()['data']['key'] #获取key
        dict=H5Method().Excel_Dict('H5商城','忘记密码',2,6,3,2)  #核验验证码
        dict['data']['phoneNum']=phone
        # dict['data']['key']=key
        dict['data']['code']=eval(code)
        dict['headers']['Referer']='http://192.168.12.21:81/forgetpsw/2'
        data=json.dumps(dict['data'])
        response=H5Method().Post_H5(dict['url'],dict['headers'],data)  #输入验证码
        print(response.json())
        self.assertEqual(response.json()['msg'],MyMethod().duQu_Excel('H5商城','忘记密码',2,8),msg='点击忘记密码，无法获取或验核验验证码')

    def test_03(self):
        '''验证码核验错误'''
        phone = '13204455502'
        # print(phone)
        # H5Method().H5_Post_register(phone,'ff123456') #注册成功
        # self.logger.info('------------注册成功-----------')
        # print(phone)
        H5Method().reset_post_password(phone)  # 发送验证码
        # code = MyMethod().redisCode_key('mall:shoppingmall:smsVeriCode:FIND_BACK_LOGIN_PWD:', phone)
        # print(code,type(code))
        # print(eval(code),type(eval(code)))
        # response=H5Method().reset_password(phone,eval(code))
        # key=response.json()['data']['key'] #获取key
        dict = H5Method().Excel_Dict('H5商城', '忘记密码', 3, 6, 3, 2)  # 核验验证码
        dict['data']['phoneNum'] = phone
        # dict['data']['key']=key
        dict['data']['code'] = '123456'
        dict['headers']['Referer'] = 'http://192.168.12.21:81/forgetpsw/2'
        data = json.dumps(dict['data'])
        response = H5Method().Post_H5(dict['url'], dict['headers'], data)  # 输入验证码
        self.assertEqual(response.json()['msg'], MyMethod().duQu_Excel('H5商城', '忘记密码', 3, 8), msg='错误验证码，验证通过')


    def test_04(self):
        '''新旧密码相同'''
        response=H5Method().resetPassWordMthod('18803119452',4,'ff123456')
        #
        # phone = '17700000000'
        # H5Method().reset_post_password(phone)  # 发送验证码
        # code = MyMethod().redisCode_key('mall:shoppingmall:smsVeriCode:FIND_BACK_LOGIN_PWD:', phone)
        # dict = H5Method().Excel_Dict('H5商城', '忘记密码', 4, 6, 3, 2)  # 核验验证码
        # dict['data']['phoneNum'] = phone
        # dict['data']['code'] = eval(code)
        # dict['headers']['Referer'] = 'http://192.168.12.21:81/forgetpsw/2'
        # data = json.dumps(dict['data'])
        # response = H5Method().Post_H5(dict['url'], dict['headers'], data)  # 输入验证码
        # key=response.json()['data']['key'] #获取key
        # dict=H5Method().Excel_Dict('H5商城', '忘记密码', 4, 4, 3, 2)
        # # dict['headers']['Referer']='http://192.168.12.21:81/forgetpsw/3'
        # dict['data']['key']=key
        # data=json.dumps(dict['data'])
        # response=H5Method().Post_H5(dict['url'],dict['headers'],data)
        self.assertEqual(response.json()['msg'],MyMethod().duQu_Excel('H5商城', '忘记密码',4,8),msg='新密码可以与旧密码相同')



    def test_05(self):
        '''密码纯英文'''
        phone = '15843675850'
        response=H5Method().resetPassWordMthod(phone, 5, 'fffffff')
        self.logger.info('修改密码为：fffffff')
        self.assertEqual(MyMethod().duQu_Excel('H5商城', '忘记密码', 5, 8),response.json()['msg'], msg='修改密码失败')

    def test_06(self):
        '''密码存数字'''
        phone = '18670030712'
        response=H5Method().resetPassWordMthod(phone, 6, '123456')  #修改密码

        self.assertEqual(response.json()['msg'], MyMethod().duQu_Excel('H5商城', '忘记密码', 6, 8), msg='修改密码失败')
    def test_07(self):
        '''验证码小于六位'''
        phone = '15220331480'
        response = H5Method().resetPassWordMthod(phone, 7, '12345')  # 修改密码
        self.assertEqual(response.json()['msg'], MyMethod().duQu_Excel('H5商城', '忘记密码', 7, 8), msg='修改密码失败')
    def test_08(self):
        '''验证码大于20位'''
        phone = '15090451148'
        response = H5Method().resetPassWordMthod(phone, 8, '123456789912345678991')  # 修改密码
        self.assertEqual(response.json()['msg'], MyMethod().duQu_Excel('H5商城', '忘记密码', 8, 8), msg='修改密码失败')
    def test_09(self):
        '''输入正确密码'''
        phone = '15279684727'
        password = 'ff' + ''.join(random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9', ], 5))
        response = H5Method().resetPassWordMthod(phone, 9, password) #修改密码
        self.logger.info('***********修改密码成功**************')
        self.assertEqual(response.json()['msg'],MyMethod().duQu_Excel('H5商城', '忘记密码',4,8),msg='修改密码失败')















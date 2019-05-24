import unittest,time,unittest,requests,HTMLTestRunner,random,json
from feng_test_method.feng_test_MethodCode import *
from feng_test_conf.feng_test_env.feng_test_config import *
from start_interface import *
from feng_test_log.feng_test_logmethod import *
from feng_test_method.H5_Method import H5Method
time = time.strftime('%d%H%M%S', time.localtime())

path=os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt'
class  Test_banner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dict=H5Method().Excel_Dict('H5商城','登录',1,4,3,2)
        H5Method().H5_login(dict['url'],dict['headers'],json.dumps(dict['data']))


    def setUp(self):
        Log()
        self.logger = logging.getLogger()
    def tearDown(self):
        pass

    def test_01(self):
        '''关键字自动联想搜索,输入测试'''
        token=MyMethod().readToken(path)
        dict=H5Method().Excel_Dict('H5商城','搜索',1,4,3,2)
        dict['headers']['token']=token[-1]
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        # MyMethod().writeFile(response.text)
        # response=MyMethod().readToken(os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/response.txt')
        # response=json.loads(response[0])
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城','搜索',1,8))['msg'],response.json()['msg'],msg='获取首页模板失败')

    def test_02(self):
        '''输入超长字符串'''
        # token=MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '搜索', 2, 4, 3, 2)
        # dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '搜索', 2, 8))['msg'], response.json()['msg'],
                         msg='输入超长字符串没有提示报错')
    def test_03(self):
        '''输入内容为空'''
        dict=H5Method().Excel_Dict('H5商城','搜索',3,4,3,2)
        response=H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '搜索', 3, 8))['msg'], response.json()['msg'],
                         msg='输入超长字符串没有提示报错')
    def test_04(self):
        '''提交关键字到服务器，保存到历史搜索'''
        # token=MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '搜索', 2, 4, 3, 2)
        # dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))

        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '搜索', 2, 8))['msg'], response.json()['msg'], msg='关键字提交失败')

    def test_05(self):
        ''''''
        pass

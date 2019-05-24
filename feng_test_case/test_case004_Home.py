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
        '''获取店铺模板信息'''
        token=MyMethod().readToken(path)
        dict=H5Method().Excel_Dict('H5商城','首页',1,4,3,2)
        dict['headers']['token']=token[-1]
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城','首页',1,8))['msg'],response.json()['msg'],msg='获取首页模板失败')
        self.assertIn(eval(MyMethod().duQu_Excel('H5商城','首页',1,8))['data']['templateType'],[1,2,3],msg='获取首页模板失败')

    def test_02(self):
        '''店铺id为空'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '首页', 2, 4, 3, 2)
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 2, 8))['msg'], response.json()['msg'], msg='获取首页模板失败')
    def test_03(self):
        '''店铺id不存在'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '首页', 3, 4, 3, 2)
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 3, 8))['msg'], response.json()['msg'], msg='获取首页模板失败')

    def test_04(self):
        '''首页列表获取'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '首页', 4, 4, 3, 2)
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 4, 8))['msg'], response.json()['msg'], msg='获取首页模板失败')
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 4, 8))['systemCode'], response.json()['systemCode'], msg='获取首页模板失败')


    def test_05(self):
        '''shopId为空加载首页列表'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '首页', 5, 4, 3, 2)
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 5, 8))['msg'], response.json()['msg'], msg='获取首页模板失败')
        # self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 4, 8))['systemCode'], response.json()['systemCode'],
        #                  msg='获取首页模板失败')

    def test_06(self):
        '''点击查看详情'''
        token=MyMethod().readToken(path)  #取出token保持登录
        dict=H5Method().Excel_Dict('H5商城','首页',6,4,3,2)  #取出Excel表格内容

        goodsId=int(dict['data']['goodsId'])  #从Excel表格中获取分销商商品id
        print(goodsId)
        print(dict['headers']['Referer'] )
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodsId)
        dict['headers']['token'] = token[-1] #
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        price=H5Method().selectSQL(goodsId)[0][9]  #数据库中取出商品价格
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 6, 8))['msg'], response.json()['msg'], msg='商品详情查看失败')
        self.assertEqual(str(price),response.json()['data']['price'],msg='数据库金额与页面展示金额不匹配')

    def test_07(self):
        '''goodsId与shopId不一致'''
        token = MyMethod().readToken(path)  # 取出token保持登录
        dict = H5Method().Excel_Dict('H5商城', '首页', 7, 4, 3, 2)  # 取出Excel表格内容
        goodsId = int(dict['data']['goodsId'])  # 从Excel表格中获取分销商商品id
        dict['headers']['Referer'] = dict['headers']['Referer'] +'/'+ str(goodsId)  #Referer+id
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 7, 8))['msg'], response.json()['msg'], msg='goodsId与shopid不一致可以查看商品详情')

    def test_08(self):
        '''goodsId为空，查看商品详情'''
        token = MyMethod().readToken(path)  # 取出token保持登录
        dict = H5Method().Excel_Dict('H5商城', '首页', 8, 4, 3, 2)  # 取出Excel表格内容
        # goodsId = int(dict['data']['goodsId'])  # 从Excel表格中获取分销商商品id
        # dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodsId)  # Referer+id
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 8, 8))['msg'], response.json()['msg'],
                         msg='goodsId与shopid不一致可以查看商品详情')

    def test_09(self):
        '''shopid为空查看商品详情'''
        token = MyMethod().readToken(path)  # 取出token保持登录
        dict = H5Method().Excel_Dict('H5商城', '首页', 9, 4, 3, 2)  # 取出Excel表格内容
        goodsId = int(dict['data']['goodsId'])  # 从Excel表格中获取分销商商品id
        dict['headers']['Referer'] = dict['headers']['Referer'] + '/'+str(goodsId)  # Referer+id
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 9, 8))['msg'], response.json()['msg'],
                         msg='goodsId与shopid不一致可以查看商品详情')
    def test_10(self):
        '''有库存一件，点击加入购物车'''

        token = MyMethod().readToken(path)  # 取出token保持登录
        dict = H5Method().Excel_Dict('H5商城', '首页', 10, 4, 3, 2)  # 取出Excel表格内容
        id=int(dict['data']['goodId'])
        H5Method().updateSQl(id,1,1)
        goodId = int(dict['data']['goodId'])  # 从Excel表格中获取分销商商品id
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)  # Referer+id
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 10, 8))['msg'], response.json()['msg'],
                         msg='存在库存，加入购物车不成功')

    def test_11(self):
        '''库存为零，加入购物车'''
        token = MyMethod().readToken(path)  # 取出token保持登录
        dict = H5Method().Excel_Dict('H5商城', '首页', 11, 4, 3, 2)  # 取出Excel表格内容
        id = int(dict['data']['goodId'])
        H5Method().updateSQl(id, 0,2)
        goodId = int(dict['data']['goodId'])  # 从Excel表格中获取分销商商品id
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)  # Referer+id
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 11, 8))['msg'], response.json()['msg'],
                         msg='存在库存，加入购物车不成功')

    def test_12(self):
        '''buyNum 传入大于1'''
        token = MyMethod().readToken(path)  # 取出token保持登录
        dict = H5Method().Excel_Dict('H5商城', '首页', 12, 4, 3, 2)  # 取出Excel表格内容
        id = int(dict['data']['goodId'])
        H5Method().updateSQl(id, 1,1)
        goodId = int(dict['data']['goodId'])  # 从Excel表格中获取分销商商品id
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)  # Referer+id
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(MyMethod().duQu_Excel('H5商城', '首页', 12, 8))['msg'], response.json()['msg'],
                         msg='存在库存，加入购物车不成功')




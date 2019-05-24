import unittest,time,unittest,requests,HTMLTestRunner,random,json
from feng_test_method.feng_test_MethodCode import *
from feng_test_conf.feng_test_env.feng_test_config import *
from start_interface import *
from feng_test_log.feng_test_logmethod import *
from feng_test_method.H5_Method import H5Method,IfiCation
time = time.strftime('%d%H%M%S', time.localtime())


path=os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt'


def duQu_Excel(ExcelName, Sheet):
    PathCode = os.path.dirname(os.path.dirname(__file__)) + '/feng_excel_case/' + ExcelName + '.xlsx'
    excel_Name = xlrd.open_workbook(PathCode)
    # 打开excel文件格式为xlsx有的是xls
    table = excel_Name.sheet_by_name(Sheet)
    return table
table=duQu_Excel('H5商城','分类',)
    # cell_a1 = table.cell(a, b).value  # a代表行——从零开始   b代表列 从零开始

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

    def test_001(self):
        '''获取分类列表'''
        token=MyMethod().readToken(path)
        dict=H5Method().Excel_Dict('H5商城','分类',1,4,3,2)
        dict['url']=dict['url']+dict['data']['shopId']
        dict['headers']['token']=token[-1]
        response = H5Method().Get_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        list_data=eval(table.cell(1,8).value)['data']  #预期返回商品分类数量
        list_data_sql=IfiCation().selectSQL(dict['data']['shopId'])#获取数据库商品分类数量
        self.assertEqual(eval(table.cell(1, 8).value)['msg'], response.json()['msg'], msg='获取分类列表失败')  # 断言msg执行成功
        self.assertEqual(len(list_data),len(list_data_sql),msg='数据库商品分类与接口返回数量不一致') # 断言分类数量
    def  test_002(self):
        '''获取分类商品列表，传入id不存在'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '分类', 2, 4, 3, 2)
        dict['url'] = dict['url'] + dict['data']['shopId']
        dict['headers']['token'] = token[-1]
        response = H5Method().Get_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='没有提示店铺不存在')  # 断言msg执行成功

    def test_003(self):
        '''获取分类商品列表，传入id为空'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '分类', 3, 4, 3, 2)
        dict['url'] = dict['url'] + dict['data']['shopId']
        dict['headers']['token'] = token[-1]
        response = H5Method().Get_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(table.cell(3, 8).value)['msg'], response.json()['msg'], msg='没有提示店铺不存在')  # 断言msg执行成功

    def test_004(self):
        '''获取全部的商品，功能暂未实现'''
        pass #功能未实现

    def test_005(self):
        '''获取指定分类的商品数量'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '分类', 5, 4, 3, 2)
        # dict['url'] = dict['url'] + dict['data']['shopId']
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(table.cell(5, 8).value)['msg'], response.json()['msg'], msg='没有提示店铺不存在')  # 断言msg执行成功
        #判断数据库该分类商品数-对比接口返回数量是否OK
        numberSQL=IfiCation().SumShopping(dict['data']['categoryId'])
        number=numberSQL[-1][-1]  #数据库该商品分类商品数量
        number_response=len(response.json()['data']['list'])
        self.assertEqual(number,number_response,msg='接口返回数据与查询数据数量不一致')

    def test_006(self):
        '''商品分类id为空,返回全部商品信息'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '分类', 6, 4, 3, 2)
        # dict['url'] = dict['url'] + dict['data']['shopId']
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(table.cell(6, 8).value)['msg'], response.json()['msg'], msg='没有提示店铺不存在')  # 断言msg执行成功
        #判断数据库该分类商品数-对比接口返回数量是否OK
        shopId=dict['data']['shopId']
        sql='SELECT coalesce(id,"sum"),COUNT(id) FROM `seller_goods_info` where  shop_id=%s and status in (1,2) GROUP by id with ROLLUP;'%shopId
        numberSQL = MyMethod().selectSQL(sql)
        number = numberSQL[-1][-1]  # 数据库该商品分类商品数量
        print(number)
        number_response = len(response.json()['data']['list'])
        print(number_response)
        self.assertEqual(number, number_response, msg='接口返回数据与查询数据数量不一致')

    def test_007(self):
        '''验证shopId与分类id不匹配'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '分类', 7, 4, 3, 2)
        # dict['url'] = dict['url'] + dict['data']['shopId']
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(table.cell(7, 8).value)['msg'], response.json()['msg'], msg='没有提示店铺不存在')  # 断言msg执行成功
        number_response = len(response.json()['data']['list']) #返回list商品数量
        self.assertEqual(0,number_response,msg='分类id不存在，出现了商品')
    def test_008(self):
        '''验证pageNum,返回第二页数据'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '分类', 8, 4, 3, 2)
        # dict['url'] = dict['url'] + dict['data']['shopId']
        dict['headers']['token'] = token[-1]
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.assertEqual(eval(table.cell(8, 8).value)['msg'], response.json()['msg'], msg='没有提示店铺不存在')  # 断言msg执行成功
        number_response = len(response.json()['data']['list'])  # 返回list商品数量
        # 判断数据库该分类商品数-对比接口返回数量是否OK
        numberSQL = IfiCation().SumShopping(dict['data']['categoryId'])
        number = numberSQL[-1][-1]  # 数据库该商品分类商品数量
        if number>=20:
            self.assertEqual(10, number_response, msg='数量返回不对')
        else:
            self.assertEqual(number-10, number_response, msg='数量返回不对')

    def test_009(self):
        '''获取pageNum1和2，验证数据不重复'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '分类', 9, 4, 3, 2)
        # dict['url'] = dict['url'] + dict['data']['shopId']
        dict['headers']['token'] = token[-1]
        dict['data']['pageNum']=1
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        list_1=response.json()['data']['list']
        page_1=[]
        for  list_code_1  in list_1:
            id_1=list_code_1['id']
            page_1.append(id_1)
        #获取page_2的商品id，列表
        dict['data']['pageNum'] = 2
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        list_2 = response.json()['data']['list']
        page_2 = []
        for list_code_2 in list_2:
            id_2 = list_code_2['id']
            page_2.append(id_2)
        print(page_1,page_2)
        page=page_1+page_2
        self.assertEqual(len(page),len(list(set(page))),msg='数据有重复，第一次加载出来的和第二次加载出来的数据重复')










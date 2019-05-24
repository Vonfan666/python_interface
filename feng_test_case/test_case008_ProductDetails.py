import unittest,time,unittest,requests,HTMLTestRunner,random,json
from feng_test_method.feng_test_MethodCode import *
from feng_test_conf.feng_test_env.feng_test_config import *
from start_interface import *
from feng_test_log.feng_test_logmethod import *
from feng_test_method.H5_Method import H5Method,IfiCation,Shopping,ProductDetails
time = time.strftime('%d%H%M%S', time.localtime())


path=os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt'


def duQu_Excel(ExcelName, Sheet):
    PathCode = os.path.dirname(os.path.dirname(__file__)) + '/feng_excel_case/' + ExcelName + '.xlsx'
    excel_Name = xlrd.open_workbook(PathCode)
    # 打开excel文件格式为xlsx有的是xls
    table = excel_Name.sheet_by_name(Sheet)
    return table
table=duQu_Excel('H5商城','商品详情')
    # cell_a1 = table.cell(a, b).value  # a代表行——从零开始   b代表列 从零开始

class  Test_banner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dict=H5Method().Excel_Dict('H5商城','登录',1,4,3,2)
        H5Method().H5_login(dict['url'],dict['headers'],json.dumps(dict['data']))

    def setUp(self):
        Log()
        self.logger = logging.getLogger()
        self.logger.info('____________________start_________________')
        self.token = MyMethod().readToken(path)[-1]
    def tearDown(self):
        self.logger.info('____________________over__________________\n')

    def test_001(self):
        '''查看状态和库存正常的商品'''
        productIdList=Shopping().GouWuChe_add(self.token)
        productId=productIdList[0]
        self.logger.info('获取的分销商商品id为：%s'%productId)
        dict=H5Method().Excel_Dict('H5商城','商品详情',1,4,3,2)
        dict['headers']['token']=self.token
        dict['data']['goodsId']=productId
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        self.logger.info('获取的商品id为：%s，获取的商品状态为：%s'%(productId,response.json()['data']['status']))
        self.assertEqual(ProductDetails().productParam(productId)[0],response.json()['data']['goodsTitle'],msg='返回商品名称不正确')
        self.assertEqual(ProductDetails().productParam(productId)[1], response.json()['data']['status'],
                         msg='返回的商品状态不正确')
        self.logger.info('获取商品状态为：1---上架中')


    def test_002(self):
        '''库存已售罄查看商品详情'''
        productIdList = Shopping().GouWuChe_add(self.token)
        productId = productIdList[0]
        self.logger.info('获取的分销商商品id为：%s' % productId)
        dict = H5Method().Excel_Dict('H5商城', '商品详情', 2, 4, 3, 2)
        dict['headers']['token'] = self.token
        dict['data']['goodsId'] = productId

        H5Method().updateSQl(productId, 0, 2)  # 根据分销商商品id修改一下商品库存
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))

        self.logger.info('获取的商品id为：%s，获取的商品状态为：%s' % (productId, response.json()['data']['status']))
        self.assertEqual(ProductDetails().productParam(productId)[0], response.json()['data']['goodsTitle'],
                         msg='返回商品名称不正确')
        self.assertEqual(ProductDetails().productParam(productId)[1], response.json()['data']['status'],
                         msg='返回的商品状态不正确')
        self.logger.info('获取商品状态为：2---已售罄')
        H5Method().updateSQl(productId, 456455, 1)  # 还原分销商商品库存和状态
    def test_003(self):
        '''商品已下架，查看商品详情'''

        productIdList = Shopping().GouWuChe_add(self.token)
        productId = productIdList[0]
        self.logger.info('获取的分销商商品id为：%s' % productId)
        dict = H5Method().Excel_Dict('H5商城', '商品详情', 3, 4, 3, 2)
        dict['headers']['token'] = self.token
        dict['data']['goodsId'] = productId

        H5Method().updateSQl(productId, 12, 3)  # 根据分销商商品id修改一下商品库存
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))

        self.logger.info('获取的商品id为：%s，获取的商品状态为：%s' % (productId, response.json()['data']['status']))
        self.assertEqual(ProductDetails().productParam(productId)[0], response.json()['data']['goodsTitle'],
                         msg='返回商品名称不正确')
        self.assertEqual(ProductDetails().productParam(productId)[1], response.json()['data']['status'],
                         msg='返回的商品状态不正确')
        self.logger.info('获取商品状态为：3---已下架')
        H5Method().updateSQl(productId, 456455, 1)  # 还原分销商商品库存和状态


    def test_004(self):
        '''传入的商品id与shopid不匹配'''
        dict = H5Method().Excel_Dict('H5商城', '商品详情', 4, 4, 3, 2)
        dict['headers']['token'] = self.token
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.logger.info('商品id与shopid不一致请求后接口返回信息为：%s'%response.json())
        self.assertEqual(eval(table.cell(4,8).value)['msg'],response.json()['msg'],msg='提示信息不对或者未给出正确提示亦或者可以查看出商品信息')


    def test_005(self):
        '''传入的商品id为空'''
        dict = H5Method().Excel_Dict('H5商城', '商品详情', 5, 4, 3, 2)
        dict['headers']['token'] = self.token
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.logger.info('商品id与shopid不一致请求后接口返回信息为：%s' % response.json())
        self.assertEqual(eval(table.cell(5, 8).value)['msg'], response.json()['msg'], msg='提示信息不对或者未给出正确提示亦或者可以查看出商品信息')

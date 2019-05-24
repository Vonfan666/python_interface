from start_interface import *
from feng_test_log.feng_test_logmethod import *
from feng_test_method.H5_Method import H5Method,Shopping,ProductDetails
import time
timeCode = time.strftime('%d%H%M%S', time.localtime())


path=os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt'

def duQu_Excel(ExcelName, Sheet):
    PathCode = os.path.dirname(os.path.dirname(__file__)) + '/feng_excel_case/' + ExcelName + '.xlsx'
    excel_Name = xlrd.open_workbook(PathCode)
    # 打开excel文件格式为xlsx有的是xls
    table = excel_Name.sheet_by_name(Sheet)
    return table
table=duQu_Excel('H5商城','下单')
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
        '''商品库存充足，提交订单'''
        #从该店铺任意获取一个商品，并修改其库存，保证其库存充足，没然后提交订单
        ID=Shopping().GouWuChe_add(self.token)[0]    #ID商品id
        print(ID)
        H5Method().updateSQl(ID,5000,1) #修改该供应商对应的商品库存






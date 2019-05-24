from start_interface import *
from feng_test_log.feng_test_logmethod import *
from feng_test_method.H5_Method import H5Method,Address
import time,requests
timeCode = time.strftime('%y%d%H%M%S', time.localtime())


path=os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt'

def duQu_Excel(ExcelName, Sheet):
    PathCode = os.path.dirname(os.path.dirname(__file__)) + '/feng_excel_case/' + ExcelName + '.xlsx'
    excel_Name = xlrd.open_workbook(PathCode)
    # 打开excel文件格式为xlsx有的是xls
    table = excel_Name.sheet_by_name(Sheet)
    return table
table=duQu_Excel('H5商城','收货地址')
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
        '''添加一个收货地址'''
        response=Address().Address_add(self.token,1,4,3,2)
        self.logger.info('添加收货地址成功')
        self.assertEqual(eval(table.cell(1,8).value)['msg'],response['msg'],msg='添加收货地址失败')
    def test_002(self):
        '''修改一个收货地址'''
        uid=eval(H5Method().token_code(self.token))['user']['id']  #根据token获取uid
        self.logger.info('读出该用户uid为：%s'%uid)
        AddressUseList=Address().Address_use(uid)

        self.logger.info('获取可使用收货地址列表为：{}'.format(AddressUseList))
        AddressId = str(random.choice(AddressUseList)[0])
        self.logger.info('获取收货地址id为：%s' % AddressId)
        timeCode = time.strftime('%y%d%H%M%S', time.localtime())
        phone = MyMethod().createPhone()
        print(type(phone))
        self.logger.info('修改后手机号码为：%s'%phone)
        userName = 'Fengfan'
        detail = 'test地址' + timeCode
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 2,4,3,2)
        dict['headers']['token'] = self.token
        dict['headers']['Referer']=dict['headers']['Referer']+AddressId
        dict['data']['phone'] = phone
        dict['data']['userName'] = userName
        dict['data']['detail'] = detail
        dict['data']['id']=AddressId
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        self.logger.info('编辑收货地址成功')
        self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='编辑收货地址成功')

    def test_003(self):
        '''查看收货地址内容'''
        uid = eval(H5Method().token_code(self.token))['user']['id']  # 根据token获取uid
        self.logger.info('读出该用户uid为：%s' % uid)
        AddressUseList = Address().Address_use(uid)
        AddressId = str(random.choice(AddressUseList)[0])
        dict=H5Method().Excel_Dict('H5商城','收货地址',3,4,3,2)
        self.logger.info('获取的参数列表为：%s'%dict)
        dict['headers']['token']=self.token
        dict['headers']['Referer']=dict['headers']['Referer']+AddressId
        dict['data']['addressId']=AddressId
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        print(response.json())
    def test_004(self):
        '''一件商品查看收货地址列表'''
        dict=H5Method().Excel_Dict('H5商城','收货地址',4,4,3,2)
        dict['headers']['token']=self.token
        response=H5Method().Get_H5(dict['url'],dict['headers'],None)
        self.logger.info('收货地址返回列表为：%s'%response.json())
        self.assertEqual(eval(table.cell(4,8).value)['systemCode'],response.json()['systemCode'],msg='获取收货地址未成功')
    def test_005(self):
        '''验证最大添加收货地址数量'''
        #第一步获取收货地址list总数量
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 4, 4, 3, 2)
        dict['headers']['token'] = self.token
        response = H5Method().Get_H5(dict['url'], dict['headers'], None)
        oldNumber=len(response.json()['data'])
        AddressNumber=10-oldNumber
        for  a  in  range(1,AddressNumber+1):  #循环添加使收货地址列表达到十个数量
            Address().Address_add(self.token, 1, 4, 3, 2)
            self.logger.info('添加第【%s】个收货地址成功'%(oldNumber+a))
        response=Address().Address_add(self.token, 1, 4, 3, 2)
        self.logger.info('添加第【11】个收货地址')
        self.assertEqual(eval(table.cell(5,8).value)['msg'],response['msg'],msg='允许添加第11个收货地址')
        self.logger.info('添加第【11】个收货地址失败')
    def test_006(self):
        '''删除一个收货地址'''
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 4, 4, 3, 2)  #查看商品数量总和
        dict['headers']['token'] = self.token
        response = H5Method().Get_H5(dict['url'], dict['headers'], None)
        oldNumber=len(response.json()['data'])

        uid = eval(H5Method().token_code(self.token))['user']['id']  # 根据token获取uid
        self.logger.info('读出该用户uid为：%s' % uid)
        AddressUseList = Address().Address_use(uid)
        self.logger.info('获取到可使用的收货地址列表：%s'%str(AddressUseList))
        AddressId = str(random.choice(AddressUseList)[0])
        self.logger.info('预删除的收货地址id为：%s' % AddressId)   #根据uid获取收货地址列表

        dict=H5Method().Excel_Dict('H5商城','收货地址',6,4,3,2)
        dict['headers']['token']=self.token
        dict['data']['addressId']=AddressId
        H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        self.logger.info('删除收货地址成功')
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 4, 4, 3, 2)  # 查看商品数量总和
        dict['headers']['token'] = self.token
        response = H5Method().Get_H5(dict['url'], dict['headers'], None)
        newNumber = len(response.json()['data'])
        self.assertEqual(oldNumber-1,newNumber,msg='删除之后和删除之前的收货地址数量一样！')

    def test_007(self):
        '''删除不存在的收货地址'''
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 4, 4, 3, 2)  # 查看商品数量总和
        dict['headers']['token'] = self.token
        response = H5Method().Get_H5(dict['url'], dict['headers'], None)
        oldNumber = len(response.json()['data'])
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 7, 4, 3, 2)
        dict['headers']['token'] = self.token
        H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 4, 4, 3, 2)  # 查看商品数量总和
        dict['headers']['token'] = self.token
        response = H5Method().Get_H5(dict['url'], dict['headers'], None)
        newNumber = len(response.json()['data'])
        self.assertEqual(oldNumber, newNumber, msg='删除不存在的订单成功')
    def test_008(self):
        '''设置默认地址'''

        dict=H5Method().Excel_Dict('H5商城', '收货地址', 4, 4, 3, 2)
        dict['headers']['token']=self.token
        #根据token里面的uid获取到该用户除默认收货地址以为的收货地址id
        uid = eval(H5Method().token_code(self.token))['user']['id']  # 根据token获取uid
        self.logger.info('读出该用户uid为：%s' % uid)
        # 原来的默认收货地址为
        OldDefault=Address().Address_OldDefault(uid)[0][0]
        self.logger.info('原来的默认收货地址为：%s'%str(OldDefault))

        AddressUseList = Address().Address_default(uid)
        self.logger.info('获取除默认地址以外的收货地址列表为：%s'%str(AddressUseList))
        AddressId = str(random.choice(AddressUseList)[0])
        self.logger.info('取出预设默认收货地址为：%s'%AddressId)
        self.logger.info('将原默认收货地址id：%s改为：%s'%(OldDefault,AddressId))
        dict=H5Method().Excel_Dict('H5商城', '收货地址', 8, 4, 3, 2)
        dict['headers']['token']=self.token
        dict['data']['addressId']=AddressId
        H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        a=Address().Address_OldDefault(uid)[0][0]
        print(a)
        self.logger.info('原默认收货地址:%s已修改为：%s'%(OldDefault,a))
        self.assertNotEqual(OldDefault,a,msg='更改之后收货地址还是一样！')
    def test_009(self):
        '''验证删除收货地址，自动默认第一个收货地址'''
        #获取默认地址
        dict = H5Method().Excel_Dict('H5商城', '收货地址', 9, 4, 3, 2)
        dict['headers']['token'] = self.token
        # 根据token里面的uid获取到该用户除默认收货地址以为的收货地址id
        uid = eval(H5Method().token_code(self.token))['user']['id']  # 根据token获取uid
        self.logger.info('读出该用户uid为：%s' % uid)
        a=Address().Address_OldDefault(uid)[0][0]  #取出收货地址id
        self.logger.info('取出该默认地址的地址id为：%s'%str(a))
        dict=H5Method().Excel_Dict('H5商城', '收货地址', 9, 4, 3, 2)
        dict['headers']['token']=self.token
        dict['data']['addressId']=str(a)
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data'])) #删除默认收货地址
        self.assertEqual(eval(table.cell(9,8).value)['msg'],response.json()['msg'],msg='删除默认地址失败')
        b = Address().Address_OldDefault(uid)[0][0]  # 删除之后，取出新的默认收货地址id
        AddressUseList=[]
        print(Address().Address_use(uid))
        for  m in Address().Address_use(uid):
            AddressUseList.append(str(m[0]))
        self.logger.info('此时可用收货地址为列表：{}'.format(AddressUseList))
        self.assertIn(str(b),AddressUseList,msg='新的收获地址不属于可以用的列表')















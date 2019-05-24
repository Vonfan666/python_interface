import unittest,unittest,requests,HTMLTestRunner,random,json,datetime
from feng_test_method.feng_test_MethodCode import *
from feng_test_conf.feng_test_env.feng_test_config import *
from start_interface import *
from feng_test_log.feng_test_logmethod import *
from feng_test_method.H5_Method import H5Method,IfiCation,Shopping,ProductDetails
import time
timeCode = time.strftime('%d%H%M%S', time.localtime())


path=os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt'

def duQu_Excel(ExcelName, Sheet):
    PathCode = os.path.dirname(os.path.dirname(__file__)) + '/feng_excel_case/' + ExcelName + '.xlsx'
    excel_Name = xlrd.open_workbook(PathCode)
    # 打开excel文件格式为xlsx有的是xls
    table = excel_Name.sheet_by_name(Sheet)
    return table
table=duQu_Excel('H5商城','确认订单')
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
        '''购买一件商品，确认订单'''
        goodsId=Shopping().GouWuChe_add(self.token)  #goodsId为商品id列表，len()之后为2
        goodId=goodsId[0]
        self.logger.info('确认订单页面的id为：%s'%goodId)
        dict=H5Method().Excel_Dict('H5商城','确认订单',1,4,3,2)
        dict['headers']['token']=self.token
        dict['headers']['Referer']=dict['headers']['Referer']+ str(goodId)
        dict['data']['goodsId']=goodId  #购买请求商品id   购买请求商品数量默认为1
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        self.logger.info('返回内容为：\n%s'%response.json())
        self.assertEqual(eval(table.cell(1,8).value)['msg'],response.json()['msg'],msg='跳转确认订单页面未成功')  #断言是否成功
        #断言商品名称
        self.assertEqual(ProductDetails().productParam(goodId)[0],response.json()['data']['products'][0]['productName'],msg='商品名称不对')
    def test_002(self):
        '''购买0件商品，确认订单'''
        goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        goodId = goodsId[0]
        self.logger.info('确认订单页面的id为：%s' % goodId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 2, 4, 3, 2)
        dict['headers']['token'] = self.token
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)
        dict['data']['goodsId'] = goodId  # 购买请求商品id   购买请求商品数量默认为1
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.logger.info('返回内容为：\n%s' % response.json())
        self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        # 断言商品名称
        # self.assertEqual(ProductDetails().productParam(goodId)[0],
        #                  response.json()['data']['products'][0]['productName'], msg='商品名称不对')
    def test_003(self):
        '''商品库存为0，状态为上架，确认订单页面'''
        goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        goodId = goodsId[0]
        self.logger.info('确认订单页面的id为：%s' % goodId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 3, 4, 3, 2)
        dict['headers']['token'] = self.token
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)
        dict['data']['goodsId'] = goodId  # 购买请求商品id   购买请求商品数量默认为1
        H5Method().updateSQl(goodId,0,1)  #修改商品库存以及状态
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        H5Method().updateSQl(goodId, 4546545, 1)  # 还原商品库存以及状态
        self.logger.info('返回内容为：\n%s' % response.json())
        # self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        self.assertEqual(eval(table.cell(3,8).value),
                         response.json(), msg='商品库存为0可以继续购买')

    def test_004(self):
        '''商品库存为0，状态为已售罄，确认订单页面'''
        goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        goodId = goodsId[0]
        self.logger.info('确认订单页面的id为：%s' % goodId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 4, 4, 3, 2)
        dict['headers']['token'] = self.token
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)
        dict['data']['goodsId'] = goodId  # 购买请求商品id   购买请求商品数量默认为1
        H5Method().updateSQl(goodId, 0, 2)  # 修改商品库存以及状态
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        H5Method().updateSQl(goodId, 4546545, 1)  # 还原商品库存以及状态
        self.logger.info('返回内容为：\n%s' % response.json())
        # self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        self.assertEqual(eval(table.cell(4, 8).value),
                         response.json(), msg='商品库存为0可以继续购买')
    def test_005(self):
        goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        goodId = goodsId[0]
        self.logger.info('确认订单页面的id为：%s' % goodId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 5, 4, 3, 2)
        dict['headers']['token'] = self.token
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)
        dict['data']['goodsId'] = goodId  # 购买请求商品id   购买请求商品数量默认为1
        H5Method().updateSQl(goodId, 1, 1)  # 修改商品库存以及状态
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        H5Method().updateSQl(goodId, 4546545, 1)  # 还原商品库存以及状态
        self.logger.info('返回内容为：\n%s' % response.json())
        # self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        self.assertEqual(eval(table.cell(5, 8).value),
                         response.json(), msg='购买数量大于库存数量，该接口判断异常')
    def test_006(self):
        '''商品id不存在'''
        # goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        # goodId = goodsId[0]
        # self.logger.info('确认订单页面的id为：%s' % goodId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 6, 4, 3, 2)
        goodId=dict['data']['goodsId']
        dict['headers']['token'] = self.token
        dict['headers']['Referer'] = dict['headers']['Referer'] + str(goodId)
        # dict['data']['goodsId'] = goodId  # 购买请求商品id   购买请求商品数量默认为1
        H5Method().updateSQl(goodId, 1, 1)  # 修改商品库存以及状态
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        H5Method().updateSQl(goodId, 4546545, 1)  # 还原商品库存以及状态
        self.logger.info('返回内容为：\n%s' % response.json())
        # self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        self.assertEqual(eval(table.cell(6, 8).value),
                         response.json(), msg='购买数量大于库存数量，该接口判断异常')

    def test_007(self):
        '''购买一件商品，可选优惠券列表'''
        goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        self.logger.info('确认订单页面的商品id为：%s' % goodsId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单',7,4,3,2)
        dict['headers']['token'] = self.token
        products=dict['data']['products']
        for a in goodsId:
            products.append({"buyCount":1,"goodsId":str(a)})
        print(products)
        dict['data']['products'] = products  # 购买请求商品id   购买请求商品数量默认为1
        self.logger.info('请求参数为：%s'%dict['data'])
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.logger.info('返回内容为：\n%s' % response.json())
        # self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        self.assertEqual(eval(table.cell(7, 8).value)['msg'],
                         response.json()['msg'], msg='购买数量大于库存数量，该接口判断异常')
        self.assertEqual(eval(table.cell(7, 8).value)['statusCode'],
                         response.json()['statusCode'], msg='购买数量大于库存数量，该接口判断异常')


        #断言优惠券状态全部是未使用
    def test_008(self):
        '''购买一件商品，可选优惠券列表'''
        goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        self.logger.info('确认订单页面的id为：%s' % goodsId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 7, 4, 3, 2)
        dict['headers']['token'] = self.token
        products = dict['data']['products']
        # classList = []  # 商品分类id列表
        # for a in goodsId:
        #     code = ProductDetails().productCoupon(a)
        #     classList.append(code)  # 根据商品id  得出 商品金额 以及商品所属分类id
        #     products.append({"buyCount": 1, "goodsId": str(a)})
        # classList=classList[0]#只选取一个商品id
        goodsId=goodsId[0]
        classList=ProductDetails().productCoupon(goodsId)
        products.append({"buyCount": 1, "goodsId": str(goodsId)})
        dict['data']['products'] = products  # 购买请求商品id   购买请求商品数量默认为1
        self.logger.info('请求参数为：%s' % dict['data'])
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.logger.info('返回内容为：\n%s' % response.json())
        # self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        self.assertEqual(eval(table.cell(7, 8).value)['msg'],
                         response.json()['msg'], msg='购买数量大于库存数量，该接口判断异常')
        self.assertEqual(eval(table.cell(7, 8).value)['statusCode'],
                         response.json()['statusCode'], msg='购买数量大于库存数量，该接口判断异常')
        print(ProductDetails.CouponYes('62302675', '17700000000'))  # 获取出该用户所有可用的优惠券列表
        listCode = ProductDetails.CouponYes('62302675', '17700000000')
        print(len(listCode))
        CouponList = []  # 创建优惠券可使用列表
        '''以下获取两个商品的可用优惠券列表'''
        for code in listCode:
            if code[1] == 0:  # 判断使用门槛
                CouponList.append(str(code[0]))
            if code[1] == 1:
                if code[3] == 0:  # 判断时间 为绝对时间
                    nowTime = datetime.datetime.now()
                    if code[4] < nowTime or nowTime < code[5] or code[4] == None:  # 如果优惠券最后使用期限<当前时间或者小于开始时间
                        pass  # 则pass
                    if code[4] >= nowTime >= code[5]:  # 最小时间《当前时间《结束时间
                        if code[2] > classList[0][1]:
                            pass
                        else:
                            if code[7] == 0:  # 判断使用范围：0,全场商品|all;1,分类商品|category;2,指定商品|appoint',
                                CouponList.append(str(code[0]))  ###需求逻辑有问题 ，需要咨询产品
                            if code[7] == 1:  # 根据分类时，则要求确认订单页面的所有商品都是属于同一分类，则展示该对应的有优惠券
                                if classList[0][0] == code[8]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
                            if code[7] == 2:  ##指定商品id
                                if goodsId == code[-1]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
                if code[3] == 1:  # 判断linux时间戳  相对时间
                    nowTime = int(time.time())
                    if int(code[6]) < nowTime or code[6] == None or code[6] == 0:
                        pass
                    if int(code[6]) >= nowTime:
                        if code[2] > classList[0][1]:
                            pass
                        else:
                            if code[7] == 0:  # 判断使用范围：0,全场商品|all;1,分类商品|category;2,指定商品|appoint',
                                CouponList.append(str(code[0]))  ###需求逻辑有问题 ，需要咨询产品
                            if code[7] == 1:  # 根据分类时，则要求确认订单页面的所有商品都是属于同一分类，则展示该对应的有优惠券
                                if classList[0][0] == code[8]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
                            if code[7] == 2:  ##指定商品id
                                if goodsId== code[-1]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
        self.logger.info('商品id列表为：%s；商品分类id和库存为：%s' % (goodsId, classList))
        self.logger.info('可以用的优惠券id列表为：%s' % CouponList)
        responseIdList = []
        for a in response.json()['data']['list']:
            responseIdList.append(a['couponId'])
        self.assertEqual(CouponList, responseIdList, msg='返回可使用优惠券不对')
    def test_009(self):
        '''购买多件商品，可选择优惠券'''

        goodsId = Shopping().GouWuChe_add(self.token)  # goodsId为商品id列表，len()之后为2
        self.logger.info('确认订单页面的id为：%s' % goodsId)
        dict = H5Method().Excel_Dict('H5商城', '确认订单',7,4,3,2)
        dict['headers']['token'] = self.token
        products=dict['data']['products']
        classList=[]  #商品分类id列表
        for a in goodsId:
            code=ProductDetails().productCoupon(a)
            classList.append(code)   #根据商品id  得出 商品金额 以及商品所属分类id
            products.append({"buyCount":1,"goodsId":str(a)})
        print(products)
        dict['data']['products'] = products  # 购买请求商品id   购买请求商品数量默认为1
        self.logger.info('请求参数为：%s'%dict['data'])
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        self.logger.info('返回内容为：\n%s' % response.json())
        # self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='跳转确认订单页面未成功')  # 断言是否成功
        self.assertEqual(eval(table.cell(7, 8).value)['msg'],
                         response.json()['msg'], msg='购买数量大于库存数量，该接口判断异常')
        self.assertEqual(eval(table.cell(7, 8).value)['statusCode'],
                         response.json()['statusCode'], msg='购买数量大于库存数量，该接口判断异常')
        print(ProductDetails.CouponYes('62302675','17700000000'))   #获取出该用户所有可用的优惠券列表
        listCode=ProductDetails.CouponYes('62302675','17700000000')
        print(len(listCode))
        CouponList=[]  #创建优惠券可使用列表
        '''以下获取两个商品的可用优惠券列表'''
        for code in  listCode:
            if  code[1]==0:  #判断使用门槛
                CouponList.append(str(code[0]))
            if code[1]==1:
                if code[3]==0: #判断时间 为绝对时间
                    nowTime = datetime.datetime.now()
                    if code[4]<nowTime or nowTime<code[5]  or  code[4]==None:  #如果优惠券最后使用期限<当前时间或者小于开始时间
                        pass #则pass
                    if code[4]>=nowTime>=code[5]:  #最小时间《当前时间《结束时间
                        if code[2]>classList[0][0][1]+classList[1][0][1]:
                            pass
                        else:
                            if code[7]==0:   #判断使用范围：0,全场商品|all;1,分类商品|category;2,指定商品|appoint',
                                CouponList.append(str(code[0]))  ###需求逻辑有问题 ，需要咨询产品
                            if code[7]==1:     #根据分类时，则要求确认订单页面的所有商品都是属于同一分类，则展示该对应的有优惠券
                                if classList[0][0][0]==classList[1][0][0]  and classList[0][0][0]==code[8]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
                            if code[7]==2:   ##指定商品id
                                if goodsId[0]==goodsId[1] and goodsId[0]==code[-1]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
                if code[3]==1:  #判断linux时间戳  相对时间
                    nowTime=int(time.time())
                    if int(code[6])<nowTime  or  code[6]==None  or code[6]==0:
                        pass
                    if int(code[6])>=nowTime:
                        if code[2] > classList[0][0][1] + classList[1][0][1]:
                            pass
                        else:
                            if code[7]==0:   #判断使用范围：0,全场商品|all;1,分类商品|category;2,指定商品|appoint',
                                CouponList.append(str(code[0]))  ###需求逻辑有问题 ，需要咨询产品
                            if code[7]==1:     #根据分类时，则要求确认订单页面的所有商品都是属于同一分类，则展示该对应的有优惠券
                                if classList[0][0][0]==classList[1][0][0]  and classList[0][0][0]==code[8]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
                            if code[7]==2:   ##指定商品id
                                if goodsId[0]==goodsId[1] and goodsId[0]==code[-1]:
                                    CouponList.append(str(code[0]))
                                else:
                                    pass
        self.logger.info('商品id列表为：%s；商品分类id和库存为：%s'%(goodsId,classList))
        self.logger.info('可以用的优惠券id列表为：%s'%CouponList)
        responseIdList=[]
        for  a  in  response.json()['data']['list']:
            responseIdList.append(a['couponId'])
        self.assertEqual(CouponList,responseIdList,msg='返回可使用优惠券不对')


    def test_010(self):
        '''获取优惠券未使用列表'''
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 9, 4, 3, 2)
        dict['headers']['token'] = self.token
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        numberCode=len(response.json()['data'])
        self.logger.info('查询所有可用优惠券内容，返回列表为：%s'%response.json())
        self.logger.info('查询该用户可用优惠券数量为：%s'%numberCode)
        tokenCode=eval(H5Method().token_code(self.token))
        shopId=tokenCode['user']['shopId']
        userId=tokenCode['user']['id']
        couponNumber=ProductDetails().CouponNumber(0,shopId,userId)
        self.assertEqual(couponNumber,numberCode,msg='该用户预期返回条数和实际返回条数不相符')
    def test_011(self):
        '''获取优惠券已使用列表'''
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 10, 4, 3, 2)
        dict['headers']['token'] = self.token
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        numberCode = len(response.json()['data'])
        self.logger.info('查询所有可用优惠券内容，返回列表为：%s' % response.json())
        self.logger.info('查询该用已使用优惠券数量为：%s' % numberCode)
        tokenCode = eval(H5Method().token_code(self.token))
        shopId = tokenCode['user']['shopId']
        userId = tokenCode['user']['id']
        couponNumber = ProductDetails().CouponNumber(1,shopId,userId)
        self.assertEqual(couponNumber, numberCode, msg='该用户预期返回条数和实际返回条数不相符')

    def test_012(self):
        '''已过期列表'''
        dict = H5Method().Excel_Dict('H5商城', '确认订单', 11, 4, 3, 2)
        dict['headers']['token'] = self.token
        response = H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        numberCode = len(response.json()['data'])
        self.logger.info('查询所有可用优惠券内容，返回列表为：%s' % response.json())
        self.logger.info('查询该用已使用优惠券数量为：%s' % numberCode)
        tokenCode = eval(H5Method().token_code(self.token))
        shopId = tokenCode['user']['shopId']
        userId = tokenCode['user']['id']
        couponNumber = ProductDetails().CouponNumber(2, shopId, userId)
        self.assertEqual(couponNumber, numberCode, msg='该用户预期返回条数和实际返回条数不相符')
    def test_013(self):
        '''优惠券使用/以及优惠券释放'''
        pass #后续补充









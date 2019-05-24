import unittest,time,unittest,requests,HTMLTestRunner,random,json
from feng_test_method.feng_test_MethodCode import *
from feng_test_conf.feng_test_env.feng_test_config import *
from start_interface import *
from feng_test_log.feng_test_logmethod import *
from feng_test_method.H5_Method import H5Method,IfiCation,Shopping
time = time.strftime('%d%H%M%S', time.localtime())


path=os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt'


def duQu_Excel(ExcelName, Sheet):
    PathCode = os.path.dirname(os.path.dirname(__file__)) + '/feng_excel_case/' + ExcelName + '.xlsx'
    excel_Name = xlrd.open_workbook(PathCode)
    # 打开excel文件格式为xlsx有的是xls
    table = excel_Name.sheet_by_name(Sheet)
    return table
table=duQu_Excel('H5商城','购物车',)
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
    def tearDown(self):
        self.logger.info('____________________over__________________\n')
    def test_001(self):
        '''购物车列表请求'''
        token=MyMethod().readToken(path)
        dict=H5Method().Excel_Dict('H5商城','购物车',1,4,3,2)
        dict['headers']['token']=token[-1]
        response=H5Method().Get_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        self.logger.info('购物车列表请求返回内容：%s'%response.json())
        self.assertEqual(eval(table.cell(1,8).value)['msg'],response.json()['msg'],msg='购物车列表请求未成功')
        #判断购物车返回数量
        body=eval(H5Method().token_code(token[-1]))  #解析toke  json格式取出字典
        self.logger.info('解析token得到：%s'%body)
        user_id=body['user']['id']   #根据解析的token获取到user_id
        return_list=Shopping().GouWuChe_number(user_id)
        self.logger.info('获取购物车商品数量列表：%s'%str(return_list))
        if len(return_list)==0:
            db_number=0
            self.logger.info('购物车商品数量为：0')
        else:
            db_number=return_list[-1][-1]  #数据库该用户购物车商品数量
            self.logger.info('购物车商品数量为：%s'%db_number)
        number=len(response.json()['data'])
        self.logger.info('接口返回购物车商品数量为：%s'%number)
        self.assertEqual(db_number,number,msg='数据该用户购物车商品数量与接口返回不一致！')

    def test_002(self):
        '''shop_id为空'''
        token = MyMethod().readToken(path)
        dict = H5Method().Excel_Dict('H5商城', '购物车', 2, 4, 3, 2)
        dict['headers']['token'] = token[-1]
        response = H5Method().Get_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        print(response.json())
        self.assertEqual(eval(table.cell(2, 8).value)['msg'], response.json()['msg'], msg='购物车列表请求未成功')

    def test_003(self):
        '''商品加入购物车，验证购物车数量增加以及删除购物车商品'''
        token=MyMethod().readToken(path)
        dict=H5Method().Excel_Dict('H5商城','首页',11,4,3,2) #sheet首页，获取接口请求数据
        shop_id=dict['data']['mallId']  #获取店铺id

        dict1 = H5Method().Excel_Dict('H5商城', '购物车', 3, 4, 3, 2)
        dict1['headers']['token'] = token[-1]
        # 加入商品到购物车之前
        response = H5Method().Get_H5(dict1['url'], dict1['headers'], json.dumps(dict1['data']))
        shop_number_old = len(response.json()['data'])
        self.logger.info('加入购物车之前的商品数量是：%s'%shop_number_old)
        list_old=response.json()['data']
        GouWuCheListShopId=[]
        for  goods_id_dict in list_old:   #列表取出原来购物车中已售罄的商品
            if goods_id_dict['status']=='1':
                goods_id=goods_id_dict['goodId']
                GouWuCheListShopId.append(goods_id)
        self.logger.info('原来的购物车中有效商品列表为：%s'%GouWuCheListShopId)
        al=IfiCation().selectSQL(shop_id)  #查询店铺下所有分类id
        self.logger.info('该店铺下所有的分类列表为:%s'%str(al))
        list_id=[]
        for  al_1 in  al:  #
            mp=al_1[0]   #mp所有的分类id
            su=IfiCation().SumShopping(mp)  #根据分类id找出下面的商品id
            if  len(su)>0: # 根据分类id找出商品数量大于1的分类
                for shop_list in su:
                    shop_id_code=shop_list[0]    #取出分销商 商品id

                    list_id.append(shop_id_code)
        self.logger.info('根据分类id找出商品库存大于1的分类为：%s' % list_id)
        for  a in  list_id:  #将所有的商品id加入到一个list
            if  a=='sum':
                list_id.remove('sum')
        print(list_id)
        for LL  in  GouWuCheListShopId:  #将购物车中已经存在的商品，从可添加的商品id列表剔除
            if  LL in list_id:
                list_id.remove(LL)

        for  b  in  list_id:     #判断商品库存是否大于1
            stock_number=Shopping().GouWuChe_stock(b)[0][0]
            if stock_number<=0:
                list_id.remove(b)
        print(stock_number)
        b=random.choice(list_id)
        self.logger.info('添加的商品id为：%s'%b)
        dict['data']['goodId']=b  #修改添加到购物车的分销商品id
        dict['headers']['Referer'] = dict['headers']['Referer'] + b
        dict['headers']['token']=token[-1]
        H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))  # 加入商品到购物车
        response=H5Method().Get_H5(dict1['url'],dict1['headers'],json.dumps(dict1['data']))
        shop_number_new=len(response.json()['data'])
        self.logger.info('加入商品到购物车之后，购物车现存商品数量为：%s'%shop_number_new)
        self.assertEqual(shop_number_old,shop_number_new-1,msg='新加入一个商品进入购物车之后，购物车商品数量没变，加入购物车未成功')
        #根据商品id获取购物车id
        GouWuCheShopId=Shopping().categoryIdMethod(b)
        # MyMethod().selectSQL('select category_id  from seller_goods_info where  id=%s'%GouWuCheShopId)
        #删除购物车上
        response=Shopping().GouWuChe_delete(GouWuCheShopId,token[-1])  #删除购物车商品成功
        print(response.json())
        self.logger.info('删除加入购物车的商品,购物车id：%s'%GouWuCheShopId)
#断言之后需要删除掉 添加到购物车的商品   封装一个删除购物车商品的方法，下面


    def test_004(self):
        '''验证购物车单个商品删除'''
        self.logger.info('test_003已验证，购物车删除单个商品')

    def test_005(self):
        '''购物车多个商品删除'''
        #先添加两个个商品到购物车
        token=MyMethod().readToken(path)
        goodIdListCode=Shopping().GouWuChe_add(token)
        self.logger.info('goodIdListCode商品列表为：%s'%goodIdListCode)
        for goodId in  goodIdListCode:  #添加两个商品加入购物车
            dict=H5Method().Excel_Dict('H5商城','首页',10,4,3,2)
            dict['headers']['token']=token[-1]
            dict['data']['goodId']=str(goodId)
            H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        dict=H5Method().Excel_Dict('H5商城','购物车',5,4,3,2)
        dict['headers']['token']=token[-1]
        for  id  in goodIdListCode:  #分销商商品表id
            #根据分销商商品id找到，购物车商品id
            print(id)
            id=Shopping().categoryIdMethod(id)
            self.logger.info('购物车商品id为：%s'%id)
            dict['data']['id']=id
            # dict['data'].pop('shopId')
            response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
            print(response.json())
            self.assertEqual(eval(table.cell(5,8).value)['msg'],response.json()['msg'],msg='删除购物车内容不成功')
    def test_006(self):
        '''存在库存，购物车商品数量增加'''
        #a、查看可以添加到购物车的商品
        token = MyMethod().readToken(path)
        goodIdListCode = Shopping().GouWuChe_add(token)
        self.logger.info('goodIdListCode商品列表为：%s' % goodIdListCode)
        #这里可能需要修改一下数据库商品库存，暂未修改
        id=str(goodIdListCode[0])
        dict=H5Method().Excel_Dict('H5商城','首页',10,4,3,2)  #商品加入购物车
        dict['headers']['token']=token[-1]
        dict['data']['goodId']=id
        H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))###商品加入购物车
        self.logger.info('分销商商品id为：%s，已加入购物车'%id)
        #根据商品id找到购物车商品id
        GouWuCheId=Shopping().categoryIdMethod(id)
        self.logger.info('根据分销商商品id，获取加入购物车后的购物车id为：%s'%GouWuCheId)
        dict=H5Method().Excel_Dict('H5商城','购物车',6,4,3,2,)
        dict['headers']['token']=token[-1]
        dict['data']['id']=GouWuCheId
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        self.logger.info('分销商商品id为：%s的商品，增加商品数量'%id)
        Shopping().GouWuChe_delete(GouWuCheId, token[-1])
        self.assertEqual(eval(table.cell(6,8).value)['msg'],response.json()['msg'],msg='添加购物车商品数量不成功')


    def test_007(self):
        '''加入购物车后-商品下架-新增数量'''
        #a、查看可以添加到购物车的商品
        token = MyMethod().readToken(path)
        goodIdListCode = Shopping().GouWuChe_add(token)
        self.logger.info('goodIdListCode商品列表为：%s' % goodIdListCode)
        #这里可能需要修改一下数据库商品库存，暂未修改
        id=str(goodIdListCode[0])
        dict=H5Method().Excel_Dict('H5商城','首页',10,4,3,2)  #商品加入购物车
        dict['headers']['token']=token[-1]
        dict['data']['goodId']=id
        H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))###商品加入购物车
        self.logger.info('分销商商品id为：%s，已加入购物车'%id)
        #根据商品id找到购物车商品id
        GouWuCheId=Shopping().categoryIdMethod(id)
        self.logger.info('根据分销商商品id，获取加入购物车后的购物车id为：%s'%GouWuCheId)
        dict=H5Method().Excel_Dict('H5商城','购物车',7,4,3,2,)
        dict['headers']['token']=token[-1]
        dict['data']['id']=GouWuCheId

        H5Method().updateSQl(id,0,1)   #修改商品库存为0,商品状态为“上架中”
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        H5Method().updateSQl(id,445464, 1)  # 修改商品库存为0,商品状态为“上架中”
        self.logger.info('分销商商品id为：%s的商品，增加商品数量'%id)
        Shopping().GouWuChe_delete(GouWuCheId, token[-1])
        self.assertEqual(eval(table.cell(7,8).value)['msg'],response.json()['msg'],msg='添加购物车商品数量成功')

    def test_008(self):
        '''加入购物车后-商品已售罄（未下架）--新增数量'''
        #a、查看可以添加到购物车的商品
        token = MyMethod().readToken(path)
        goodIdListCode = Shopping().GouWuChe_add(token)
        self.logger.info('goodIdListCode商品列表为：%s' % goodIdListCode)
        #这里可能需要修改一下数据库商品库存，暂未修改
        id=str(goodIdListCode[0])
        dict=H5Method().Excel_Dict('H5商城','首页',10,4,3,2)  #商品加入购物车
        dict['headers']['token']=token[-1]
        dict['data']['goodId']=id
        H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))###商品加入购物车
        self.logger.info('分销商商品id为：%s，已加入购物车'%id)
        #根据商品id找到购物车商品id
        GouWuCheId=Shopping().categoryIdMethod(id)
        self.logger.info('根据分销商商品id，获取加入购物车后的购物车id为：%s'%GouWuCheId)
        dict=H5Method().Excel_Dict('H5商城','购物车',8,4,3,2,)
        dict['headers']['token']=token[-1]
        dict['data']['id']=GouWuCheId

        H5Method().updateSQl(id,455454,3)   #修改商品库存为0,商品状态为“上架中”
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        H5Method().updateSQl(id,445464, 1)  # 修改商品库存为0,商品状态为“上架中”
        self.logger.info('分销商商品id为：%s的商品，增加商品数量'%id)
        Shopping().GouWuChe_delete(GouWuCheId, token[-1])
        self.assertEqual(eval(table.cell(8,8).value)['msg'],response.json()['msg'],msg='添加购物车商品数量成功')


























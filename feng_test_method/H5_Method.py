import xlrd,pymysql,requests
from feng_test_conf.feng_test_env.feng_test_config import MustCode
from feng_test_log.feng_test_logmethod import *
from feng_test_method.feng_test_MethodCode import MyMethod
import  json,random
import base64,gzip
class  H5Method():
    def __init__(self):
        Log()
        self.logger = logging.getLogger()
    @staticmethod
    def token_code(token):
        sp = token.split('.')
        a = sp[0].replace(r'-', r"+").replace(r'_', r"/") + '=='
        b = sp[1].replace(r'-', r"+").replace(r'_', r"/") + '=='
        a = a.encode('gbk')
        headers = base64.b64decode(a)
        b = b.encode('gbk')
        body = base64.b64decode(b)
        body = gzip.decompress(body)
        body = body.decode('gbk')
        return body
    @staticmethod
    # 直接获取Excel表格内容，并返回一个字典
    def  Excel_Dict(ExcelName,SheetName,Row,column_url,column_header,column_data):
        url = MustCode['url'] + MyMethod().duQu_Excel(ExcelName,SheetName,Row,column_url)
        headers = MyMethod().duQu_Excel(ExcelName,SheetName,Row,column_header)
        data = MyMethod().duQu_Excel(ExcelName,SheetName,Row,column_data)
        Excel_Dict_Code={'url':url,'headers':eval(headers),'data':eval(data)}
        return Excel_Dict_Code

    @staticmethod
    # 直接获取Excel表格内容，并完成接口访问，返回接口返回内容
    def Post_register(ExcelName,SheetName,Row,column_url,column_header,column_data):
        url = MustCode['url'] + MyMethod().duQu_Excel(ExcelName, SheetName, Row, column_url)
        headers = MyMethod().duQu_Excel(ExcelName, SheetName, Row, column_header)
        data = MyMethod().duQu_Excel(ExcelName,SheetName, Row, column_data)
        response = requests.post(url, headers=eval(headers), data=data, verify=False)
        return response
    #  H5个人商城 登录获取token
    @staticmethod
    def H5_login(url,headers,json):
        url = url
        headers = headers
        data    = json
        response=requests.post(url,headers=headers,data=data,verify=False)
        token=response.json()['data']['data']
        with open(os.path.dirname(os.path.dirname(__file__))+'/feng_test_method/token.txt','w')  as  f:
            f.write(token)
    @staticmethod
    def login_H5(url, headers, json):
        url = MustCode['url'] + url
        headers = headers
        data = json
        response = requests.post(url, headers=headers, data=data, verify=False)
        return response
    @staticmethod
    # 注册账号
    def H5_Post_register(phone,password):
        dict=H5Method().Excel_Dict('H5商城','注册',1,4,3,2)  #发送验证码
        dict['data']['phoneNum']=phone
        data=json.dumps(dict['data'])
        H5Method().Post_H5(dict['url'],dict['headers'],data)
        code = MyMethod().redisCode(phone)  # 获取验证码
        dict=H5Method().Excel_Dict('H5商城','注册',1,4,3,2)   #填写验证码
        url =MustCode['url'] +  '/shoppingmall/anon/compareIdentifyingCode'
        dict['url']=url
        dict['data']['code']=eval(code)
        dict['data']['phoneNum']=phone
        print(1,dict)
        data=json.dumps(dict['data'])
        print(data)
        response = H5Method().Post_H5(dict['url'],dict['headers'], data)
        print(response.json())
        key = response.json()['data']['key']  #输入密码
        a = H5Method().Excel_Dict('H5商城', '注册', 5, 4, 3, 2)
        a['data']['password']=password
        a['data']['key'] = key
        data = json.dumps(a['data'])
        H5Method().Post_H5(a['url'], a['headers'], data)
    @staticmethod
    #忘记密码_发送验证码
    def reset_post_password(phone):
        dict=H5Method().Excel_Dict('H5商城','忘记密码',1,4,3,2)
        dict['data']['phoneNum']=phone
        data=json.dumps(dict['data'])
        dict['headers']['Referer']='http://192.168.12.21:81/forgetpsw/2'
        response=H5Method().Post_H5(dict['url'],dict['headers'],data)
        print(response.json())#忘记密码发送验证码
    @staticmethod
    #输入验证码反馈key
    def reset_password(phone,resetCode):
        dict=H5Method().Excel_Dict('H5商城','忘记密码',1,6,3,2)
        dict['data']['phoneNum'] = phone
        dict['data']['code']=eval(resetCode)
        data=json.dumps(dict['data'])
        response=H5Method().Post_H5(dict['url'], dict['headers'], data)  # 忘记密码发送验证码
        return  response
    @staticmethod
    # 封装get请求
    def Get_H5(url,headers,param):
        url = url
        headers = headers
        param = param
        if param==None:
            response = requests.get(url, headers=headers,verify=False)
        else:
            response=requests.get(url,headers=headers,json=param,verify=False)
        return  response
    @staticmethod
    # 封装post请求
    def  Post_H5(url,headers,json):
        url = url
        headers = headers
        data = json
        response=requests.post(url,headers=headers,data=data,verify=False)
        return response

    @staticmethod
    # 完成短信验证码，进入输入密码页面
    def set_password():
        phoneNumCode = MyMethod().createPhone()
        url =MustCode['url'] + MyMethod().duQu_Excel('H5商城', '注册', 4, 4)
        headers = MyMethod().duQu_Excel('H5商城', '注册', 4, 3)
        shop_id = MyMethod().duQu_Excel('H5商城', '注册', 4, 2)
        data = {'phoneNum': phoneNumCode, 'shopId': shop_id}
        data=json.dumps(data)
        H5Method().Post_H5(url, eval(headers), data)  # 注册
        redisCode=MyMethod().redisCode(phoneNumCode)
        data=json.loads(data)
        data['code']=eval(redisCode)
        data = json.dumps(data)
        url =MustCode['url'] +  '/shoppingmall/anon/compareIdentifyingCode' #填写验证码
        response=H5Method().Post_H5(url, eval(headers), data)
        return response
    @staticmethod
    #修改密码
    def resetPassWordMthod(phone,Row,password):
        H5Method().reset_post_password(phone)  # 发送验证码
        code = MyMethod().redisCode_key('mall:shoppingmall:smsVeriCode:FIND_BACK_LOGIN_PWD:', phone)
        dict = H5Method().Excel_Dict('H5商城', '忘记密码', 2, 6, 3, 2)  # 核验验证码
        dict['data']['phoneNum'] = phone
        dict['data']['code'] = eval(code)
        dict['headers']['Referer'] = 'http://192.168.12.21:81/forgetpsw/2'
        data = json.dumps(dict['data'])
        response = H5Method().Post_H5(dict['url'], dict['headers'], data)  # 输入验证码
        key = response.json()['data']['key']  # 获取key
        dict = H5Method().Excel_Dict('H5商城', '忘记密码', Row, 4, 3, 2)
        dict['headers']['Referer'] = 'http://192.168.12.21:81/forgetpsw/3'
        dict['data']['key'] = key
        dict['data']['password']=password
        data = json.dumps(dict['data'])
        response = H5Method().Post_H5(dict['url'], dict['headers'], data)
        return response
    #H5数据库
    @staticmethod
    def selectSQL(id):
        sql='select * from seller_goods_info where  id=%s'%id
        db=pymysql.connect(host="192.168.12.21", port=3307 ,user="mycat", password="cPfeU4ZJ9PhY",db="test_mall",charset ='utf8')
        cursor=db.cursor()
        #cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql) #执行sql语句,并返回一个
        return cursor.fetchall()#取出的所有的值

    @staticmethod
    def  updateSQl(id,count,status):  # 分销商商品id——修改库粗
        # 0,仓库中|warehouse;1,上架中|selling;2,已售罄|sold;3,已下架|already_down',
        sql = 'update supplier_goods_info a,seller_goods_info b set a.stock=%s,b.status=%s where a.id=b.goods_id and b.id=%s '%(count,status,id)
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        try:
            db.commit()
        except:
            db.rollback()

class IfiCation():
    '''查询对应id分类数量'''
    @staticmethod
    def selectSQL(shop_id):
        sql = 'select * from seller_goods_category where  shop_id="%s"' % shop_id
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        return cursor.fetchall()  # 取出的所有的值
    @staticmethod
    def SumShopping(category_id):
        '''判断数据库的所属分类id下的商品'''
        sql = 'SELECT coalesce(id,"sum"),COUNT(id) FROM `seller_goods_info` where  category_id=%s and status=1 GROUP by id with ROLLUP'%category_id
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        return cursor.fetchall()  # 返回分销商 商品id
class Shopping():
    @staticmethod
    def GouWuChe_number(member_id):
        '''统计用户购物车商品数量'''
        sql = 'SELECT coalesce(id,"sum"),COUNT(id) FROM `shoppingmall_shopping_car` where  member_id="%s"  and is_delete=0 and settle_status=0 group by  id  with ROLLUP'%member_id
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个

        return cursor.fetchall()  # 取出的所有的值

    @staticmethod
    def GouWuChe_stock(shop_id):
        #根据分销商商品id取出库存
        sql = 'SELECT b.stock FROM seller_goods_info a, supplier_goods_info b  where b.id=a.goods_id and a.id=%s and a.status=1 '%shop_id
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个

        return cursor.fetchall()  # 取出的所有的值
    @staticmethod
    def GouWuChe_add(token):
        '''可添加购物车商品id列表'''
        dict = H5Method().Excel_Dict('H5商城', '购物车', 1, 4, 3, 2)
        sql = 'select id from  seller_goods_info WHERE  shop_id=%s and  status=1'%dict['data']['shopId']
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        Sql_id=[] #数据库所有商品
        SqlListId=cursor.fetchall()
        for  A  in   SqlListId:
            Sql_id.append(A[0])
        dict['headers']['token'] = token[-1]
        response = H5Method().Get_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        id_list=response.json()['data']  #获取data列表
        responseListId=[]
        for a  in id_list: #已存在购物车的商品id
            a1=a['goodId']
            responseListId.append(a1)
        for  code  in responseListId:  #获取可添加到购物车列表
            if  code  in  Sql_id:
                Sql_id.remove(code)
        goodIdListCode=random.sample(Sql_id,2)  #随机选取两位
        return goodIdListCode
    @staticmethod
    def GouWuChe_delete(id,token):  #购物车id
        '''删除购物车商品'''
        dict=H5Method().Excel_Dict('H5商城','购物车',4,4,3,2)
        dict['data']['id']=id
        dict['headers']['token']=token
        response=H5Method().Post_H5(dict['url'],dict['headers'],json.dumps(dict['data']))
        return response
    @staticmethod
    def user_id():
        #用户会员id
        dict=H5Method().Excel_Dict('H5商城','登录',1,4,3,2)
        shop_id=dict['data']['shopId']
        members_account=dict['data']['userName']
        sql='select id from  shoppingmall_user WHERE  shop_id=%s and  members_account="%s"'%(shop_id,members_account)
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        return cursor.fetchall()[-1][-1]  # 取出的所有的值
    @staticmethod
    def categoryIdMethod(good_id):  #good_id是商品id
        '''取出购物车id'''
        sql = 'select id  from shoppingmall_shopping_car where  good_id=%s and member_id=%s and  is_delete=0 '%(good_id,Shopping().user_id())
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        return cursor.fetchall()[0][0]  # 取出的所有的值

class ProductDetails():
    @staticmethod
    def productParam(goodId):#商品id，店铺id
        '''根据商品id获取商品名称'''
        sql = 'select goods_title,status  from seller_goods_info where id=%s '%goodId  #取出名称和状态
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        return cursor.fetchall()[0]  # 取出的所有的值
    @staticmethod
    def productCoupon(goodId):
        '''根据商品id取出商品分类id以及商品金额'''
        sql = 'select category_id,price  from seller_goods_info where id=%s ' % goodId  # 根据商品id取出金额和所属分类
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        return cursor.fetchall()  # 取出的所有的值，为一个二维元组
    @staticmethod
    def CouponYes(shopId,user_account): #店铺id  和  用户账号
        '''统计所有可用优惠券id'''
       # ['discount_form','trigger_amount','use_limit','expiry_date_type','expiry_date_end','relative_time','use_range','limit_category_id','limit_product_id']
        sql = "SELECT coupon_id,use_limit,trigger_amount,expiry_date_type,expiry_date_start,expiry_date_end,relative_time,use_range,limit_category_id,limit_product_id,a.shop_id from  seller_coupon a,seller_coupon_receive b where a.id=b.coupon_id and a.shop_id=%s and  b.user_account=%s and b.coupon_status='0' and b.is_delete=0"%(shopId,user_account)  # 根据商品id取出金额和所属分类
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        # cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql)  # 执行sql语句,并返回一个
        return cursor.fetchall()  # 取出的所有的值，为一个二维元组

    @staticmethod
    def CouponNumber(statusCode,shopId,userId):
        '''统计当前用户可用优惠券数量'''
        sql='select count(id) from  seller_coupon_receive where coupon_status=%s and shop_id="%s" and user_id="%s" and is_delete=0'%(statusCode,shopId,userId)

        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor=db.cursor()
        cursor.execute(sql)
        db.close()
        return cursor.fetchall()[0][0]

    @staticmethod
    def order_01():   #根据shopId获取该店铺下所有的商品id列表
        sql=''
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor=db.cursor()
        cursor.execute(sql)
        db.close()
        return cursor.fetchall()[0][0]

class Address():
    @staticmethod
    def  Address_add(token,a,b,c,d):   #添加修改收货地址
        timeCode = time.strftime('%y%d%H%M%S', time.localtime())
        phone = MyMethod().createPhone()
        userName = 'Fengfan'
        detail = 'test地址' + timeCode
        dict = H5Method().Excel_Dict('H5商城', '收货地址',a,b,c,d)
        dict['headers']['token'] = token
        dict['data']['phone'] = phone
        dict['data']['userName'] = userName
        dict['data']['detail'] = detail
        response=H5Method().Post_H5(dict['url'], dict['headers'], json.dumps(dict['data']))
        return response.json()
    @staticmethod
    def Address_use(uid):    #可以使用的收货地址
        sql='SELECT * FROM `shoppingmall_user_address` where  user_id="%s" and  is_delete=0'%uid
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor=db.cursor()
        cursor.execute(sql)
        db.close()
        return cursor.fetchall()

    @staticmethod
    def Address_OldDefault(uid):  #获取默认收货地址id
        sql = 'SELECT * FROM `shoppingmall_user_address` where  user_id="%s" and  is_delete=0 and is_default=1' % uid
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        db.close()
        return cursor.fetchall()

    @staticmethod
    def Address_default(uid):  #获取除默认收货地址以外的地址
        sql = 'SELECT * FROM `shoppingmall_user_address` where  user_id="%s" and  is_delete=0 and is_default=0' % uid
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        db.close()
        return cursor.fetchall()



























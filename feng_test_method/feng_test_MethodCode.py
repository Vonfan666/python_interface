import xlrd,pymysql,requests
from feng_test_log.feng_test_logmethod import *
import  redis,random

class MyMethod():
    def __init__(self):
        Log()
        self.logger = logging.getLogger()

        '''excelb表格读取'''
    def duQu_Excel(self,ExcelName,Sheet, a, b):
        PathCode=os.path.dirname(os.path.dirname(__file__))+'/feng_excel_case/'+ExcelName+'.xlsx'
        excel_Name = xlrd.open_workbook(PathCode)
        # 打开excel文件格式为xlsx有的是xls
        table = excel_Name.sheet_by_name(Sheet)
        cell_a1 = table.cell(a, b).value  # a代表行——从零开始   b代表列 从零开始
        return cell_a1

    @staticmethod
    def selectSQL(sql):
        db = pymysql.connect(host="192.168.12.21", port=3307, user="mycat", password="cPfeU4ZJ9PhY", db="test_mall",
                             charset='utf8')
        cursor=db.cursor()
        #cursor.execute("select *  from  yzb_user WHERE NAME like '%s'"%('冯%'))
        cursor.execute(sql) #执行sql语句,并返回一个
        return cursor.fetchall()#取出的所有的值

    @staticmethod
    def redisCode(Usernamecode):
        pool = redis.ConnectionPool(host='192.168.12.21', port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        a = Usernamecode
        b = 'mall:shoppingmall:smsVeriCode:USER_REGISTRATION:'
        return r.get(b+a).decode('gbk')

    @staticmethod
    def redisCode_key(key,Usernamecode):
        pool = redis.ConnectionPool(host='192.168.12.21', port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        a = Usernamecode
        b = key
        return r.get(b + a).decode('gbk')


    @staticmethod
    def createPhone():
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                   "153", "155", "156", "157", "158", "159", "186", "187", "188"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


    @staticmethod
    def readToken(path):
        with open(path,'r')  as f:
            token=f.readlines()
        return token
    @staticmethod
    def writeFile(file):
        with open(r'C:\Users\Administrator\Desktop\python_interface\feng_test_method\response.txt','w')  as f:
            f.write(file)







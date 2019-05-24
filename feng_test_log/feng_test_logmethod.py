__author__='fengfan'
import logging,time,os
import logging.config
import logging.handlers
def Log():
    logging.config.fileConfig(os.path.dirname(os.path.dirname(__file__))+'/feng_test_conf/feng_test_env/mylog.conf')  # 该路径是调用env下面的mylog日志配置文件

    logger = logging.getLogger(__name__)
    fmt = '[%(asctime)s](%(levelname)s)%(name)s : %(message)s\n'
    formartter = logging.Formatter(fmt)
    consoleLog = logging.StreamHandler()  # 创建一个输入日志到控制台Streamhandler的实例！
    consoleLog.setFormatter(formartter)  # 控制台输出格式
    consoleLog.setLevel(logging.INFO)  # 设置输出的控制台的日志为info+
    logger.addHandler(consoleLog)  # 控制台]
    #进行日志回滚备份
    # curTime = time.strftime('%Y%m%d%H%M%S', time.localtime())
    # logFile = r'C:\Users\feng\Desktop\python01\fengfan_unittest\feng_test_log\feng_test_logfile\\' + curTime + '.log'
    #         #文件写到本地
    # handler=logging.handlers.RotatingFileHandler(logFile, maxBytes=4096000000, backupCount=9)
    # handler.setFormatter(formartter)   #本地文件输出格式
    # handler.setLevel(logging.INFO)  #设置logger的level为info，打印info以上的日志
    # logger.addHandler(handler) #handler上面有定义，写到本地，这个是把日志像本地文件输出
    #避免打印重复
    #logger.removeHandler(handler)
    logger.removeHandler(consoleLog)
    return logging.getLogger()
if  __name__ == '__main__':
    Log()




import threading

import operate.ProxySpiderFirst as ps1
import operate.ProxySpiderSecond as ps2
import operate.ProxySpiderThird as ps3
import operate.ProxySpiderFourth as ps4


def SpiderStartUp():
    # 总共有4个代理爬虫所以开启4个线程同时运行
    t1 = threading.Thread(target=ps1.start_up())
    t2 = threading.Thread(target=ps2.start_up())
    t3 = threading.Thread(target=ps3.start_up())
    t4 = threading.Thread(target=ps4.start_up())
    t1.start()
    t2.start()
    t3.start()
    t4.start()


# 主程序运行入口
if __name__ == '__main__':
    SpiderStartUp()

import win32api, win32con, telnetlib, random, json
from concurrent.futures.thread import ThreadPoolExecutor
import redisitem.RedisOperation as ro
import log.logModel as lm

# 浏览器信息
head_data = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.90 Safari/537.36 ',
}


# 获取代理ip
def GetProxyIP():
    # 获取redis对象
    r = ro.getRedisObj()
    # 随机获取一条数据
    i = random.sample(ro.getDicKeys(), 1)[0]
    if i:
        # 得到数据的value值，为字典类型的json字符串，将其转为字典类型
        ip_info = json.loads(r.hget("proxy_ip", i))
        try:
            # 测试代理是否可用
            telnetlib.Telnet(ip_info["ip"], ip_info["post"], timeout=2)
            # 记录日志
            lm.log_info(ip_info["ip"] + ":" + ip_info["post"] + "监测为可用代理")
            # 将可用代理写入桌面txt文件
            with open(get_desktop() + "/可用代理.txt", 'a', encoding='utf-8') as f:
                f.write(ip_info["ip"] + " " + ip_info["post"] + "\r\n")

        except Exception as e:
            # 代理不可用，在redis中将其删除
            r.delete(i)
            lm.log_info(ip_info["ip"] + ":" + ip_info["post"] + "监测为不可用代理，已删除")


# 获取桌面路径
def get_desktop():
    # 获取注册表值
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 0, win32con.KEY_READ)
    # 返回桌面路径
    return win32api.RegQueryValueEx(key, 'Desktop')[0]


# 开始函数
def startup():
    while True:
        # 开启线程池
        pool = ThreadPoolExecutor(max_workers=20)
        for i in range(20):
            # 多线程运行检查函数
            pool.submit(GetProxyIP)
        # 回收线程池
        pool.shutdown()

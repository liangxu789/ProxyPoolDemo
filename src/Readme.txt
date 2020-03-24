文件结构
-src
    - bin
        - start
            - spiderStart.py   启动程序，获取代理ip
            - checkStart.py    启动检查程序
    - check
        - checkProxyPool       检查代理ip是否可用
    - log
        - logModel 日志模块
    - operate
        - ProxySpiderFirst     代理爬虫
        - ProxySpiderSecond    代理爬虫
        - ProxySpiderThird     代理爬虫
        - ProxySpiderFourth    代理爬虫
    - redisitem
        - RedisOperation       redis操作包
    - tools
        - GetProxyIP           获取代理ip
        - randomCode           随机码
- redis-config                 redis配置文件

操作步骤：
1.如果没有redis，先去安装配置，可参考https://blog.csdn.net/qq_37725650/article/details/79723442进行安装。
2.打开redis的server。在redis根目录中的redis-server.exe文件
3.在redis_config中配置redis，输入ip和端口号
4.先执行bin-start-spiderStart.py文件。运行一段时间后,继续执行bin-start-checkStart.py文件
5.会在桌面显示可用代理，文件内容格式为"ip 端口号"

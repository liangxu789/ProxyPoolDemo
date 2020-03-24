import redis
import redis_config as rc

pool = redis.ConnectionPool(host=rc.HOST, port=rc.POST)

r = redis.Redis(connection_pool=pool)


def setDic(key, value):
    r.hset("proxy_ip", key, value)


def getRedisObj():
    return r


def getDicKeys():
    return r.hkeys("proxy_ip")

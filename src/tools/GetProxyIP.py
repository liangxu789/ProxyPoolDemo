import json
import random
import redisitem.RedisOperation as ro


def GetProxyIP():
    r = ro.getRedisObj()
    i = random.sample(ro.getDicKeys(), 1)[0]
    ip_info = json.loads(r.hget("proxy_ip", i))
    return "http://" + ip_info["ip"] + ":" + ip_info["post"]

from pyquery import PyQuery as pq
import time, json, requests, multiprocessing
import log.logModel as lm
import redisitem.RedisOperation as ro
import tools.randomCode as rc
import tools.GetProxyIP as gip

# 代理网页主页地址
Proxy_url = "http://www.66ip.cn/"

# 浏览器信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.90 Safari/537.36 '
}


#获取网页内容
def get_page_content(url, proxy):
    try:
        if proxy:
            r = requests.get(url, headers=headers, timeout=10, proxies=proxy)
        else:
            r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            lm.log_info("获取" + url + "的页面数据成功")
            return r.text
        else:
            lm.log_warning("获取" + url + "的页面数据失败 正在换代理获取重新获取。。。")
            proxy_list = {
                "http": gip.GetProxyIP(),
            }
            get_page_content(url, proxy_list)
    except:
        lm.log_error(url + "链接错误 取消此次链接")
        get_page_content(url, None)


#获取页码信息
def parse_page_num(url):
    doc = pq(get_page_content(url, None))
    return int(int(doc(".style7 span").text()) / 7)


#循环获取页面信息
def get_html(interval):
    page_num = parse_page_num(Proxy_url)
    for i in range(page_num):
        try:
            new_url = Proxy_url + str(i + 1) + ".html"
            lm.log_info("正在获取" + new_url + "的信息")
            html = get_page_content(new_url, None)
            parse_html(html)
            time.sleep(interval)
        except Exception as e:
            lm.log_error(e.args[0])
            continue

#获取代理，将其存到Redis中
def parse_html(html):
    doc = pq(html.encode('iso-8859-1').decode('gbk'))
    for i in doc("#main table tr"):
        i_html = pq(i)
        result_dic = {"ip": i_html("td").eq(0).text(), "port": i_html("td").eq(1).text()}
        if result_dic["ip"] != "ip":
            result = json.dumps(result_dic)
            ro.setDic(rc.getRandomCode(), result)
            lm.log_info(str(result_dic) + "已经存到Redis中")


def start_up():
    p = multiprocessing.Process(target=get_html, args=(3,))
    p.start()

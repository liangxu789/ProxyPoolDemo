from pyquery import PyQuery as pq
import time, json, requests, multiprocessing
import log.logModel as lm
import redisitem.RedisOperation as ro
import tools.randomCode as rc
import tools.GetProxyIP as gip

Proxy_url = "https://www.xicidaili.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.90 Safari/537.36 '
}

suffix = ['nn', 'nt', 'wn', 'wt', 'qq']


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


def parse_page_num(url):
    doc = pq(get_page_content(url, None))
    return int(doc(".next_page").prev().text())


def get_html(interval):
    for suf in suffix:
        url_joint = Proxy_url + "/" + suf
        page_num = parse_page_num(url_joint)
        for i in range(page_num):
            try:
                new_url = url_joint + "/" + str(i + 1)
                lm.log_info("正在获取" + new_url + "的信息")
                html = get_page_content(new_url, None)
                parse_html(html)
                time.sleep(interval)
            except Exception as e:
                lm.log_error(e.args[0])
                continue


def parse_html(html):
    doc = pq(html)
    for i in doc("#ip_list .odd"):
        i_html = pq(i)
        result_dic = {"ip": i_html("td").eq(1).text(), "port": i_html("td").eq(2).text()}
        result = json.dumps(result_dic)
        ro.setDic(rc.getRandomCode(), result)
        lm.log_info(str(result_dic) + "已经存到Redis中")


def start_up():
    p = multiprocessing.Process(target=get_html, args=(3,))
    p.start()

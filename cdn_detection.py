import dns.resolver as d
import requests as rq,re,time,json
from bs4 import BeautifulSoup

def check_cdn(tar):
    # 目标域名cdn检测
    result = []
    myResolver = d.Resolver()
    myResolver.lifetime = myResolver.timeout = 2.0
    dnsserver = [['114.114.114.114'], ['8.8.8.8'], ['208.67.222.222'],['1.0.0.1']]
    for i in dnsserver:
        myResolver.nameservers = i
        try:
            record = myResolver.query(tar,'A',tcp=True)
            result.append(record[0].address)
        except Exception as e:
            pass
    return True if len(list(result)) > 1 else False

# 构造HTTP请求在线查找DNS: 查询网站：coding.tools   查询DNS：64.6.64.6
def check_from_web_CODEINGTOOLS(url):
    hdr = {
    'authority': 'coding.tools',
    'method': 'POST',
    'path': '/cn/nslookup',
    'scheme': 'https',
    'accept': '*/*',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'content-length': '48',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': ('__cfduid=df6b9245736de542eb4d28bc7f52e14ac1555584535;'
    #           ' _ga=GA1.2.1260195905.1555584528; _gid=GA1.2.839966760.1555584528'),
    'origin': 'https://coding.tools',
    'referer': 'https://coding.tools/cn/nslookup',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'}
    req_data = {
    'queryStr': url,
    'querytype': 'A',
    'dnsserver': '64.6.64.6'}
    request_host = 'https://coding.tools/cn/nslookup'
    response = rq.post(request_host,data=req_data,headers=hdr)
    txt = response.text
    ip_list = None
    try:
        ip_list = find_ip(txt)
    except IndexError:
        print('There is nothing returned from coding.tools')
        return None
    except Exception:
        print('search error')
    return ip_list
    # if len(ip_list)==1:
    #     print("The URL don't use CDN, IP: ",end='')
    #     print(ip_list[0])
    #     return (True , ip_list)
    # else:
    #     print("The URL used CDN: ")
    #     for i in ip_list:
    #         print("IP： ",i)
    #     return (True,ip_list)

# 从在线DNS返回的数据中返回结果：
def find_ip(s):
    com1 = re.compile(r"Name.*",re.S|re.I|re.M)
    com2 = re.compile(r"\d+.\d+.\d+.\d+",re.M)
    s = com1.findall(s,0)[0]
    l = com2.findall(s,0)
    l = list(set(l))
    return l
if __name__ == '__main__':
    d1,d2,d3,d4,d5 = '8.8.8.8','208.67.222.222','9.9.9.9','209.244.0.3','64.6.64.6'
    co = []
    t1 = time.time()
    u1 = 'xusy2333.cn'
    print(u1)
    check_from_web_CODEINGTOOLS(u1)
    t2 = time.time()
    co.append([d1,t2-t1])
    print(t2-t1)
    # check_from_web_CODEINGTOOLS(u1,d2)
    # t3 = time.time()
    # co.append([d2,t3-t2])
    # print(t3-t2)
    # check_from_web_CODEINGTOOLS(u1,d3)
    # t4 = time.time()
    # co.append([d3,t4-t3])
    # print(t4-t3)
    # check_from_web_CODEINGTOOLS(u1,d4)
    # t5 = time.time()
    # co.append([d4,t5-t4])
    # print(t5-t4)
    # check_from_web_CODEINGTOOLS(u1,d5)
    # t6 = time.time()
    # co.append([d5,t6-t5])
    # print(t6-t5)
    # for i in co:
    #     print(i)
    # print(check_cdn(u1))
    # t3 = time.time()
    # print(t3-t2)
    # u2 = 'douban.com'
    # check_from_web_CODEINGTOOLS(u2)
    # u3 = 'xusy2333.cn'
    # check_from_web_CODEINGTOOLS(u3)
# # # # # coding:utf-8
# # # # import socket
# # # # import struct
# # # # import time
# # # # import os
# # # # import select
# # # #
# # # # ICMP_ECHO_REQUEST = 8
# # # # '''
# # # # 校验和
# # # # 在ip中只校验20字节的ip报头
# # # #                 icmp 校验 校验整个报文（报头加上数据）
# # # # 校验和计算：
# # # #         发送数据时；
# # # #                 1 把校验和字段设置为0
# # # #                 2 把需要校验的数据看成16位为单位的数字 依次进行二进制反码求和
# # # #                 3 得到结果
# # # # '''
# # # #
# # # #
# # # # def checksum(source_string):
# # # #     sum = 0
# # # #     countTo = (len(source_string) / 2) * 2
# # # #     # 首先计算字符串的长度
# # # #     count = 0
# # # #     while count < countTo:
# # # #         thisVal = ord(source_string[count + 1]) * 256 + ord(source_string[count])
# # # #         sum = sum + thisVal
# # # #         sum = sum & 0xffffffff
# # # #         count = count + 2
# # # #     if countTo < len(source_string):
# # # #         sum = sum + ord(source_string[len(source_string) - 1])
# # # #         sum = sum & 0xffffffff
# # # #     sum = (sum >> 16) + (sum & 0xffff)
# # # #     sum = sum + (sum >> 16)
# # # #     answer = ~sum
# # # #     answer = answer & 0xffff
# # # #     answer = answer >> 8 | (answer << 8 & 0xff00)
# # # #     return answer
# # # #
# # # #
# # # # def send_ping(my_socket, dest_addr, id):
# # # #     header = struct.pack("bbHHh", 8, 0, 0, id, 1)
# # # #     # 构造一个空的头
# # # #     webtime = struct.pack("d", time.time())
# # # #     # 增加发送时间戳 作为icmp的data
# # # #
# # # #     '''
# # # #     关于计算目的主机和源主机数据传送的时间： echo-request 构造的数据包中添加时间戳，
# # # #     echo-reply 返回数据 解包后得到time  计算时间差
# # # #     '''
# # # #
# # # #     data = webtime
# # # #     chksum = checksum(header + data)
# # # #     # icmp 的检验和是检验头部和数据域的 区别与ip检验和
# # # #     header = struct.pack("bbHHh", 8, 0, socket.htons(chksum), id, 1)
# # # #     # 把16位正整数从主机字节序转换成网络序 socket.htons()
# # # #     # 1>Unix系统在实现ping程序时把ICMP报文中的标识符字段置成发送进程的ID号。这样即使在同一台主机上同时运行了多个ping程序实例，ping程序也可以识别出返回的信息。
# # # #     # 2>序列号从0开始，每发送一次新的回显请求就加1。ping程序打印出返回的每个分组的序列号，允许我们查看是否有分组丢失，失序或重复。.
# # # #
# # # #     packet = header + data
# # # #     my_socket.sendto(packet, (dest_addr, 1))
# # # #     # socket.sendto(string, address)
# # # #
# # # #
# # # # def recive_ping(my_socket, id, timeout):
# # # #     timeleft = timeout
# # # #     while True:
# # # #         startedselect = time.time();
# # # #         # select.select(rlist, wlist, xlist[, timeout])
# # # #         whatnow = select.select([my_socket], [], [], timeleft)
# # # #         time_select = (time.time() - startedselect)
# # # #         if whatnow[0] == []:
# # # #             return
# # # #         time_receive = time.time()
# # # #         recvpacket, addr = my_socket.recvfrom(1024)
# # # #         icmpheader = recvpacket[20:28]
# # # #         # 一个ICMP报文包括IP头部（20字节）、ICMP头部（8字节）前20个字节是ip头部
# # # #         type, code, checknum, ID, sequence = struct.unpack("bbHHh", icmpheader)
# # # #         if ID == id:
# # # #             time_sent = struct.unpack("d", recvpacket[28:])[0]
# # # #             return time_receive - time_sent
# # # #         time_out = timeleft - time_select
# # # #         if time_out >= 0:
# # # #             return
# # # #
# # # #
# # # # def do(dest_addr, timeout=2):
# # # #     icmp = socket.getprotobyname("icmp")
# # # #
# # # #     s = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
# # # #     id = os.getpid()
# # # #     send_ping(s, dest_addr, id)
# # # #     delay = recive_ping(s, id, timeout)
# # # #     print
# # # #     " get ping in %0.4fms" % delay
# # # #
# # # #
# # # # if __name__ == '__main__':
# # # #     do('192.168.1.1')
# # # # # [p = 30, 2, left]
# # # # import socket,struct
# # # # s = socket.ntohs(0x0800)
# # # # print(s,type(s))
# # # # s = b'asd111'
# # # # pkt = struct.pack('6s',s)
# # # # print(pkt,type(pkt))
# # # # un = struct.unpack(str(len(pkt))+'s',pkt)
# # # # print(un,type(un))
# # # #
# # # # import time
# # # # print(time.get_clock_info('time'))
# # # # print(time.gmtime())
# # # # print(time.localtime())
# # # # print()
# # # # t = time.ctime()
# # # # print(t)
# # # # print(42*'2')
# # # # t = '-'.join(t.split())
# # # # # yy = time.
# # # # # t = t.join('-')
# # # # print(t)
# # # # t = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
# # # # print(t)
# # #
# # # # s ="|{:^12s}|{:15s}|{:20s}|".format('port','status','service')
# # # # print(51*'-')
# # # # print(s)
# # # # r = [[1,'open'],[3,'open|filtered']]
# # # # for i in r:
# # # #     print("|{:^12s}|{:15s}|{:20}|".format(str(i[0]),i[1],20*' '))
# # # # print(51*'-')
# # #
# # # import stackless,time
# # # lis = []
# # # def show(i):
# # #     global lis
# # #     print(111)
# # #     lis.append(i)
# # #
# # # def calc(i):
# # #     # a,b,c = 0,0,1
# # #     if i in (0,1):
# # #         return i
# # #     else:
# # #         return calc(i-2)+calc(i-1)
# # # # def arr(max):
# # # #     lis = []
# # #
# # # def run_and_add_result(result,task):
# # #     pass
# # # t = time.time()
# # #
# # # # stackless.tasklet(show)(2)
# # # # stackless.tasklet(show)(3)
# # # # stackless.run()
# # # print(calc(20))
# # # # print(lis)
# # # t1 = time.time()
# # # print('time',t1-t)
# # #
# # # import socket
# # # raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
# # # raw_socket.close()
# # #
# # # import stackless as st,socket
# # #
# # # a = [12]
# # # result = []
# # # def get_host_ip():
# # #     try:
# # #         ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # #         ss.connect(('8.8.8.8', 80))
# # #         ip = ss.getsockname()[0]
# # #     finally:
# # #         ss.close()
# # #     return str(ip)
# # # #
# # # # def rcv_again(s,addr):
# # # #     try:
# # # #         s.connect(addr)
# # #
# # # def try_rcv(addr):
# # #     global result
# # #     s = socket.socket()
# # #     s.settimeout(0.005)
# # #     # tar = (ip, port)
# # #     try:
# # #         s.connect(addr)
# # #     except socket.timeout:
# # #         result.append([addr[1], 'close|filtered'])
# # #     except Exception:
# # #         result.append([addr[1], 'close'])
# # #     else:
# # #         result.append([addr[1], 'open'])
# # #     finally:
# # #         s.close()
# # #     return result
# # #
# # # chnl = st.channel()
# # #
# # # def show(i,a):
# # #     global eg
# # #     # print(i,st.current,chnl.queue)
# # #     val = chnl.receive()
# # #     if val[0] == -1:
# # #         pass
# # #     elif val[0] != i:
# # #         print(i,'send')
# # #         chnl.send(val)
# # #     else:
# # #         print(val[1])
# # #         chnl.send((-1,123))
# # #         # return
# # #     if i == 1:
# # #         chnl.send((3,123))
# # #     a += [i]
# # #     print('now: ',i,st.current)
# # #
# # # eg = None
# # # for i in range(5):
# # #     if i == 1:
# # #         eg = st.tasklet(show)(i, a)
# # #         continue
# # #     st.tasklet(show)(i,a)
# # # st.tasklet(chnl.send((3,123)))
# # # st.run()
# # # print(chnl.queue)
# # # print(a)
# #
# # # from syn_scan import *
# # # from tcp_scan import *
# # # from udp_scan import *
# # # import stackless as stk
# # # import socket,time
# # #
# # # st_result = []
# # # send_chnl = stk.channel()
# # # rcvd_chnl = stk.channel()
# # #
# # # def udp_stk(des_ip,portlis):
# # #     pre_port = None
# # #
# # #     while portlis and pre_port != -1:
# # #         temp = portlis.pop(0)
# # #         pre_port = temp
# # #         src_addr = send_udp_pkt((des_ip,temp))
# # #         send_chnl.send(src_addr)
# # #
# # #         if not portlis:
# # #             pre_port = -1
# # #
# # # def manage_rcv(des_ip):
# # #     pass
# # #
# # #
# # #
# # #
# # # def oo(i):
# # #     print('i: ',i)
# # #     stk.schedule()
# # #     print('oo')
# # #
# # # import socket
# # # ip = '123.9.9'
# # # print(socket.inet_ntoa(socket.inet_aton(ip)))
# # # print('\x1b[5;31;48m' + 'Success!' + '\x1b[0m')
# # # print('\x1b[5;33;48m' + 'Success!' + '\x1b[0m')
# #
# # import dns.resolver as d
# # # CDN检测结果存在不确定性，函数中只要4个权威DNS得到同样的结果就说明不存在CDN，
# # # 而实际上每次检测结果不同，所以： 域名存在CDN   是   函数检测出CDN 的必要不充分条件
# # # 函数中有国外权威DNS，但也只是提高了成功率
# #
# # def check_cdn(tar):
# #     # 目标域名cdn检测
# #     result = []
# #     myResolver = d.Resolver()
# #     myResolver.lifetime = myResolver.timeout = 2.0
# #     dnsserver = [['114.114.114.114'], ['8.8.8.8'], ['208.67.222.222'],['1.0.0.1']]
# #     for i in dnsserver:
# #         myResolver.nameservers = i
# #         try:
# #             record = myResolver.query(tar,'A',tcp=True)
# #             result.append(record[0].address)
# #         except Exception as e:
# #             pass
# #     result = set(result)
# #     print(result)
# #     return True if len((result)) > 1 else False
# #
# # a = check_cdn('baidu.com')
# # b = check_cdn('xusy2333.cn')
# # c = check_cdn('tsjjfzgs.com')
# # print(a,b,c)
# import json
#
# req_data = {
# 'queryStr': 'baidu.com',
# 'querytype': 'A',
# 'dnsserver': '8.8.8.8'}
#
# # s = json.dumps(req_data)
# # variables2=json.loads(s)
# # assert(req_data==variables2)
# # print(type(req_data))
# # def dict_to_binary(the_dict):
# #     str = json.dumps(the_dict)
# #     binary = ' '.join(format(ord(letter), 'b') for letter in str)
# #     binary = bytes(binary,encoding='utf-8')
# #     return binary
# # b = dict_to_binary(req_data)
# # print(type(b),b)
#
# # import re
# # def find_ip(s):
# #     com1 = re.compile(r"Name.*",re.S|re.I|re.M)
# #     com2 = re.compile(r"\d+.\d+.\d+.\d+",re.M)
# #     s = com1.findall(s,0)[0]
# #     l = com2.findall(s,0)
# #     l = list(set(l))
# #     return l
# #
# # d = '''Server:		8.8.8.8
# # Address:	8.8.8.8#53
# #
# # Non-authoritative answer:
# # Name:	baidu.com
# # Address: 220.181.57.216
# # Name:	baidu.com
# # Address: 220.181.57.22
# # Name:	baidu.com
# # Address: 220.181.57.216
# # Name:	baidu.com
# # Address: 123.125.114.144'''
# # print(d)
# # lis = find_ip(d)
# # s = '/edit\r\n'
# # s = s[:-2]
# # print(s)
#
# # import re
# #
# #
# # t = '''Domain Name: xusy2333.cn
# # ROID: 20180416s10001s00371092-cn
# # Domain Status: ok
# # Registrant ID: hc9936152222575
# # Registrant: 徐诗瑶
# # Registrant Contact Email: xu_sy11111@mail.dlut.edu.cn
# # Sponsoring Registrar: 阿里云计算有限公司（万网）
# # Name Server: dns29.hichina.com
# # Name Server: dns30.hichina.com
# # Registration Time: 2018-04-16 20:33:59
# # Expiration Time: 2020-04-16 20:33:59
# # DNSSEC: unsigned
# # '''
# #
# # # hsname = re.compile(r".*Registrant:.*",re.M|re.I).findall(t,0)[0][12:]
# # host_name = re.compile(r".*Registrant:.*",re.M|re.I).findall(t,0)[0]
# # host_name = host_name[host_name.index(':')+2:]
# # print(host_name)
# # name1 = re.compile(r".*Registrant Contact Email:.*",re.M|re.I).findall(t,0)[0]
# # print(name1)
# #
# # domain_status = re.compile(r".*Domain Status:.*",re.M|re.I).findall(t,0)[0]
# # host_email = re.compile(r".*Registrant Contact Email:.*",re.M|re.I).findall(t,0)[0]
# # company = re.compile(r".*Sponsoring Registrar:.*",re.M|re.I).findall(t,0)[0]
# # reg_time = re.compile(r".*Registrant Contact Email:.*",re.M|re.I).findall(t,0)[0]
# # exp_time = re.compile(r".*Registrant Contact Email:.*",re.M|re.I).findall(t,0)[0]
# #
# # s = 'sd:sd'
# # print(s[s.index(':')+1:])
# #
#
# import re
#
# s =  '''
# <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
# <html>
#  <head>
#   <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
#   <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
#   <title>
#    runoob.com的Whois信息 - 站长工具
#   </title>
#   <meta content="whois,whois查询,whois信息查询,whois查询工具,域名whois,域名whois查询,域名注册信息查询" name="keywords">
#    <meta content="站长之家-站长工具提供whois查询工具，汉化版的域名whois查询工具。" name="description"/>
#    <script>
#     var jsurlbase = '//csstools.chinaz.com/tools/js';
#         var imgurlbase = '//csstools.chinaz.com/tools/images';
#         var styleurlbase = '//csstools.chinaz.com/tools/styles';
#    </script>
#    <script src="//csstools.chinaz.com/common/js/mobilepage.js?v=201702" type="text/javascript">
#    </script>
#    <link href="//csstools.chinaz.com/common/styles/all-base.css?v=201803" rel="stylesheet" type="text/css"/>
#    <link href="//csstools.chinaz.com/common/styles/publicstyle.css?v=201902" rel="stylesheet" type="text/css"/>
#    <script src="//csstools.chinaz.com/common/js/jquery-1.11.3.min.js" type="text/javascript">
#    </script>
#    <script src="//csstools.chinaz.com/common/js/jq-public.js?v=201708" type="text/javascript">
#    </script>
#    <script src="//csstools.chinaz.com/common/layer/layer.js?v=201801" type="text/javascript">
#    </script>
#    <script src="//csstools.chinaz.com/tools/js/member.js?v=201803" type="text/javascript">
#    </script>
#    <!--[if IE 6]>
#     <script type="text/javascript" src="//csstools.chinaz.com/common/js/DD_belatedPNG.js"></script>
#     <script>    DD_belatedPNG.fix('*');</script>
#     <![ENDIF]-->
#    <link href="//csstools.chinaz.com/whois/styles/whoisstyle.css" rel="stylesheet" type="text/css">
#    </link>
#   </meta>
#  </head>
#  <body>
#   <!--top-public-begin-->
#   <div class="ww100">
#    <!--ToolTop-begin-->
#    <div class="ToolTop bor-b1s clearfix">
#     <div class="wrapper02 SimSun">
#      <ul class="TnavList pr zI52" id="menu">
#       <li class="def">
#        <a class="def" href="//www.chinaz.com">
#         <span>
#          站长之家
#         </span>
#        </a>
#       </li>
#       <li class="tdrap">
#        <a href="//tool.chinaz.com" target="_blank">
#         <span>
#          站长工具
#         </span>
#         <i class="corner icon">
#         </i>
#        </a>
#        <p class="tdrap-on">
#         <a href="//alexa.chinaz.com" target="_blank">
#          ALEXA排名查询
#         </a>
#         <a href="//rank.chinaz.com" target="_blank">
#          百度权重查询
#         </a>
#         <a href="//seo.chinaz.com" target="_blank">
#          SEO概况查询
#         </a>
#         <a href="//link.chinaz.com" target="_blank">
#          友情链接查询
#         </a>
#         <a href="//pr.chinaz.com" target="_blank">
#          Google PR查询
#         </a>
#         <a href="//whois.chinaz.com" target="_blank">
#          Whois信息查询
#         </a>
#         <a href="//icp.chinaz.com" target="_blank">
#          域名备案查询
#         </a>
#        </p>
#       </li>
#       <li class="tdrap">
#        <a href="http://sc.chinaz.com" target="_blank">
#         <span>
#          站长素材
#         </span>
#         <i class="corner icon">
#         </i>
#        </a>
#        <p class="tdrap-on">
#         <a href="//font.chinaz.com/" target="_blank">
#          字体下载
#         </a>
#         <a href="//desk.chinaz.com/" target="_blank">
#          高清壁纸
#         </a>
#         <a href="//sc.chinaz.com/jianli/" target="_blank">
#          简历模板
#         </a>
#         <a href="//sc.chinaz.com/tupian/" target="_blank">
#          高清图片
#         </a>
#         <a href="//sc.chinaz.com/shiliang/" target="_blank">
#          矢量素材
#         </a>
#         <a href="//sc.chinaz.com/ppt/" target="_blank">
#          PPT模板
#         </a>
#         <a href="//sc.chinaz.com/psd/" target="_blank">
#          PSD素材
#         </a>
#        </p>
#       </li>
#       <li class="def">
#        <a href="//down.chinaz.com" target="_blank">
#         <span>
#          源码下载
#         </span>
#        </a>
#       </li>
#       <li class="tdrap">
#        <a href="//top.chinaz.com" target="_blank">
#         <span>
#          网站排行
#         </span>
#         <i class="corner icon">
#         </i>
#        </a>
#        <p class="tdrap-on">
#         <a href="//top.chinaz.com/hangye/" target="_blank">
#          行业网站排名
#         </a>
#         <a href="//top.chinaz.com/diqu/" target="_blank">
#          地区网站排名
#         </a>
#         <a href="//alexa.chinaz.com/Global/" target="_blank">
#          全球网站排名
#         </a>
#         <a href="//top.chinaz.com/waptop/" target="_blank">
#          移动网站排名
#         </a>
#         <a href="//top.chinaz.com/gongsi/" target="_blank">
#          公司排行榜
#         </a>
#         <a href="//live.chinaz.com/" target="_blank">
#          直播排行榜
#         </a>
#        </p>
#       </li>
#       <li class="def">
#        <a href="//aso.chinaz.com/" target="_blank">
#         <span>
#          APP榜单
#         </span>
#        </a>
#       </li>
#       <li class="tdrap">
#        <a class="Tnone" href="javascript:mobilepage();">
#         <span>
#          手机版
#         </span>
#         <i class="corner icon">
#         </i>
#        </a>
#        <p class="tdrap-on">
#         <img src="//csstools.chinaz.com/tools/images/mtool.chinaz.com.qrcode.png"/>
#        </p>
#       </li>
#       <li class="def">
#        <a href="//zj.chinaz.com/" target="_blank">
#         <span>
#          SEO中介
#         </span>
#        </a>
#       </li>
#       <li class="def">
#        <a href="//old.tool.chinaz.com/" target="_blank">
#         <span>
#          工具旧版
#         </span>
#        </a>
#       </li>
#       <li class="def">
#        <a class="sNew" href="//tool.chinaz.com/soft" target="_blank">
#         <span>
#          SEO工具包
#         </span>
#        </a>
#       </li>
#      </ul>
#      <div class="fr TrigW" id="chinaz_topbar">
#      </div>
#     </div>
#    </div>
#    <!--ToolTop-end-->
#    <!--ToolHead-begin-->
#    <div class="ToolHead">
#     <div class="wrapper clearfix">
#      <h1 class="ToolLogo fl">
#       <a href="/">
#        <img src="//csstools.chinaz.com/tools/images/public/logos/logo-whois.png"/>
#       </a>
#      </h1>
#      <div class="fr topTsRight ml10" id="topTxt">
#      </div>
#      <div class="fr topTsCenter">
#       <script src="//stats.chinaz.com/gj_g/tool_468.js" type="text/javascript">
#       </script>
#      </div>
#     </div>
#    </div>
#    <!--ToolHead-end-->
#    <!--ToolNavbar-begin-->
#    <div class="ToolNavbar" id="ToolNav">
#     <div class="navbar-bg">
#      <div class="navbar-bg-top">
#       <div class="navbar-content pr">
#        <div class="navbar-content-box">
#         <div class="wrapper02 clearfix" id="Navbar">
#          <ul class="w114">
#           <li class="dt">
#            <a href="http://tool.chinaz.com">
#             首页
#            </a>
#           </li>
#           <li class="dd">
#            <a href="//api.chinaz.com" target="_blank">
#             站长数据API
#            </a>
#            <a href="//aso.chinaz.com" target="_blank">
#             APP榜单监控
#            </a>
#            <a href="//zj.chinaz.com" target="_blank">
#             SEO优化中介
#            </a>
#            <a href="//cdn.chinaz.com" target="_blank">
#             CDN云观测
#            </a>
#           </li>
#          </ul>
#          <ul class="odd">
#           <li class="dt">
#            <a href="http://ip.tool.chinaz.com">
#             域名/IP类
#            </a>
#           </li>
#           <li class="dd">
#            <a href="http://tool.chinaz.com/DomainDel/" target="_blank">
#             域名到期查询
#            </a>
#            <a href="http://del.chinaz.com" target="_blank">
#             过期域名查询
#            </a>
#            <a href="http://whois.chinaz.com" target="_blank">
#             WHOIS查询
#            </a>
#            <a href="http://ip.tool.chinaz.com" target="_blank">
#             IP 查询
#            </a>
#            <a href="http://ip.tool.chinaz.com/Same/" target="_blank">
#             同IP网站查询
#            </a>
#            <a href="http://tool.chinaz.com/dns/" target="_blank">
#             DNS查询
#            </a>
#           </li>
#          </ul>
#          <ul class="both">
#           <li class="dt">
#            <a href="http://icp.chinaz.com">
#             网站信息查询
#            </a>
#           </li>
#           <li class="dd">
#            <a class="rig" href="http://alexa.chinaz.com" target="_blank">
#             Alexa排名
#            </a>
#            <a href="http://icp.chinaz.com" target="_blank">
#             网站备案查询
#            </a>
#            <a class="rig" href="http://tool.chinaz.com/webdetect/" target="_blank">
#             网页检测
#            </a>
#            <a href="http://tool.chinaz.com/pagestatus/" target="_blank">
#             HTTP状态查询
#            </a>
#            <a class="rig" href="http://tool.chinaz.com/Tools/pagecode.aspx" target="_blank">
#             查看网页源代码
#            </a>
#            <a href="http://tool.chinaz.com/tools/robot.aspx" target="_blank">
#             机器人模拟抓取
#            </a>
#            <a class="rig" href="http://tool.chinaz.com/robots/" target="_blank">
#             robots.txt生成
#            </a>
#            <a href="http://mobile.chinaz.com/fiturl_baidu.html" target="_blank">
#             移动适配生成
#            </a>
#            <a class="rig" href="http://tool.chinaz.com/sitespeed" target="_blank">
#             网站速度测试
#            </a>
#            <a href="http://ping.chinaz.com/" target="_blank">
#             ping测试
#            </a>
#            <a class="rig" href="http://mobile.chinaz.com/" target="_blank">
#             Wap适配
#            </a>
#            <a href="http://tool.chinaz.com/Gzips/" target="_blank">
#             网站GZIP压缩
#            </a>
#           </li>
#          </ul>
#          <ul class="both">
#           <li class="dt">
#            <a href="http://seo.chinaz.com">
#             SEO查询
#            </a>
#           </li>
#           <li class="dd">
#            <a class="rig" href="http://seo.chinaz.com" target="_blank">
#             SEO综合查询
#            </a>
#            <a href="http://wapseo.chinaz.com" target="_blank">
#             移动SEO查询
#            </a>
#            <a class="rig" href="http://link.chinaz.com" target="_blank">
#             友情链接检测
#            </a>
#            <a href="http://outlink.chinaz.com" target="_blank">
#             反链查询
#            </a>
#            <a class="rig" href="http://tool.chinaz.com/shoulu/" target="_blank">
#             收录查询
#            </a>
#            <a href="http://tool.chinaz.com/baidu/metadig.aspx" target="_blank">
#             META信息挖掘
#            </a>
#            <a class="rig" href="http://pr.chinaz.com" target="_blank">
#             PR查询
#            </a>
#            <a href="http://tool.chinaz.com/kws/" target="_blank">
#             关键词排名查询
#            </a>
#            <a class="rig" href="http://tool.chinaz.com/baidu/words.aspx" target="_blank">
#             关键词挖掘
#            </a>
#            <a href="http://tool.chinaz.com/kwevaluate" target="_blank">
#             关键词优化分析
#            </a>
#            <a class="rig" href="http://tool.chinaz.com/websitepk.aspx" target="_blank">
#             竞争网站分析
#            </a>
#            <a href="http://tool.chinaz.com/seocheck" target="_blank">
#             SEO优化建议
#            </a>
#           </li>
#          </ul>
#          <ul class="odd">
#           <li class="dt">
#            <a class="pr" href="http://rank.chinaz.com/all">
#             权重查询
#             <span class="ico-navNew pa">
#             </span>
#            </a>
#           </li>
#           <li class="dd">
#            <a href="http://rank.chinaz.com" target="_blank">
#             百度权重查询
#            </a>
#            <a href="http://rank.chinaz.com/baidumobile" target="_blank">
#             百度移动权重查询
#            </a>
#            <a href="http://rank.chinaz.com/sorank" target="_blank">
#             360权重查询
#            </a>
#            <a href="http://rank.chinaz.com/rank360" target="_blank">
#             360移动权重查询
#            </a>
#            <a href="http://index.chinaz.com/bid" target="_blank">
#             关键词推广创意查询
#            </a>
#            <a href="http://index.chinaz.com/" target="_blank">
#             关键词指数
#            </a>
#           </li>
#          </ul>
#          <ul class="odd">
#           <li class="dt">
#            <a href="http://tool.chinaz.com/map.aspx">
#             辅助工具
#            </a>
#           </li>
#           <li class="dd">
#            <a href="http://tool.chinaz.com/Tools/textencrypt.aspx" target="_blank">
#             加密解密
#            </a>
#            <a href="http://tool.chinaz.com/Tools/Unicode.aspx" target="_blank">
#             编码转换
#            </a>
#            <a href="http://tool.chinaz.com/Tools/JsCodeConfusion.aspx" target="_blank">
#             压缩格式化
#            </a>
#            <a href="http://tool.chinaz.com/Tools/onlinecolor.aspx" target="_blank">
#             配色工具
#            </a>
#            <a href="http://tool.chinaz.com/Tools/unixtime.aspx" target="_blank">
#             Unix时间戳
#            </a>
#            <a href="http://tool.chinaz.com/Tracert/" target="_blank">
#             路由器追踪
#            </a>
#           </li>
#          </ul>
#         </div>
#        </div>
#       </div>
#      </div>
#     </div>
#    </div>
#    <!--ToolNavbar-end-->
#    <div class="wrapper02 ptb10 ToolsWrapIM clearfix" id="navAfter">
#    </div>
#    <div class="Map-navbar wrapper mb10 clearfix">
#     <div class="Mnav-left fl">
#      当前位置：
#      <a href="http://tool.chinaz.com/">
#       站长工具
#      </a>
#      &gt;
#      <a href="http://whois.chinaz.com/">
#       Whois查询
#      </a>
#     </div>
#     <div class="Mnav-right02 fr" id="loc">
#     </div>
#    </div>
#   </div>
#   <!--top-public-end-->
#   <style>
#    .verif-wrap{ height:40px;}
#     .verif-wrap .verif-txt{ line-height:40px; height:40px;color: #c0c1c4;}
#
#     .verif-wrap .verif-cont{ padding:5px; _padding:0px;height:28px;line-height:28px; _height:28px;_line-height:28px; color:#56688a; width:84px; font-size:14px;}
#     .verif-wrap .verif-cont,.verif-wrap .verif-img{ border:1px solid #c6cede; display:inline-block; float:left; margin-right:10px; }
#     .verif-wrap .verif-img{ height:32px; cursor:pointer;}
#     .verif-wrap .verif-img span#loadimgtxt{ display:inline-block; float:left; padding-left: 5px; line-height:32px;}
#     .verif-wrap .verif-img img{ max-height:32px; display:inline-block; float:left; min-width: 100%;}
#     .verif-wrap .verif-img a{ display:inline-block; padding:10px 10px 0px 10px; float:right;}
#     .verif-hint{font-size:14px; color:#c0c1c4; position:absolute; left:10px;letter-spacing:normal; font-weight:normal; z-index:0; top:7px;}
#   </style>
#   <!--Tool-MainWrap-begin-->
#   <div class="Tool-MainWrap wrapper pr">
#    <a class="viptag" href="//my.chinaz.com/toolvip/vip" target="_blank">
#    </a>
#    <p class="ClassHead-wrap clearfix">
#     <a class="CHeadcur ml15" href="javascript:">
#      whois查询
#     </a>
#     <a class="rev" href="/suffix">
#      最新注册
#     </a>
#     <a href="/reverse?ddlSearchMode=1&amp;host=DomainAbuse@service.aliyun.com">
#      邮箱反查
#     </a>
#     <a href="/reverse?ddlSearchMode=2&amp;host=">
#      注册人反查
#     </a>
#     <a href="/reverse?ddlSearchMode=3&amp;host=95187">
#      电话反查
#     </a>
#     <a href="/reverse?ddlSearchMode=0">
#      域名批量反查
#     </a>
#     <!--<a href="http://www.juming.com/?tt=126777" target="_blank"class="col-red">域名抢注</a>-->
#     <a class="col-red" href="http://www.juming.com/regym.htm?tt=126777" target="_blank">
#      域名注册
#     </a>
#     <a href="/reverse?ddlSearchMode=4&amp;host=runoob.com">
#      历史查询
#     </a>
#     <a class="rev" href="/gblsuf">
#      全球域名后缀
#     </a>
#    </p>
#    <div class="DelHeadWrap bor-b1s04">
#     <!--PingSearch-begin-->
#     <div class="publicSearch w570 auto">
#      <form action="/aspx/_default.aspx.cs" autocomplete="off" method="post">
#       <div class="search-write-wrap clearfix pr">
#        <span class="search-write-left pr">
#         <input class="search-write-cont w460 WrapHid" id="DomainName" name="DomainName" type="text" url="true" value="runoob.com"/>
#         <a class="quickdelete _CentHid" href="javascript:" title="清空">
#         </a>
#         <b class="search-hint CentHid" style="display:none">
#          请输入网址，例如：chinaz.com
#         </b>
#        </span>
#        <input id="ws" name="ws" type="hidden" value="grs-whois.hichina.com"/>
#        <span class="search-write-right">
#         <input class="search-write-btn" type="submit" value="查询"/>
#        </span>
#        <div class="BomreWa" id="history-box">
#         <div class="BomreWrap">
#          <a class="IMSearBtn ml10 lh40 tdbone" href="javascript:" id="selecthis">
#           查询记录
#           <i class="corner icon">
#           </i>
#          </a>
#          <div class="Bomrecord" id="selecthis-box" style="display: none">
#           <div class="BomCor-arrow">
#            <em>
#             ◆
#            </em>
#            <i>
#             ◆
#            </i>
#           </div>
#           <div class="BomreList">
#           </div>
#          </div>
#         </div>
#        </div>
#       </div>
#      </form>
#     </div>
#     <!--PingSearch-end-->
#    </div>
#    <!--IcpMain02-begin-->
#    <div class="IcpMain02">
#     <div class="WhoisWrap clearfix">
#      <div class="whoisl-wrap fl">
#       <div class="WhoisHead fwnone">
#        <p class="Titleft YaHei col-gray03 fl">
#         域名
#         <i class="plr5 col-blue02">
#          <a href="http://www.runoob.com" rel="nofollow" target="_blank">
#           runoob.com
#          </a>
#         </i>
#         的信息
#         <span class="fz12 col-gray04 plr5">
#          以下信息更新时间：2019-04-20 13:16:03
#         </span>
#         <a class="fz12 mt10" href="/?Domain=runoob.com&amp;isforceupdate=1&amp;ws=grs-whois.hichina.com">
#          立即更新
#         </a>
#        </p>
#        <a class="getapi fr mt5" href="//api.chinaz.com/ApiDetails/Whois" style="" target="_blank">
#         获取API
#        </a>
#       </div>
#       <ul class="WhoisLeft" id="sh_info">
#        <li class="bor-b1s LI7">
#         <div class="fl WhLeList-left h64">
#          <span class="pt10 dinline">
#           域名
#          </span>
#         </div>
#         <div class="fr WhLeList-right">
#          <p class="h30 bor-b1s02">
#           <a class="col-gray03 fz18 pr5" href="http://runoob.com" rel="nofollow" target="_blank">
#            runoob.com
#           </a>
#           <a href="reverse?host=runoob.com&amp;ddlSearchMode=0" target="_blank">
#            [whois 反查]
#           </a>
#           <a class="fr col-red" href="//kf.tool.chinaz.com?host=runoob.com" target="_blank">
#            申请删除隐私
#           </a>
#          </p>
#          <p class="OtherSuf">
#           <span>
#            其他常用域名后缀查询：
#           </span>
#           <a href="/?DomainName=runoob.cn" target="_blank">
#            cn
#           </a>
#           <a href="/?DomainName=runoob.com" target="_blank">
#            com
#           </a>
#           <a href="/?DomainName=runoob.cc" target="_blank">
#            cc
#           </a>
#           <a href="/?DomainName=runoob.net" target="_blank">
#            net
#           </a>
#           <a href="/?DomainName=runoob.org" target="_blank">
#            org
#           </a>
#          </p>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s">
#         <div class="fl WhLeList-left">
#          注册商
#         </div>
#         <div class="fr WhLeList-right">
#          <div class="block ball">
#           <span>
#            Alibaba Cloud Computing (Beijing) Co., Ltd
#           </span>
#          </div>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s bg-list">
#         <div class="fl WhLeList-left">
#          联系邮箱
#         </div>
#         <div class="fr WhLeList-right block ball lh24">
#          <span>
#           DomainAbuse@service.aliyun.com
#          </span>
#          <a href="/reverse?host=DomainAbuse@service.aliyun.com&amp;ddlSearchMode=1" target="_blank">
#           [whois反查]
#          </a>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s">
#         <div class="fl WhLeList-left">
#          联系电话
#         </div>
#         <div class="fr WhLeList-right block ball lh24">
#          <span>
#           95187
#          </span>
#          <a href="/reverse?host=95187&amp;ddlSearchMode=3" target="_blank">
#           [whois反查]
#          </a>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s bg-list">
#         <div class="fl WhLeList-left">
#          创建时间
#         </div>
#         <div class="fr WhLeList-right">
#          <span>
#           2015年06月23日
#          </span>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s">
#         <div class="fl WhLeList-left">
#          过期时间
#         </div>
#         <div class="fr WhLeList-right">
#          <span>
#           2019年06月23日
#          </span>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s bg-list">
#         <div class="fl WhLeList-left">
#          域名服务器
#         </div>
#         <div class="fr WhLeList-right">
#          <span>
#           grs-whois.hichina.com
#          </span>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s">
#         <div class="fl WhLeList-left">
#          DNS
#         </div>
#         <div class="fr WhLeList-right">
#          vip1.alidns.com
#          <br/>
#          vip2.alidns.com
#          <br/>
#         </div>
#        </li>
#        <li class="clearfix bor-b1s bg-list">
#         <div class="fl WhLeList-left">
#          状态
#         </div>
#         <div class="fr WhLeList-right clearfix">
#          <p class="lh30 pr tip-sh">
#           <span>
#            域名普通状态(
#            <a href="http://www.icann.org/epp#ok" rel="nofollow" target="_blank">
#             ok
#            </a>
#            )
#           </span>
#           <i class="QhintCent autohide">
#            可正常使用。没有需要立即进行的操作，也没有设置任何保护措施。当有其他状态时，OK状态不显示，但并不代表不正常
#           </i>
#          </p>
#         </div>
#        </li>
#        <li class="tc h30 lh30 fz14 col-blue02 bor-b1s flag">
#         -------站长之家
#         <a href="http://whois.chinaz.com">
#          Whois查询
#         </a>
#         --------
#        </li>
#        <li class="clearfix bg-list pt15">
#         <p class="MoreInfo" id="detail_info">
#         </p>
#        </li>
#       </ul>
#      </div>
#      <div class="WhoisRight fr ml10">
#       <h4 class="WhoisRightHead YaHei fwnone bb-blue clearfix">
#        <i class="iconi">
#        </i>
#        <span>
#         网站的信息
#        </span>
#       </h4>
#       <div class="WhoisRightSite tc" id="infoLoad">
#        <img src="//csstools.chinaz.com/whois/images/public/loader.gif"/>
#       </div>
#       <div class="WhoisRightSite autohide" id="titleInfo">
#       </div>
#       <h4 class="WhoisRightHead YaHei fwnone bb-blue mt10 clearfix">
#        <i class="iconi">
#        </i>
#        <span>
#         相关查询
#        </span>
#       </h4>
#       <div class="WhoisRightOther">
#        <a href="http://del.chinaz.com" target="_blank">
#         过期域名查询
#        </a>
#        <a href="http://tool.chinaz.com/DomainDel/?wd=runoob.com" target="_blank">
#         域名删除时间查询
#        </a>
#        <a href="http://pr.chinaz.com/?PRAddress=runoob.com" target="_blank">
#         PR查询
#        </a>
#        <a href="http://ip.tool.chinaz.com/?ip=runoob.com" target="_blank">
#         IP地址查询
#        </a>
#        <a href="http://tool.chinaz.com/baidu?wd=runoob.com" target="_blank">
#         网站收录查询
#        </a>
#        <a href="http://alexa.chinaz.com/?domain=runoob.com" target="_blank">
#         Alexa排名查询
#        </a>
#        <a href="http://link.chinaz.com/" target="_blank">
#         友情链接检测
#        </a>
#        <a href="http://seo.chinaz.com/?host=runoob.com" target="_blank">
#         SEO综合查询
#        </a>
#        <a href="http://rank.chinaz.com/?host=runoob.com" target="_blank">
#         网站权重查询
#        </a>
#       </div>
#       <div id="scroll">
#        <div id="r_content">
#         <script src="//stats.chinaz.com/gj_g/sl300.js">
#         </script>
#        </div>
#       </div>
#      </div>
#     </div>
#    </div>
#    <!--IcpMain02-end-->
#   </div>
#   <!--Tool-MainWrap-begin-->
#   <link href="//csstools.chinaz.com/plugins/layer/skin/layer.css" rel="stylesheet" type="text/css">
#    <script type="text/javascript">
#     jQuery(function () {
#     $("#upd").click(function(){
#     $("#vcodeimg").click();
#     $("#vcodebox").show();
#     });
#     $("#vcodeimg").load(function(){
#     $(this).show().siblings(".lodding").remove();
#     }).error(function(){
#     $(this).before('<div class="pa lodding w100 lh45">加载失败，重试</div>');
#     }).click(function(){
#         $("input[name='isforceupdate']").val(1);
#         if(!$(".lodding").length)
#             $(this).hide().before('<div class="pa lodding w120 lh45"><img src="'+imgurlbase+'/public/spinner.gif"" />&nbsp;正在加载验证码</div>');
#     });
#         jQuery("#detail_info a").each(function(){
#             if(jQuery(this).text()!=="[whois反查]"){
#                 jQuery(this).remove();
#             }
#         });
#         var ymzt = new Array();
#         var dns = new Array();
#         jQuery(".WhoisLeft li").each(function (index) {
#             if (jQuery(this).children().eq(0).text() == "域名状态") {
#                 ymzt[index] = jQuery(this).children().eq(1).children().text();
#                 jQuery(this).hide();
#             }
#             if (jQuery(this).children().eq(0).text() == "DNS服务器") {
#                 dns[index] = jQuery(this).children().eq(1).children().text();
#                 jQuery(this).hide();
#             }
#         });
#         var ymzt_html = '', dns_html = '';
#         for (var i = 0; i < ymzt.length; i++) {
#             if (ymzt[i] != "undefined" && ymzt[i] != null && ymzt[i] != "")
#                 ymzt_html += ymzt[i] + "<br/>";
#         }
#         for (var i = 0; i < dns.length; i++) {
#             if (dns[i] != "undefined" && dns[i] != null && dns[i] != "")
#                 dns_html += dns[i] + "<br/>";
#         }
#         if (ymzt_html.length > 0 || dns_html.length > 0) {
#             if (jQuery("#sh_info li").last().prev().hasClass("flag")) {
#                 jQuery("#sh_info li").last().prev().before("<li class=\"bor-b1s\"><div class=\"fl WhLeList-left\">DNS服务器</div><div class=\"fr WhLeList-right\"><span>" + dns_html + "</span></div></li><li class=\"bor-b1s\"><div class=\"fl WhLeList-left\">域名状态</div><div class=\"fr WhLeList-right\"><span>" + ymzt_html + "</span></div></li>");
#             } else {
#                 jQuery("#sh_info li").append("<li class=\"bor-b1s\"><div class=\"fl WhLeList-left\">DNS服务器</div><div class=\"fr WhLeList-right\"><span>" + dns_html + "</span></div></li><li class=\"bor-b1s\"><div class=\"fl WhLeList-left\">域名状态</div><div class=\"fr WhLeList-right\"><span>" + ymzt_html + "</span></div></li>");
#             }
#         }
#         jQuery(".tip-sh").find("span a").each(function(index){
#             jQuery(this).mouseover(function(){jQuery(this).parent().next().removeClass("autohide")}).mouseout(function(){jQuery(this).parent().next().addClass("autohide")});
#         });
#                 jQuery(".WhoisLeft li").removeClass("bg-list").addClass("clearfix");
#         jQuery(".WhoisLeft li:even").addClass("bg-list");
#                     getTitle();
#                             getDetail();
#                         })
#     function getTitle() {
#         jQuery.ajax({
#             type: "post",
#             url: "/getTitleInfo.ashx",
#             data: { host: 'runoob.com',isupdate:request("isforceupdate") },
#             success: function (data) {
#                 jQuery("#infoLoad").addClass("autohide");
#                 jQuery("#titleInfo").removeClass("autohide");
#                 jQuery("#titleInfo").html(data);
#                 rightAd();
#             },
#             complete: function (XHR, TS) {
#                 XHR = null;
#                 jQuery("#retry").on("click", function () {
#                     jQuery("#infoLoad").removeClass("autohide");
#                     jQuery("#titleInfo").addClass("autohide");
#                     getTitle();
#                 });
#             }
#         })
#     }
#     function getDetail(){
#         jQuery.ajax({
#             type: "post",
#             url: "/getDetailInfo.ashx",
#             beforeSend:function(){jQuery("#detail_info").html("<span class=\"tc block auto\"><img src=\"//csstools.chinaz.com/whois/images/public/loader.gif\"/></span>");},
#             data: { domain: 'runoob.com',whoisServer:'grs-whois.hichina.com',deskey:'ECvBP9vjbuWQWpCMsYphWMTG0Bxf606i' ,isupdate:request("isforceupdate")},
#             success: function (data) {
#                 jQuery("#detail_info").html(data);
#                 jQuery("#detail_info a").each(function(){
#                     if(jQuery(this).text()!=="[whois反查]"){
#                         jQuery(this).remove();
#                     }
#                 });
#                 rightAd();
#             },
#             complete: function (XHR, TS) {
#                 XHR = null;
#                 if(jQuery("#sh_info li").last().find("p").text().indexOf("请求数据超时,请与管理员联系。")>=0||jQuery.trim(jQuery("#sh_info li").last().find("p").text())==''||jQuery("#sh_info li").last().find("p").text().indexOf("您的请求过于频繁，如有疑问请联系我们。")>=0){
#                     jQuery("#sh_info li").last().addClass("autohide");
#                     jQuery("#sh_info li").last().prev().addClass("autohide");
#                 }else{
#                     jQuery("#sh_info li").last().removeClass("autohide");
#                     jQuery("#sh_info li").last().prev().removeClass("autohide");
#                 }
#                 jQuery(".WhoisLeft li").removeClass("bg-list").addClass("clearfix");
#                 jQuery(".WhoisLeft li:even").addClass("bg-list");
#             }
#         })
#     }
#     function rightAd(){
#
#         if ($("#scroll").length) {
#          fn();
#          boxScroll({ _scroll: $("#r_content"), _width: 300, _height: 260, _top: $("#scroll").offset().top, _left: $("#scroll").offset().left, endElm: $("#centerTxt") });
#         $(window).resize(function () {
#             boxScroll({ _scroll: $("#r_content"), _width: 300, _height: 260, _top: $("#scroll").offset().top, _left: $("#scroll").offset().left, endElm: $("#centerTxt") });
#         });
#     }
#     }
#     function showDomainStatus() {
#         var status = document.getElementById("domainstatus");
#         if (status.style.display == "none") {
#             status.style.display = "block";
#         }
#         else {
#             status.style.display = "none";
#         }
#     }
#     function request(paras) {
#         var url = location.href;
#         var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
#         var paraObj = {}
#         for (i = 0; j = paraString[i]; i++) {
#             paraObj[j.substring(0, j.indexOf("=")).toLowerCase()] = j.substring(j.indexOf("=") + 1, j.length);
#         }
#         var returnValue = paraObj[paras.toLowerCase()];
#         if (typeof (returnValue) == "undefined") {
#             return "";
#         } else {
#             return returnValue;
#         }
#     }
#     $("form").submit(function () {
#         if ($("#DomainName").val().trim()=="") {
#             layer.alert("<p class=\"col-red tc\">输入的网址不合法，请重新输入</p>", { time: 3000, btn: '', title: '提示', move: false });
#             jQuery("#host").val("");
#             jQuery("#host").focus();
#             return false;
#         }
#         $("form").attr("action", "/" + $("#DomainName").val());
#     });
#    </script>
#    <!--footer-public-begin-->
#    <div class="wrapper mt10" style=" background:#f1f9ff">
#     <div id="centerTxt">
#     </div>
#     <div class="ToolsWrap" id="centerImg">
#     </div>
#     <div class="ToolAbout wrapper03">
#      <div class="clearfix">
#       <h4 class="HeadH4 YaHei fz16 col-blue02 fwnone fl">
#        工具简介
#       </h4>
#       <div class="fr fz14" id="toolsIntro">
#       </div>
#      </div>
#      <div class="col-gray01 ToolAbCont">
#       <p>
#        Whois 简单来说，就是一个用来查询域名是否已经被注册，以及注册域名的详细信息的数据库（如域名所有人、域名注册商、域名注册日期和过期日期等）。通过域名Whois服务器查询，可以查询域名归属者联系方式，以及注册和到期时间,可以用
#        <b style="color:Red;">
#         whois.chinaz.com
#        </b>
#        访问！
#       </p>
#       <p>
#        <strong>
#         关于域名到期删除规则实施的解释：
#        </strong>
#       </p>
#       <p>
#        国际域名：
#       </p>
#       <p>
#        (1) 到期当天暂停解析，如果在72小时未续费，则修改域名DNS指向广告页面（停放）。域名到期后30-45天为域名保留期（不同注册商政策规定时间不同）
#       </p>
#       <p>
#        (2) 过了保留期域名将进入赎回期（REDEMPTIONPERIOD，为期30天）
#       </p>
#       <p>
#        (3) 过了赎回期域名将进入为期5天左右的删除期，删除期过后域名开放，任何人可注。
#       </p>
#       <p>
#        <strong>
#         关于域名状态的解释：
#        </strong>
#        <a href="javascript:;" onclick="showDomainStatus()">
#         点击查看
#        </a>
#       </p>
#       <div id="domainstatus" style="display:none;">
#        <p>
#         cn域名各个状态说明：
#        </p>
#        <p>
#         以client开头的状态表示由客户端(注册商)可以增加的状态
#        </p>
#        <p>
#         以server开头的状态表示服务器端(CNNIC)操作增加的状态
#        </p>
#        <p>
#         既不以client开头也不以server开头的状态由服务器端管理
#        </p>
#        <p>
#         域名的状态解释：
#        </p>
#        <p>
#         ok 正常状态
#        </p>
#        <p>
#         inactive 非激活状态(注册的时候没有填写域名服务器，不能进行解析)
#        </p>
#        <p>
#         clientDeleteProhibited 禁止删除
#        </p>
#        <p>
#         serverDeleteProhibited 禁止删除
#        </p>
#        <p>
#         clientUpdateProhibited 禁止修改
#        </p>
#        <p>
#         serverUpdateProhibited 禁止修改
#        </p>
#        <p>
#         pendingDelete 正在删除过程中
#        </p>
#        <p>
#         pendingTransfer 正在转移过程中
#        </p>
#        <p>
#         clientTransferProhibited 禁止转移
#        </p>
#        <p>
#         serverTransferProhibited 禁止转移
#        </p>
#        <p>
#         clientRenewProhibited 禁止续费
#        </p>
#        <p>
#         serverRenewProhibited 禁止续费
#        </p>
#        <p>
#         clientHold 停止解析
#        </p>
#        <p>
#         serverHold 停止解析
#        </p>
#        <p>
#         pendingVerification 注册信息正在确认过程中
#        </p>
#       </div>
#       <p>
#        国内域名：
#       </p>
#       <p>
#        (1) 到期当天暂停解析，如果在72小时未续费，则修改域名DNS指向广告页面（停放）。35天内，可以自动续费。
#       </p>
#       <p>
#        (2) 过期后36－48天，将进入13天的高价赎回期，此期间域名无法管理。
#       </p>
#       <p>
#        (3) 过期后48天后仍未续费的，域名将随时被删除。
#       </p>
#      </div>
#     </div>
#    </div>
#    <!--siteBar-begin-->
#    <div class="wrapper mt10 bor-b1s06 clearfix">
#     <div class="ToFooter fl w24-0">
#      <a class="ToCurt" href="javascript:">
#       SEO相关
#      </a>
#      <a href="javascript:">
#       其他工具相关
#      </a>
#     </div>
#     <div class="fr lh43 pr10 new_fea">
#      <a href="http://icp.chinaz.com/" target="_blank">
#       网站备案
#      </a>
#      <a href="http://mobile.chinaz.com/" target="_blank">
#       Wap适配
#      </a>
#      <a href="http://tool.chinaz.com/speedcom.aspx" target="_blank">
#       网站测速PK
#      </a>
#      <a href="http://del.chinaz.com/" target="_blank">
#       过期域名查询
#      </a>
#      <a href="http://tool.chinaz.com/keywordsarea/" target="_blank">
#       关键词异地排名
#      </a>
#     </div>
#    </div>
#    <div class="GMFocusBox auto">
#     <div class="StabShow">
#      <div class="tFull">
#       <div class="GMFimglist02 pr">
#        <div class="Fotline">
#        </div>
#        <ul class="siteBar wrapper clearfix">
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           域名类
#          </h5>
#          <p class="plist">
#           <a href="http://whois.chinaz.com" target="_blank">
#            WHOIS查询
#           </a>
#           <a href="http://tool.chinaz.com/dns/" target="_blank">
#            DNS查询
#           </a>
#           <a href="http://del.chinaz.com" target="_blank">
#            过期域名查询
#           </a>
#           <a href="http://tool.chinaz.com/nslookup/" target="_blank">
#            NsLookup查询
#           </a>
#           <a href="http://tool.chinaz.com/DomainDel/" target="_blank">
#            域名删除时间
#           </a>
#           <a href="http://icp.chinaz.com" target="_blank">
#            备案查询
#           </a>
#           <a href="http://del.chinaz.com/type" target="_blank">
#            删除域名归档
#           </a>
#           <a href="http://icp.chinaz.com/searchs" target="_blank">
#            备案批量查询
#           </a>
#          </p>
#         </li>
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           IP类
#          </h5>
#          <p class="plist">
#           <a href="http://ip.tool.chinaz.com" target="_blank">
#            IP 查询
#           </a>
#           <a href="http://ip.tool.chinaz.com/ipbatch" target="_blank">
#            IP 批量查询
#           </a>
#           <a href="http://tool.chinaz.com/Same/" target="_blank">
#            同IP网站查询
#           </a>
#           <a href="http://tool.chinaz.com/ipwhois/" target="_blank">
#            IP WHOIS查询
#           </a>
#           <!--<a href="http://tool.chinaz.com/port/" target="_blank">端口扫描</a>-->
#          </p>
#         </li>
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           百度相关
#          </h5>
#          <p class="plist">
#           <a href="http://tool.chinaz.com/keywords" target="_blank">
#            关键词排名
#           </a>
#           <a href="http://tool.chinaz.com/baidu/words.aspx" target="_blank">
#            关键词挖掘
#           </a>
#           <a href="http://outlink.chinaz.com/" target="_blank">
#            反链查询
#           </a>
#           <a href="http://rank.chinaz.com" target="_blank">
#            权重查询
#           </a>
#           <a href="http://tool.chinaz.com/baidu/" target="_blank">
#            收录查询
#           </a>
#           <a href="http://tool.chinaz.com/baidu/entry" target="_blank">
#            收录率查询
#           </a>
#           <a href="http://tool.chinaz.com/kwevaluate" target="_blank">
#            关键词优化分析
#           </a>
#           <a href="http://tool.chinaz.com/baidu/metadig.aspx" target="_blank">
#            Meta信息挖掘
#           </a>
#          </p>
#         </li>
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           测速/监控
#          </h5>
#          <p class="plist">
#           <a href="http://ping.chinaz.com" target="_blank">
#            PING检测
#           </a>
#           <a href="http://tool.chinaz.com/Tools/webcheck.aspx" target="_blank">
#            网站被黑检测
#           </a>
#           <a href="http://tool.chinaz.com/speedtest.aspx" target="_blank">
#            国内网站测速
#           </a>
#           <a href="http://tool.chinaz.com/history/" target="_blank">
#            网站历史记录
#           </a>
#           <a href="http://tool.chinaz.com/speedworld.aspx" target="_blank">
#            海外网站测速
#           </a>
#           <a href="http://tool.chinaz.com/history/" target="_blank">
#            SEO历史记录
#           </a>
#           <a href="http://tool.chinaz.com/speedcom.aspx" target="_blank">
#            国内网速对比
#           </a>
#           <a href="http://alexa.chinaz.com/alexa_history.aspx" target="_blank">
#            ALexa历史报告
#           </a>
#          </p>
#         </li>
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           网页相关
#          </h5>
#          <p class="plist">
#           <a href="http://tool.chinaz.com/webdetect/" target="_blank">
#            网页检测
#           </a>
#           <a href="http://tool.chinaz.com/webscan" target="_blank">
#            网站安全检测
#           </a>
#           <a href="http://tool.chinaz.com/Links/" target="_blank">
#            死链检测
#           </a>
#           <a href="http://tool.chinaz.com/Gzips/" target="_blank">
#            网站GZIP压缩
#           </a>
#           <a href="http://tool.chinaz.com/pagestatus/" target="_blank">
#            网页状态检测
#           </a>
#           <a href="http://tool.chinaz.com/Tools/Density.aspx" target="_blank">
#            关键词密度分析
#           </a>
#           <a href="http://tool.chinaz.com/Tools/MetaCheck.aspx" target="_blank">
#            META信息查询
#           </a>
#           <a href="http://tool.chinaz.com/Tools/PageCode.aspx" target="_blank">
#            查看网页源代码
#           </a>
#          </p>
#         </li>
#        </ul>
#       </div>
#      </div>
#     </div>
#    </div>
#    <div class="GMFocusBox auto autohide">
#     <div class="StabShow">
#      <div class="tFull">
#       <div class="GMFimglist02 pr">
#        <div class="Fotline">
#        </div>
#        <ul class="siteBar wrapper clearfix">
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           配色/在线汉字
#          </h5>
#          <p class="plist">
#           <a href="http://tool.chinaz.com/Tools/cj" target="_blank">
#            中日传统色彩
#           </a>
#           <a href="http://tool.chinaz.com/Tools/pinyindictionary.aspx" target="_blank">
#            拼音字典
#           </a>
#           <a href="http://tool.chinaz.com/Tools/img" target="_blank">
#            传图识色
#           </a>
#           <a href="http://tool.chinaz.com/Tools/word_spell.aspx" target="_blank">
#            汉字拼音
#           </a>
#           <a href="http://tool.chinaz.com/Tools/web" target="_blank">
#            WEB安全色
#           </a>
#           <a href="http://tool.chinaz.com/Tools/lowercase-uppercase.aspx" target="_blank">
#            英文大小写
#           </a>
#           <a href="http://tool.chinaz.com/Tools/use" target="_blank">
#            网页常用色彩
#           </a>
#           <a href="http://tool.chinaz.com/Tools/gb_big.aspx" target="_blank">
#            繁/简/火星文
#           </a>
#          </p>
#         </li>
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           WEB相关
#          </h5>
#          <p class="plist">
#           <a href="http://tool.chinaz.com/htmlcheck.aspx" target="_blank">
#            Html标签检测
#           </a>
#           <a href="http://tool.chinaz.com/Tools/httptest.aspx" target="_blank">
#            Http接口测试
#           </a>
#           <a href="http://tool.chinaz.com/Tools/htmlchar.aspx" target="_blank">
#            Html特殊符号
#           </a>
#           <a href="http://tool.chinaz.com/Tools/regexgenerate" target="_blank">
#            正则表达式生成
#           </a>
#           <a href="http://tool.chinaz.com/Tools/cssdesigner.aspx" target="_blank">
#            CSS在线编辑
#           </a>
#           <a href="http://tool.chinaz.com/webscan" target="_blank">
#            网站安全检测
#           </a>
#           <a href="http://tool.chinaz.com/Tools/pagecode.aspx" target="_blank">
#            查看网页源代码
#           </a>
#           <a href="http://tool.chinaz.com/Tools/wordcounter" target="_blank">
#            在线字符统计
#           </a>
#          </p>
#         </li>
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           加密解密
#          </h5>
#          <p class="plist">
#           <a href="http://tool.chinaz.com/Tools/md5.aspx" target="_blank">
#            MD5加密
#           </a>
#           <a href="http://tool.chinaz.com/Tools/jscodeconfusion.aspx" target="_blank">
#            Js代码混淆
#           </a>
#           <a href="http://tool.chinaz.com/Tools/escape.aspx" target="_blank">
#            Escape加/解密
#           </a>
#           <a href="http://tool.chinaz.com/Tools/jsformat.aspx" target="_blank">
#            Js/Html格式化
#           </a>
#           <a href="http://tool.chinaz.com/Tools/urlcrypt.aspx" target="_blank">
#            Url16进制
#           </a>
#           <a href="http://tool.chinaz.com/js.aspx" target="_blank">
#            Js混淆压缩
#           </a>
#           <a href="http://tool.chinaz.com/Tools/thunder_flashget.aspx" target="_blank">
#            Url加/解密
#           </a>
#           <a href="http://tool.chinaz.com/Tools/textencrypt.aspx" target="_blank">
#            文字加/解密
#           </a>
#          </p>
#         </li>
#         <li class="fl bor-r1s">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           单位换算
#          </h5>
#          <p class="plist">
#           <a href="http://tool.chinaz.com/Tools/angle" target="_blank">
#            角度换算
#           </a>
#           <a href="http://tool.chinaz.com/Tools/time" target="_blank">
#            时间换算
#           </a>
#           <a href="http://tool.chinaz.com/Tools/heat" target="_blank">
#            热量换算
#           </a>
#           <a href="http://tool.chinaz.com/Tools/length" target="_blank">
#            长度换算
#           </a>
#           <a href="http://tool.chinaz.com/Tools/area" target="_blank">
#            面积换算
#           </a>
#           <a href="http://tool.chinaz.com/Tools/calculator" target="_blank">
#            计算器
#           </a>
#           <a href="http://tool.chinaz.com/Tools/datastore" target="_blank">
#            数据存储
#           </a>
#           <a href="http://tool.chinaz.com/Tools/subnetmask" target="_blank">
#            子网掩码
#           </a>
#          </p>
#         </li>
#         <li class="fl">
#          <h5 class="fz14 fwnone col-blue02 pb5">
#           编码转换
#          </h5>
#          <p class="plist">
#           <a href="http://tool.chinaz.com/Tools/unicode.aspx" target="_blank">
#            Unicode
#           </a>
#           <a href="http://tool.chinaz.com/Tools/html_ubb.aspx" target="_blank">
#            Html/UBB
#           </a>
#           <a href="http://tool.chinaz.com/Tools/unixtime.aspx" target="_blank">
#            Unix时间戳
#           </a>
#           <a href="http://tool.chinaz.com/Tools/urlencode.aspx" target="_blank">
#            UrlEncode
#           </a>
#           <a href="http://tool.chinaz.com/Tools/native_ascii.aspx" target="_blank">
#            NATIVE/ASCII
#           </a>
#           <a href="http://tool.chinaz.com/qrcode" target="_blank">
#            二维码生成
#           </a>
#           <a href="http://tool.chinaz.com/Tools/utf-8.aspx" target="_blank">
#            UTF-8编码
#           </a>
#           <a href="http://tool.chinaz.com/tools/html_js.aspx" target="_blank">
#            HTML/JS转换
#           </a>
#          </p>
#         </li>
#        </ul>
#       </div>
#      </div>
#     </div>
#    </div>
#    <!--siteBar-end-->
#    <div class="wrapper mt10">
#     <div class="fotatxtd auto" id="bottomImg">
#     </div>
#    </div>
#    <!--ToolFooter-begin-->
#    <div class="ww100 bor-t1s mt10 bg-white">
#     <div class="ToolFooter wrapper02">
#      <p class="linkbtn">
#       <a href="http://www.chinaz.com/aboutus/index.html" target="_blank">
#        关于站长之家
#       </a>
#       |
#       <a href="http://ww.chinaz.com/aboutus/contact.php" target="_blank">
#        联系我们
#       </a>
#       |
#       <a href="http://www.chinaz.com/aboutus/ad.html" target="_blank">
#        广告服务
#       </a>
#       |
#       <a href="http://www.chinaz.com/aboutus/link.html" target="_blank">
#        友情链接
#       </a>
#       |
#       <a href="http://www.chinaz.com/aboutus/events.html" target="_blank">
#        网站动态
#       </a>
#       |
#       <a href="http://www.chinaz.com/aboutus/announce.html" target="_blank">
#        版权声明
#       </a>
#       |
#       <a href="http://www.chinaz.com/aboutus/join.html" target="_blank">
#        人才招聘
#       </a>
#       |
#       <a href="http://www.chinaz.com/aboutus/help.html" target="_blank">
#        帮助
#       </a>
#      </p>
#      <p class="info">
#       <span>
#        © CopyRight 2002-2019, CHINAZ.COM, Inc.All Rights Reserved.
#       </span>
#       <span>
#        闽ICP备08105208号
#       </span>
#       <span>
#        增值电信业务经营许可证闽B2-20120007号
#       </span>
#       <a class="col-gray02" href="http://www.wy.cn" rel="nofollow" target="_blank">
#        服务器资源由唯一网络赞助
#       </a>
#       <span class="col-gray02 ml10">
#        亿速云提供
#        <a class="col-blue03" href="http://www.yisu.com/" rel="nofollow" target="_blank">
#         云服务器
#        </a>
#        支持
#       </span>
#      </p>
#     </div>
#    </div>
#    <!--ToolFooter-end-->
#    <!--footer-public-end-->
#    <div id="ToolBox">
#     <div id="xhead">
#     </div>
#     <ul id="xlist">
#     </ul>
#     <div id="xfoot">
#     </div>
#    </div>
#    <script src="///stats.chinaz.com/gj_g/tool_a.js" type="text/javascript">
#    </script>
#    <script charset="utf-8" src="//my.chinaz.com/js/uc.js" type="text/javascript">
#    </script>
#    <div class="TFloat-item" id="toTop">
#     <a href="javascript:" id="TFloat" title="回到顶部">
#     </a>
#     <a class="feedback" href="http://tool.chinaz.com/contact" target="_blank">
#     </a>
#     <a class="Record" href="javascript:" id="record">
#     </a>
#     <div class="Record-show" id="RecordShow" style="display:none;">
#      <div class="Tgroup">
#       <a href="http://seo.chinaz.com/" target="_blank">
#        SEO查询
#       </a>
#       <a href="http://icp.chinaz.com/" target="_blank">
#        备案查询
#       </a>
#       <a href="http://ip.tool.chinaz.com/" target="_blank">
#        IP查询
#       </a>
#       <a href="http://tool.chinaz.com/keywords" target="_blank">
#        关键词查询
#       </a>
#       <a href="http://link.chinaz.com/" target="_blank">
#        友情链接
#       </a>
#       <a class="col-hint" href="http://tool.chinaz.com/map.aspx" target="_blank">
#        更多工具
#       </a>
#      </div>
#      <div class="arr">
#      </div>
#     </div>
#    </div>
#    <div class="autohide">
#     <script charset="gb2312" language="JavaScript" src="//s11.cnzz.com/stat.php?id=5082706&amp;web_id=5082706" type="text/javascript">
#     </script>
#    </div>
#   </link>
#  </body>
# </html>
#
# '''
# # s = '''<div class="Tgroup">
# #       <a href="http://seo.chinaz.com/" target="_blank">
# #        SEO查询
# #       </a>
# #       <a href="http://icp.chinaz.com/" target="_blank">
# #        备案查询
# #       </a>'''
#
# # print(s)
#
# href = re.compile(r'<a.*\n.*\n.*</a>',re.I|re.M)
# aurl = href.findall(s,0)
# print(aurl)
#
# for i in aurl:
#     print(i)
#     s = s.replace(i,'')
#
# # print(s)

import re

info = '''Registrant Contact Email: xu_sy11111@mail.dlut.edu.cn
Sponsoring Registrar: 阿里云计算有限公司（万网）
Registrar Abuse Contact Email: DomainAbuse@service.aliyun.com
Registrar Abuse Contact Phone: +86.95187

'''

r1 = re.compile(r'Registrant Contact Email:.*\n',re.M|re.I)
try:
    s1 = r1.findall(info)[0]
except:
    r1 = re.compile(r'Registrar Abuse Contact Email:.*\n', re.M | re.I)
    try:
        s1 = r1.findall(info)[0]
    except:
        s1 = ''
finally:
    if s1 != '':
        s1 = s1[s1.index(':')+2:-1]
print(s1)
# if len(s1) == 0:
#     r1 = re.compile(r'Registrar Abuse Contact Email:.*\n',re.M|re.I)
#     s1 = r1.findall(info)[0][31:-1]
# else:
#     s1 = s1[0][26:-1]
# print(s1)
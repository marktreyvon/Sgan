# 主文件/入口文件：完成参数解析及具体功能函数的调用
from syn_scan import *
from tcp_scan import *
from udp_scan import *
from truly_stackless import *
from cdn_detection import *
from info_collection import *
from sensitive_doc_detection import *
import time
import argparse

title = """
███████╗ ██████╗  █████╗ ███╗   ██╗
██╔════╝██╔════╝ ██╔══██╗████╗  ██║
███████╗██║  ███╗███████║██╔██╗ ██║
╚════██║██║   ██║██╔══██║██║╚██╗██║
███████║╚██████╔╝██║  ██║██║ ╚████║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
"""
# analysis the input port:
def analysis_port(d):
    s = d[0]
    all_port = [21, 22, 23, 53, 80, 111, 139, 161, 389, 443, 445, 512, 513, 514,
                873, 1025, 1433, 1521, 3128, 3306, 3311, 3312, 3389, 5432, 5900,
                5984, 6082, 6379, 7001, 7002, 8000, 8080, 8081, 8090, 9000, 9090,
                8888, 9200, 9300, 10000, 11211, 27017, 27018, 50000, 50030, 50070]
    if s == 'all':
        return all_port
    if '-' in s:
        d = s.index('-')
        fir = int(s[:d])
        end = int(s[d + 1:])
        lis = []
        for i in range(fir, end + 1):
            lis.append(i)
        lis.sort()
        return lis
    elif ',' in s:
        lis = s.split(',')
        for i in range(len(lis)):
            lis[i] = int(lis[i])
        lis.sort()
        return lis
    else:
        return [s]

# output the result:
def output(result,method):
    if method == 'tcp':
        print('scan method: TCP connect()')
    elif method == 'syn':
        print('scan method: TCP SYN')
    elif method == 'udp':
        print('scan method: UDP scan')

    print('IP: ' + des_ip + '         ' + time.ctime() )
    print(51 * '-' )
    print("|{:^12s}|{:^15s}|{:^20s}|".format('port', 'status', 'service'))
    print(51 * '-')
    for i in result:
        print("|{:^12s}|{:^15s}|{:^20}|".format(str(i[0]),i[1],20*' '))
    print(51 * '-' )

# if the destination is url rather than IP, use this function to search info instead of scanning ports
def get_url_info(des_url):
    # check CDN from DNS:
    dns_result = check_from_web_CODINGTOOLS(des_url)
    if len(dns_result) == 1 :
        print('Target [',des_url,'] do not use CDN, IP:',dns_result[0])
    else:
        print('Target [',des_url,'] use CDN, IP:')
        for i in dns_result:
            print('                                 ',i)

    # search  whois
    whois_info = info_dic(des_url)
    print(69 * '-' )
    for i in whois_info:
        print("|{:^16s}|{:^50s}|".format(i, whois_info[i]))
        print(69 * '-')

    # choose whether detect sensitive file and directory
    choice = input('Simple Info Collection Finished, Want To Scan Sensitive File ?   [y/n]')
    detect_result = []
    if choice == 'y':
        file = input('Please Input The File Dictionary:')
        if file == '':
            detect_result = sensitive_detect(des_url)
        else:
            detect_result = sensitive_detect(des_url,file)
    if len(detect_result) == 0:
        print('Cannot Find Any Sensitive Things,Maybe You Should Use A Bigger Dictionary!')
    else:
        print('Sensitive Detect Result:')
        for i in detect_result:
            # print(i)
            print("{:^5d} :   {:<35s}".format(i[1],i[0]))
    main_finished(t)

# return the total time cost when finiished
def main_finished(t):
    t1 = time.time()-t
    print('Total Time Cost: ', t1, 'Seconds')
    exit()

if __name__ == '__main__':
    print(title)
    # parameter init:
    pars = argparse.ArgumentParser(prog='Sgan', description='A simple scanner, a wheel just like Nmap', add_help=True,
                                   usage='python3 %(prog)s.py IPaddres [Method] [Options]')
    pars.add_argument('des_ip', type=str, help='Destination IP addres')
    pars.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    pars.add_argument('method', type=str, default='tcp', help='Scan method (default : TCP scan)', nargs='?')
    pars.add_argument('-S',  default=False, action= 'store_true', dest='is_stackless', help='Use Stackless Python microthread to improve the velocity')
    pars.add_argument('-o', '--output', action='store_true', default=False, dest='is_save', help='Use this parameter to save your scan result as text')
    pars.add_argument('-p', dest='port', help='Choose the port you want to scan ,eg: 1-255(range)  1,2,3(specific)  255(single)  all(all the important ports given by Sgan)',
                      nargs=1)
    args_list = pars.parse_args()
    t = time.time()

    # analyse the parameter
    default_port = [135, 139, 1080, 1433, 3306, 3389, 80, 445, 443]
    default_port.sort()
    des_ip = args_list.des_ip
    des_url = None
    method = args_list.method
    des_port = args_list.port
    is_default_port = 0
    is_save_result = args_list.is_save
    is_stk = args_list.is_stackless
    try:
        if not des_port:
            des_port = default_port
            is_default_port = 1
        else:
            des_port = list(analysis_port(des_port))
        try:
            des_ip  = socket.inet_ntoa(socket.inet_aton(des_ip))
        except Exception as e:
            # print('\x1b[5;31;48m' + 'Error' + '\x1b[0m'+': IP address format error, eg: 1.1.1.1')
            # raise Exception
            des_url = des_ip
            des_ip = None
    except Exception:
        print('\x1b[5;31;48m' + 'Error' + '\x1b[0m'+': An unexpected error has occurred')
        pars.print_help()
        main_finished(t)

    # try to search the infomation of url, instead of scanning:
    if des_ip is None:
        t = time.time()
        get_url_info(des_url)

    # scan begin
    t = time.time()
    result = []
    if method == 'tcp':
        if  not is_stk:
            result = tcp_scan(des_ip, des_port)
        else:
            print('\x1b[5;31;48m' + 'Error' + '\x1b[0m'+": The scan method TCP connect() don't support using Stackless Python")
            pars.print_help()
            main_finished(t)
    elif method == 'syn':
        if not is_stk:
            result = syn_scan(des_ip, des_port)
        else:
            print('\x1b[5;33;48m' + 'Warning' + '\x1b[0m'+": Use SYN method with Stakless Python seems cannot get accrurate result. Please read README.")
            stk.tasklet(rcvd_chnl.send)('asd')
            for i in des_port:
                stk.tasklet(syn_send_stk)(des_ip,i)
            stk.tasklet(rcv_syn_pkt_from_datalink)(des_ip)
            stk.run()
            result = st_result
    elif method == 'udp' :
        if not is_stk:
            result = udp_scan(des_ip, des_port)
        else:
            stk.tasklet(rcvd_chnl.send)('asd')
            for i in des_port:
                stk.tasklet(udp_send_stk)(des_ip,i)
            stk.tasklet(rcv_udp_pkt_from_datalink)(des_ip)
            stk.run()
            result = st_result
    else:
        print('\x1b[5;31;48m' + 'Error' + '\x1b[0m'+': method format error')
        pars.print_help()
        main_finished(t)

    # output
    print('scan info: IP:', des_ip)
    if is_stk:
        print('use Stackless Python')
    if is_default_port:
        print('use default port lists')
    if is_save_result:
        txt = 'Sgan--' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) + '-' + des_ip + '.txt'
        with open(txt,'wt',encoding='utf-8') as f:
            f.writelines('IP: '+ des_ip+'         '+time.ctime()+'\n')
            f.writelines(51*'-'+'\n')
            f.writelines("|{:^12s}|{:^15s}|{:^20s}|\n".format('port','status','service'))
            f.writelines(51*'-'+'\n')
            for i in result:
                f.writelines("|{:^12s}|{:^15s}|{:^20}|".format(str(i[0]),i[1],20*' ')+'\n')
            f.writelines(51 * '-' + '\n')

    output(result, method)
    main_finished(t)
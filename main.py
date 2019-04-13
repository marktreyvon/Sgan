from syn_scan import *
from tcp_scan import *
from udp_scan import *
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
        return lis
    elif ',' in s:
        lis = s.split(',')
        for i in range(len(lis)):
            lis[i] = int(lis[i])
        return lis
    else:
        return [s]

def output(result,method,cost):
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

    print()
    print('total time cost: ', cost, 'Seconds')

if __name__ == '__main__':
    print(title)

    pars = argparse.ArgumentParser(prog='Sgan', description='A simple scanner, a wheel just like Nmap', add_help=True,
                                   usage='%(prog)s [options] IPaddres')
    pars.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    pars.add_argument('des_ip', type=str, help='destination IP addres')
    pars.add_argument('method', type=str, default='tcp', help='scan method (default : TCP scan)', nargs='?')
    pars.add_argument('-t', type=int, default=1, dest='threads', help='num of scan threads  (default : 1)', nargs=1)
    pars.add_argument('-o', '--output', action='store_true', default=False, dest='is_save', help='use this parameter to save your scan result as text')
    pars.add_argument('-p', dest='port', help='choose the port you want to scan ,eg: 1-255(range) 1,2,3(specific) 255(single)',
                      nargs=1)
    args_list = pars.parse_args()

    # analyse the parameter
    default_port = [135, 139, 1080, 1433, 3306, 3389, 80, 445, 443]
    default_port.sort()
    des_ip = args_list.des_ip
    method = args_list.method
    des_port = args_list.port
    is_default_port = 0
    is_save_result = args_list.is_save
    thread_num = args_list.threads[0]
    try:
        if not des_port:
            des_port = default_port
            is_default_port = 1
        else:
            des_port = list(analysis_port(des_port))
        if '.' not in des_ip:
            print('IP address format error, eg: 1.1.1.1')
            raise Exception
    except Exception:
        print('An unexpected error has occurred')
        pars.print_help()
        exit()

    # scan begin
    result = []
    t = time.time()
    if method == 'tcp':
        result = tcp_scan(des_ip, des_port)
    elif method == 'syn':
        result = syn_scan(des_ip, des_port)
    elif method == 'udp':
        result = udp_scan(des_ip, des_port)
    else:
        print('method error')
        pars.print_help()
        exit()
    # output
    print('scan info: IP:', des_ip)
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
    now = time.time()
    now = now - t
    output(result, method, now)





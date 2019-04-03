from syn_scan import *
from tcp_scan import *
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


if __name__ == '__main__':
    print(title)

    pars = argparse.ArgumentParser(prog='Sgan', description='A simple scanner, a wheel just like Nmap', add_help=True,
                                   usage='%(prog)s [options] IPaddres')
    pars.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    pars.add_argument('des_ip', type=str, help='destination IP addres')
    pars.add_argument('method', type=str, default='tcp', help='scan method (default : SYN scan)', nargs='?')
    pars.add_argument('-p', help='choose the port you want to scan ,eg: 1-255(range) 1,2,3(specific) 255(single)',
                      nargs=1)
    args_list = pars.parse_args()

    # analyse the parameter
    default_port = [135, 139, 1080, 1433, 3306, 3389, 80, 445, 443]
    all_port = [21, 22, 23, 53, 80, 111, 139, 161, 389, 443, 445, 512, 513, 514,
                873, 1025, 1433, 1521, 3128, 3306, 3311, 3312, 3389, 5432, 5900,
                5984, 6082, 6379, 7001, 7002, 8000, 8080, 8081, 8090, 9000, 9090,
                8888, 9200, 9300, 10000, 11211, 27017, 27018, 50000, 50030, 50070]
    default_port.sort()
    des_ip = args_list.des_ip
    method = args_list.method
    des_port = args_list.p
    try:
        if not des_port:
            print('use default port list')
            des_port = default_port
        else:
            des_port = list(analysis_port(des_port))
        if '.' not in des_ip:
            print('IP address format error, eg: 1.1.1.1')
            raise Exception
    except Exception:
        print('error')
        pars.print_help()
        exit()

    # scan begin
    t = time.time()
    print('scan info: IP:', des_ip)
    if method == 'tcp':
        print('scan method: tcp connec()')
        tcp_scan(des_ip, des_port)
    elif method == 'syn':
        print('scan method: tcp SYN')
        syn_scan(des_ip, des_port)
    else:
        print('method error')
    now = time.time()
    now = now - t
    print()
    print('total time cost: ', now, 'Seconds')




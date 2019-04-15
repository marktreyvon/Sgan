from syn_scan import *
from tcp_scan import *
from udp_scan import *
import stackless as stk
import socket,time

st_result = []

def tcp_scan_single_stk(ip,port):
    global result
    s = socket.socket()
    tar = (ip,port)
    try:
        s.connect(tar)
    except socket.timeout:
        result.append([tar[1],'close|filtered'])
    except Exception:
        result.append([tar[1],'close'])
    else:
        result.append([tar[1], 'open'])
    finally:
        s.close()
    # return result

def syn_scan_single_stk(des_ip, des_port):
    global st_result
    src_ip = get_host_ip()
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    # pack:
    ipobj = ip(src_ip, des_ip)
    iph = ipobj.pack()
    src_port = 9999
    tcpobj = tcp(src_port, des_port)
    tcph = tcpobj.pack(ipobj.source, ipobj.destination)
    packet = iph + tcph

    # send:
    s.sendto(packet, (des_ip, des_port))

    # receive:新建套接字接收SYNACK数据包存于pkt
    pkt = b''
    raw_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
    raw_socket.settimeout(0.05)
    try:
        pkt = raw_socket.recv(1024)
    except Exception as e:
        pass
    timeout = 3  # test 2 times whether recevied the right packet
    while timeout > 0 or not pkt:
        timeout -= 1
        if not pkt:
            s.sendto(packet, (des_ip, des_port))
            raw_socket.settimeout(0.05)
            s.settimeout(0.05)
            try:
                pkt = raw_socket.recv(1024)
            except Exception as e:
                if timeout == 1:
                    st_result.append([des_port, 'filtered'])
                    return
            continue
        else:
            data = struct.unpack("!6s6sH20s24s2s", pkt)
            check_result = check_synack(data, des_ip, des_port)
            if check_result == -1:
                continue
            elif check_result in (0, 1):
                break
    raw_socket.close()
    s.close()
    if not pkt:
        st_result.append([des_port, 'close'])
        return
    if check_result:
        st_result.append([des_port, 'open'])
    else:
        st_result.append([des_port, 'close'])

def udp_scan_single_stk(des_ip, des_port):
    global st_result
    des_addr = (des_ip,des_port)
    src_addr = send_udp_pkt(des_addr)
    des_ip,des_port = des_addr
    src_ip,src_port = src_addr
    raw_socket = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
    raw_socket.settimeout(0.025)
    # receive:
    '''
            rcv_code:
              -1:      timeout                                      open|filtered
                1:      received udp   packet            open
                2:      icmp port unreach                  closed
                3:      icmp unreach                            filtered
    '''
    rcv_code = -1
    for i in range(5):
        try:
            rcv = raw_socket.recv(1024)
            rcv_ip = socket.inet_ntoa(struct.unpack('4s',rcv[26:30])[0])
            rcv_proto = struct.unpack('B',rcv[23:24])[0]
            if rcv_ip != des_ip:
                continue
            else:
                if rcv_proto == 17:
                    rcv_code = 1
                elif rcv_proto == 1:
                    icmp_code = int(struct.unpack('B',rcv[35:36])[0])
                    if icmp_code == 3:
                        rcv_code = 2
                    elif icmp_code in (1,2,9,10,13):
                        rcv_code = 3
                break
        except socket.timeout as t:
            pass
    raw_socket.close()
    if rcv_code == -1:
        st_result.append([des_port,'open|filtered'])
    elif rcv_code == 1:
        st_result.append([des_port,'open'])
    elif rcv_code == 2:
        st_result.append([des_port,'close'])
    elif rcv_code == 3:
        st_result.append([des_port,'filtered'])

def choose_method(addr, method='tcp'):
    global st_result
    if method == 'tcp':
        for i in addr:
            stk.tasklet(tcp_scan_single_stk)(i[0],i[1])
    if method == 'syn':
        for i in addr:
            stk.tasklet(syn_scan_single_stk)(i[0],i[1])
    if method == 'udp':
        for i in addr:
            stk.tasklet(udp_scan_single_stk)(i[0],i[1])
    stk.run()


if __name__ == "__main__":
    ip2= '192.168.90.130'
    ip4= '192.168.90.133'
    ip1 = '172.19.19.215'
    ip3 = '123.206.9.135'
    # lis = [i+123 for i in range(10)]
    lis = [123]
    addr = [(ip4,i) for i in lis]
    t = time.time()

    # stackless:
    print('stackless:')
    choose_method(addr,'udp')
    print(st_result)
    print('time cost:',time.time()-t)
    t = time.time()

    # single thread:
    print('single:')
    result1 = []
    for i in addr:
        result1 += udp_scan_single(i[0],i[1])
    print(result1)
    print('time cost:',time.time()-t)


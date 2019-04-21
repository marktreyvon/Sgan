# 模块：Stackless Python 多线程扫描实现
from syn_scan import *
from tcp_scan import *
from udp_scan import *
import stackless as stk
import socket, time

# the final results from stackless version
st_result = []
method = None

# two signals for schedule the scan process:
#             send_chnl: sent from the sent tasklet----> the revd tasklet can try to rcv pkt
#             rcvd_chnl: sent from the rcvd tasklet----> rcv finished, sys can run the next send tasklet
send_chnl = stk.channel()
rcvd_chnl = stk.channel()


# create a function that is used to rcv all the response from destination,
#       which collects the pkt from the datalink layer whatever the scan method.
def rcv_udp_pkt_from_datalink(des_ip):
    global st_result
    flag_timeout = 0
    while 1:
        des_port = send_chnl.receive()
        flag_timeout = 0
        raw_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
        raw_socket.settimeout(0.002)
        # receive:
        # '''
        #         rcv_code:
        #             -1:     timeout                                        open|filtered
        #             1:      received udp   packet                          open
        #             2:      icmp port unreach                              closed
        #             3:      icmp unreach                                   filtered
        # '''
        rcv_code = -1
        for i in range(4):
            try:
                rcv = raw_socket.recv(1024)
                rcv_ip = socket.inet_ntoa(struct.unpack('4s', rcv[26:30])[0])
                rcv_proto = struct.unpack('B', rcv[23:24])[0]
                if rcv_ip != des_ip:
                    continue
                else:
                    if rcv_proto == 17:
                        rcv_code = 1
                    elif rcv_proto == 1:
                        icmp_code = int(struct.unpack('B', rcv[35:36])[0])
                        if icmp_code == 3:
                            rcv_code = 2
                        elif icmp_code in (1, 2, 9, 10, 13):
                            rcv_code = 3
                    break
            except socket.timeout as t:
                flag_timeout += 1
        if flag_timeout == 4:
            st_result.append([des_port, 'open|filtered'])
            rcvd_chnl.send(' ')
            continue
        raw_socket.close()
        if rcv_code == 1:
            st_result.append([des_port, 'open'])
        elif rcv_code == 2:
            st_result.append([des_port, 'close'])
        elif rcv_code == 3:
            st_result.append([des_port, 'filtered'])
        rcvd_chnl.send(' ')
        # break


def rcv_syn_pkt_from_datalink(des_ip):
    global st_result
    flag_timeout = 0
    while 1:
        des_port = send_chnl.receive()
        flag_timeout = 0
        raw_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
        raw_socket.settimeout(0.002)
        # receive:
        # '''
        #         rcv_code:
        #             1:      received SYN/ACK   packet                open
        #             2:       received RST/ACK   packet               closed
        #             3:      SYN pkt time out                            filtered
        # '''
        rcv_code = -1
        for i in range(10):
            try:
                rcv = raw_socket.recv(1024)
                rcv_ip = socket.inet_ntoa(struct.unpack('4s', rcv[26:30])[0])
                if rcv_ip != des_ip:
                    continue
                else:
                    tcp_code = int(struct.unpack('B', rcv[47:48])[0])
                    if tcp_code == 18:
                        rcv_code = 1
                    elif tcp_code == 20:
                        rcv_code = 2
                    break
            except socket.timeout as t:
                flag_timeout += 1
        if flag_timeout == 10:
            st_result.append([des_port, 'filtered'])
            raw_socket.close()
            rcvd_chnl.send(' ')
            continue
        raw_socket.close()
        if rcv_code == 1:
            st_result.append([des_port, 'open'])
        elif rcv_code == 2:
            st_result.append([des_port, 'close'])
        else:
            st_result.append([des_port, 'filtered'])
        rcvd_chnl.send(' ')


def syn_send_stk(des_ip, des_port):
    if rcvd_chnl.receive():
        pass
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
    send_chnl.send(des_port)


def udp_send_stk(des_ip, des_port):
    if rcvd_chnl.receive():
        pass
    des_addr = (des_ip, des_port)
    try:
        src_addr = send_udp_pkt(des_addr)
    except Exception as e:
        print(e)
    else:
        # send msg to rcvd tasklet
        send_chnl.send(des_port)


if __name__ == "__main__":
    ip2 = '192.168.90.130'
    ip4 = '192.168.90.133'
    ip1 = '172.19.19.215'
    ip3 = '123.206.9.135'
    # lis = [i+123 for i in range(10)]
    lis = [123, 514, 12345]
    addr = [(ip4, i) for i in lis]
    t = time.time()
    method = 'syn'
    # method =  'udp'
    # stackless:
    print('stackless:')
    stk.tasklet(rcvd_chnl.send)('asd')
    for i in addr:
        if method == 'syn':
            stk.tasklet(syn_send_stk)(i[0], i[1])
        elif method == 'udp':
            stk.tasklet(udp_send_stk)(i[0], i[1])
    stk.tasklet(rcv_syn_pkt_from_datalink)(ip4)
    stk.run()

    for i in st_result:
        print(i)
    print('time cost:', time.time() - t)
    t = time.time()

    # single thread:
    # print('single:')
    # result1 = []
    # for i in addr:
    #     result1 += udp_scan_single(i[0],i[1])
    # print(result1)
    # print('time cost:',time.time()-t)


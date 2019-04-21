# 模块：UDP扫描
import socket,struct

def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()
    return str(ip)

def send_udp_pkt(des_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b'', des_addr)
    addr = s.getsockname()
    s.close()
    return addr

def udp_scan_single(ip,port):
    des_addr = (ip,port)
    src_addr = send_udp_pkt(des_addr)
    result = judge_pkt(des_addr,src_addr)
    return result

def udp_scan_single_old(des_addr):
    result = []
    addr = send_udp_pkt(des_addr)
    port = des_addr[1]
    rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rs.settimeout(1)
    rs.bind(addr)
    try:
        rcv_data = rs.recvfrom(1024)
        if rcv_data:
            result.append([port,'open'])
            return result
    except socket.timeout as to:
        send_udp_pkt(des_addr)
        try:
            rs.recvfrom(1024)
            if rcv_data:
                result.append([port,'open'])
                return result
            elif not rcv_data:
                result.append([port,'open|filtered'])
                return result
        except socket.timeout:
            result.append([port,'open|filtered'])
    except Exception as e:
        print('scan error:',des_addr,end=' ')
        print(e)
    finally:
        rs.close()
    return result

def udp_scan(ip,portlis):
    result = []
    for i in portlis:
        result += udp_scan_single((ip,int(i)))
    print(result)
    return result

def send_udp_pkt(des_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b'', des_addr)
    addr = s.getsockname()
    s.close()
    return addr

# judge the receive packet whether udp pkt or icmp pkt
def judge_pkt(des_addr,src_addr):
    result = []
    des_ip,des_port = des_addr
    src_ip,src_port = src_addr
    raw_socket = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
    raw_socket.settimeout(0.3)
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
        result.append([des_port,'open|filtered'])
    elif rcv_code == 1:
        result.append([des_port,'open'])
    elif rcv_code == 2:
        result.append([des_port,'close'])
    elif rcv_code == 3:
        result.append([des_port,'filtered'])
    return result


if __name__ == '__main__':
    des_addr = ('192.168.90.133',9998)
    # src_addr = send_udp_pkt(des_addr)
    # addr = send_udp_pkt(('171.19.88.5',9999))
    # print('src_addr',src_addr)
    # judge_pkt(des_addr,src_addr)
    print(udp_scan_single(('192.168.90.133',9999)))
    print(udp_scan_single(('192.168.90.130',9998)))
    # udp_scan('171.19.88.5',[137,4020,9999])
    # udp_scan('192.168.90.130',[137,4020,9999])
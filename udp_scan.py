import socket

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

def udp_scan_single(des_addr):
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

# udp_scan_single(('192.168.90.130',9999))
# udp_scan_single(('192.168.90.130',9998))
udp_scan('192.168.90.130',[12409,61919,9999,9998])
# 一个简单的 UDP echo 程序
import socket
def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()
    return str(ip)

def create_udp_client(des_addr,src_addr=(get_host_ip(),9999)):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_data = input("send data:")
    s.sendto(bytes(send_data, encoding='utf-8'), des_addr)
    print("sended, receiving...")
    addr = s.getsockname()
    s.close()
    rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rs.bind(addr)
    print('bind: ',addr)
    try:
        rcv_data = rs.recvfrom(1024)
        print("receive: ", rcv_data)
    except Exception as e:
        print('error', e)
    finally:
        rs.close()
        print('closed')


def create_udp_server(src_addr=('172.19.88.5',9999)):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(src_addr)
    print(src_addr,' is listening')
    try:
        rcv_data,rcv_addr = s.recvfrom(1024)
        s.close()
        ns = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print('received: ', rcv_data,rcv_addr)
        ns.bind(src_addr)
        ns.sendto(b'received the data: '+rcv_data,rcv_addr)
        print('reply sent')
    except Exception as e:
        print('error  ',e)
    finally:
        ns.close()
        print('closed')
def send_udp_pkt(des_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(b'', des_addr)
    addr = s.getsockname()
    s.close()
    return addr

# addr = ('192.168.90.130',54817)
# print(send_udp_pkt(addr))
create_udp_server()
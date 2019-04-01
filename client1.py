import socket
def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()

    return str(ip)
# ipPort = (get_host_ip(),9999)
ipPort = ('192.168.90.130',9991)

# a = input()
# if a != '':
#     ipPort[0] = a
print('ip: ', ipPort[0])
# ipPort = tuple(ipPort)
s = socket.socket()


try:
    s.connect(ipPort)
except Exception:
    print('error')
    print(Exception)
    print(Exception.mro())
    print(Exception.__context__)


while 1:
    sendData = input('send: ').strip()
    s.send(bytes(sendData,encoding='utf-8'))
    # s.sendall(b'sendData')
    # print('waiting...')

    recvData = s.recv(1024)
    print('received: ',str(recvData,encoding='utf-8'))
s.close()
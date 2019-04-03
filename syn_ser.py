import socket
def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()

    return str(ip)
ipPort = (get_host_ip(),9991)

s = socket.socket()
s.bind(ipPort)
s.listen()
print(ipPort)
print('listening...')

while 1:
    conn,addr = s.accept()
    if conn is not None:
        print('user connected')

    # while 1:
    #     try:
    #         recvData = conn.recv(1024)
    #
    #         print('received: ',str(recvData,encoding='utf-8'),' .')
    #         sendData = input('please reply:').strip()
    #         conn.send(bytes(sendData,encoding='utf-8'))
    #         print('waiting for result...')
    #     except Exception:
    #         print('server error')
    #         conn.close()
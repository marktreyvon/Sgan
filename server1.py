

ipPort = (get_host_ip(),9991)

s = socket.socket()

s.bind(ipPort)

# while 1:
#     print('a',end='')
#
s.listen()
print('listening...')

# while 1:
#     print('a',end='')
while 1:
    conn,addr = s.accept()
    if conn is not None:
        print('user connected')
    while 1:
        try:
            recvData = conn.recv(1024)

            print('received: ',str(recvData,encoding='utf-8'))
            sendData = input('please reply:').strip()
            conn.send(bytes(sendData,encoding='utf-8'))
            print('waiting for result...')
        except Exception:
            print('server error')
            conn.close()
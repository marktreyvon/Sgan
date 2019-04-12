import socket

def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()

    return str(ip)

s = socket.socket()
ip = (get_host_ip(),9999)
print('listen: ',ip)
s.bind(ip)
s.listen()
while 1:
    pass

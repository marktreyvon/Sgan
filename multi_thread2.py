import socket,time,threading as th


def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()
    return str(ip)

def tcp_connection_scan(ip,port):
    s = socket.socket()
    tar = (ip,port)
    try:
        s.connect(tar)
        print(tar[1], ' is open')
    except Exception:
        # print(tar[1], 'is close')
        # print('',end=' ')
        pass
    finally:
        s.close()
def scan_tcp(ip,port):
    for i in range(len(port)):
        tcp_connection_scan(ip,port[i])
ip = get_host_ip()
t = time.time()
print('IP:',ip)
port = [135,138,9999,9991,445,1080]
# scan_tcp(ip,port)

# initial the whole port:
all_port = []
sum = 1000
for i in range(100):
    temp = []
    all_port.append(temp)
for i in range(sum):
    num = i%100
    all_port[num].append(i)


# bind the thread:
for i in range(100):
    t0 = th.Thread(target=scan_tcp(ip,all_port[i]))
    t0.start()
now = time.time()
now = now-t
print()
print('total cost: ',now)
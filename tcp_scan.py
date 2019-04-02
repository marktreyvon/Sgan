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
    except Exception:
        print(tar[1], 'is close')
    else:
        print(tar[1], 'is open')
    finally:
        s.close()
def tcp_scan(ip,port):
    for i in range(len(port)):
        tcp_connection_scan(ip,int(port[i]))

if __name__ == '__main__':
    ip = get_host_ip()
    t = time.time()
    print('IP:',ip)
    port = [135,138,9999,9991,445,1080]
    # tcp_scan(ip,port)

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
        t0 = th.Thread(target=tcp_scan(ip,all_port[i]))
        t0.start()
    now = time.time()
    now = now-t
    print()
    print('total cost: ',now)
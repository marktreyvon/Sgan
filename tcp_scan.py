import socket,time,threading as th

def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()
    return str(ip)

def tcp_scan_single(ip,port):
    result = []
    s = socket.socket()
    tar = (ip,port)
    try:
        s.connect(tar)
    except socket.timeout:
        result.append([tar[1],'close|filtered'])
    except Exception:
        result.append([tar[1],'close'])
    else:
        result.append([tar[1], 'open'])
    finally:
        s.close()
    return result
def tcp_scan(ip,port):
    result = []
    for i in range(len(port)):
        result += tcp_scan_single(ip,int(port[i]))
    return result

if __name__ == '__main__':
    # ip = get_host_ip()
    ip = '172.19.143.45'
    t = time.time()
    print('IP:',ip)
    portlis= [135,138,9999,9991,445,1080]
    port = 9991
    tcp_scan_single(ip,port)

    # initial the whole port:
    # all_port = []
    # sum = 1000
    # for i in range(100):
    #     temp = []
    #     all_port.append(temp)
    # for i in range(sum):
    #     num = i%100
    #     all_port[num].append(i)

    # # bind the thread:
    # for i in range(100):
    #     t0 = th.Thread(target=tcp_scan(ip,all_port[i]))
    #     t0.start()
    now = time.time()
    now = now-t
    print()
    print('total cost: ',now)
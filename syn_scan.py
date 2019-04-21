# 模块：SYN扫描
import socket
import struct

def get_host_ip():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()
    return str(ip)


def checksum(data):
    s = 0
    n = len(data) % 2
    for i in range(0, len(data) - n, 2):
        # s+= ord(data[i]) + (ord(data[i+1]) << 8)
        s += data[i] + (data[i + 1] << 8)
    if n:
        # s+= ord(data[i+1])
        s += data[i + 1]
    while (s >> 16):
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff
    return s


class ip():
    def __init__(self, source, destination):
        self.version = 4
        self.ihl = 5  # Internet Header Length
        self.tos = 0  # Type of Service
        self.tl = 0  # total length will be filled by kernel
        self.id = 2222
        self.flags = 1  # More fragments
        self.offset = 0
        self.ttl = 62
        self.protocol = socket.IPPROTO_TCP
        self.checksum = 0  # will be filled by kernel
        self.source = socket.inet_aton(source)
        self.destination = socket.inet_aton(destination)

    def pack(self):
        ver_ihl = (self.version << 4) + self.ihl
        flags_offset = (self.flags << 14) + self.offset
        ip_header = struct.pack("!BBHHHBBH4s4s",
                                ver_ihl,
                                self.tos,
                                self.tl,
                                self.id,
                                flags_offset,
                                self.ttl,
                                # self.protocol,
                                6,
                                self.checksum,
                                self.source,
                                self.destination)
        return ip_header


class tcp():
    def __init__(self, srcp, dstp):
        self.srcp = srcp
        self.dstp = dstp
        self.seqn = 0
        self.ackn = 0
        self.offset = 5  # Data offset: 5x4 = 20 bytes
        self.reserved = 0
        self.urg = 0
        self.ack = 0
        self.psh = 0
        self.rst = 0
        self.syn = 1
        self.fin = 0
        self.window = socket.htons(6666)
        self.checksum = 0
        self.urgp = int(0)
        self.payload = ""

    def pack(self, source, destination):
        data_offset = (self.offset << 4) + 0
        flags = self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh << 3) + (self.ack << 4) + (self.urg << 5)
        tcp_header = struct.pack("!HHLLBBHHH",
                                 self.srcp,
                                 self.dstp,
                                 self.seqn,
                                 self.ackn,
                                 data_offset,
                                 flags,
                                 self.window,
                                 self.checksum,
                                 self.urgp)
        # pseudo header fields
        source_ip = source
        destination_ip = destination
        reserved = 0
        protocol = socket.IPPROTO_TCP
        total_length = len(tcp_header) + len(self.payload)
        # Pseudo header
        psh = struct.pack("!4s4sBBH",
                          source_ip,
                          destination_ip,
                          reserved,
                          protocol,
                          total_length)
        psh = psh + tcp_header + self.payload.encode(encoding='utf-8')
        tcp_checksum = checksum(psh)
        tcp_header = struct.pack("!HHLLBBH",
                                 self.srcp,
                                 self.dstp,
                                 self.seqn,
                                 self.ackn,
                                 data_offset,
                                 flags,
                                 self.window)
        tcp_header += struct.pack("H", tcp_checksum) + struct.pack("!H", self.urgp)
        return tcp_header


# check the SYN/ACK
"""
return:     1 == port open 
                    0 == port closed
                    -1 == address error
"""


def check_synack(s, des_ip, des_port):
    theip = socket.inet_ntoa(s[3][12:16])
    port = s[4][:2]
    port = struct.unpack('H', port)[0]
    port = socket.ntohs(port)
    if (theip, port) != (des_ip, des_port):
        return -1
    result = s[4][13]
    # why result = 18 automatically?
    if result == 18:
        return 1
    else:
        return 0


def syn_scan_single(des_ip, des_port):
    result_list = []
    src_ip = get_host_ip()
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    # pack:
    ipobj = ip(src_ip, des_ip)
    iph = ipobj.pack()
    src_port = 9999
    tcpobj = tcp(src_port, des_port)
    tcph = tcpobj.pack(ipobj.source, ipobj.destination)
    packet = iph + tcph
    # send:
    s.sendto(packet, (des_ip, des_port))
    # receive:新建套接字接收SYNACK数据包存于pkt
    pkt = b''
    data = ''
    check_result = None
    raw_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))
    raw_socket.settimeout(0.05)

    try:
        pkt = raw_socket.recv(1024)
    except Exception as e:
        pass
    timeout = 3  # test 2 times whether recevied the right packet
    while timeout > 0 or not pkt:
        timeout -= 1
        if not pkt:
            s.sendto(packet, (des_ip, des_port))
            raw_socket.settimeout(0.05)
            s.settimeout(0.05)
            try:
                pkt = raw_socket.recv(1024)
            except Exception as e:
                if timeout == 1:
                    result.append([des_port, 'filtered'])
                    return
            continue
        else:
            data = struct.unpack("!6s6sH20s24s2s", pkt)
            check_result = check_synack(data, des_ip, des_port)
            if check_result == -1:
                continue
            elif check_result in (0, 1):
                break
    raw_socket.close()
    s.close()
    if not pkt:
        result.append([des_port, 'close'])
        return
    if result:
        result.append([des_port, 'open'])
    else:
        result.append([des_port, 'close'])
    return result

def syn_scan(ip, portlis):
    result = []
    for i in range(len(portlis)):
        result += syn_scan_single(ip, int(portlis[i]))
    return result

if __name__ == '__main__':
    iip = '123.206.9.135'
    syn_scan_single(iip, 80)
    syn_scan_single(iip, 9991)
    syn_scan_single(iip, 135)
    syn_scan_single(iip, 139)
    syn_scan_single(iip, 3389)
    syn_scan_single(iip, 445)
# # coding:utf-8
# import socket
# import struct
# import time
# import os
# import select
#
# ICMP_ECHO_REQUEST = 8
# '''
# 校验和
# 在ip中只校验20字节的ip报头
#                 icmp 校验 校验整个报文（报头加上数据）
# 校验和计算：
#         发送数据时；
#                 1 把校验和字段设置为0
#                 2 把需要校验的数据看成16位为单位的数字 依次进行二进制反码求和
#                 3 得到结果
# '''
#
#
# def checksum(source_string):
#     sum = 0
#     countTo = (len(source_string) / 2) * 2
#     # 首先计算字符串的长度
#     count = 0
#     while count < countTo:
#         thisVal = ord(source_string[count + 1]) * 256 + ord(source_string[count])
#         sum = sum + thisVal
#         sum = sum & 0xffffffff
#         count = count + 2
#     if countTo < len(source_string):
#         sum = sum + ord(source_string[len(source_string) - 1])
#         sum = sum & 0xffffffff
#     sum = (sum >> 16) + (sum & 0xffff)
#     sum = sum + (sum >> 16)
#     answer = ~sum
#     answer = answer & 0xffff
#     answer = answer >> 8 | (answer << 8 & 0xff00)
#     return answer
#
#
# def send_ping(my_socket, dest_addr, id):
#     header = struct.pack("bbHHh", 8, 0, 0, id, 1)
#     # 构造一个空的头
#     webtime = struct.pack("d", time.time())
#     # 增加发送时间戳 作为icmp的data
#
#     '''
#     关于计算目的主机和源主机数据传送的时间： echo-request 构造的数据包中添加时间戳，
#     echo-reply 返回数据 解包后得到time  计算时间差
#     '''
#
#     data = webtime
#     chksum = checksum(header + data)
#     # icmp 的检验和是检验头部和数据域的 区别与ip检验和
#     header = struct.pack("bbHHh", 8, 0, socket.htons(chksum), id, 1)
#     # 把16位正整数从主机字节序转换成网络序 socket.htons()
#     # 1>Unix系统在实现ping程序时把ICMP报文中的标识符字段置成发送进程的ID号。这样即使在同一台主机上同时运行了多个ping程序实例，ping程序也可以识别出返回的信息。
#     # 2>序列号从0开始，每发送一次新的回显请求就加1。ping程序打印出返回的每个分组的序列号，允许我们查看是否有分组丢失，失序或重复。.
#
#     packet = header + data
#     my_socket.sendto(packet, (dest_addr, 1))
#     # socket.sendto(string, address)
#
#
# def recive_ping(my_socket, id, timeout):
#     timeleft = timeout
#     while True:
#         startedselect = time.time();
#         # select.select(rlist, wlist, xlist[, timeout])
#         whatnow = select.select([my_socket], [], [], timeleft)
#         time_select = (time.time() - startedselect)
#         if whatnow[0] == []:
#             return
#         time_receive = time.time()
#         recvpacket, addr = my_socket.recvfrom(1024)
#         icmpheader = recvpacket[20:28]
#         # 一个ICMP报文包括IP头部（20字节）、ICMP头部（8字节）前20个字节是ip头部
#         type, code, checknum, ID, sequence = struct.unpack("bbHHh", icmpheader)
#         if ID == id:
#             time_sent = struct.unpack("d", recvpacket[28:])[0]
#             return time_receive - time_sent
#         time_out = timeleft - time_select
#         if time_out >= 0:
#             return
#
#
# def do(dest_addr, timeout=2):
#     icmp = socket.getprotobyname("icmp")
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
#     id = os.getpid()
#     send_ping(s, dest_addr, id)
#     delay = recive_ping(s, id, timeout)
#     print
#     " get ping in %0.4fms" % delay
#
#
# if __name__ == '__main__':
#     do('192.168.1.1')
# # [p = 30, 2, left]
import socket,struct
s = socket.ntohs(0x0800)
print(s,type(s))
s = b'asd111'
pkt = struct.pack('6s',s)
print(pkt,type(pkt))
un = struct.unpack(str(len(pkt))+'s',pkt)
print(un,type(un))

# Sgan（尝试造轮子）
## A simple port scanner with funny functions.

## 一个简单的端口扫描软件，附带杂七杂八的功能。

### 软件环境：Kali_2018.4_amd64 + Python3 （暂不支持Windows）

### 预计实现：

- TCP扫描
  - connect（）
  - SYN/FIN/NULL
- UDP扫描
- ……

## 遇到的问题：
1. Windows系统不支持通过socket.PF_PACKET从数据链路层获取数据包，需要另寻他法。这意味着SYN扫描在Windows上不能得到正确的结果
2. Windows系统并不完全遵守RFC793，这意味着NULL、FIN扫描Windows得不到正确的/准确的结果；
3. 端口扫描有一定误报率，次数少结果不确定，次数多容易ban IP；

## 参考文献：
[端口扫描原理](https://zenoh.iteye.com/blog/1264915)
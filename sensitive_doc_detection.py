
import requests

u1 = 'https://yun.dyedu.net'
u1 = 'http://www.runoob.com'

dic = []
with open('dic/dir_test.txt',mode='r') as f:
    # for i in f:
    #     dic.append(u1+f.readline()[:-1])
    dic = f.read().split()
for i in range(len(dic)):
    dic[i] = u1 + dic[i]
# dic = dic[0].split()
# print(dic)
# print(len(dic))
# print(dic)
# web_result = []
for i in dic:
    print(i,end='  ')
    try:
        # rr = requests.get(u1+'/robots.txt')
        # print(rr)
        r1 = requests.get(i)
        print(r1.url,r1.status_code)
    except Exception as e:
        print(e)
# print(r1)
# for i in dic:

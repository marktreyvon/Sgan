# 模块：通过字典进行敏感文件/目录探测
import requests,time

def sensitive_detect(url,file='default.txt'):
    if url.find('http') == -1:
        url = 'http://'+ url
    dic = []
    web_result = []
    try:
        if file == 'default.txt':
            raise Exception
        with open('/root/Documents/dic/'+file,mode='r') as f:
            dic = f.read().split()
    except:
        print("file '"+file+"' not found, try to use default dict")
        with open('/root/Documents/dic/default.txt',mode='r') as f:
            dic = f.read().split()
    for i in range(len(dic)):
        dic[i] = url + dic[i]
    dic = [url+'/robots.txt'] + dic
    for i in dic:
        try:
            r1 = requests.get(i)
            code = r1.status_code
            # if code != 404:
            web_result.append([r1.url,code])
        except Exception as e:
            print(e)
    return web_result

if __name__ == "__main__":
    t1 = time.time()
    u1 = 'https://yun.dyedu.net'
    u1 = 'http://www.runoob.com'
    a = sensitive_detect(u1,"dir_test.txt")
    for i in a:
        print(i)
    print(len(a))
    t2 = time.time()
    print(t2-t1)
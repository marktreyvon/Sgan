# 模块： 通过本地whois收集域名信息
import os,re

def get_info(url):
    cmd = os.popen('whois '+url)
    return cmd.read()
def info_dic(url):
    info  =get_info(url)
    r1 = re.compile(r'Domain Name:.*\n',re.M|re.I)
    r2= re.compile(r'Domain Status:.*\n',re.M|re.I)
    try:
        host_name = r1.findall(info)[0][13:-1]
        domain_status = r2.findall(info)[0][15:-1]
    except Exception as e:
        return info_dic(url)
    host_email = ''
    r3 = re.compile(r'Registrant Contact Email:.*\n',re.M|re.I)
    try:
        host_email  = r3.findall(info)[0]
    except:
        r3 = re.compile(r'Registrar Abuse Contact Email:.*\n', re.M | re.I)
        try:
            host_email  = r3.findall(info)[0]
        except:
            host_email  = ''
    finally:
        if host_email  != '':
            host_email  = host_email [host_email .index(':')+2:-1]
    company = ''
    r4 = re.compile(r'Registrar:.*\n',re.M|re.I)
    company  = r4.findall(info)[0]
    company  = company [company .index(':')+2:-1]
    domain_status = domain_status.split(' ')[0]
    d = {'Name':host_name,
                'Domain Status': domain_status,
                'Email': host_email,
                'Company': company
    }
    return(d)


if __name__ == '__main__':
    u1 = 'runoob.com'
    u2 = 'jd.com'
    u3 = 'xusy2333.cn'
    print(info_dic(u1))
    print(info_dic(u2))
    print(info_dic(u3))
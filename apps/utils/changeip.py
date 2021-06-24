# change Server IP
# 通过centos服务器配置静态ip的形式更改他的ip
import os, sys

def conf_ip(ip=218, DNS1="192.168.1.1", DNS2="8.8.8.8"):
    """原文件内容
    TYPE="Ethernet"
    BOOTPROTO="static"
    IPV4_FAILURE_FATAL="no"
    DNS1=192.168.1.1
    DNS2=8.8.8.8
    IPADDR=192.168.1.219
    GATEWAY=192.168.1.1
    NM_CONTROLLED=no
    NETMASK=255.255.255.0
    NAME="ens32"
    UUID="c4620b6e-c7cb-4770-9f3c-5a404ca2f1b1"
    DEVICE="ens32"
    ONBOOT="yes"
    """

    net_params = []
    # f = open("/etc/sysconfig/network-scripts/ifcfg-ens32", "r+")
    f = open("test.txt", "r+")
    for i in f:
        if "IPADDR=" in i:
            net_params.append("IPADDR=192.168.1.{0}\n".format(ip))
            continue
        if "DNS1=" in i:
            net_params.append("DNS1={0}\n".format(DNS1))
            continue
        if "DNS2=" in i:
            net_params.append("DNS2={0}\n".format(DNS2))
            continue
        if "BOOTPROTO=" in i:
            net_params.append('BOOTPROTO="static"\n')
            continue
        net_params.append(i)

    # 在末尾写入
    # iplist.extend(['\nIPADDR=192.168.1.{0}\n'.format(ip), 'NETMASK=255.255.255.0\n', 'GATEWAY="192.168.1.1"\n'])
    # 从头开始写文件
    f.seek(0, 0)
    f.writelines(net_params)
    # 写完将原先的删去
    f.truncate()
    f.close()

def set_hostname(host):
    with open("/etc/hostname", "w") as f:
        f.write(host)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        conf_ip(sys.argv[1])
        # set_hostname(sys.argv[2])
        os.remove(sys.argv[0])
        cmd = "service network restart"
        b = os.system(cmd)
        print(b)
    else:
        print("-------程序启动错误-------")
    # conf_ip(220)
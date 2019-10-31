# namecheap_ddns

Python DDNS client for namecheap

# English

Because the namecheap ddns clients are not very good and the get ip API may can not be used in China, this program use TAOBAO ip database to get the public ip and push it to namecheap DNS server.

## How to use

1.  Edit parameters:

```python
# Your namecheap ddns key
ddns_key = "YOUR_DDNS_KEY"
# Your domain list
domain_list = ['DOMAIN1.COM']
# Host list of each domain
host_list = {
    'DOMAIN1.COM': ['www', 'api', '...']
}
# How long to refresh the IP, if the IP is the same as last time, will not push to DNS server.
renew_time = 5  # Min
```

2.  Run `python auto_renew.py`, you can also add it into the service on Linux or task scheduler on windows to make it run after start up the server.

# 中文

由于Namecheap的客户端不尽如人意，并且使用的获取IP的API偶尔不能在国内使用，所以该程序使用淘宝IP地址API来获取自己的公网IP并推送到Namecheap的DNS服务器。

## 如何使用

1.  编辑参数

```python
# Namecheap的DDNS key
ddns_key = "YOUR_DDNS_KEY"
# 域名列表
domain_list = ['DOMAIN1.COM']
# 每个域名的主机列表，均会进行更新
host_list = {
    'DOMAIN1.COM': ['www', 'api', '...']
}
# 每隔多久更新一次IP，如果ip与上次相同则不会更新
renew_time = 5  # Min
```

2.  运行`python auto_renew.py`, 也可以加入到开机启动或者Windows的计划任务，以便开机运行，自动更新IP地址。

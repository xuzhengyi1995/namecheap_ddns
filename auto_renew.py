# Auto renew the ip information for the DDNS of NameCheap
# XUZhegyi, 2019-05-13

import json
import time

from getHtml import GetHtml

# *********settings*********
ddns_key = "YOUR_DDNS_KEY"
domain_list = ['DOMAIN1.COM']
host_list = {
    'DOMAIN1.COM': ['www', 'api', '...']
}
renew_time = 5  # Min
# *********settings*********

get_ip_api = "http://ip.taobao.com/service/getIpInfo.php?ip=myip"
update_ip_api = "https://dynamicdns.park-your-domain.com/update?host=%s&domain=%s&password=%s&ip=%s"
get_ip = GetHtml()
update_ip = GetHtml()
send_header = {'Accept': 'application/json'}
get_ip.set(header=send_header, url=get_ip_api)


def logger(file, message):
    file.write(message + '\n')
    print(message)


def get_my_ip():
    try:
        my_ip_json = json.loads(get_ip.get(t_out=10).decode('utf-8'))
        return my_ip_json['data']['ip']
    except:
        return None


def send_update_request(ip=None, log_file=None):
    log = open('log_file.txt', 'a') if not log_file else log_file
    if not ip:
        return None
    else:
        try:
            for domain in domain_list:
                for host in host_list[domain]:
                    this_update_url = update_ip_api % (
                        host, domain, ddns_key, ip)
                    update_ip.set(header=send_header, url=this_update_url)
                    try:
                        response = update_ip.get(t_out=15).decode('utf-8')
                        if response == "" or not response:
                            log_write = '[ERROR] ' + time.asctime() + ': "' + host + '.' + \
                                domain + '" can not be updated!'
                            logger(log, log_write)
                            send_update_request(ip, log)
                        else:
                            log_write = '[UPDATED] ' + time.asctime() + ': "' + host + '.' + \
                                domain + '" updated successfully!'
                            logger(log, log_write)
                    except:
                        log_write = '[ERROR] ' + time.asctime() + ': "' + host + '.' + \
                            domain + '" can not be updated!'
                        logger(log, log_write)
                        send_update_request(ip, log)
        except:
            log_write = time.asctime() + ': data error!'
            logger(log, log_write)
        if not log_file:
            log.close()


if __name__ == '__main__':
    log = open('log_file.txt', 'a')
    time_count = 0
    renew_time_backup = renew_time
    last_ip = None
    while True:
        time_count += 1
        log_write = '----------------------------------------------------------'
        logger(log, log_write)
        log_write = '[INFO] ' + time.asctime() + ': Updating...'
        logger(log, log_write)
        # Get ip
        my_ip = None
        try_times = 0
        while(not my_ip and try_times < 10):
            my_ip = get_my_ip()
            try_times += 1
            if not my_ip:
                time.sleep(5)
        if my_ip:
            log_write = '[INFO] My ip is %s' % my_ip
            renew_time = renew_time_backup
        else:
            log_write = '[ERROR] Can not get ip at the moment, will try again shortly.'
            renew_time = 2
            my_ip = last_ip
        logger(log, log_write)
        # Verify if this time the ip is the same
        if last_ip and last_ip == my_ip:
            logger(log, "[INFO] The ip is not changed, will check next time.")
        else:
            # Save the ip address
            last_ip = my_ip
            # Send update request
            send_update_request(my_ip, log)
            log_write = '[INFO] ' + time.asctime() + ': Updated'
            logger(log, log_write)
        log.flush()
        # Switch log file
        if time_count >= 500:
            log.truncate(0)
            time_count = 0
        time.sleep(60 * renew_time)
    log.close()

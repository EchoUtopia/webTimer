import pcap
import dpkt
import sys
import redis
import time
import json


def get_config():
    f = open("./configs.json")
    try:
        return json.load(f)
    finally:
        f.close()

def get_ip_list():
    return ["42.236.2.139","180.149.134.141","223.85.194.250"]


r = redis.Redis(host='localhost',port=6379,db=0)

def get_unit(timestamp):
    timestamp = float(timestamp)
    minute = time.strftime("%M",time.localtime(timestamp))
    five_minute_unit = int(minute) // 5 + 1
    return five_minute_unit


def get_table(remote_ip,timestamp):
    five_minute_unit = get_unit(timestamp)
    return "ip:%s:%s" %(remote_ip,five_minute_unit)

def del_or_not(remote_ip,timestamp,last_timestamp):
    now_unit = get_unit(timestamp)
    last_unit = get_unit(last_timestamp)
    if now_unit == 1 and last_unit == 12:
        pattern = "ip:%s*" % remote_ip
        keys = r.keys(pattern)
        r.delete(keys)
        return True
    return False

def update_up_data(remote_ip,timestamp):
    table = get_table(remote_ip,timestamp)
    last_timestamp = r.hget(table,"timestamp") or 0
    del_or_not(remote_ip,timestamp,last_timestamp)
    timestamp_diff = timestamp - int(last_timestamp)
    if timestamp_diff > 3:
        r.hincrby(table,"visit_count",1)


def update_down_data(remote_ip,timestamp):
    rp = r.pipeline()
    table = get_table(remote_ip,timestamp)
    print table
    if r.hexists(table,"timestamp"):
        data = r.hgetall(table)
        if del_or_not(remote_ip,timestamp,data['timestamp']):
            rp.hset(table,"timestamp",timestamp)
            rp.hincrby(table,"total_time",0)
            rp.execute()
        else:

            timestamp_diff = timestamp - int(data['timestamp'])
            if  timestamp_diff> 3 and timestamp_diff < 300:
                rp.hset(table,"timestamp",timestamp)
                rp.hincrby(table,"total_time",timestamp_diff)
            elif timestamp_diff >= 300:
                rp.hset(table,"timestamp",timestamp)
            rp.execute()
        
    else:
        rp.hset(table,"timestamp",timestamp)
        rp.hincrby(table,"total_time",0)
        rp.execute()

def sniff():
    config = get_config()
    ip_list = get_ip_list()
    # cfilter = "(ip.dst==%(ip)s|| ip.src==%(ip)s) && (tcp.port==443 || tcp.port == 80) &&(http || ssl)" % {"ip":config['ip']}
    cfilter = "(port 80 or port 443) and (src host %(ip)s or dst host %(ip)s)" % {"ip":config['ip']}
    # cfilter = "ssl"
    print cfilter
    pc = pcap.pcap()
    pc.setfilter(cfilter)
    for ptime,pdata in pc:
        ptime = int(ptime)
        p=dpkt.ethernet.Ethernet(pdata)
        src='%d.%d.%d.%d' % tuple(map(ord,list(p.data.src)))
        dst='%d.%d.%d.%d' % tuple(map(ord,list(p.data.dst)))
        if  src in ip_list:
            update_down_data(src,ptime)
        elif src == config['ip'] and dst in ip_list:
            update_up_data(dst,ptime)

if __name__ == "__main__":
    sniff()
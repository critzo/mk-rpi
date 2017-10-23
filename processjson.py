#!/usr/bin/python
import json
import os
import subprocess
#from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
#import prometheus_client.exposition

dev_loc = 'guatemala1' #os.environ['PROJ_CON_DEVICE_LOCATION']
#dev_sch = os.environ['PROJ_CON_SCHOOL']
#pushgw = os.environ['PUSHGW_SERVER']
#pushgw_user = os.environ['PUSHGW_USERNAME']
#pushgw_pass = os.environ['PUSHGW_PASS']

def pushgw_auth_handler(url, method, timeout, headers, data):
    u = pushgw_user
    p = pushgw_pass
    return prometheus_client.exposition.basic_auth_handler(url, method, timeout, headers, data, username=u, password=p)

with open('data.json') as data_file:
	data = json.load(data_file)

# attempt at using the python prometheus_client 	
#registry = CollectorRegistry()
#m = Gauge('measurement_start_time', 'Measurement Start Time', registry=registry)
#m.set(data['measurement_start_time']
#d = Gauge('download', 'Download Speed', registry=registry)
#d.set(data['test_keys']['simple']['download']
#u = Gauge('upload', 'Upload Speed', registry=registry)
#u.set(data['test_keys']['simple']['upload']
#p = Gauge('ping', 'Ping', registry=registry)
#p.set(data['test_keys']['simple']['ping']
#min_rtt = Gauge('min_rtt', 'Minimum RTT', registry=registry)
#min_rtt.set(data['test_keys']['advanced']['min_rtt']
#max_rtt = Gauge('max_rtt', 'Maximum RTT', registry=registry)
#max_rtt.set(data['test_keys']['advanced']['max_rtt']
#avg_rtt = Gauge('avg_rtt', 'Average RTT', registry=registry)
#avg_rtt.set(data['test_keys']['advanced']['avg_rtt']
#packet_loss = Gauge('packet_loss', 'Percent Packet Loss', registry=registry)
#packet_loss.set(data['test_keys']['advanced']['packet_loss']
#sender_lim = Gauge('sender_lim', 'Sender Limited Ratio', registry=registry)
#sender_lim.set(data['test_keys']['advanced']['sender_limited']
#recv_lim = Gauge('recv_lim', 'Receiver Limited Ratio', registry=registry)
#recv_lim.set(data['test_keys']['advanced']['receiver_limited']
#cong_lim = Gauge('cong_lim', 'Congestion Limited Ratio', registry=registry)
#cong_lim.set(data['test_keys']['advanced']['congestion_limited']

#push_to_gateway(pushgw, 'projconnect', registry)
#url = "https://104.154.133.198:9091/metrics/job/"+dev_loc+"/instance/"+dev_sch+"/"+prom_results

cmd = """cat <<EOF | curl -k --data-binary @- https://104.154.133.198/metrics/job/"""+dev_loc+"""
# TYPE download gauge
download{label="Download Speed"} """+str(data['test_keys']['simple']['download'])+"""
# TYPE upload gauge
upload{label="Upload Speed"} """+str(data['test_keys']['simple']['upload'])+"""
# TYPE ping gauge
ping{label="Ping Test"} """+str(data['test_keys']['simple']['ping'])+"""
# TYPE min_rtt gauge
min_rtt{label="Minimum Round Trip Time"} """+str(data['test_keys']['advanced']['min_rtt'])+"""
# TYPE max_rtt gauge
max_rtt{label="Maximum Round Trip Time"} """+str(data['test_keys']['advanced']['max_rtt'])+"""
# TYPE avg_rtt gauge
avg_rtt{label="Average Round Trip Time"} """+str(data['test_keys']['advanced']['avg_rtt'])+"""
# TYPE cong_lim gauge
cong_lim{label="Congestion Limited Ratio"} """+str(data['test_keys']['advanced']['congestion_limited'])+"""
# TYPE recv_lim gauge
recv_lim{label="Receiver Limited Ratio"} """+str(data['test_keys']['advanced']['receiver_limited'])+"""
# TYPE send_lim gauge
send_lim{label="Sender Limited Ratio"} """+str(data['test_keys']['advanced']['sender_limited'])+"""
EOF
"""

subprocess.check_output(cmd, shell=True)

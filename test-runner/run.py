import argparse
import datetime
import json
import logging
import os
import random
import re
import subprocess
import time
import urllib2

import pytz
import tzlocal

def setup_logger():
    logger = logging.getLogger('pyNDT')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    file_handler = logging.FileHandler('pyndt.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()

def format_time(utc_time):
    utc_time_explicit = utc_time.replace(tzinfo=pytz.utc)
    localized = utc_time_explicit.astimezone(tzlocal.get_localzone())
    localized = localized.replace(microsecond=0)
    return localized.strftime('%Y-%m-%dT%H:%M:%S%z')
    
def do_ndt_test():
    now = int(subprocess.check_output(["date", "-u", "+%s"]))
    dev_loc = os.environ['PROJ_CON_DEVICE_LOCATION']
    dev_sch = os.environ['PROJ_CON_SCHOOL']
    result_raw = subprocess.check_output(["measurement_kit", "--reportfile=/data/"+dev_loc+"--"+dev_sch+"--%d.njson"%now, "ndt"])

    with open('/data/'+dev_loc+'--'+dev_sch+--'%d.njson'%now) as data_file:
        data = json.load(data_file)
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

    return result_raw

def perform_test_loop():
    while True:
        try:
            ndt_result = do_ndt_test()
        except Exception as ex:
            logger.error('Error in NDT test: %s', ex)
        sleeptime = random.expovariate(1.0/3600.0)
        resume_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=sleeptime)
        logger.info('Sleeping for %u seconds (until %s)', sleeptime, resume_time)
        time.sleep(sleeptime)

if __name__ == "__main__":
    perform_test_loop()
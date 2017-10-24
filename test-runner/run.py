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
    reportfile = "%s--%s--%d.njson" % (dev_loc, dev_sch, now)
    flags = "--reportfile=/data/%s" % reportfile
    result_raw = subprocess.check_output(["measurement_kit", flags, "ndt"])

    with open('/data/%s' % reportfile) as data_file:
        data = json.load(data_file)

    cmd = """cat <<EOF | curl -k --data-binary @- https://104.154.133.198/metrics/job/%s
# TYPE download gauge
download{label="Download Speed"} %s
# TYPE upload gauge
upload{label="Upload Speed"} %s
# TYPE ping gauge
ping{label="Ping Test"} %s
# TYPE min_rtt gauge
min_rtt{label="Minimum Round Trip Time"} %s
# TYPE max_rtt gauge
max_rtt{label="Maximum Round Trip Time"} %s
# TYPE avg_rtt gauge
avg_rtt{label="Average Round Trip Time"} %s
# TYPE cong_lim gauge
cong_lim{label="Congestion Limited Ratio"} %s
# TYPE recv_lim gauge
recv_lim{label="Receiver Limited Ratio"} %s
# TYPE send_lim gauge
send_lim{label="Sender Limited Ratio"} %s
EOF""" % (
    dev_loc,
    str(data['test_keys']['simple']['download']),
    str(data['test_keys']['simple']['upload']),
    str(data['test_keys']['simple']['ping']),
    str(data['test_keys']['advanced']['min_rtt']),
    str(data['test_keys']['advanced']['max_rtt']),
    str(data['test_keys']['advanced']['avg_rtt']),
    str(data['test_keys']['advanced']['congestion_limited']),
    str(data['test_keys']['advanced']['receiver_limited']),
    str(data['test_keys']['advanced']['sender_limited'])
    )
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
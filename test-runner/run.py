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
    
def run_ndt_test():
    now = int(subprocess.check_output(["date", "-u", "+%s"]))
    site = os.environ['SITE']
    test = 'ndt'
    device_loc = os.environ['DEVICE_LOC']
    connection_loc = os.environ['CONNECTION_LOC']
    reportfile = "%s-%s-%s-%s-%d.njson" % (site, test, device_loc, connection_loc, now)
    flags = "--reportfile=/data/%s" % reportfile
    result_raw = subprocess.check_output(["measurement_kit", flags, "ndt"])

    with open('/data/%s' % reportfile) as data_file:
        data = json.load(data_file)

    return result_raw

def run_dash_test():
    now = int(subprocess.check_output(["date", "-u", "+%s"]))
    site = os.environ['SITE']
    test = 'dash'
    device_loc = os.environ['DEVICE_LOC']
    connection_loc = os.environ['CONNECTION_LOC']
    reportfile = "%s-%s-%s-%s-%d.njson" % (site, test, device_loc, connection_loc, now)
    flags = "--reportfile=/data/%s" % reportfile
    result_raw = subprocess.check_output(["measurement_kit", flags, "dash"])

    with open('/data/%s' % reportfile) as data_file:
        data = json.load(data_file)

    return result_raw

def run_speedtest_test():
    now = int(subprocess.check_output(["date", "-u", "+%s"]))
    site = os.environ['SITE']
    test = 'speedtest'
    device_loc = os.environ['DEVICE_LOC']
    connection_loc = os.environ['CONNECTION_LOC']
    reportfile = "%s-%s-%s-%s-%d.json" % (site, test, device_loc, connection_loc, now)
    flags = "--secure --json > /data/%s" % reportfile
    result_raw = subprocess.check_output(["speedtest", flags], shell=True)

    with open('/data/%s' % reportfile) as data_file:
        data = json.load(data_file)

    return result_raw

def perform_test_loop():
    while True:
        try:
            ndt_result = run_ndt_test()
            speedtest_result = run_speedtest_test()
            dash_result = run_dash_test()
        except Exception as ex:
            logger.error('Test Error test: %s', ex)

        sleeptime = random.expovariate(1.0/3600.0)
        resume_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=sleeptime)
        logger.info('Sleeping for %u seconds (until %s)', sleeptime, resume_time)
        time.sleep(sleeptime)

if __name__ == "__main__":
    perform_test_loop()
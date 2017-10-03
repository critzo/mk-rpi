import argparse
import csv
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

def do_ndt_test():
    result_raw = subprocess.check_output(["measurement_kit", "ndt"])
    #return parse_ndt_result(result_raw.split('\n'), ndt_hostname, datetime.datetime.utcnow())
    return results_raw

def perform_test_loop():
    while True:
        try:
            ndt_result = do_ndt_test()
        except Exception as ex:
            logger.error('Error in NDT test: %s', ex)
        sleeptime = random.expovariate(1.0/3600.0)
        resume_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=sleeptime)
        logger.info('Sleeping for %u seconds (until %s)', sleeptime, format_time(resume_time))
        time.sleep(sleeptime)

if __name__ == "__main__":
    perform_test_loop()
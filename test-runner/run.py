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
    dev_loc = os.environ['DEVICE_LOC']
    dev_sch = os.environ['CONNECTION_LOC']
    pushgw = os.environ['PUSHGW_SERVER']
    reportfile = "%s--%s--%d.njson" % (dev_loc, dev_sch, now)
    flags = "--reportfile=/data/%s" % reportfile
    result_raw = subprocess.check_output(["measurement_kit", flags, "ndt"])

    with open('/data/%s' % reportfile) as data_file:
        data = json.load(data_file)

    cmd = """cat <<EOF | curl -k --data-binary @- https://%s/metrics/job/%s

# TYPE test_keys_adv__avg_rtt gauge
test_keys_adv__avg_rtt{label=Average Round Trip Time"} %s
# TYPE test_keys_adv__cong_lim gauge
test_keys_adv__cong_lim{label="Congestion Limited Ratio"} %s
# TYPE test_keys_adv__fast_retran gauge
test_keys_adv__fast_retran{label="fast_retran"} %s
# TYPE test_keys_adv__max_rtt gauge
test_keys_adv__max_rtt{label="Maximum Round Trip Time"} %s
# TYPE test_keys_adv__min_rtt gauge
test_keys_adv__min_rtt{label="Minimum Round Trip Time"} %s
# TYPE test_keys_adv__mss gauge
test_keys_adv__mss{label="mss"} %s
# TYPE test_keys_adv__out_of_order gauge
test_keys_adv__out_of_order{label="out_of_order"} %s
# TYPE test_keys_adv__packet_loss gauge
test_keys_adv__packet_loss{label="Percent Packet Loss"} %s
# TYPE test_keys_adv__recv_lim gauge
test_keys_adv__recv_lim{label="Receiver Limited Ratio"} %s
# TYPE test_keys_adv__send_lim gauge
test_keys_adv__send_lim{label="Sender Limited Ratio"} %s
# TYPE test_keys_adv__timeouts gauge
test_keys_adv__timeouts{label="Timeouts"} %s
# TYPE test_keys_simple__download gauge
test_keys_simple__download{label="Download Speed"} %s
# TYPE test_keys_simple__ping gauge
test_keys_simple__ping{label="Ping Test"} %s
# TYPE test_keys_simple__upload gauge
test_keys_simple__upload{label="Upload Speed"} %s
# TYPE test_keys_summary_data__CWND-Limited gauge
test_keys_summary_data__CWND-Limited{label="CWND-Limited"} %s
# TYPE test_keys_summary_data__CWNDpeaks gauge
test_keys_summary_data__CWNDpeaks{label="CWNDpeaks"} %s
# TYPE test_keys_summary_data__Sndbuf gauge
test_keys_summary_data__Sndbuf{label="Sndbuf"} %s
# TYPE test_keys_summary_data__aspd gauge
test_keys_summary_data__aspd{label="aspd"} %s
# TYPE test_keys_summary_data__avgrtt gauge
test_keys_summary_data__avgrtt{label="avgrtt"} %s
# TYPE test_keys_summary_data__bad_cable gauge
test_keys_summary_data__bad_cable{label="bad_cable"} %s
# TYPE test_keys_summary_data__bw gauge
test_keys_summary_data__bw{label="bw"} %s
# TYPE test_keys_summary_data__c2sAck gauge
test_keys_summary_data__c2sAck{label="c2sAck"} %s
# TYPE test_keys_summary_data__c2sData gauge
test_keys_summary_data__c2sData{label="c2sData"} %s
# TYPE test_keys_summary_data__congestion gauge
test_keys_summary_data__congestion{label="congestion"} %s
# TYPE test_keys_summary_data__cwin gauge
test_keys_summary_data__cwin{label="cwin"} %s
# TYPE test_keys_summary_data__cwndtime gauge
test_keys_summary_data__cwndtime{label="cwndtime"} %s
# TYPE test_keys_summary_data__half_duplex gauge
test_keys_summary_data__half_duplex{label="half_duplex"} %s
# TYPE test_keys_summary_data__link gauge
test_keys_summary_data__link{label="link"} %s
# TYPE test_keys_summary_data__loss gauge
test_keys_summary_data__loss{label="loss"} %s
# TYPE test_keys_summary_data__maxCWNDpeak gauge
test_keys_summary_data__maxCWNDpeak{label="maxCWNDpeak"} %s
# TYPE test_keys_summary_data__minCWNDpeak gauge
test_keys_summary_data__minCWNDpeak{label="minCWNDpeak"} %s
# TYPE test_keys_summary_data__mismatch gauge
test_keys_summary_data__mismatch{label="mismatch"} %s
# TYPE test_keys_summary_data__order gauge
test_keys_summary_data__order{label="order"} %s
# TYPE test_keys_summary_data__rttsec gauge
test_keys_summary_data__rttsec{label="rttsec"} %s
# TYPE test_keys_summary_data__rwin gauge
test_keys_summary_data__rwin{label="rwin"} %s
# TYPE test_keys_summary_data__rwintime gauge
test_keys_summary_data__rwintime{label="rwintime"} %s
# TYPE test_keys_summary_data__s2cAck gauge
test_keys_summary_data__s2cAck{label="s2cAck"} %s
# TYPE test_keys_summary_data__s2cData gauge
test_keys_summary_data__s2cData{label="s2cData"} %s
# TYPE test_keys_summary_data__sendtime gauge
test_keys_summary_data__sendtime{label="sendtime"} %s
# TYPE test_keys_summary_data__spd gauge
test_keys_summary_data__spd{label="spd"} %s
# TYPE test_keys_summary_data__swin gauge
test_keys_summary_data__swin{label="swin"} %s
# TYPE test_keys_summary_data__timesec gauge
test_keys_summary_data__timesec{label="timesec"} %s
# TYPE test_keys_summary_data__waitsec gauge
test_keys_summary_data__waitsec{label="waitsec"} %s
# TYPE test_keys_test_c2s__connect_times gauge
test_keys_summary_data__test_c2s__connect_times{label="test_c2s__connect_times"} %s
# TYPE test_keys_test_c2s__params__num_streams gauge
test_keys_summary_data__test_c2s__params__num_streams{label="test_c2s__params__num_streams"} %s
# TYPE test_keys_test_c2s__receiver_data__avg_speed gauge
test_keys_summary_data__test_c2s__receiver_data__avg_speed{label="test_c2s__receiver_data__avg_speed"} %s
# TYPE test_keys_test_s2c__connect_times gauge
test_keys_summary_data__test_s2c__connect_times{label="test_s2c__connect_times"} %s
# TYPE test_keys_test_s2c__params__num_streams gauge
test_keys_summary_data__test_s2c__params__num_streams{label="test_s2c__params__num_streams"} %s
# TYPE test_keys_test_s2c__params__snaps_delay gauge
test_keys_summary_data__test_s2c__params__snaps_delay{label="test_s2c__params__snaps_delay"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__AckPktsIn gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__AckPktsIn{label="test_s2c__receiver_data__web100_data__AckPktsIn"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__AckPktsOut gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__AckPktsOut{label="test_s2c__receiver_data__web100_data__AckPktsOut"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__BytesRetrans gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__BytesRetrans{label="test_s2c__receiver_data__web100_data__BytesRetrans"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CongAvoid gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CongAvoid{label="test_s2c__receiver_data__web100_data__CongAvoid"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CongestionOverCount gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CongestionOverCount{label="test_s2c__receiver_data__web100_data__CongestionOverCount"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CongestionSignals gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CongestionSignals{label="test_s2c__receiver_data__web100_data__CongestionSignals"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CountRTT gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CountRTT{label="test_s2c__receiver_data__web100_data__CountRTT"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CurCwnd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CurCwnd{label="test_s2c__receiver_data__web100_data__CurCwnd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CurMSS gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CurMSS{label="test_s2c__receiver_data__web100_data__CurMSS"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CurRTO gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CurRTO{label="test_s2c__receiver_data__web100_data__CurRTO"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CurRwinRcvd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CurRwinRcvd{label="test_s2c__receiver_data__web100_data__CurRwinRcvd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CurRwinSent gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CurRwinSent{label="test_s2c__receiver_data__web100_data__CurRwinSent"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__CurSsthresh gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__CurSsthresh{label="test_s2c__receiver_data__web100_data__CurSsthresh"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__DSACKDups gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__DSACKDups{label="test_s2c__receiver_data__web100_data__DSACKDups"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__DataBytesIn gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__DataBytesIn{label="test_s2c__receiver_data__web100_data__DataBytesIn"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__DataBytesOut gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__DataBytesOut{label="test_s2c__receiver_data__web100_data__DataBytesOut"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__DataPktsIn gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__DataPktsIn{label="test_s2c__receiver_data__web100_data__DataPktsIn"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__DataPktsOut gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__DataPktsOut{label="test_s2c__receiver_data__web100_data__DataPktsOut"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__DupAcksIn gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__DupAcksIn{label="test_s2c__receiver_data__web100_data__DupAcksIn"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__DupAckOut gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__DupAckOut{label="test_s2c__receiver_data__web100_data__DupAckOut"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__Duration gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__Duration{label="test_s2c__receiver_data__web100_data__Duration"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__ECNEnabled gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__ECNEnabled{label="test_s2c__receiver_data__web100_data__ECNEnabled"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__FastRetran gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__FastRetran{label="test_s2c__receiver_data__web100_data__FastRetran"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MaxCwnd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MaxCwnd{label="test_s2c__receiver_data__web100_data__MaxCwnd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MaxMSS gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MaxMSS{label="test_s2c__receiver_data__web100_data__MaxMSS"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MaxRTO gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MaxRTO{label="test_s2c__receiver_data__web100_data__MaxRTO"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MaxRTT gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MaxRTT{label="test_s2c__receiver_data__web100_data__MaxRTT"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MaxRwinRcvd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MaxRwinRcvd{label="test_s2c__receiver_data__web100_data__MaxRwinRcvd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MaxRwinSent gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MaxRwinSent{label="test_s2c__receiver_data__web100_data__MaxRwinSent"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MaxSsthresh gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MaxSsthresh{label="test_s2c__receiver_data__web100_data__MaxSsthresh"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MinMSS gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MinMSS{label="test_s2c__receiver_data__web100_data__MinMSS"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MinRTO gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MinRTO{label="test_s2c__receiver_data__web100_data__MinRTO"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MinRTT gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MinRTT{label="test_s2c__receiver_data__web100_data__MinRTT"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MinRwinRcvd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MinRwinRcvd{label="test_s2c__receiver_data__web100_data__MinRwinRcvd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__MinRwinSent gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__MinRwinSent{label="test_s2c__receiver_data__web100_data__MinRwinSent"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__NagleEnabled gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__NagleEnabled{label="test_s2c__receiver_data__web100_data__NagleEnabled"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__OtherReductions gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__OtherReductions{label="test_s2c__receiver_data__web100_data__OtherReductions"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__PktsIn gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__PktsIn{label="test_s2c__receiver_data__web100_data__PktsIn"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__PktsOut gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__PktsOut{label="test_s2c__receiver_data__web100_data__PktsOut"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__PktsRetrans gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__PktsRetrans{label="test_s2c__receiver_data__web100_data__PktsRetrans"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__RcvWinScale gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__RcvWinScale{label="test_s2c__receiver_data__web100_data__RcvWinScale"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SACKEnabled gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SACKEnabled{label="test_s2c__receiver_data__web100_data__SACKEnabled"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SACKsRcvd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SACKsRcvd{label="test_s2c__receiver_data__web100_data__SACKsRcvd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SampleRTT gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SampleRTT{label="test_s2c__receiver_data__web100_data__SampleRTT"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SendStall gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SendStall{label="test_s2c__receiver_data__web100_data__SendStall"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SlowStart gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SlowStart{label="test_s2c__receiver_data__web100_data__SlowStart"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SmoothedRTT gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SmoothedRTT{label="test_s2c__receiver_data__web100_data__SmoothedRTT"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimBytesCwnd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimBytesCwnd{label="test_s2c__receiver_data__web100_data__SndLimBytesCwnd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimBytesRwin gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimBytesRwin{label="test_s2c__receiver_data__web100_data__SndLimBytesRwin"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimBytesSender gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimBytesSender{label="test_s2c__receiver_data__web100_data__SndLimBytesSender"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimTimeCwnd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimTimeCwnd{label="test_s2c__receiver_data__web100_data__SndLimTimeCwnd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimTimeRwin gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimTimeRwin{label="test_s2c__receiver_data__web100_data__SndLimTimeRwin"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimTimeSender gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimTimeSender{label="test_s2c__receiver_data__web100_data__SndLimTimeSender"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimTransCwnd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimTransCwnd{label="test_s2c__receiver_data__web100_data__SndLimTransCwnd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimTransRwin gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimTransRwin{label="test_s2c__receiver_data__web100_data__SndLimTransRwin"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndLimTransSender gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndLimTransSender{label="test_s2c__receiver_data__web100_data__SndLimTransSender"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SndWinScale gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SndWinScale{label="test_s2c__receiver_data__web100_data__SndWinScale"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__StartTimeUsec gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__StartTimeUsec{label="test_s2c__receiver_data__web100_data__StartTimeUsec"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SubsequentTimeeouts gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SubsequentTimeeouts{label="test_s2c__receiver_data__web100_data__SubsequentTimeeouts"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__SumRTT gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__SumRTT{label="test_s2c__receiver_data__web100_data__SumRTT"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__Timeouts gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__Timeouts{label="test_s2c__receiver_data__web100_data__Timeouts"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__TimestampsEnabled gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__TimestampsEnabled{label="test_s2c__receiver_data__web100_data__TimestampsEnabled"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__WinScaleRcvd gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__WinScaleRcvd{label="test_s2c__receiver_data__web100_data__WinScaleRcvd"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__WinScaleSent gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__WinScaleSent{label="test_s2c__receiver_data__web100_data__WinScaleSent"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__X_Rcvbuf gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__X_Rcvbuf{label="test_s2c__receiver_data__web100_data__X_Rcvbuf"} %s
# TYPE test_keys_test_s2c__receiver_data__web100_data__X_Sndbuf gauge
test_keys_summary_data__test_s2c__receiver_data__web100_data__X_Sndbuf{label="test_s2c__receiver_data__web100_data__X_Sndbuf"} %s
EOF""" % (

# TYPE test_keys_test_c2s__sender_data_# gauge
# test_keys_summary_data__sender_data{label="test_c2s__sender_data"} %s

# TYPE test_keys_test_s2c__receiver_data__# gauge
#test_keys_summary_data__test_s2c__receiver_data__#{label="test_s2c__receiver_data__#"} %s

    str(pushgw),
    dev_loc,
    str(data['test_keys']['advanced']['avg_rtt']),
    str(data['test_keys']['advanced']['congestion_limited']),
    str(data['test_keys']['advanced']['fast_retran']),
    str(data['test_keys']['advanced']['max_rtt']),
    str(data['test_keys']['advanced']['min_rtt']),
    str(data['test_keys']['advanced']['mss']),
    str(data['test_keys']['advanced']['out_of_order']),
    str(data['test_keys']['advanced']['packet_loss']),
    str(data['test_keys']['advanced']['receiver_limited']),
    str(data['test_keys']['advanced']['sender_limited']),
    str(data['test_keys']['advanced']['timeouts']),
    str(data['test_keys']['simple']['download']),
    str(data['test_keys']['simple']['ping']),
    str(data['test_keys']['simple']['upload']),
    str(data['test_keys']['summary_data']['CWND-Limited']),
    str(data['test_keys']['summary_data']['CWNDpeaks']),
    str(data['test_keys']['summary_data']['Sndbuf']),
    str(data['test_keys']['summary_data']['aspd']),
    str(data['test_keys']['summary_data']['avgrtt']),
    str(data['test_keys']['summary_data']['bad_cable']),
    str(data['test_keys']['summary_data']['bw']),
    str(data['test_keys']['summary_data']['c2sAck']),
    str(data['test_keys']['summary_data']['c2sData']),
    str(data['test_keys']['summary_data']['congestion']),
    str(data['test_keys']['summary_data']['cwin']),
    str(data['test_keys']['summary_data']['cwndtime']),
    str(data['test_keys']['summary_data']['half_duplex']),
    str(data['test_keys']['summary_data']['link']),
    str(data['test_keys']['summary_data']['loss']),
    str(data['test_keys']['summary_data']['maxCWNDpeak']),
    str(data['test_keys']['summary_data']['minCWNDpeak']),
    str(data['test_keys']['summary_data']['mismatch']),
    str(data['test_keys']['summary_data']['order']),
    str(data['test_keys']['summary_data']['rttsec']),
    str(data['test_keys']['summary_data']['rwin']),
    str(data['test_keys']['summary_data']['rwintime']),
    str(data['test_keys']['summary_data']['s2cAck']),
    str(data['test_keys']['summary_data']['s2cData']),
    str(data['test_keys']['summary_data']['sendtime']),
    str(data['test_keys']['summary_data']['spd']),
    str(data['test_keys']['summary_data']['swin']),
    str(data['test_keys']['summary_data']['timesec']),
    str(data['test_keys']['summary_data']['waitsec']),
    str(data['test_keys']['summary_data']['test_c2s']['connect_times']),
    str(data['test_keys']['summary_data']['test_c2s']['params']['num_streams']),
    str(data['test_keys']['summary_data']['test_c2s']['receiver_data']['avg_speed']),
#    str(data['test_keys']['summary_data']['test_c2s']['sender_data']['#']),
    str(data['test_keys']['summary_data']['test_s2c']['connect_times']),
    str(data['test_keys']['summary_data']['test_s2c']['params']['num_streams']),
    str(data['test_keys']['summary_data']['test_s2c']['params']['snaps_delay']),
#    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['#']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['AckPktsIn']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['AckPktsOut']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['BytesRetrans']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CongAvoid']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CongestionOverCount']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CongestionSignals']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CountRTT']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CurCwnd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CurMSS']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CurRTO']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CurRwinRcvd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CurRwinSent']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['CurSsthresh']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DSACKDups']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DataBytesIn']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DataBytesOut']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DataPktsIn']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DataPktsOut']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DataAcksIn']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DataAcksOut']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DupAcksIn']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['DupAcksOut']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['Duration']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['ECNEnabled']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['FastRetran']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MaxCwnd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MaxMSS']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MaxRTO']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MaxRTT']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MaxRwinRcvd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MaxRwinSent']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MaxSsthresh']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MinMSS']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MinRTO']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MinRTT']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MinRwinRcvd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['MinRwinSent']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['NagleEnabled']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['Otherreductions']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['PktsIn']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['PktsOut']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['PktsRetrans']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['RcvWinScale']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SACKEnabled']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SACKsRcvd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SampleRTT']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SendStall']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SlowStart']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SmoothedRTT']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimBytesCwnd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimBytesRwin']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimBytesSender']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimTimeCwnd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimTimeRwin']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimTimeSender']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimTransCwnd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimTransRwin']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndLimTransSender']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SndWinScale']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['StartTimeUsec']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SubequentTimeouts']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['SumRTT']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['Timeouts']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['TimestampsEnabled']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['WinScaleRcvd']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['WinScaleSent']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['X_Rcvbuf']),
    str(data['test_keys']['summary_data']['test_s2c']['receiver_data']['web100_data']['X_Sndbuf'])
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
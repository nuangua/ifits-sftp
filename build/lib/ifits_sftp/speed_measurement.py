#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading
from collections import deque
import sys, os
import time
import datetime
import psutil
import platform
from ifits_sftp import config
from ifits_sftp import sftp
from ifits_sftp import geolocation as geo
import json
import uuid
import socket
import requests
from uuid import getnode


from ifits_aws import config as ifitsaws_config
from ifits_aws.data import ciphering
from ifits_aws.dynamodb import operations

def calc_speeds(rate, dt=3, interface='Wi-Fi'):
    t0 = time.time()
    counter = psutil.net_io_counters(pernic=True)[interface]
    last_tot = (counter.bytes_sent, counter.bytes_recv)

    while True:
        time.sleep(dt)
        t1 = time.time()
        counter = psutil.net_io_counters(pernic=True)[interface]
        tot = (counter.bytes_sent, counter.bytes_recv)
        ul, dl = [(now - last) / (t1 - t0) / 1000.0
                  for now, last in zip(tot, last_tot)]
        # print("ul=%.1f, dl=%.1f,tot=%s,last_tot=%s" % (ul, dl, tot, last_tot))
        rate.append((ul, dl))
        t0 = t1
        last_tot = tot


def print_rate(rate):
    try:
        print 'UL: {0:.0f} kB/s / DL: {1:.0f} kB/s'.format(*rate[-1])
    except IndexError:
        'UL: - kB/s/ DL: - kB/s'

def average_rate(rate_list):
    average_ul = 0.0
    average_dl = 0.0
    for rate in rate_list:
        print("rate=%s" % (rate))

        try:
            #print 'UL: {0:.1f} kB/s / DL: {1:.1f} kB/s'.format(*rate[-1])
            ul_rate = round(rate[-1][0], 1)
            dl_rate = round(rate[-1][1], 1)
            average_ul += ul_rate
            average_dl += dl_rate
        except IndexError:
            'UL: - kB/s/ DL: - kB/s'
    return (average_ul, average_dl)

# detect current active interfaces
def detect_active_interfaces():
    active_interfaces = []
    io_counters = psutil.net_io_counters(pernic=True)
    for key,value in io_counters.iteritems():
        if value.bytes_sent != 0 and value.bytes_recv != 0 and value.packets_sent != 0 and value.packets_recv != 0:
            active_interfaces.append(key)
    return active_interfaces


class Speed(object):

    def __init__(self):
        self.last_avg = 0.0
        self.active_interfaces = self.detect_active_interfaces()
        self.transfer_rate_list = []
        print("self.active_interfaces=%s" % (self.active_interfaces))
        for index, interface in enumerate(self.active_interfaces):
            # Create the ul/dl thread and a deque of length 1 to hold the ul/dl- values
            self.transfer_rate_list.append(deque(maxlen=1))
            thread_instance = threading.Thread(target=self.calc_speeds, args=(self.transfer_rate_list[index], 5, interface,))

            # The program will exit if there are only daemonic threads left.
            thread_instance.daemon = True
            thread_instance.start()

    def calc_speeds(self, rate, delay_time=3, interface='Wi-Fi'):
        t0 = time.time()
        counter = psutil.net_io_counters(pernic=True)[interface]
        last_tot = (counter.bytes_sent, counter.bytes_recv)

        while True:
            time.sleep(delay_time)
            t1 = time.time()
            counter = psutil.net_io_counters(pernic=True)[interface]
            tot = (counter.bytes_sent, counter.bytes_recv)
            ul, dl = [(now - last) / (t1 - t0) / 1000.0
                      for now, last in zip(tot, last_tot)]
            #print("ul=%.1f, dl=%.1f,tot=%s,last_tot=%s" % (ul, dl, tot, last_tot))
            rate.append((ul, dl))
            #rate = (ul, dl)
            t0 = t1
            last_tot = tot

    def average_rate(self):
        average_ul = 0.0
        average_dl = 0.0
        #print(self.transfer_rate_list)
        for rate in self.transfer_rate_list:
            try:
                # print 'UL: {0:.1f} kB/s / DL: {1:.1f} kB/s'.format(*rate[-1])
                ul_rate = round(rate[-1][0], 1)
                dl_rate = round(rate[-1][1], 1)
                average_ul += ul_rate
                average_dl += dl_rate
            except IndexError:
                'UL: - kB/s/ DL: - kB/s'
        #print("average_ul=%.1f, average_dl=%.1f" % (average_ul, average_dl))
        return (average_ul, average_dl)

    # detect current active interfaces
    def detect_active_interfaces(self):
        active_interfaces = []
        """
        io_counters = psutil.net_io_counters(pernic=True)
        for key,value in io_counters.iteritems():
            if value.bytes_sent != 0 and value.bytes_recv != 0 and value.packets_sent != 0 and value.packets_recv != 0:
                active_interfaces.append(key)
        if 'Ethernet' in active_interfaces:
            active_interfaces = ['Ethernet']
        """
        info = psutil.net_if_addrs()
        for k, v in info.items():
            for item in v:
                if item[0] == 2 and '127.0.0.1' not in item[1] and '192.168' not in item[1] and '169.254' not in item[1]:
                    active_interfaces.append(k)
        return active_interfaces



def get_basic_data():
    meta_data = {}
    while len(meta_data.keys()) == 0:
        try:
            data = requests.get('http://ipinfo.io').json()
            print("data=%s" % (str(data)))
            meta_data.update(data)
        except:
            print("get meta_data failed, wait for 2 seconds and try again!")
            data = geo.get_ipinfo()
            print("data=%s" % (str(data)))
            meta_data.update(data)
            time.sleep(2)
    meta_data["mac"] = str(getnode())
    meta_data["uuid"] = str(uuid.uuid1())
    return meta_data

if __name__ == "__main__":

    GUID = uuid.uuid1()

    eof = ""

    if platform.system() == "Windows":
        eof = "\r"
    elif platform.system() == "Linux":
        eof = "\n"
    elif platform.system() == "Darwin":
        eof = "\r"
    RESULT_FILE_NAME = "sftp_rates_results_%i.csv" % (int(time.time()))
    RESULT_PATH = os.path.join(os.path.expanduser('~'), 'Documents', 'sftp')
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)
    RESULT_FILE_PATH = os.path.join(RESULT_PATH, RESULT_FILE_NAME)
    file = open(RESULT_FILE_PATH, 'a')
    HEAD = r"guid,uuid,timestamp,datetime,mac,ip,region,country,city,loc,org,test_type,ul_rate,dl_rate,updated" + str(eof)
    file.write(HEAD)
    file.flush()

    meta_data = get_basic_data()
    print("meta_data=%s" % (str(meta_data)))
    FILESIZE = 40 * 1024 * 1024
    ul_test = sftp.SftpTest(FILESIZE, config.SFTP_TRANSFER_UL, 10, overwrite=True)
    ul_test.start()
    time.sleep(3)
    ul_speed = Speed()
    while not ul_test.is_finished():
        time.sleep(7)
        (ul_rate, dl_rate) = ul_speed.average_rate()
        print("ul_rate=%.2f, dl_rate=%.2f" % (float(round(ul_rate, 2)), float(round(dl_rate, 2))))
        ul_data = {}
        ul_data.update(meta_data)
        now = time.time()
        ul_data["guid"] = str(GUID)
        ul_data["timestamp"] = str(now)
        ul_data["datetime"] = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S.%M')
        ul_data["test_type"] = config.SFTP_TRANSFER_UL
        ul_data["ul_rate"] = float(round(ul_rate, 2))
        ul_data["dl_rate"] = float(round(dl_rate, 2))
        ul_data["updated"] = "0"
        print(json.dumps(ul_data))
        line_data = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            ul_data["guid"],ul_data["uuid"], ul_data["timestamp"],ul_data["datetime"],ul_data["mac"], ul_data["ip"],\
            ul_data["region"],ul_data["country"], ul_data["city"], ul_data["loc"].replace(",",":"),ul_data["org"], \
            ul_data["test_type"],ul_data["ul_rate"],ul_data["dl_rate"],ul_data["updated"]
        )
        line_data += str(eof)
        file.write(line_data)
        file.flush()

        encrypted_data = ciphering.encrypt_schedule_json(ul_data, ifitsaws_config.CIPHER_RATE_OBJECT)
        #print("encrypted_data=%s" % (encrypted_data))
        JSONPayload = json.dumps(encrypted_data)
        operations.insert_or_update_object(encrypted_data, ifitsaws_config.CIPHER_RATE_OBJECT)

    ul_test.join()

    meta_data = get_basic_data()
    print("meta_data=%s" % (str(meta_data)))

    dl_test = sftp.SftpTest(FILESIZE, config.SFTP_TRANSFER_DL, 10, overwrite=True)
    dl_test.start()
    time.sleep(3)
    dl_speed = Speed()
    while not dl_test.is_finished():
        time.sleep(7)
        (ul_rate, dl_rate) = dl_speed.average_rate()
        print("ul_rate=%.2f, dl_rate=%.2f" % (float(round(ul_rate, 2)), float(round(dl_rate, 2))))
        dl_data = {}
        dl_data.update(meta_data)
        now = time.time()
        dl_data["guid"] = str(GUID)
        dl_data["timestamp"] = str(now)
        dl_data["datetime"] = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S.%M')
        dl_data["test_type"] = config.SFTP_TRANSFER_DL
        dl_data["ul_rate"] = float(round(ul_rate, 2))
        dl_data["dl_rate"] = float(round(dl_rate, 2))
        dl_data["updated"] = "0"
        print(json.dumps(dl_data))
        line_data = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            dl_data["guid"], dl_data["uuid"], dl_data["timestamp"], dl_data["datetime"], dl_data["mac"], dl_data["ip"], \
            dl_data["region"], dl_data["country"],dl_data["city"], dl_data["loc"].replace(",",":"), dl_data["org"], \
            dl_data["test_type"], dl_data["ul_rate"], dl_data["dl_rate"],dl_data["updated"]
        )
        line_data += str(eof)
        file.write(line_data)
        file.flush()

        encrypted_data = ciphering.encrypt_schedule_json(dl_data, ifitsaws_config.CIPHER_RATE_OBJECT)
        #print("encrypted_data=%s" % (encrypted_data))
        JSONPayload = json.dumps(encrypted_data)
        operations.insert_or_update_object(encrypted_data, ifitsaws_config.CIPHER_RATE_OBJECT)

    dl_test.join()

    file.close()
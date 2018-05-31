#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import requests
import geoip2.database
from ifits_sftp import config

PUBLIC_IP_ADDRESS = requests.get('http://ip.42.pl/raw').text


def get_ipinfo(public_ip=PUBLIC_IP_ADDRESS):
    ipinfo = {}
    if public_ip == None or public_ip == "":
        return None
    ipinfo['ip'] = public_ip
    with geoip2.database.Reader(os.path.join(config.GEOIP_PATH, config.GEOIP_CITY)) as reader:
        response = reader.city(public_ip)
        ipinfo['city'] = response.city.name
        ipinfo['country'] = response.country.name
        #ipinfo['country'] = response.country.iso_code
        ipinfo['region'] = response.continent.name
        ipinfo['loc'] = "%.4f:%.4f" % (response.location.latitude, response.location.longitude)

    with geoip2.database.Reader(os.path.join(config.GEOIP_PATH, config.GEOIP_ASN)) as reader:
        response = reader.asn(public_ip)
        ipinfo['org'] = "AS%s %s" % (str(response.autonomous_system_number), str(response.autonomous_system_organization))
    return ipinfo

if __name__=="__main__":
    ipinfo = get_ipinfo()
    print(json.dumps(ipinfo))
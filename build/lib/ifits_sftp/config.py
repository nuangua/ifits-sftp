#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from idata_security import config, ciphering
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#: geoip2 configuration, reference to https://dev.maxmind.com/geoip/geoip2/geolite2/
GEOIP_PATH = os.path.join(BASE_DIR, "geo_datasets")
GEOIP_COUNTRY = "GeoLite2-Country.mmdb"
GEOIP_CITY = "GeoLite2-City.mmdb"
GEOIP_ASN = "GeoLite2-ASN.mmdb"

SFTP_HOSTNAME = r"esft.intel.com"
SFTP_USERNAME = r"sys_intel_ifits_prod"
SFTP_PASSWORD = ciphering.decrypt_data("uX2yXwQlxUIKAqGU/yaxJ9A+Pr7i4aecxjcGElUWCUvqzRey/7DgsFNXPmtFmJIOwxLsDPnGSf+9I+ys+BwfbUp4WcYaeGFRiXzFq4gKT0VH2I+66L0caW1UUSoICeM31T7k4adzDscdqD2kdnRDR8A4jXdj0AxSMfsdJhKS581YtiX/nwY70ZffbKBGuD9YZEWD8SUgHqCK9DbaBqVBNqIYA/CQM4Lbb1rc/Muc5i3vFNziFi8qJUl2CfVIQD7s6xePWsIQe4vDhPC60TX7p0bXm987w2uTdyEclBqzNe66BXCTgJfbntyv8o33CnMtoKOeeAPr1sU4bFe14oLnI9koA1w9RjM/BH9ZP6PzQL/QDENJmXD1xmkFodNORNzKE6yGA68Fs0ai867fQEQMsypltwz8Oa7XNbc0J02eV2Jyl5Nrd1Q+VXwWqLwqOxTCEVj5ORwyEBGwvYeqvZebdEGMb8ceOXIWIzhH0j8fuYHsu53mV7buX29OpTPeT8Us3CDaX0rFmUplzmJDngJPaTawt8EkjXnoKK814IdM0E3F8onHSojMnSW7Y6TPxLFwgWsiJlJKL0Ym28MhNeqVYs+iWy8yzTSDonj6Kkk940FOGzaK5/4Im88WY5mnW4hTWfjR19tqDnY9WU5ur2TyKj0eZAxwyhup4Nt8lvgh5Rc=", ciphering.load_ifits_private_key())

SFTP_BASE_PATH = r"/00_FT_IFITS"
SFTP_ARTEFACTS_PATH = SFTP_BASE_PATH + r"/ARTEFACTS"
SFTP_BUILDS_PATH = SFTP_ARTEFACTS_PATH + r"/BUILDS"
SFTP_NVM_PATH = SFTP_ARTEFACTS_PATH + r"/CUST_NVM"
SFTP_SCRIPTS_PATH = SFTP_ARTEFACTS_PATH + r"/POST_PROCESSING_SCRIPTS"
SFTP_POST_SCRIPTS_PATH = SFTP_ARTEFACTS_PATH + r"/POST_PROCESSING_SCRIPTS"
SFTP_TEST_SCRIPTS_PATH = SFTP_ARTEFACTS_PATH + r"/TEST_SCRIPTS"
SFTP_TOOLS_PATH = SFTP_ARTEFACTS_PATH + r"/TOOLS"

SFTP_QC_PATH = SFTP_BASE_PATH + r"/QC_EXPORT"
SFTP_TRACES_PATH = SFTP_BASE_PATH + r"/TRACES"

SFTP_TRANSFER_UL = "upload"
SFTP_TRANSFER_DL = "download"
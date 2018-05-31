#!/bin/bash

yum install gcc python-devel -y
pip install -U pip setuptools sphinx
pip install -U idata-security-1.0.3.tar.gz
pip install -U ifits-utils-1.0.2.tar.gz
pip install -U ifits-aws-1.1.0.tar.gz
pip install -U ifits-sftp-1.0.2.tar.gz

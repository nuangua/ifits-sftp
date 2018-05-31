# ifits-sftp

ifits-sftp library provides APIs and tools for sftp server testing.

## Documentation

Detailed documentation on [GitHub Wiki](https://github.intel.com/ft/ifits-sftp/wiki).

## Installation

* pip install Sphinx
* pip install -U https://github.intel.com/idata/idata-security/raw/master/dist/idata-security-1.0.3.tar.gz
(or pip install -U git+https://github.intel.com/idata/idata-security.git)
* pip install -U https://github.intel.com/ft/ifits-utils/raw/master/dist/ifits-utils-1.0.2.tar.gz
(or pip install -U git+https://github.intel.com/ft/ifits-utils.git)
* pip install -U https://github.intel.com/ft/ifits-aws/raw/master/dist/ifits-aws-1.1.0.tar.gz
(or pip install -U git+https://github.intel.com/ft/ifits-aws.git)
* pip install -U https://github.intel.com/ft/ifits-sftp/raw/master/dist/ifits-sftp-1.0.2.tar.gz
(or pip install -U https://github.intel.com/ft/ifits-sftp/raw/master/dist/ifits_sftp-1.0.2-py2-none-any.whl)
(or pip install -U git+https://github.intel.com/ft/ifits-sftp.git)

## Usage

### Command Line Tools

* ifits-sftp_test

    ifits-sftp_test is a command line program. When you install ifits-sftp library, a ifits-sftp_test command is added to your system, which can be run from the command prompt as follows:

    > ifits-sftp_test

    If you cannot run the ifits-sftp_test command directly(possibly because the location it was installed isn't on your operatoring system's PATH) then you can run ifits-sftp_test with the Python interpreter:

    >python -m ifits_sftp.speed_measurement


### Python APIs


## Development

* install git client
* run command `git clone https://github.intel.com/ft/ifits-sftp.git` to download source codes to local path
* run command `python setup.py bdist_wheel` to build an individual wheel
* run command `python setup.py sdist` to build an individual source codes package

## Features

## Future Plans

## Latest Changes

## License

Copyright &copy; 2017

Intel FT TECH

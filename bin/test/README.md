# ifits-sftp_test

ifits-sftp_test is to test sftp server upload and download prformance.

# Preconditions

* OS: Windows
* Python: 2.7 is tested, python3 is not tested. If python environment on your test machine is not ready, please install [python2.7.14](https://github.intel.com/ft/ifits-sftp/raw/master/bin/test/python-2.7.14.amd64.msi) and configure python environment as below

![configure python environment variables](https://github.intel.com/ft/ifits-sftp/raw/master/docs/snapshots/config_python_env_vars.png)


## Installation

* download [mysetup.exe](https://github.intel.com/ft/ifits-sftp/raw/master/bin/test/mysetup.exe) and install it to the default path on the test machine(windows OS). The installation password is 'run?SFTS1!'

* connect the test machine to internet

* Go to path C:\Tools\ifits-sftp, click the install.cmd to install the ifits-sftp and its dependencies

* make sure the system time zone and date time is correct with your local time zone and date time.

![correct time zon and date time](https://github.intel.com/ft/ifits-sftp/raw/master/docs/snapshots/correct_timezone_and_datetime.png)

* run command 'python -m ifits_sftp.speed_measurement' to start test. If any problem, please contact with David Koo(nuanguang.gu@intel.com) for help.

![test step 1](https://github.intel.com/ft/ifits-sftp/raw/master/bin/test/test_pic1.png)

![test step 2](https://github.intel.com/ft/ifits-sftp/raw/master/bin/test/test_pic2.png)

![test step 3](https://github.intel.com/ft/ifits-sftp/raw/master/bin/test/test_pic3.png)

* test results data. After finished testing, the testing data will save to ~\Documents\sftp\, also the testing data will be updated to aws dynamoDB automatically during testing. So you don't need do anything after it's finished.

![test step 4](https://github.intel.com/ft/ifits-sftp/raw/master/bin/test/test_pic4.png)

## Usage

* run command 'python -m ifits_sftp.speed_measurement'

## Features

## Future Plans

## Latest Changes

## License

Copyright &copy; 2017

Intel FT TECH

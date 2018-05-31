#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import threading
import pysftp
from ifits_sftp import config
from ifits_utils import files_generator
import numpy as np
from uuid import getnode

try:
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None    # disable host key checking.
    print("#################################################################################")
    print("above exception is normal, please ignore it! It's ready to start testing...")
    print("#################################################################################")
except:
    print("disable host key checking...")

class SftpClient(threading.Thread):

    def __init__(self, filename, local_path, remote_path, transfer_type, overwrite=True):
        super(SftpClient, self).__init__()
        self.transferred = 0.0
        self.totalToBeTransferred = 0.0
        self.filename = filename
        self.local_path = local_path
        self.remote_path = remote_path
        self.transfer_type = transfer_type
        self.overwrite = overwrite
        self.is_finished = False

    def run(self):
        self.transfer_files(self.filename, self.local_path, self.remote_path, self.transfer_type, self.overwrite)

    def progress_callback(self, transferred, totalToBeTransferred):
        percents = round(100.0 * transferred / float(totalToBeTransferred), 1)
        print("percentage=%s %%" % (str(percents)))
        self.transferred = transferred
        self.totalToBeTransferred = totalToBeTransferred
        if percents == 100.0:
            self.is_finished = True

    # transfer files to sftp server
    def transfer_files(self, filename, local_path, remote_path, transfer_type, overwrite=True):
        local_file_path = os.path.join(local_path, filename)
        remote_file_path = remote_path + "/" + filename
        if transfer_type==config.SFTP_TRANSFER_UL and not os.path.exists(local_file_path):
            print("the uploaded file %s not exist. Please check it before uploading it!" % (local_file_path))
            return False
        with pysftp.Connection(config.SFTP_HOSTNAME, username=config.SFTP_USERNAME,password=config.SFTP_PASSWORD, cnopts=cnopts) as sftp:
            if transfer_type==config.SFTP_TRANSFER_DL and not sftp.exists(remote_file_path):
                print("the downloaded file %s not exist. Please check it before downloading it!" % (remote_file_path))
                return False
            if transfer_type == config.SFTP_TRANSFER_UL:
                if not sftp.exists(remote_file_path) or overwrite:
                    with pysftp.cd(local_path):
                        with sftp.cd(remote_path):
                            sftp.put(filename, callback=self.progress_callback, preserve_mtime=False)
                if sftp.exists(remote_file_path) and sftp.isfile(remote_file_path):
                    return True
                else:
                    return False
            elif transfer_type == config.SFTP_TRANSFER_DL:
                if not os.path.exists(local_file_path) or overwrite:
                    with pysftp.cd(local_path):
                        with sftp.cd(remote_path):
                            sftp.get(filename, callback=self.progress_callback, preserve_mtime=False)
                if os.path.exists(local_file_path) and os.path.isfile(local_file_path):
                    return True
                else:
                    return False

class SftpTest(object):

    def __init__(self, filesize, transfer_type, thread_num, overwrite=True):
        self.transfer_thread_list = []
        self.filesize = filesize
        self.thread_num = thread_num
        self.overwrite = overwrite

        for iter in range(self.thread_num):
            filepath = files_generator.get_or_create_file(filesize, "filesize_mac_%s_%s_%s.txt" % (str(filesize), str(getnode()), str(iter)))
            dirname = os.path.dirname(filepath)
            filename = os.path.basename(filepath)
            ul = SftpClient(filename, dirname, config.SFTP_BUILDS_PATH, transfer_type, overwrite=overwrite)
            self.transfer_thread_list.append(ul)

    def start(self):
        for transfer_thread in self.transfer_thread_list:
            transfer_thread.start()

    def is_finished(self):
        finished_list = []
        for transfer_thread in self.transfer_thread_list:
            finished_list.append(transfer_thread.is_finished)
        aver = np.average(finished_list)
        return True if aver == 1 else False

    def join(self):
        for transfer_thread in self.transfer_thread_list:
            #print("###before join")
            transfer_thread.join()
            #print("###after join")

if __name__ == "__main__":

    FILESIZE = 10*1024*1024

    ul_test = SftpTest(FILESIZE, config.SFTP_TRANSFER_UL, 10, overwrite=True)
    print("start uploading files...")
    ul_test.start()
    ul_test.join()
    print("stop uploading files...")

    dl_test = SftpTest(FILESIZE, config.SFTP_TRANSFER_DL, 10, overwrite=True)
    print("start downloading files...")
    dl_test.start()
    dl_test.join()
    print("stop downloading files...")
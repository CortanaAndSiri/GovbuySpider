# -*- coding: UTF-8 -*-
import paramiko
import os
import datetime


# hostname = "47.97.188.209"
# username = "root"
# password = "ka!Gov28"
# port = 22
hostname = "47.110.90.14"
username = "root"
password = "GovBuy2018!"
port = 22


def upload(local_dir, remote_dir):
    # 实例化一个对象
    transport = paramiko.Transport((hostname, port))
    # 建立连接
    transport.connect(username=username, password=password)
    # 实例化一个sftp对象，指定连接通道
    sftp = paramiko.SFTPClient.from_transport(transport)
    starttime = datetime.datetime.now()
    for root, dirs, files in os.walk(local_dir):
      # print(root)
        remote_list = sftp.listdir(remote_dir)
      # print(remote_dir)
        # 去重
        upload_files = list(set(files) - set(remote_list))
      # print(len(upload_files))
        # 上传文件
        for filename in upload_files:
            local_filepath = os.path.join(root, filename)
            # print(root)
          # print(local_filepath)
            remote_filepath = os.path.join(remote_dir, filename)
            sftp.put(local_filepath, remote_filepath)
    endtime = datetime.datetime.now()

  # print(endtime-starttime)
    transport.close()


upload(r"D:/doc&pdf&png/full", r"/data/static_file/full/")

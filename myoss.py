# -*- coding: utf-8 -*-

import os
#import shutil
import oss2

#---------------------------
# upload_file_to_oss
#---------------------------
def upload_file_to_oss(config,oss_filename, local_filename):
    try:
        access_key_id = config['access_key_id']
        access_key_secret = config['access_key_secret']
        bucket_name = config['bucket_name']
        endpoint = config['endpoint']
        bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
        bucket.put_object_from_file(oss_filename, local_filename)
        return 0
    except Exception as e:
        print(str(e))
        return -1

#---------------------------
# main
#---------------------------
if __name__ == "__main__":
    config = {"duration": 60,
              "access_key_id": "xxx",
              "access_key_secret": "yyy",
              "bucket_name": "pm25-sensor-img",
              "endpoint": "https://oss-cn-hangzhou.aliyuncs.com"}
    retcode = upload_file_to_oss(config,'hello-' + str(time.time()) + '.txt','hello.txt')
    print('retcode:',retcode)
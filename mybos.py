# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Samples for bos client.
"""

import os
import random
import string
import traceback

from baidubce import exception
from baidubce.services.bos import canned_acl
from baidubce.services.bos.bos_client import BosClient

import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


logger = logging.getLogger('baidubce.services.bos.bosclient')
fh = logging.FileHandler('sample.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)


def _create_file(file_name, size):
    """Create a file with the file size is size"""
    file = open(file_name, "w")
    file.seek(size)
    file.write('\x00')
    file.close()

def _random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    
def file_upload_bos(config,local_filename):
    try:
        bucket_name = config['bucket_name']
        bucket_name = str(bucket_name)
        
        #p = config['dir']
        AK = config['AK']
        SK = config['SK']
        HOST = config['HOST']
    
        #print('step 1')
        #print('file name:',local_filename)
        bos_config = BceClientConfiguration(credentials=BceCredentials(str(AK), str(SK)),endpoint=str(HOST))
        bos_client = BosClient(bos_config)

        #print('step 2')
        #print 'bucket_name:',bucket_name,type(bucket_name)
        if not bos_client.does_bucket_exist(bucket_name):
            bos_client.create_bucket(bucket_name)

        #print('step 3')            
        key = str(local_filename.split('/')[-1])
        #print('key:',key)
        bos_client.put_object_from_file(bucket_name, str(key), str(local_filename))
        print(local_filename + ' has been uploaded to bucket:' + bucket_name)
        return 0
    except Exception as e:
        print('file_upload_bos exception:' + str(e))
        traceback.print_exc()  
        return -1

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    source_bucket = 'sourcebucket'
    target_bucket = 'targetbucket'
    source_key = 'sourcekey' + _random_string(6)
    target_key = 'targetkey' + _random_string(6)
    prefix = 'prefix' + _random_string(6)
    bucket_name = 'samplebucket'
    key = 'samplekey' + _random_string(6)
    file_name = 'samplefile'
    download = 'download'

    ######################################################################################################
    #            bucket operation samples
    ######################################################################################################

    # create a bos client
    config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)    
    bos_client = BosClient(config)

    # check if bucket exists
    if not bos_client.does_bucket_exist(bucket_name):
        bos_client.create_bucket(bucket_name)

    # delete a bucket(you can't  delete a bucket which is not empty)
    # clear it first
    #for obj in bos_client.list_all_objects(bucket_name):
    #    bos_client.delete_object(bucket_name, obj.key)
    #bos_client.delete_bucket(bucket_name)

    # create the bucket again
    #bos_client.create_bucket(bucket_name)

    # list your buckets
    #response = bos_client.list_buckets()
    #for bucket in response.buckets:
    #    __logger.debug("[Sample] list buckets:%s", bucket.name)

    ######################################################################################################
    #            object operation samples
    ######################################################################################################

    # put a string as object
    bos_client.put_object_from_string(bucket_name, key, "This is string content.")

    # get a object as string
    content = bos_client.get_object_as_string(bucket_name, key)
    __logger.debug("[Sample] get object as string:%s", content)

    # put a file as object
    _create_file(file_name, 4096)
    bos_client.put_object_from_file(bucket_name, key, file_name)

    # get object into file
    bos_client.get_object_to_file(bucket_name, key, download)
    __logger.debug("[Sample] get object into file, file size:%s", os.path.getsize(download))




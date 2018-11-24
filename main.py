# -*- coding:utf-8 -*-
#!/usr/bin/python
#
# Copyright (c) 2017, Aixi Wang <aixi.wang@hotmail.com>
#
#=========================================================


import sys
import os.path
import os

import time
import utils
import myoss
import mybos

import cap as cap


#if len(sys.argv) != 3:
#    print "%s input_file output_file" % (sys.argv[0])
#    sys.exit()
#else:
#    input_file = sys.argv[1]
#    output_file = sys.argv[2]#
#
#if not os.path.isfile(input_file):
#    print "No such file '%s'" % input_file
#    sys.exit()

INPUT_FILE = './img/in_%%.jpg'
OUTPUT_FILE = './img/out_%%.jpg'
P2_FILE = './img/P2_%%.jpg'
P3_FILE = './img/P3_%%.jpg'
P4_FILE = './img/P4_%%.jpg'
ERR_FILE = './img/err_%%.jpg'

TASK_DURATION = 60


    
#====================================
# main  
#====================================
if __name__ == "__main__":
    retcode,config_json = utils.gen_config()
    print 'mask_jon:',config_json
    
    
    while True:
        t1 = time.time()
        f1 = utils.gen_filename(INPUT_FILE,t1)



        duration = config_json['duration']
        
        # create folder for img storing
        if os.path.exists('./img') == False:
            os.system('mkdir img')

        # call cap function to capture picture
        print 'f1:',f1
        ret,w,h = cap.cap(f1,640,480)    
        if ret == -1:
            print 'capture image fail!'
        else:
            retcode = 0
            
            if config_json['cloud'] == 'oss':
                # upload file ...
                retcode = myoss.upload_file_to_oss(config_json['oss'],f1)
                
            elif config_json['cloud'] == 'bos':
                retcode = mybos.file_upload_bos(config_json['bos'],f1)
            else:
                print('no cloud defined, no file uploaded')
                
            print 'upload retcode:',retcode
            
        while (time.time() - t1) < duration:
            time.sleep(1)

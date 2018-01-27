# -*- coding:utf-8 -*-
#!/usr/bin/python
#
# Copyright (c) 2017, Aixi Wang <aixi.wang@hotmail.com>
#
#=========================================================

import cv2
import numpy as np
import sys
import os.path
import os

import time
import utils
import myoss


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
    while True:
        t1 = time.time()
        f1 = utils.gen_filename(INPUT_FILE,t1)


        #
        # init local config values
        #
        print 'mask_jon:',config_json
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
            # upload file ...
            retcode = myoss.upload_file_to_oss(config_json,f1.split('/')[-1],f1)
            print 'upload retcode:',retcode
            
        while (time.time() - t1) < duration:
            time.sleep(1)

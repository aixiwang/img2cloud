#!/usr/bin/python
#
# please install python-v4l2capture
#
# This file is an example on how to capture a picture with
# python-v4l2capture.
#
# 2009, 2010 Fredrik Portstrom
#
# I, the copyright holder of this file, hereby release it into the
# public domain. This applies worldwide. In case this is not legally
# possible: I grant anyone the right to use this work for any
# purpose, without any conditions, unless such conditions are
# required by law.

from PIL import Image
import select
import v4l2capture
import time
import os

def cap(f,w,h):
    i = 0
    while i < 10:
        try:

            video = v4l2capture.Video_device("/dev/video0")
            size_x, size_y = video.set_format(640, 480)
            video.create_buffers(1)
            video.queue_all_buffers()
            video.start()
            select.select((video,), (), ())
            image_data = video.read()
            video.close()
            image = Image.frombytes("RGB", (size_x, size_y), image_data)
            image.save(f)
            print "Saved ",f,"(Size: " + str(size_x) + " x " + str(size_y) + ")"
            return 0,size_x,size_y
            
        except Exception as e:
            print 'exception:',str(e)
            try:
                os.system('rm usb.txt')            
                os.system('lsusb > usb.txt')
                f = open('usb.txt','rb')
                s = f.read()
                f.close()
                s2 = s.split('\n')
                #print(s2)
                for d in s2:
                    #print d
                    if d.find('Sunplus') > 0:
                        s3 = d.split(' ')
                        bus_cam = s3[1][0:3]
                        dev_cam = s3[3][0:3]
                        
                        #print('cam Bus:',bus_cam)
                        #print('cam Dev:',dev_cam)
                        reset_cmd = './reset /dev/bus/usb/' + bus_cam + '/' + dev_cam
                        #print('reset_cmd:',reset_cmd)
                
                os.system(reset_cmd)
                print('reset usb cam:',reset_cmd)
                time.sleep(3)
            except:
                print('try to reset camera to recovery')
                
            i += 1
            
    return -1,0,0

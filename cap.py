#!/usr/bin/python

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
            #size_x, size_y = video.set_format(640, 480,fourcc = 'MJPG')
            size_x, size_y = video.set_format(640, 480)
            video.set_fps(1)
            video.create_buffers(1)
            video.queue_all_buffers()
            video.start()
            
            print('cap 1')
            #time.sleep(1)
            select.select((video,), (), ())
            print('cap 2')
            #image_data = video.read_and_queue()
            image_data = video.read()
            video.close()
            print('cap 3')
            image = Image.frombytes("RGB", (size_x, size_y), image_data)
            image.save(f)
            #f = open(f,'wb')
            #f.write(image_data)
            print('cap 4')
            print "Saved ",f,"(Size: " + str(size_x) + " x " + str(size_y) + ")"
            return 0,size_x,size_y
            
        except Exception as e:
            print 'exception 1:',str(e)
            
            try:
                video.close()
            except Exception as e:
                print('exception 2',str(e))
                

            try:
                print('try to reset camera to recovery')            
                #os.system('rm usb.txt')            
                os.system('lsusb > usb.txt')
                f2 = open('usb.txt','rb')
                s = f2.read()
                f2.close()
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
                #time.sleep(3)
            except Exception as e:
                print('exception 3',str(e))


                
            i += 1
            
    return -1,0,0

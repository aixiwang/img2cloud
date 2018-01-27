# -*- coding:utf-8 -*-
#!/usr/bin/python
#
# Copyright (c) 2017, Aixi Wang <aixi.wang@hotmail.com>
# 
#=========================================================


#from matplotlib import pyplot
import json
import os
import math
import time

DEBUG = 0
img_x = 0
img_y = 0
contours = []
img = None


#----------------------
# gen_config
#----------------------
def gen_config():
    mask_json = {}
    
    if os.path.exists('config.json'):
        try:
            f = open('config.json','rb')
            s = f.read()
            mask_json = json.loads(s)
            print 'read mask_json from file config.json'
            retcode = 0

        except:
            retcode = -1
        # return directly from config.json
        return retcode,mask_json

    #    
    # return error
    #
    else:     
        return -1,None



    
#----------------------
# my_img_binarization
#---------------------- 
def my_img_binarization(f1,f2):
    img = cv2.imread(f1)
    new_image = img.copy()
    new_image.fill(255)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = im_gray.shape[0]
    w = im_gray.shape[1]
    sum = 0
    for y in xrange(0,h):
        for x in xrange(0,w):
            sum += im_gray[y][x]
            
    avg = sum/(h*w)       
    print 'avg:',avg

    # binarization
    for y in xrange(0,h):
        for x in xrange(0,w):
            if im_gray[y][x] < avg:
                new_image[y][x][2] = 0
                new_image[y][x][1] = 0
                new_image[y][x][0] = 0


    # remove isolated points
    for y in xrange(0,h):
        for x in xrange(0,w):
            if new_image[y][x][0] == 0 and (y == 0 or y == (h-1)):
                new_image[y][x][2] = 255
                new_image[y][x][1] = 255
                new_image[y][x][0] = 255
                
            elif new_image[y][x][0] == 0 and (x == 0 or x == (w-1)):
                new_image[y][x][2] = 255
                new_image[y][x][1] = 255
                new_image[y][x][0] = 255
            elif new_image[y][x][0] == 0 and new_image[y-1][x-1][0] == 255 and new_image[y+1][x+1][0] == 255 and new_image[y-1][x][0] == 255 and new_image[y+1][x][0] == 255 and new_image[y][x-1][0] == 255 and new_image[y][x+1][0] == 255 and new_image[y-1][x+1][0] == 255 and new_image[y+1][x-1][0] == 255:
                new_image[y][x][2] = 255
                new_image[y][x][1] = 255
                new_image[y][x][0] = 255
            else:
                pass

    cv2.imwrite(f2,new_image)
    return 0, new_image

    
#-------------------
# log_dump
#-------------------
def log_dump(filename,content):
    fpath = filename
    f = open(filename,'ab')
    t_s = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    
    content = t_s + '->' + str(content) + '\r\n'
    
    if type(content) == str:
        content_bytes = content.encode('utf-8')
        f.write(content_bytes)
    else:
        f.write(content)
    
    f.close()

#----------------------------
# gen_filename
#----------------------------        
def gen_filename(f_template,t):
    t_s = time.strftime('%Y%m%d-%H%M%S', time.localtime(t))
    return f_template.replace('%%',t_s)
    
#----------------------
# main
#----------------------
if __name__ == "__main__":
    pass

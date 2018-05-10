#!/usr/bin/env python

import sys
import pyvips

# left = 10
# top = 10
# width = 64
# height = 64

# image = pyvips.Image.new_from_file(sys.argv[1])
# print(image.width)
# roi = image.extract_area(3000, 3000, 5000, 5000)
# out = roi.embed(300,3000,image.width,image.height,background=[255,255,255])
# out.write_to_file("hello.tif",predictor='horizontal', compression='deflate')
# print('average:', roi.avg())

import cv2

global img, vipimg
global point1, point2
global filename

def on_mouse(event, x, y, flags, param):
    global img, vipimg, point1, point2, filename
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):               #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (255,0,0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:         #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 5) 
        cv2.imshow('image', img2)
        min_x = min(point1[0],point2[0])*20
        min_y = min(point1[1],point2[1])*20
        width = abs(point1[0] - point2[0])*20
        height = abs(point1[1] -point2[1])*20
        roi = vipimg.extract_area(min_x,min_y,width,height)
        out = roi.embed(min_x,min_y,vipimg.width,vipimg.height,background=[255,255,255])
        newfile = filename.split('_section_')[1]+'-new.tif'
        out.write_to_file(newfile,predictor='horizontal', compression='deflate')
def main(file):
    global img,vipimg,filename
    filename = file
    vipimg = pyvips.Image.new_from_file(file)
    rsi = vipimg.resize(0.05)
    rsi.write_to_file("hello.tif",predictor='horizontal', compression='deflate')
    img = cv2.imread('hello.tif')
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse)
    cv2.imshow('image', img)
    cv2.waitKey(0)

if __name__ == '__main__':
    fileheader = 'f_21.99x_section_'
    i = int(sys.argv[1])
    main(fileheader+'%03d'%(i)+'.tif')
'''
/*******************************************************************
 * Project Name: Generic GUI YOLO
 * File Name: python_gst.py
 * Description: Open source library for data acquisition from USB Cameras and Gstreamer
 * Author: Umi-Reco 
 * License: MIT (see LICENSE file for details)
 ******************************************************************/
''' 

import cv2
import sys
import requests
import os
import json as json2
from datetime import datetime

def set_config_from_file():

    name_user   = os.getlogin()
    path_config = os.path.join('/','home',name_user,'Server','app','static','database','config.json')
    
    with open(path_config,'r') as f_config:
        json_config = json2.load(f_config)
    
    f_config.close()
    return json_config

def read_camera_gstreamer(json_config):
    pipeline = (
        "v4l2src device=/dev/video0 ! "  # Video source (webcam)
        "video/x-raw,format=(string)GRAY8, width=(int)4200, height=(int)3120 ! " # Desired capabilities
        "nvvidconv ! " # Convert to a common format
        "appsink" # Sink to allow OpenCV to access the frames
    )

    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Could not open video stream with GStreamer pipeline.")
        sys.exit(1)

    url_api = json_config['system']['ip'] + "/api/image_recv"

    print("Reading frames from camera...")
    c_count = 0
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to read frame.")
            break
        else:
            new_dimensions = (300, 200)
            outputFrame = cv2.resize(frame, new_dimensions)
            payload = {
                "array": outputFrame.tolist(),
                "image_count":c_count
            } 

            try:
                response = requests.post(url_api, json=payload, timeout=0.001)
            except:
                pass
            
            c_count = c_count + 1

            #d = datetime.now()
            #name_file = d.strftime('%Y%m%d_%H%M%S_%f.bmp')
            #path_img = os.path.join(dir_img,name_file)
            #print(path_img)
            #cv2.imwrite(path_img,frame)        

    # Release the VideoCapture object and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    json_config = set_config_from_file()
    print(json_config)
    read_camera_gstreamer(json_config)
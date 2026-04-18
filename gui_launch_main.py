
'''
/*******************************************************************
 * Project Name: Generic GUI for Machine Learning
 * File Name: gui_launch_main.py
 * Description: Open source library for uploading yolo model and running on camera
 * Author: Umi-Reco 
 * License: MIT (see LICENSE file for details)
 ******************************************************************/
''' 

from   flask import Flask, render_template, request,Response
from   datetime import datetime
import numpy  as np
import pandas as pd
import json   as json2
import signal
import cv2
import pytz
import subprocess
import time
import zipfile
import shutil
import os
import atexit
tz_utc   = pytz.timezone('UTC')

#making static and database directory
dir_static   = os.path.join(os.path.realpath(os.path.dirname(__file__)), "static")
dir_db       = os.path.join(os.path.realpath(os.path.dirname(__file__)), "static/database")
dir_models   = os.path.join(os.path.realpath(os.path.dirname(__file__)), "static/models")
dir_exports  = os.path.join(os.path.realpath(os.path.dirname(__file__)), "static/exports")
dir_python   = os.path.join(os.path.realpath(os.path.dirname(__file__)), "static/python")

path_config  = os.path.join(dir_db, "config.json")
path_py_ai   = os.path.join(dir_python,'python_gst.py')

def search_models(dir_models):
    l_name_models = os.listdir(dir_models)
    l_name_models = [s for s in l_name_models if '.pt' in s]
    return l_name_models

def generate_frame():
    while True:
        outputFrame          = np.array(json_img['data'],dtype=np.uint8)
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

def get_curr_time_utc():
    dt_utc       = datetime.now().replace(tzinfo=tz_utc) 
    str_utc      = dt_utc.strftime("%Y-%m-%d %H:%M:%S.%f")[0:-3] + 'Z'
    return str_utc

def get_curr_memory():
    stat     = shutil.disk_usage('/')
    curr_mem = round(stat[2]/stat[0] * 100.0,1)
    return curr_mem

#loading deviced data as json from config.json file
def set_config_from_file(path_config):
    with open(path_config,'r') as f_config:
        json_config_file = json2.load(f_config)
        f_config.close()
    return json_config_file

def save_config_to_file():
    json_out = json_config.copy()
    with open(path_config,'w') as f:
        json2.dump(json_out,f,indent=4)
    return json_config

json_config = set_config_from_file(path_config)

dict_process = {
    "process_ai":""
}
        
json_img = {
    'data':[]
}

#starting the flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/system_status', methods=['POST','GET'])
def api_system_status():
    json_reply = {
        "datetime":get_curr_time_utc(),
        "memory":get_curr_memory(),
        "gain":json_config['camera']['gain'],
        "exposure":json_config['camera']['exposure'],
        "model":json_config['deployment']['model'],
        "status":json_config['deployment']['status']
    }
    return json_reply

@app.route('/api/get_models', methods=['GET','POST'])
def api_get_models():
    json_models = {
        "models":search_models(dir_models)
    }
    print(json_models)
    return json_models

@app.route('/api/set_model', methods=['POST'])
def api_set_model():
    if request.is_json:
        received_data = request.json
        json_config['deployment']['model'] = received_data['model'] 
        json_config['deployment']['status'] = 'Model changed'

    return json_config

@app.route('/api/save_camera', methods=['POST'])
def save_camera():
    if request.is_json:
        received_data = request.json
        json_config['camera']['gain']      = received_data['gain']
        json_config['camera']['exposure']  = received_data['exposure']
        save_config_to_file()
        json_config['deployment']['status'] = 'Updated camera settings'
    return json_config

@app.route("/video_feed")
def video_feed():
	return Response(generate_frame(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/api/image_recv', methods=['POST'])
def api_image_recv():
    if request.method == 'POST':
        data = request.get_json()
        json_img['data'] = data['array']
        json_config['deployment']['image_count'] = data['image_count']

    return json_config

@app.route('/api/stop_ai', methods=['POST','GET'])
def api_stop_ai():
    if dict_process['process_ai']:
        dict_process['process_ai'].send_signal(signal.SIGTERM)
        dict_process['process_ai'] = ''
    json_config['deployment']['status'] = 'Stop AI processing'

    return json_config

@app.route('/api/start_ai', methods=['POST','GET'])
def api_start_ai():
    save_config_to_file()
    dict_process['process_ai'] = subprocess.Popen(['python3',path_py_ai])
    json_config['deployment']['status'] = 'Start AI processing'
    return None

#running the app, set the ip and the port in the sh file
if __name__ == "__main__":
    app.run(port=5500, host='127.0.0.1')

#code to be executed before closing the server
def cleanup():
    str_delete_query = "sudo rm -r " + dir_exports + "/*"
    return None

atexit.register(cleanup)

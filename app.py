import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from io import BytesIO
from flask_socketio import SocketIO#, emit, send
from collections import deque
from engine.load import JsonConfig, Stack, clean_tempfile
from third_party.filemanager import get_filelist
from engine.get_all_modules import all_const_front
from utils.config import IMG_CACHE_DIR
from flask_cors import CORS
import asyncio
from engine.dag import RecursiveParse
import os.path as osp
import os
import cv2
import pprint
from functools import partial
import shutil
from threading import Thread
import threading
from time import sleep
import traceback
import flask
import numpy as np
# from flask import request
from flask import Flask, abort, request, send_file,render_template
import json
import sys

from numpy import ndarray

from engine.decorators import ExeStack
from engine.ndarray_tools import check_ndarray, normal_ndarray_to_gray, to_base64
from utils.exception import NDArrayTypeError

sys.path.append('.')


app = Flask(__name__,
static_folder='./frontend/dist',  
template_folder = "./frontend/dist",
static_url_path="") 

app.debug = True
app.config['SECRET_KEY'] = 'socket.io'
app.config['LOGIN_DISABLED'] = True
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')



@app.route('/')
def index():
    return render_template('index.html',name='index')

stack = Stack()
stack.start()




@app.route('/api/elements')
def elements():
    # discript_all.update(reskvfront)
    return all_const_front


@app.route('/api/observers/<name>', methods=['GET', 'POST'])
def observers(name):
    if request.method == 'POST':
        # pprint.pprint(request.get_json())
        jsd = request.get_json()
        jsoncfg = JsonConfig(name)
        # line = json.dumps(jsd, indent=2)
        jsoncfg.save_params(jsd)
        # with open('./server/observers.json', 'w') as f:
            # f.write(line)
        return {}
    elif request.method == 'GET':
        # with open('./server/observers.json', 'r') as f:
        #     line = f.read()
        # return json.loads(line)
        jsoncfg = JsonConfig(name)
        return jsoncfg.load_params()

# @socketio.on('execute_event')
# def execute_event():
#     data = jsoncfg.load_params()
#     # stack.deq.append(
#         # partial()
#     # )
#     ExeStack.init_store()
#     try:
#         RecursiveParse().run(data)
#     except Exception as e:
#         # ExeStack.exception(traceback.format_exc())
#         raise e


@app.route('/api/execute/<name>',methods=['GET'])
def execute(name):
    data = JsonConfig(name).load_params()
    # stack.deq.append(
        # partial()
    # )
    ExeStack.init_store()
    try:
        RecursiveParse().run(data)
    except Exception as e:
        # ExeStack.exception(traceback.format_exc())
        raise e
    return {'type':'success'}

@app.route('/api/config/<name>',methods=['PUT','DELETE'])
def set_current_name(name):
    if request.method == 'PUT':
        name = JsonConfig(name).new_config()
        return {'type':'success','data':name}
    elif request.method == 'DELETE':
        JsonConfig(name).delete_config_by_name(name)
        return {'type':'success'}

# @app.route('/api/config/<name>',methods=['DELETE',])
# def set_current_name(name):
    # name = jsoncfg.set_current_name(name)
    # return {'type':'success','data':name}

@app.route('/api/config',methods=['GET',])
def list_config_names():
    _ = JsonConfig.list_config_names()
    _['type'] = 'success'
    return _
# @app.login_manager.unauthorized_handler
# @app.route('/api/ndarraytempimg/<int:post_id>',methods=['GET',])
# login_requied


# @socketio.on('query_ndarray_temp_img_event')
# @app.route('/api/ndarray', methods=['POST',])
# def query_ndarray():
#     # ExeStack.ndarray_store[1] = np.zeros((100, 100), dtype='uint8')
#     # print(post_id, ExeStack.ndarray_store)
#     if request.method == 'POST':
#         data = request.get_json()
#         post_id = data['ndid']
#         mat = ExeStack.ndarray_store.get(post_id, None)

#         # print('get key:',post_id,ExeStack.ndarray_store.keys())
#         try:
#             mat = check_ndarray(mat, post_id)
#         except NDArrayTypeError as e:
#             print(e)
#             # abort(404)
#             return {"type":"error",'msg':str(e)}
#         mat = normal_ndarray_to_gray(mat)
#         b64, type = to_base64(mat)
#         print('base64 data:',len(b64),type)
#         datastream  = "data:image/{};base64,{}".format(type, b64.decode('utf-8'))
#         return {
#             "type": "success",
#             "post_id":post_id,
#             "data": datastream}
        # return


@app.route('/ndarray/<imageid>', methods=['GET', ])
def ndarray_get(imageid):
    mat = ExeStack.ndarray_store.get(imageid, None)

    # print('get key:',post_id,ExeStack.ndarray_store.keys())
    try:
        mat = check_ndarray(mat, imageid)
    except NDArrayTypeError as e:
        print(e)
        # abort(404)
        return {"type": "error", 'msg': str(e)}
    mat = normal_ndarray_to_gray(mat)
    # im = cv2.imread("{}.jpg".format(imageid))
    print('mat shape',mat.shape)
    type_ = 'png'
    _, mat = cv2.imencode('.'+type_, mat)
    f = BytesIO(mat.tobytes())
    return send_file(f, mimetype="image/{}".format(type_))




def format_number(num):
    if 0<=num<=999:
        return str(num)
    else:
        return "{:.1e}".format(num)

@app.route('/ndarrayPix', methods=['POST', ])
def ndarray_pix():
    if request.method == 'POST':
        data = request.get_json()
        # print('data',data)
        id = data['id']
        xmin = int(data['xmin'])
        ymin = int(data['ymin'])
        xmax = int(data['xmax'])
        ymax = int(data['ymax'])
        # id, xmin, ymin, xmax, ymax
        mat = ExeStack.ndarray_store.get(id, None)
        try:
            mat = check_ndarray(mat, id)
        except NDArrayTypeError as e:
            return {"type": "error", 'msg': str(e)}
        # retNDArray = mat[ymin:ymax, xmin:xmax]
        results = []
        # h, w = mat.shape[:2]
        print(mat.shape,mat.dtype)
        for i in range(xmin, xmax):
            for j in range(ymin, ymax):
                v = mat[j, i]
                if len(v.shape)>0:
                    v = np.mean(v,dtype=v.dtype)
                _ = {
                    'y': str(int(j)),
                    'x': str(int(i)),
                    'v': float(v),
                    'format':format_number(v)
                }
                results.append(_)
        return {
            'type': 'success',
            'post_id': id,
            'data': results
        }


@socketio.on('connect', )
def connected_msg():
    print('client connected!', request.sid)

    def while_emit():
        while True:
            socketio.sleep(0.1)
            # print(ExeStack.store)
            while ExeStack.store:
                msg = ExeStack.store.pop(0)
                socketio.emit('emitResult', msg)
    socketio.start_background_task(target=while_emit)
#


# @app.route("/file/upload", methods=['POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         file.save(f"./cache/{secure_filename(file.filename)}")
#         return {}


# @app.route('/api/file/download', methods=['GET'])
# def download():
#     pass

# @app.route('/api/file/list',methods=['GET'])
# def listFiles():
#     files = os.listdir('./cache')
#     return {"files":files}


@app.route('/api/file/listdir/', methods=['GET', 'POST'])
def listDir():
    try:
        if request.method == 'POST':
            data = request.get_json()
            dir = data['dirs']
            origin = data['origin']
            _ = osp.join(origin, dir)
            print('get dir', dir)
            _, dir = get_filelist(_)
            return {"data": _, 'origin': dir}
        elif request.method == 'GET':
            _, dir = get_filelist('~')
            return {"data": _, 'origin': dir}
    except ValueError as e:
        return {
            'success': False,
            'msg': str(e)
        }



if __name__ == '__main__':
    # app.run(debug=True)
    # clean_tempfile(IMG_CACHE_DIR)
    socketio.run(app)


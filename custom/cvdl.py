from functools import wraps
from typing import Any, Tuple
import pdb
import cv2
from numpy import ndarray
import numpy as np
import cv2
from utils.exception import ArgsError

from third_party.cv2_enums import ENUM_CV_DNN_BACKEND,ENUM_CV_DNN_TARGET
try:
    from custom.opencv_zoo.models.image_classification_mobilenet.mobilenet_v2 import MobileNetV2
    from custom.opencv_zoo.models.text_recognition_crnn.crnn import CRNN
    from custom.opencv_zoo.models.text_detection_db.db import DB
    from engine.decorators import rx_func,ExeStack
    # IMPORT_TAG = True 
except Exception as e:
    # IMPORT_TAG = False
    from engine.decorators import fake_rx_func as rx_func
    print('Check if the opencv_zoo is installed correctly')

# def register_model(func):
#     model = None
#     @wraps(func)
#     def inner(*args,**kwargs):
#         nonlocal model
#         # print(func,args,kwargs)
#         return func(*args,**kwargs)
    
#     # print(func_type,type(func_type))
#     # inner.func_type=func_type
#     return inner

# # cv2.dnn.
    
# @register_model

# def visualize(image, boxes, texts, color=(0, 255, 0), isClosed=True, thickness=2):
#     output = image.copy()

#     pts = np.array(boxes[0])
#     output = cv2.polylines(output, pts, isClosed, color, thickness)
#     for box, text in zip(boxes[0], texts):
#         cv2.putText(output, text, (box[1].astype(np.int32)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
#     return output
    #  = {}

@rx_func()
def mobilenet_infer(image:ndarray,
        func_uniquekey:str = "mobilenet",
        modelPath:str='./custom/opencv_zoo/models/image_classification_mobilenet/image_classification_mobilenetv2_2022apr.onnx',
        labelPath:str="./custom/opencv_zoo/models/image_classification_mobilenet/imagenet_labels.txt",
        backendId:ENUM_CV_DNN_BACKEND=ENUM_CV_DNN_BACKEND.DNN_BACKEND_DEFAULT,
        targetId:ENUM_CV_DNN_TARGET=ENUM_CV_DNN_TARGET.DNN_TARGET_CPU
        )->Any:
    if func_uniquekey not in ExeStack.model_register.keys():

        ExeStack.model_register[func_uniquekey] =  MobileNetV2(
            modelPath=modelPath, 
            labelPath=labelPath, 
            backendId=backendId, 
            targetId=targetId)
    
    return ExeStack.model_register[func_uniquekey].infer(image)

@rx_func()
def text_recognition_crnn(
    image:ndarray,
    roi:tuple,
    func_uniquekey:str="text_recognition",
    rec_model_path:str="./custom/opencv_zoo/models/text_recognition_crnn/text_recognition_CRNN_CN_2021nov.onnx",
    charset_path:str="./custom/opencv_zoo/models/text_recognition_crnn/charset_3944_CN.txt",
    backendId:ENUM_CV_DNN_BACKEND=ENUM_CV_DNN_BACKEND.DNN_BACKEND_DEFAULT,
    targetId:ENUM_CV_DNN_TARGET=ENUM_CV_DNN_TARGET.DNN_TARGET_CPU
    )->Any:
    if func_uniquekey not in ExeStack.model_register.keys():

        ExeStack.model_register[func_uniquekey] = CRNN(modelPath=rec_model_path, 
                charsetPath=charset_path,
                    backendId=backendId, 
                    targetId=targetId)

    return ExeStack.model_register[func_uniquekey].infer(image,roi)
    


    
@rx_func()
def text_detection_db(
    image,
    func_uniquekey:str="text_detection",
    det_model_path:str="./custom/opencv_zoo/models/text_detection_db/text_detection_DB_TD500_resnet18_2021sep.onnx",
    input_size:Tuple=(736,736),
    binary_threshold:float=0.3,
    polygon_threshold:float=0.5,
    max_candidates:int=200,
    unclip_ratio:float=2.0,
    backendId:ENUM_CV_DNN_BACKEND=ENUM_CV_DNN_BACKEND.DNN_BACKEND_DEFAULT,
    targetId:ENUM_CV_DNN_TARGET=ENUM_CV_DNN_TARGET.DNN_TARGET_CPU
    )->Any:
    if func_uniquekey not in ExeStack.model_register.keys():

        ExeStack.model_register[func_uniquekey] = DB(modelPath=det_model_path,
                inputSize=input_size,
                binaryThreshold=binary_threshold,
                polygonThreshold=polygon_threshold,
                maxCandidates=max_candidates,
                unclipRatio=unclip_ratio,
                backendId=backendId,
                targetId=targetId
        )


    return ExeStack.model_register[func_uniquekey].infer(image)

@rx_func()
def text_recognition_visualize(
        image:ndarray,
        boxes:ndarray,
        texts:list,
        color:Tuple=(0, 255, 0), 
        isClosed:bool=True, 
        thickness:int=2):
    output = image.copy()
    pts = np.array(boxes)
    output = cv2.polylines(output, pts, isClosed=isClosed, color=color, thickness=thickness)
    for box, text in zip(boxes, texts):
        cv2.putText(output, text, (box[1].astype(np.int32)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    return output
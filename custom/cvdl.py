from functools import wraps
from typing import Any
import pdb
import cv2
from numpy import ndarray
from engine.decorator import view,rx_func
from utils.exception import ArgsError
from third_party.cv2_enums import ENUM_CV_DNN_BACKEND,ENUM_CV_DNN_TARGET
try:
    from custom.opencv_zoo.models.image_classification_mobilenet.mobilenet_v2 import MobileNetV2
except Exception as e:
    raise ArgsError('Check if the opencv_zoo is installed correctly')

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
model_register = {"model":None}


@rx_func()
def mobilenet_infer(image:ndarray,
        modelPath:str='./custom/opencv_zoo/models/image_classification_mobilenet/image_classification_mobilenetv1_2022apr.onnx',
        labelPath:str="./custom/opencv_zoo/models/image_classification_mobilenet/imagenet_labels.txt",
        backendId:ENUM_CV_DNN_BACKEND=ENUM_CV_DNN_BACKEND.DNN_BACKEND_DEFAULT,
        targetId:ENUM_CV_DNN_TARGET=ENUM_CV_DNN_TARGET.DNN_TARGET_CPU
        )->Any:
    # model
    # if model == None:
    if model_register['model']==None:

        model_register['model'] = MobileNetV2(
            modelPath=modelPath, 
            labelPath=labelPath, 
            backendId=backendId, 
            targetId=targetId)
    
    return model_register['model'].infer(image)


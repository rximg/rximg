import cv2
from numpy import ndarray
from numpy.typing import ArrayLike,NDArray
from typing import Any, Tuple
from engine.ndarray_tools import normal_ndarray_to_gray
from utils.config import IMG_CACHE_DIR
from engine.decorator import rx_func
import os.path as osp
import pdb
import typing
import glob
from third_party.rxtypes import ImageShow,PrintShow
from typing import List
from utils.exception import ObservableTypeError
from engine.decorator import ExeStack
import traceback
# from rx.core import Observable
import numpy as np
from utils.config import LAMBDACONTEXT

@rx_func()
def imshow(mat:NDArray) -> Any:
    assert isinstance(mat,ndarray),'mat({}) must be ndarray:{}'.format(type(mat),mat)
    # imname = str(id(mat))+'.png'
    # dir_ = IMG_CACHE_DIR+ imname
    # print('write to static',dir_)
    mat = normal_ndarray_to_gray(mat)
    imid = str(id(mat))
    ExeStack.ndarray_store[imid] = mat
    # cv2.imwrite(dir_,mat)
    return ImageShow(imname=imid,ret=mat) 


@rx_func()#注册成rx模块识别的函数
def roi_img(mat:NDArray,xmin:int,ymin:int,xmax:int,ymax:int)->NDArray:
    return mat[ymin:ymax,xmin:xmax]


# @rx_func()
# def imread_upload(filename:str) -> Any:
#     # pdb.set_trace()
#     filename = osp.join('./cache',filename)
#     _ = cv2.imread(filename=filename,flags=1)
#     return _

@rx_func(func_type='file')
def glob_dirs(dirs:List):
    res = []
    for i in dirs:
        res= res+glob.glob(i)
    return res


@rx_func()
def print_(input_:typing.Any):
    return PrintShow(input_)

@rx_func(func_type="list_")
def list_(*args):
    return args

#TODO change parameter to var
@rx_func(func_type="parameter")
def parameter(input_):
    return input_
# def lambda_called(line, kwargs):
#     # ret = eval(line, kwargs)
#     return eval(line, kwargs)

@rx_func()
def take_return_index(returns,index:int):
    # def fun(*args,**kwargs):
        # return func(*args,**kwargs)[index]
    return returns[index]

# @rx_func()
# def test(abc:Tuple):
#     return abc

def except_eval(line,kwargs):
    try:
        print('lambda:',line)
        return eval(line,kwargs)
    except Exception as e:
        print(traceback.format_exc())
        ExeStack.exception(traceback.format_exc())
        raise e

class LambdaCallable(object):

    def __init__(self, line, args=None, ):
        self.line = line
        self.args = args

    def __call__(self, args):
        kwargs = LAMBDACONTEXT.copy()
        if len(self.args)==1:
            kwargs[self.args[0]]=args
        elif len(self.args)>1:
        # assert len(self.args) == len(args), "input key len:{} vs args len:{}".format(len(self.args),len(args))
            for k, v in zip(self.args, args):
                kwargs[k] = v
        ret = except_eval(self.line, kwargs,)

        return ret

@rx_func(func_type='lambda')
def LAMBDA(line:str,args:List)->Any:
    if len(args) == 0:
        return except_eval(line, LAMBDACONTEXT.copy())
    else:
        # context.update(args)
        return LambdaCallable(line, args)

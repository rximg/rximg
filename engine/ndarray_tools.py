import base64
import numpy as np
import cv2
from numpy.typing import NDArray
import sys
sys.path.append('.')
from utils.exception import NDArrayTypeError

def check_ndarray(mat,id):
    if not isinstance(mat,np.ndarray):
        raise NDArrayTypeError('error ndarray id:{}'.format(id))
    shape = mat.shape
    if len(shape) == 2:
        return mat
    elif len(shape) == 3:
        if shape[-1]==1:
            return mat[::,::,0]
        elif shape[-1]==3:
            return np.mean(mat,axis=2).astype(mat.dtype)
        else:
            raise NDArrayTypeError('error ndarray shape:{}'.format(shape))
    else:
        raise NDArrayTypeError('error ndarray shape:{}'.format(shape))
    

def normal_ndarray_to_gray(mat):
    shape = mat.shape
    if isinstance(np.dtype,np.complexfloating):
        mat = np.abs(mat) 
    if mat.dtype != 'uint8':
        mat = (mat - np.min(mat))/(np.max(mat)-np.min(mat))
        mat = (mat*255).astype('uint8')
    return mat


def to_base64(mat:NDArray,type='png'):
    flag, mat = cv2.imencode('.'+type,mat)
    b64 = base64.urlsafe_b64encode(mat.tobytes())
    return b64,type


if __name__ == "__main__":
    pass
    
    image = np.asarray(bytearray(src), dtype="uint8")
    im = cv2.imdecode(image,cv2.IMREAD_COLOR)
    print(im)

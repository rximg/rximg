from email.policy import default
from enum import IntEnum,Enum
from  typing import Sequence,Optional,Dict,Union
import numpy as np
from numpy import typing
typing.NDArray

class CVENUM(object):
    
    @classmethod
    def get(cls):
        res = {}
        for k,v in cls.__members__.items():
            res[k] = v.value

        return res

class CVINTENUM(IntEnum):
    
    
    @classmethod
    def get(cls):
        res = {}
        for k,v in cls.__members__.items():
            res[k] = v.value

        return res

class CVSTRENUM(Enum):

    @classmethod
    def get(cls):
        res = {}
        for k,v in cls.__members__.items():
            res[k] = v.value

        return res

class ENUM_CV_DTYPE(CVSTRENUM):

    default = 'uint8'
    uint8 = 'uint8'
    uint16 = 'uint16'
    uint32 = 'uint32'
    uint64 = 'uint64'

    float16 = "float16"
    float32 = "float32"
    float64 = "float64"

    half = "half"
    single = "single" 
    double = "double"
    float_ = "float_"
    longdouble = "longdouble"
    longfloat = "longfloat"

    complex = "complex"
    

class ENUM_CV_FFT_NORM(CVSTRENUM):

    default="backward"
    backward="backward"
    ortho="ortho" 
    forward="forward"


class ENUM_CV_ORDER(CVSTRENUM):

    # backward="backward"
    # ortho="ortho" 
    # forward="forward"
    default="C"
    C="C"
    F="F"
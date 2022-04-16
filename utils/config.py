

IMG_CACHE_DIR = './static/result/'

import reactivex as rx
import numpy as np
import cv2

OPDICT = {
    'map':rx.operators.map
}


LAMBDACONTEXT = {
    'np':np,
    'cv2':cv2,
}

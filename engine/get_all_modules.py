# import sys

# sys.path.append('.')

from third_party import cv2_modules,np_modules,observer_modules
from engine.module_parsers import CustomRXFunctionParser
import inspect
import os
import os.path as osp
import reactivex as rx
from reactivex import operators

class CustomModules(object):

    def __init__(self) -> None:
        super().__init__()
        self.dir = 'custom'

    def get_modules(self, name):
        cmd = self.dir+'.'+name
        mod = __import__(cmd, fromlist=[name])
        callss = [getattr(mod, m) for m in dir(mod)]
        callss = [v for k, v in mod.__dict__.items() if hasattr(v, 'rx_func')]
        return callss

    def get_submodule_names(self,):
        files = os.listdir(self.dir)
        submodules = [f for f in files if osp.isfile(osp.join(self.dir, f))]
        submodules = [osp.splitext(s)[0] for s in submodules]
        submodules = [s for s in submodules if not s.startswith('__')]
        return submodules

    def get(self):

        reskvfront, reskvback = {}, {}
        for i in self.get_submodule_names():
            reskvfront_i, reskvback_i = {}, {}
            calls = self.get_modules(i)
            for c in calls:
                # print(c)
                reskvback_i[c.__name__] = c
                reskvfront_i[c.__name__] = CustomRXFunctionParser(c,str(i)).get()
                # print(reskvfront_i[c.__name__])
            if calls:
                reskvfront[i]=reskvfront_i
                reskvback[i]=reskvback_i
        return reskvfront, reskvback


class CVModules(object):

    def __init__(self) -> None:
        super(object).__init__()
        self.mod = cv2_modules
        # print(self.mod)
        self.reskvfront = {}
        self.reskvback = {}
        self.enumback = {}
        # self.mod = cv2_modules

    def get_func_from_module(self, mod):
        rx_funcs = []
        for m in dir(mod):
            f = getattr(mod,m)
            if callable(f):
                if hasattr(f,'rx_func') and f.rx_func==True:
                    rx_funcs.append(f)
        return rx_funcs

    def get(self):
        calls = self.get_func_from_module(self.mod)
        for c in calls:
            self.reskvback[c.__name__] = c
            self.reskvfront[c.__name__] = CustomRXFunctionParser(c,"cv2").get()

class NPModules(object):

    def __init__(self) -> None:
        super(object).__init__()
        self.mod = np_modules
        # print(self.mod)
        self.reskvfront = {}
        self.reskvback = {}
        self.enumback = {}
        # self.mod = cv2_modules

    def get_func_from_module(self, mod):
        rx_funcs = []
        for m in dir(mod):
            f = getattr(mod,m)
            if callable(f):
                if hasattr(f,'rx_func') and f.rx_func==True:
                    rx_funcs.append(f)
        return rx_funcs

    def get(self):
        calls = self.get_func_from_module(self.mod)
        for c in calls:
            self.reskvback[c.__name__] = c
            self.reskvfront[c.__name__] = CustomRXFunctionParser(c,"np").get()

        # print(self.reskvback)

class RXModules(object):

    def __init__(self) -> None:
        super().__init__()
        self.mod = observer_modules
        self.reskvfront = {}
        self.reskvback = {}

    def get_func_from_module(self, mod):
        rx_funcs = []
        for m in dir(mod):
            f = getattr(mod,m)
            if callable(f):
                if hasattr(f,'rx_func') and f.rx_func==True:
                    rx_funcs.append(f)
        return rx_funcs

    def get_rxs(self):
        calls = self.get_func_from_module(self.mod)
        for c in calls:
            self.reskvback[c.__name__] = c
            self.reskvfront[c.__name__] = CustomRXFunctionParser(c,"observables").get()
        # observables_back,observables_front = {},{}
        # for r in dir(rx):
        #     func = getattr(rx,r)
        #     if inspect.isfunction(func):#type(_)==types.FunctionType:
        #         observables_back[r]=func
        #         observables_front[r] =CustomRXFunctionParser(func,"observables").get()
        operators_back,operators_front = {},{}
        for r in dir(operators):
            func = getattr(operators,r)
            if inspect.isfunction(func):
                operators_back[r]=func
                operators_front[r] =CustomRXFunctionParser(func,"operators").get()
        self.rx_backend = {
            "observables":self.reskvback,
            "operators":operators_back,
        }
        self.rx_frontend = {
            "observables":self.reskvfront,
            "operators":operators_front,
        }
    


def get_all_third_partys():
    cvmod = CVModules()
    cvmod.get()
    npmod = NPModules()
    npmod.get()
    rxmod = RXModules()
    rxmod.get_rxs()
    reskvfront = {
        "cv2":cvmod.reskvfront,
        "np":npmod.reskvfront
    }
    reskvfront.update(rxmod.rx_frontend)
    reskvback = {
        "cv2":cvmod.reskvback,
        "np":npmod.reskvback,
    }
    reskvback.update(rxmod.rx_backend)
    enums_back = {
        "cv2":cvmod.enumback,
        "np":npmod.enumback
    }
    
    return reskvfront,reskvback,enums_back


custom_discript, custom_instance = CustomModules().get()
reskvfront,reskvback,enums_back = get_all_third_partys()
all_const_front = reskvfront
all_const_front.update(custom_discript)
all_const_front.pop('core')
all_const_back = reskvback
all_const_back.update(custom_instance)

all_enums_back = enums_back

import numpy as np
from reactivex import operators as ops
import cv2
from custom import core
all_context = {
    'np':np,
    'cv2':cv2,
    "ops":ops,
    "rx":rx,
    "core":core
}
 
# from genericpath import isfile
import pprint
import inspect
import re
from numpy.typing import NDArray
from enum import Enum
import json
import os
import os.path as osp
import pdb
import typing
import reactivex as rx
from reactivex import Observable
import sys
sys.path.append('.')
import numpy as np
# from engine.decorator import RETURN_TYPE
type_map = {
    typing.Any: "Any",
    bool: "bool",
    str:"str",
    int:"int",
    float:"float",
    tuple:"tuple",
    typing.Tuple:"tuple",
    np.uint8:'int',
    np.typing.NDArray:"NDArray",
    typing.List: "list",
    typing.Callable: "Callable",
    Observable:"Observable",
    inspect._empty:"Any"
}

kind_map={
    inspect.Parameter.VAR_POSITIONAL:"VAR_POSITIONAL",
    inspect.Parameter.POSITIONAL_OR_KEYWORD:"POSITIONAL_OR_KEYWORD",
    inspect.Parameter.KEYWORD_ONLY:"KEYWORD_ONLY"
}



class ArgsParser(object):

    def __init__(self,func,) -> None:
        super().__init__()
        self.args_abstract = {}
        self.func = func
        self.is_VAR_POSITIONAL = False

    def get(self,):
        sig = inspect.signature(self.func)
        for i,item in enumerate(sig.parameters.items()):
            k,v = item
            _ = self.parse(k,v)
            _['index'] = i
            _['name'] = k
            self.args_abstract[k] = _
        try:
            json.dumps(self.args_abstract)
        except Exception as e:
            print(self.args_abstract)
            raise e
        return self.args_abstract

    def get_enum_type(self,obj):
        res = {}
        for k,v in obj.__members__.items():
            res[k] = v.value
        return {
                    "type": 'choices',
                    "name":obj.__name__,
                    "choices":res,
                    "kind":"POSITIONAL_OR_KEYWORD",
                    "value":obj.default.value
                }

    def parse(self,k,v):
        #TODO support typing.Optional 
        name = v.name
        kind = v.kind
        default = v.default
        # annotation_type = v.an
        annotation = v.annotation
        # if str(annotation).startswith('typing.Optional'):
        #     annotation = eval(re.search("\[(.*)\]",str(annotation)).groups()[0]) 
        annotation_str = type_map.get(v.annotation, 'Any')
        if kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY):
            if inspect.isclass(annotation) and issubclass(annotation,Enum):
                return self.get_enum_type(annotation)
            else:
                if v.default==inspect.Parameter.empty:
                    default = None
                elif annotation in (int,float,bool):
                    default = v.default
                else:
                    default = str(v.default)
                return {
                    "type": annotation_str,
                    "kind":kind_map.get(v.kind,None),
                    "value":default
                }
        elif kind == inspect.Parameter.VAR_POSITIONAL:
            return {
                "type": 'list',
                "kind":kind_map.get(kind,None),}
        elif kind in (inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.VAR_KEYWORD):
            raise ValueError("unsuported arg kind:{}".format(kind))

def briefRetrunType(s):
    if s==np.ndarray or s ==NDArray:
        return 'NDArray'
    s = str(s)
    s = s.replace('typing.Any','Any')
    s = s.replace('typing.Callable','Callable')
    # s = s.replace('typing.Callable','Callable')
    s = s.replace('reactivex.observable.observable.Observable',
        'Observable')
    s = s.replace("<class 'inspect._empty'>","empty")
    if s.startswith("Observable"):
        s = "Observable"
    elif s.startswith("Callable"):
        s = "Callable"
    return s



class CustomRXFunctionParser(object):

    def __init__(self,func,mod_name) -> None:
        super().__init__()
        self.func =func
        self.mod_name = mod_name


    def get(self):
        aparser = ArgsParser(self.func)
        argsd = aparser.get()
        sig = inspect.signature(self.func)
        ret_ann = sig.return_annotation
        # pdb.set_trace()
        # returns = None
        # pdb.set_trace()exit()
        # if isinstance(ret_ann,RETURN_TYPE):
            # pdb.set_trace()
            # returns = ret_ann.returns
        _ = {
            "name": self.func.__name__,
            "args": argsd,
            "from": self.mod_name, 
            # "returns":returns
            "returnType":briefRetrunType(sig.return_annotation)
        }
        if hasattr(self.func,'func_type'):
            _["type"] = self.func.func_type
            # print(_["type"],type(_["type"]))
        if aparser.is_VAR_POSITIONAL:
            _['HAS_VAR_POSITIONAL']=True
        # if hasattr(self.func, 'return_view'):
        #     # print('return_view', c.return_view)
        #     _['return_view'] = self.func.return_view
        return _
        
    






if __name__ == '__main__':
    pass
    # _ = get_all_modules()
    # pprint.pprint(custom_discript)
    # pprint.pprint(custom_instance)

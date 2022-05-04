from functools import wraps
import traceback
import typing
from typing import List,Tuple,Dict,Set,Sequence
import pdb
from flask_socketio import SocketIO, emit
from third_party.rxtypes import CustomType
from numpy import   ndarray
import reactivex as rx
exe_stack = []

def recursion_json_check(obj):
    
    if isinstance(obj,typing.Dict):
        ret = {}
        for k,v in obj.items():
            if isinstance(v,typing.Dict) or isinstance(v,Sequence) :
                value = recursion_json_check(v)
            elif isinstance(v,bool):
                value = v
            else:
                value = str(v)
            ret[k] = value
        return ret
    elif isinstance(obj,str):
        return obj
    elif isinstance(obj,bool):
        return obj
    elif isinstance(obj,Sequence):
        ret = []
        for v in obj:
            if isinstance(v,typing.Dict) or isinstance(v,Sequence) :
                value = recursion_json_check(v)
            else:
                value = str(v)
            ret.append(value)
        return ret 
    else:
        return str(obj)



class ExeStack(object):
    store = []
    ndarray_store = {}
    def __init__(self) -> None:
        super().__init__()
        self.name =""
        self.args = []
        self.kwargs = []
        self.rets = []
        
    def brief(self,v):
        if isinstance(v,ndarray):
            self.ndarray_store[str(id(v))] = v
            return  {
                'repr':"NDARRAY-{}".format(v.shape),
                'id':str(id(v)),
                'if_show':True,
                'type':"NDARRAY"
            }
        elif isinstance(v,CustomType):
            return v.json()
        else:
            return str(v)

    def brief_repr(self,v):
        v = self.brief(v)
        if isinstance(v,dict):
            return v['repr']
        else:
            return v
    
    def addfunc(self,func,args:typing.Sequence,kwargs:typing.Dict):
        if hasattr(func,'__name__'):
            self.name = func.__name__
        else:
            self.name = str(func)
        self.args = [self.brief_repr(a) for a in args]
        # print("kwargs:",kwargs)
        if kwargs.items():
            for k,v in kwargs.items():
                self.kwargs.append("{}={}".format(k,self.brief_repr(v)))

    def add_ret(self,v):
        self.rets = self.brief(v)

    @classmethod
    def stack(cls,obj):

        cls.store.append(recursion_json_check( {
            'type':"result",
            'name':obj.name,
            'args':obj.args,
            'kwargs':obj.kwargs,
            'ret':obj.rets,
            'visible':obj.visible
        }))

    @classmethod
    def exception(cls,trace):
        cls.store.append(
            {
                'type':"exception",
                "trace":trace,
            }
        )

    # @classmethod
    # def log_exe_stack(cls):
    #     lines = []
    #     for obj in cls.store:
    #         lines.append('='*10)
    #         lines.append('FUNC:{}'.format(obj.name))
    #         # if arg:
    #         for a in obj.args:
    #             lines.append(a)
    #         for v in obj.kwargs:
    #             lines.append(v)
    #         for ret in obj.rets:
    #             lines.append("ret:{}".format(ret))
    #     obj.lines = lines
    #     with open('./server/exe_stack.log','w') as f:
    #         f.write('\n'.join(lines))

def view(func):
    ret_collects = []
    @wraps(func)
    def inner(*args,**kwargs):
        res = func(*args,**kwargs)
        ret_collects.append(res)
        # pdb.set_trace()
        return res
    inner.return_view = True
    inner.ret_collects = ret_collects
    return inner

def rx_func(func_type='callable',func_visible=True):
    def rx_func_func(func):
        @wraps(func)
        def inner(*args,**kwargs):
            # print(func,args,kwargs)
            exe_obj = ExeStack()
            exe_obj.addfunc(func,args,kwargs)
            # exe_stack.append([name,args,kwargs])
            try:
                res = func(*args,**kwargs)
            except Exception as e:
                print("====error====")
                print(traceback.format_exc())
                ExeStack.exception(traceback.format_exc())
                exe_obj.visible = func_visible
                ExeStack.stack(exe_obj)
                raise e
            # exe_stack[-1] = exe_stack[-1]+[res]
            exe_obj.add_ret(res)
            exe_obj.visible = func_visible
            ExeStack.stack(exe_obj)
            # emit('emitResult',{'type':'func','data':str(res)})  
            if isinstance(res,CustomType):
                return res.ret
            else:
                return res
        inner.rx_func = True
        
        # print(func_type,type(func_type))
        inner.func_type=func_type
        return inner
    return rx_func_func

class RETURN_TYPE(object):
    def __init__(self,returns:typing.Sequence) -> None:
        super().__init__()
        self.returns = returns



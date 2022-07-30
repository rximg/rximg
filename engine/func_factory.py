import pdb
import reactivex as rx
from reactivex import operators  as ops
from utils.exception import ArgsError
# from rx import Observable
from engine.get_all_modules import all_const_back, all_enums_back,all_context
from typing import Any, Callable, Dict, List
from engine.decorator import ExeStack
import traceback
from utils.config import OPDICT
import numpy as np

#TODO 考虑一下把choices变成一个引用
def is_null(x): return (not hasattr(x, 'all')) and (x == None or x == "")


def get_typed_argv(type_str, value):
    # type_str,value = item['type'],item['value']
    # module = item.get('from',None)
    if value=='None':
        return None
    if type_str == "Any":
        return value
    elif type_str in ('int', 'float', 'bool'):
        return eval(type_str)(value)
    elif type_str in ('tuple',):
        
        return eval(value)
    elif type_str == "choices":
        return value
    else:
        return value


def find_title_key(key, items):
    if key in items.keys():
        return key
    for itemkey in items.keys():
        if itemkey.startswith(key):
            return itemkey


def return_output(ret, output_indexs):
    if output_indexs == None or len(output_indexs) == 0:
        return ret
    rets = [ret[i] for i in output_indexs]
    print("type(rets)",type(rets),rets[0])
    if len(rets) == 1:
        return rets[0]
    else:
        return rets


class Args(object):

    def __init__(self, data,context) -> None:
        super().__init__()
        # self.is_null = False
        self.not_ready_args = []
        self.data = data
        self.null_args = []
        self.args = []
        self.kwargs = {}
        self.index_dict = {}
        # self.context = context
        self.build_args(data,context)

    def __repr__(self) -> str:
        arg_str = ",".join([str(a) for a in self.args]) if self.args else ""
        withinputs = {}
        for k, v in self.kwargs.items():
            withinputs[k] = v #if v else "!"
        kwargs_str = "".join(["{}={},".format(k, v)
                             for k, v in withinputs.items()])
        if arg_str:
            return "({},{})".format(arg_str, kwargs_str)
        else:
            return "({})".format(kwargs_str)

    def build_args(self, data: Dict,context):

        for k, v in data.items():
            value = v['value']
            ret = None
            # print(v)
            self.index_dict[k]=v.get('index',0)
            if value == None:
                self.null_args.append(k)
            elif isinstance(value,str) and value=='None':
                self.null_args.append(k)
            elif isinstance(value, str) and value.startswith('@'):
                ret = self.build_on_context(value[1:],context)
            elif isinstance(value, List):
                ret = []
                for item in value:
                    if isinstance(item, str) and item.startswith('@'):
                        ret.append(self.build_on_context(item[1:],context))
                    else:
                        ret.append(item)
            else:
                ret = get_typed_argv(v.get('type',"Any"), value)
            kind = v.get("kind","POSITIONAL_OR_KEYWORD")
            if kind in ("POSITIONAL_OR_KEYWORD",):
                self.kwargs[k] = ret
            elif kind == "VAR_POSITIONAL":
                if isinstance(ret,List):
                    self.args = ret
                elif ret==None:
                    self.args = []
                else:
                    self.args = [ret]
                print('get VAR_POSITIONAL',ret,self.args)
            else:
                raise ValueError("arg kind error:{}".format(data))

    def build_on_context(self,key,context):
        if key.find('(')>-1:
            res = eval(key,all_context)
        elif key.find('.') > -1:
            mode, sub = key.split('.')
            res = all_const_back[mode][sub]
        else:
            res = context[key]
        return res


class Func(object):

    def __init__(self, info,context) -> None:
        self.info = info
        # self.type_ = info['type']
        self.module = info['from']
        self.args = Args(info.get('args', {}),context)

    def __repr__(self) -> str:
        return "{}{}".format(self.info['name'], self.args)

    def get_instance(self,):
        info = self.info
        input_len = len(self.args.null_args)
        if input_len == 1:
            instance = SingleCallable(
                info['name'], self.module, self.args,)
        elif input_len > 1:
            instance = MutilArgCallable(
                info['name'],self.module, self.args, 
            )
        else:
            instance = eval_called(info['name'], self.module, self.args,)
        op = info.get('op',"")
        # print(info['name'],instance,op)
        if op:
            return OPDICT[op](instance)
        return instance

    # def get_instance(self):
    #     return self.create_func(self.info)



def eval_called(func, module, args: Args):
    try:
        eval_func = all_const_back[module][func]
    except KeyError as e:
        error = ValueError("key error:{}.{}".format(module,func))
        ExeStack.exception(str(error))
        raise error
    try:
        print("eval_func",eval_func.__name__,args.args,args.kwargs)
        ret = eval_func(*args.args, **args.kwargs)
    except Exception as e:
        # ExeStack.exception(traceback.format_exc())
        raise e
    return ret



class SingleCallable(object):

    def __init__(self,
                 func: str,
                 module: str,
                 args: Args,) -> None:
        """
        @param: func, a string to query method from model
        @param: args,args must be a dict,the placeholder key is the key with value == None
        
        """
        self.str_func = func
        self.module_name = module
        self.func = all_const_back[module][func]
        self.args = args

    def __call__(self, placeholder: Any) -> Any:
        null_key = self.args.null_args[0]
        self.args.kwargs[null_key] = placeholder
        # print("SingleCallable",self.args.args,self.func)
        ret = self.func(*self.args.args, **self.args.kwargs)
        return ret

    def __repr__(self) -> str:
        return "{}{}".format(self.str_func, self.args)
# def print_numpy(n):
#     if isinstance(n,np.ndarray):
#         return "{} {}".format(n.shape,n.dtype)
#     else:
#         return str(n)

#TODO placehold类型
class MutilArgCallable(SingleCallable):

    def __init__(self, func: str, module: str, args: Args) -> None:
        super().__init__(func, module, args,)

    def __call__(self, placeholders: Any) -> Any:
        null_key = self.args.null_args
        if isinstance(placeholders,list):
            if len(null_key) != len(placeholders):
                raise ArgsError("null inputs:{} vs args input:{}".format(len(null_key) , len(placeholders)))
        # print((self.args.null_args,[ print_numpy(p) for p in placeholders]))
        try:
            indexs = [(self.args.index_dict[n],n) for n in self.args.null_args]
            indexs.sort()
            arg_keys = [k for i,k in indexs]
            for k,v in zip(arg_keys,placeholders):
                self.args.kwargs[k] = v
            ret = self.func(*self.args.args, **self.args.kwargs)
            return ret
        except Exception as e:
            print(traceback.format_exc())

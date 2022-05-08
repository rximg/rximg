import sys
sys.path.append('.')

from typing import List,Dict
import json
import pdb
from enum import Enum
from engine.func_factory import Func
import cv2
import numpy as np
# from custom.core import Subscribable
import reactivex.operators as ops
from reactivex import Observable
from utils.exception import DAGCircleError
rxim_print = lambda x : print(x)
# lst = [1,2,3]
is_null = lambda x : (not hasattr(x,'all')) and (x == None or x == "")

# def get_obj_by_str(line:str):
#     if line.startswith('$'):
#         line = line[1:]
#     find = line.find(':')
#     if find > -1:
#         line = line[:find]
#     obj = eval(line)
#     return obj

# def safe_type(obj):
#     if isinstance(obj,int):
#         return obj
#     elif isinstance(obj,float):
#         return obj
#     else:
#         return str(obj)

class DAGParser(object):


    def __init__(self,data) -> None:
        self.data = data
        self.sorted = []

    def run(self):
        nodes = self.build_graph(self.data)
        _ = self.topological_sorting(nodes)
        if len(nodes)!=len(_):
            raise DAGCircleError("find circle in DAG:{}<=>{}".format(len(nodes),len(_)))
        return _



    def build_graph(self,func_jsons:Dict):
        nodes = {}
        for k,value in func_jsons.items():
            in_ = []
            for arg_k,arg_v in value['args'].items():
                # print(arg_v)
                # if isinstance(arg_v,Dict):
                value = arg_v['value']
                if isinstance(value,str) and value !="" and value[0] == '@' and (not value.find('.')>-1):
                    in_.append(value[1:])
                elif isinstance(value,List):
                    for list_item in value:
                        if isinstance(list_item,str) and list_item[0] == '@' and (not list_item.find('.')>-1):
                            in_.append(list_item[1:])
            nodes[k] = {'in':in_,'out':[],'on_trace':False}
        # print(nodes)
        for k,v in nodes.items():
            for i in v['in']:
                nodes[i]['out'].append(k)
        # pprint(nodes)
        return nodes


    def topological_sorting(self,nodes:Dict):
        sorted_key = []
        empty_in_lst = []
        for k,v in list(nodes.items()):
            if not v['in']:
                empty_in_lst.append(k)
        while len(empty_in_lst):
            empty_in_node = empty_in_lst.pop(0)
            # print(empty_in_node,nodes[empty_in_node])
            sorted_key.append(empty_in_node)
            for out_k in nodes[empty_in_node]['out']:
                
                nodes[out_k]['in'].remove(empty_in_node)
                if not nodes[out_k]['in']:
                    empty_in_lst.append(out_k)

        return sorted_key


class RecursiveParse(object):

    def __init__(self) -> None:
        super().__init__()
        self.stack = []
        self.ready = {}


    def build_on_sorted(self,observers,sorteddag):
        context = {}
        for dagk in sorteddag:
            func_item = observers[dagk]
            func = Func(func_item,context)
            context[dagk] = func.get_instance()
        return context


    def run(self,data,):
        observers={}
        observers.update(data["observers"])
        observers.update(data["relations"])
        observers.update(data["parameters"])
        dag = DAGParser(observers)
        sorteddag = dag.run()
        ready = self.build_on_sorted(observers,sorteddag)
        # for k,v in ready.items():
            # if isinstance(v,Subscribable):
                # print('subscribe',v)
                # v.subscribe()


if __name__ == "__main__":

    # with open('./tests/dag_observers.json','r') as f:
    #     line = f.read()
    #     odata = json.loads(line)
    with open('./configs/seamlessClone.json','r') as f:
        line = f.read()
        rdata = json.loads(line)
    # obss = data["observers"]
    # relas = data["relations"]
    RecursiveParse().run(rdata)

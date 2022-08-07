
from collections import deque
import os
import os.path as osp
import json
import shutil
import sys
from threading import Thread
from time import sleep
import traceback
from typing import Dict

from engine.decorator import ExeStack

default_config = {
    "observers":{},
    "relations":{},
    "parameters":{},
    "edges":{}
}

class JsonConfig(object):


    def __init__(self,name) -> None:
        # self.meta_config_path = './configs/meta.json'
        self.config_dir = './configs/'
        self.current_name = name        # else:

    
    def new_config(self,):
        # self.current_name = value
        with open(self.config_dir+self.current_name +'.json','w') as f:
            f.write(json.dumps(default_config,indent=2))
        return self.current_name 

    @staticmethod
    def list_config_names():
        dirs = os.listdir('./configs/')
        dirs = [osp.splitext(d)[0] for d in dirs if d.endswith('.json')]
        # dirs.remove('meta')
        # if len(dirs) == 0 :
        #     dirs.append(self.current_name)
        
        return {
            'names':dirs,
            # 'current':self.current_name
        }


    def delete_config_by_name(self,name):

        path = osp.join(self.config_dir,name+'.json')
        if osp.isfile(path):
            os.remove(path)

    @property
    def current_config_dir(self):
        return "{}/{}.json".format(self.config_dir,self.current_name)

    def save_params(self,data:Dict):
        # path = 
        with open(self.current_config_dir,'w') as f:
            f.write(json.dumps(data,indent=2))
            

    def load_params(self,):
        if osp.isfile(self.current_config_dir):
            with open(self.current_config_dir,'r') as f:
                line = f.read()
                data = json.loads(line)
                return data
        else:
            return default_config

class Stack(Thread):

    def __init__(self) -> None:
        Thread.__init__(self)
        self.deq = deque(maxlen=5)
        self.daemon = True

    def run(self):
        while True:
            if len(list(self.deq)) != 0:
                task = self.deq.popleft()
                # try:
                task()
                # except Exception as e:
                    # print(traceback.format_exc())
                    # ExeStack.exception(traceback.format_exc())
                # print('len task',len(list(self.deq)))
            sleep(0.1)


def clean_tempfile(dir):
    if osp.isdir(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


if __name__ == "__main__":
    pass
    jcfg = JsonConfig()
    jcfg.save_params({})
    c = jcfg.load_params()
    print(c)
    jcfg.set_current_name('abc')
    jcfg.save_params({})
    c = jcfg.load_params()
    print(c)
    


                
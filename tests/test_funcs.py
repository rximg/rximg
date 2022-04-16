
import json
from engine.func_factory import Func
import pytest

def get_test_info(filename,key):
    with open(filename,'r') as f:
        line = f.read()
    js = json.loads(line)
    return js[key]

# def test_args():
#     pass

# def test_funcs():
#     info = get_test_info('tests/test_observers.json','testargs')
#     func = Func(info)
#     instance = func.get_instance()
#     assert instance=="12|1|1"

#     info = get_test_info('tests/test_observers.json','testargs')
#     info['args']['a0']['value']=None
#     func = Func(info)
#     instance = func.get_instance()
#     assert instance(2)=="12|2|1"
    # print(instance)
    # assert func.is_ready

def test_lambda():
    info = get_test_info('tests/test_lambda.json','lambda')
    func = Func(info)
    assert func.is_ready
    instance = func.get_instance()
    assert instance==2

def test_lambda_args():
    info = get_test_info('tests/test_lambda.json','lambdaargs')
    func = Func(info)
    instance = func.get_instance()
    assert instance(1,1)==2
    assert instance(1,100)==101
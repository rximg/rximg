from functools import partial
from utils.exception import ObservableTypeError
from reactivex import Observable, Subject
from reactivex.subject import ReplaySubject,BehaviorSubject
from typing import Callable, List
from engine.decorator import rx_func
from typing import Any
# subjects = []

# class Subscribable(object):
#     subjects = []
#     def __init__(self,head,subscribe) -> None:
#         self.head=head
#         self.subscribe_call = subscribe

#     def subscribe(self):
#         print(self.head,self.subscribe_call)
#         self.head.subscribe(self.subscribe_call)

#     def __repr__(self) -> str:
#         return "{}:{}".format(self.head,self.subscribe_call)
class SubjectStore(object):
    store = {}

    def __init__(self) -> None:
        pass

@rx_func(func_visible=False)
def build_observerable(head:Observable,pipe:List,subscribe:List)->Observable:
    if not isinstance(head,Observable):
        raise ObservableTypeError("head type:{}".format(type(head)))
    if len(pipe):
        pipe = [p for p in pipe if p is not None]
        head = head.pipe(*pipe)
    # for sub in subscribe:
    if subscribe:
        head.subscribe(subscribe)
    return head


@rx_func(func_visible=False)
def get_subject(uuid:str,type_='replay')->Observable:
    # if num==-1:
    #     return SubjectStore.store[head].values()
    # else:
    # uuid = '{}_{}'.format(head,num)
    if uuid in SubjectStore.store.keys():
        return SubjectStore.store[uuid]
    else:
        if type_ == 'behavior': 
            subj = BehaviorSubject(None)
        else:
            subj = ReplaySubject()
        SubjectStore.store[uuid] = subj
        return subj

# @rx_func(func_visible=False)
# def add_subject(head:str,num:int)->Observable:
#     subj = ReplaySubject()
#     if head not in Subject.store.keys():
#         SubjectStore.store[head] = {num:subj}
#     else:
#         SubjectStore.store[head].update({num:subj})

    # head.subscribe(subj)
    # Subscribable.subjects.append(partial(head.subscribe,subj))
    # return subj

# @rx_func(func_visible=False)
# def build_identity(head:Observable)->Observable:
#     if not isinstance(head,Observable):
#         raise ObservableTypeError("head type:{}".format(type(head)))
#     return head
    # subj = Subject()
    # Subscribable.subjects.append(partial(head.subscribe,subj))
    # return subj

# @rx_func(func_visible=False)
# def build_subsribe(head:Observable,subscribe:Any)->Callable:
#     return Subscribable(head,subscribe)



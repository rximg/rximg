from functools import partial
from utils.exception import ObservableTypeError
from reactivex import Observable, Subject
from reactivex.subject import ReplaySubject
from typing import Callable, List
from engine.decorator import view,rx_func
from typing import Any
# subjects = []

class Subscribable(object):
    subjects = []
    def __init__(self,head,subscribe) -> None:
        self.head=head
        self.subscribe_call = subscribe

    def subscribe(self):
        print(self.head,self.subscribe_call)
        self.head.subscribe(self.subscribe_call)

    def __repr__(self) -> str:
        return "{}:{}".format(self.head,self.subscribe_call)

@rx_func(func_visible=False)
def build_observerable(head:Observable,pipe:List)->Observable:
    if not isinstance(head,Observable):
        raise ObservableTypeError("head type:{}".format(type(head)))
    if len(pipe):
        pipe = [p for p in pipe if p is not None]
        head = head.pipe(*pipe)

    # subj = Subject()
    # head.subscribe(subj)
    # Subscribable.subjects.append(partial(head.subscribe,subj))
    return head

@rx_func(func_visible=False)
def build_subject(head:Observable)->Observable:
    if not isinstance(head,Observable):
        raise ObservableTypeError("head type:{}".format(type(head)))
    subj = ReplaySubject()
    head.subscribe(subj)
    # Subscribable.subjects.append(partial(head.subscribe,subj))
    return subj

# @rx_func(func_visible=False)
# def build_identity(head:Observable)->Observable:
#     if not isinstance(head,Observable):
#         raise ObservableTypeError("head type:{}".format(type(head)))
#     return head
    # subj = Subject()
    # Subscribable.subjects.append(partial(head.subscribe,subj))
    # return subj

@rx_func(func_visible=False)
def build_subsribe(head:Observable,subscribe:Any)->Callable:
    return Subscribable(head,subscribe)



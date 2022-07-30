from ast import arg
import reactivex as rx

from reactivex import operators as op
from reactivex import Observable, Subject
from reactivex.subject import ReplaySubject,BehaviorSubject
import traceback
import pdb
def on_error(args):
    if args:
        pdb.set_trace()
        print(args)
    # raise args
    # print(traceback.format_exc())

a0 = rx.of(*[1,2,3])
subj = ReplaySubject()
a0 = a0.pipe(op.map(lambda x:x/0))
a0.subscribe(subj,on_error=on_error)
# subj.subscribe(print)

b0 = rx.create(subj.subscribe)
b0.subscribe(print,on_error=on_error)

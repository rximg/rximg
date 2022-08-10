from enum import IntEnum
from engine.decorators import rx_func
import typing
from asyncio import Future

from typing import (
    Any,
    Callable,
    Iterable,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
    overload,
)
import cv2
import os.path as osp
import os
import pdb
import requests
import sys
sys.path.append('.')

import reactivex 
from reactivex.observable import Observable
from reactivex.subject import Subject

_T = TypeVar("_T")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_TKey = TypeVar("_TKey")
_TState = TypeVar("_TState")

_A = TypeVar("_A")
_B = TypeVar("_B")
_C = TypeVar("_C")
_D = TypeVar("_D")
_E = TypeVar("_E")
_F = TypeVar("_F")
_G = TypeVar("_G")

@rx_func(mutable_args=('args'))
def of(*args: _T) -> Observable[_T]:
    """This method creates a new observable sequence whose elements are taken
    from the arguments.

    .. marble::
        :alt: of

        [    of(1,2,3)    ]
        ---1--2--3--|

    Note:
        This is just a wrapper for
        :func:`reactivex.from_iterable(args) <reactivex.from_iterable>`

    Example:
        >>> res = reactivex.of(1,2,3)

    Args:
        args: The variable number elements to emit from the observable.

    Returns:
        The observable sequence whose elements are pulled from the
        given arguments
    """
    return reactivex.from_iterable(args)

@rx_func(mutable_args=('args'))
def zip(*args: Observable[Any]) -> Observable[Tuple[Any, ...]]:
    """Merges the specified observable sequences into one observable
    sequence by creating a :class:`tuple` whenever all of the
    observable sequences have produced an element at a corresponding
    index.

    .. marble::
        :alt: zip

        --1--2---3-----4---|
        -a----b----c-d------|
        [       zip()       ]
        --1,a-2,b--3,c-4,d-|

    Example:
        >>> res = rx.zip(obs1, obs2)

    Args:
        args: Observable sources to zip.

    Returns:
        An observable sequence containing the result of combining
        elements of the sources as a :class:`tuple`.
    """
    from reactivex.observable.zip import zip_

    return zip_(*args)


@rx_func(mutable_args=('sources','default_source'))
def case(
    mapper: Callable[[], _TKey],
    sources: Mapping[_TKey, Observable[_T]],
    default_source: Optional[Union[Observable[_T], "Future[_T]"]] = None,
) -> Observable[_T]:
    """Uses mapper to determine which source in sources to use.

    .. marble::
        :alt: case

        --1---------------|
        a--1--2--3--4--|
         b--10-20-30---|
        [case(mapper, { 1: a, 2: b })]
        ---1--2--3--4--|

    Examples:
        >>> res = reactivex.case(mapper, { '1': obs1, '2': obs2 })
        >>> res = reactivex.case(mapper, { '1': obs1, '2': obs2 }, obs0)

    Args:
        mapper: The function which extracts the value for to test in a
            case statement.
        sources: An object which has keys which correspond to the case
            statement labels.
        default_source: [Optional] The observable sequence or Future that will
            be run if the sources are not matched. If this is not provided,
            it defaults to :func:`empty`.

    Returns:
        An observable sequence which is determined by a case statement.
    """

    from reactivex.observable.case import case_

    return case_(mapper, sources, default_source)



@rx_func(mutable_args=('subject'))
def create_by_Subject(subject:Subject)->Observable[_T]:
    try:
        return reactivex.create(subject.subscribe)
    except Exception as e:
        print(subject)
        raise e

@rx_func(mutable_args=('sources'))
def concat(*sources: Observable[_T]) -> Observable[_T]:
    """Concatenates all of the specified observable sequences.

    .. marble::
        :alt: concat

        ---1--2--3--|
        --6--8--|
        [     concat()     ]
        ---1--2--3----6--8-|

    Examples:
        >>> res = reactivex.concat(xs, ys, zs)

    Args:
        sources: Sequence of observables.

    Returns:
        An observable sequence that contains the elements of each source in
        the given sequence, in sequential order.
    """

    from reactivex.observable.concat import concat_with_iterable_

    return concat_with_iterable_(sources)

@rx_func()
def empty(scheduler: Optional[reactivex.abc.SchedulerBase] = None) -> Observable[Any]:
    """Returns an empty observable sequence.

    .. marble::
        :alt: empty

        [     empty()     ]
        --|

    Example:
        >>> obs = reactivex.empty()

    Args:
        scheduler: [Optional] Scheduler instance to send the termination call
            on. By default, this will use an instance of
            :class:`ImmediateScheduler <reactivex.scheduler.ImmediateScheduler>`.

    Returns:
        An observable sequence with no elements.
    """

    from reactivex.observable.empty import empty_

    return empty_(scheduler)

@rx_func(mutable_args=('sources'))
def merge(*sources: Observable[Any]) -> Observable[Any]:
    """Merges all the observable sequences into a single observable sequence.

    .. marble::
        :alt: merge

        ---1---2---3---4-|
        -a---b---c---d--|
        [     merge()      ]
        -a-1-b-2-c-3-d-4-|

    Example:
        >>> res = reactivex.merge(obs1, obs2, obs3)

    Args:
        sources: Sequence of observables.

    Returns:
        The observable sequence that merges the elements of the
        observable sequences.
    """
    from reactivex.observable.merge import merge_

    return merge_(*sources)

@rx_func()
def range(
    start: int,
    stop: Optional[int] = None,
    step: Optional[int] = None,
    scheduler: Optional[reactivex.abc.SchedulerBase] = None,
) -> Observable[int]:
    """Generates an observable sequence of integral numbers within a
    specified range, using the specified scheduler to send out observer
    messages.

    .. marble::
        :alt: range

        [    range(4)     ]
        --0--1--2--3--|

    Examples:
        >>> res = reactivex.range(10)
        >>> res = reactivex.range(0, 10)
        >>> res = reactivex.range(0, 10, 1)

    Args:
        start: The value of the first integer in the sequence.
        stop: [Optional] Generate number up to (exclusive) the stop
            value. Default is `sys.maxsize`.
        step: [Optional] The step to be used (default is 1).
        scheduler: [Optional] The scheduler to schedule the values on.
            If not specified, the default is to use an instance of
            :class:`CurrentThreadScheduler
            <reactivex.scheduler.CurrentThreadScheduler>`.

    Returns:
        An observable sequence that contains a range of sequential
        integral numbers.
    """
    from reactivex.observable.range import range_

    return range_(start, stop, step, scheduler)

@rx_func()
def repeat_value(value: _T, repeat_count: Optional[int] = None) -> Observable[_T]:
    """Generates an observable sequence that repeats the given element
    the specified number of times.

    .. marble::
        :alt: repeat_value

        [ repeat_value(4) ]
        -4-4-4-4->

    Examples:
        >>> res = reactivex.repeat_value(42)
        >>> res = reactivex.repeat_value(42, 4)

    Args:
        value: Element to repeat.
        repeat_count: [Optional] Number of times to repeat the element.
            If not specified, repeats indefinitely.

    Returns:
        An observable sequence that repeats the given element the
        specified number of times.
    """
    from reactivex.observable.repeat import repeat_value_

    return repeat_value_(value, repeat_count)
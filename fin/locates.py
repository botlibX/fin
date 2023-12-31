# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402


"find objects"


import os
import time


from .objects import fqn, ident, items, update
from .default import Default
from .storage import Storage, read


def __dir__():
    return (
        'find',
        'fntime',
        'ident',
        'last',
        'search',
        'spl'
    )


__all__ = __dir__()


def find(mtc, selector=None, index=None) -> []:
    clz = Storage.long(mtc)
    nr = -1
    for fnm in sorted(Storage.fns(clz), key=fntime):
        obj = Default()
        read(obj, fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        nr += 1
        if index is not None and nr != int(index):
            continue
        yield (fnm, obj)



def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        return inp[0]


def search(obj, selector) -> bool:
    res = False
    if not selector:
        return True
    for key, value in items(selector):
        if key not in obj:
            res = False
            break
        for vval in spl(str(value)):
            val = getattr(obj, key, None)
            if str(vval).lower() in str(val).lower():
                res = True
            else:
                res = False
                break
    return res


"utility"


def fntime(daystr) -> float:
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def spl(txt) -> []:
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]

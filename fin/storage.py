# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402


"directory of objects"


import datetime
import os
import pathlib
import _thread


from .objects import Object, dump, fqn, load, update


def __dir__():
    return (
        'Storage',
        'read',
        'write'
    )


__all__ = __dir__()


lock = _thread.allocate_lock()


class Storage(Object):

    classes = {}
    wd = ""

    @staticmethod
    def add(clz) -> None:
        if not clz:
            return
        name = str(clz).split()[1][1:-2]
        Storage.classes[name] = clz

    @staticmethod
    def fns(mtc="") -> []:
        dname = ''
        pth = Storage.store(mtc)
        for rootdir, dirs, _files in os.walk(pth, topdown=False):
            if dirs:
                for dname in sorted(dirs):
                    if dname.count('-') == 2:
                        ddd = os.path.join(rootdir, dname)
                        fls = sorted(os.listdir(ddd))
                        for fll in fls:
                            yield strip(os.path.join(ddd, fll))

    @staticmethod
    def long(name) -> str:
        split = name.split(".")[-1].lower()
        res = name
        for named in Storage.classes:
            if split in named.split(".")[-1].lower():
                res = named
                break
        if "." not in res:
            for fnm in Storage.types():
                claz = fnm.split(".")[-1]
                if fnm == claz.lower():
                    res = fnm
        return res

    @staticmethod
    def skel():
        cdir(os.path.join(Storage.wd, "store", ""))

    @staticmethod
    def store(pth="") -> str:
        return os.path.join(Storage.wd, "store", pth)

    @staticmethod
    def types() -> []:
        return os.listdir(Storage.store())


def fetch(obj, pth) -> None:
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def ident(obj) -> str:
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )

def read(obj, pth) -> None:
    pth2 = Storage.store(pth)
    fetch(obj, pth2)
    return strip(pth)


def write(obj, pth=None) -> str:
    if pth is None:
        pth = ident(obj)
    pth2 = Storage.store(pth)
    sync(obj, pth2)
    return pth


def sync(obj, pth) -> None:
    with lock:
        cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)


"utility"


def cdir(pth) -> None:
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def strip(pth, nmr=3) -> str:
    return os.sep.join(pth.split(os.sep)[-nmr:])

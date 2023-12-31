# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E1101,W0718,W0612,E0611


"groups"


from . import Object


def __dir__():
    return (
            'Collection',
           )


__all__ = __dir__()


class Collection(Object):

    def __init__(self):
        Object.__init__(self)
        self.objs = []    

    def add(self, obj) -> None:
        self.objs.append(obj)

    def first(self):
        if self.objs:
            return self.objs[0]

    def remove(self, obj):
        if obj in self.objs:
            self.objs.remove(obj)

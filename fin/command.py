#!/usr/bin/env python3
# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,E0102,W0611,W0718,W0125


"commands"


from .excepts import Error
from .objects import Object
from .parsers import parse_command


def __dir__():
    return (
        "Command",
    )


__all__ = __dir__()


class Command(Object):

    cmds = Object()

    @staticmethod
    def add(func) -> None:
        setattr(Command.cmds, func.__name__, func)

    @staticmethod
    def handle(evt):
        parse_command(evt)
        func = getattr(Command.cmds, evt.cmd, None)
        if func:
            try:
                func(evt)
                evt.show()
            except Exception as exc:
                Error.add(exc)
        evt.ready()

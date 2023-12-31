#!/usr/bin/env python3
# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,E0102,W0611,W0718,W0125


"clients"


from .brokers import Fleet
from .command import Command
from .handler import Handler


def __dir__():
    return (
        "Client",
    )


__all__ = __dir__()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", Command.handle)
        Fleet.add(self)

    def announce(self, txt):
        self.raw(txt)

    def say(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        pass

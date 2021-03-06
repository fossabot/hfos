#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# HFOS - Hackerfleet Operating System
# ===================================
# Copyright (C) 2011-2017 Heiko 'riot' Weinen <riot@c-base.org> and others.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Heiko 'riot' Weinen"
__license__ = "GPLv3"

"""
Module: Logger
==============

HFOS own logger to avoid namespace clashes etc. Comes with some fancy
functions.

Log Levels
----------

verbose = 5
debug = 10
info = 20
warn = 30
error = 40
critical = 50
off = 100


"""

from circuits.core import Event
import pprint
# from circuits import Component, handler
# from uuid import uuid4
# import json


import time
import sys
import inspect
import six

# import os

root = None

events = 2
network = 4
verbose = 5
debug = 10
info = 20
warn = 30
error = 40
critical = 50
hilight = 60
off = 100

# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
lvldata = {
    events: ['EVENT', '\033[1:36m'],
    verbose: ['VERB', '\033[1;30m'],
    network: ['NET', '\033[1;34m'],
    debug: ['DEBUG', '\033[1;97m'],
    info: ['INFO', '\033[1;92m'],
    warn: ['WARN', '\033[1;93m'],
    error: ['ERROR', '\033[1;31;43m'],
    critical: ['CRIT', '\033[1;33;41m'],
    hilight: ['HILIGHT', '\033[1;4;30;106m']
}

terminator = '\033[0m'

count = 0

logfile = "/var/log/hfos/service.log"

console = verbose
live = False

verbosity = {'global': console,
             'file': off,
             'system': info,
             'console': console
             }

uncut = True
color = True  # TODO: Make this switchable via args

mute = []
solo = []

LiveLog = []

start = time.time()


def set_logfile(path):
    global logfile
    logfile = path


def ismuted(what):
    """
    Checks if a logged event is to be muted for debugging purposes.

    Also goes through the solo list - only items in there will be logged!

    :param what:
    :return:
    """

    state = False

    for item in solo:
        if item not in what:
            state = True
        else:
            state = False
            break

    for item in mute:
        if item in what:
            state = True
            break

    return state


def setup_root(newroot):
    """
    Sets up the root component, so the logger knows where to send logging
    signals.

    :param newroot:
    """
    global root

    root = newroot


def hfoslog(*what, **kwargs):
    """Logs all *what arguments.

    :param *what: Loggable objects (i.e. they have a string representation)
    :param lvl: Debug message level
    :param exc: Switch to better handle exceptions, use if logging in an
                except clause
    :param emitter: Optional log source, where this can't be determined
                    automatically
    :param sourceloc: Give specific source code location hints, used internally
    """

    # Count all messages (missing numbers give a hint at too high log level)
    global count
    count += 1

    if 'lvl' in kwargs:
        lvl = kwargs['lvl']
        if lvl < verbosity['global']:
            return
    else:
        lvl = info

    if 'emitter' in kwargs:
        emitter = kwargs['emitter']
    else:
        emitter = 'UNKNOWN'

    if 'exc' in kwargs:
        exception = True
    else:
        exception = False

    output = None

    timestamp = time.time()
    runtime = timestamp - start

    callee = None

    if verbosity['global'] <= debug:
        # Automatically log the current function details.

        if 'sourceloc' not in kwargs:

            # Get the previous frame in the stack, otherwise it would
            # be this function
            func = inspect.currentframe().f_back.f_code
            # Dump the message + the name of this function to the log.

            if exception:
                exc_type, exc_obj, exc_tb = sys.exc_info()  # NOQA
                line_no = exc_tb.tb_lineno
                lvl = error
            else:
                line_no = func.co_firstlineno

            callee = "[%.10s@%s:%i]" % (
                func.co_name,
                func.co_filename,
                line_no
            )
        else:
            callee = kwargs['sourceloc']

    msg = "[%s] : %5s : %.5f : %3i : [%5s]" % (time.asctime(),
                                               lvldata[lvl][0],
                                               runtime,
                                               count,
                                               emitter)

    content = ""

    if callee:
        if not uncut and lvl > 10:
            msg += "%-60s" % callee
        else:
            msg += "%s" % callee

    for thing in what:
        content += " "
        if kwargs.get('pretty', False):
            content += pprint.pformat(thing)
        else:
            content += str(thing)

    msg += content

    if ismuted(msg):
        return

    if not uncut and lvl > 10 and len(msg) > 1000:
        msg = msg[:1000]

    if lvl >= verbosity['file']:
        try:
            f = open(logfile, "a")
            f.write(msg + '\n')
            f.flush()
            f.close()
        except IOError:
            print("Can't open logfile %s for writing!" % logfile)
            # sys.exit(23)

    if lvl >= verbosity['console']:
        output = str(msg)
        if six.PY3 and color:
            output = lvldata[lvl][1] + output + terminator
        try:
            print(output)
        except UnicodeEncodeError as e:
            print(output.encode("utf-8"))
            hfoslog("Bad encoding encountered on previous message:", e,
                    lvl=error)
        except BlockingIOError:
            hfoslog("Too long log line encountered:", output[:20], lvl=error)

    if live:
        LiveLog.append(output)

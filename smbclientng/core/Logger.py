#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : LocalFileIO.py
# Author             : Podalirius (@podalirius_)
# Date created       : 24 June 2024


import os
import re
from enum import Enum


class LogLevel(Enum):
    INFO = 1
    DEBUG = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class Logger(object):
    """
    A Logger class that provides logging functionalities with various levels such as INFO, DEBUG, WARNING, ERROR, and CRITICAL.
    It supports color-coded output, which can be disabled, and can also log messages to a file.

    Attributes:
        __debug (bool): If True, debug level messages will be printed and logged.
        __nocolors (bool): If True, disables color-coded output.
        logfile (str|None): Path to a file where logs will be written. If None, logging to a file is disabled.

    Methods:
        __init__(debug=False, logfile=None, nocolors=False): Initializes the Logger instance.
        print(message=""): Prints a message to stdout and logs it to a file if logging is enabled.
        info(message): Logs a message at the INFO level.
        debug(message): Logs a message at the DEBUG level if debugging is enabled.
        error(message): Logs a message at the ERROR level.
    """

    def __init__(self, config, logfile=None):
        super(Logger, self).__init__()
        self.config = config
        self.logfile = logfile
        #
        if self.logfile is not None:
            if os.path.exists(self.logfile):
                k = 1
                while os.path.exists(self.logfile+(".%d"%k)):
                    k += 1
                self.logfile = self.logfile + (".%d" % k)
            open(self.logfile, "w").close()

    def print(self, message=""):
        nocolor_message = re.sub(r"\x1b[\[]([0-9;]+)m", "", message)
        if self.config.no_colors:
            print(nocolor_message)
        else:
            print(message)
        self.__write_to_logfile(nocolor_message)

    def info(self, message):
        nocolor_message = re.sub(r"\x1b[\[]([0-9;]+)m", "", message)
        if self.config.no_colors:
            print("[info] %s" % nocolor_message)
        else:
            print("[\x1b[1;92minfo\x1b[0m] %s" % message)
        self.__write_to_logfile("[info] %s" % nocolor_message)

    def debug(self, message):
        if self.config.debug == True:
            nocolor_message = re.sub(r"\x1b[\[]([0-9;]+)m", "", message)
            if self.config.no_colors:
                print("[debug] %s" % nocolor_message)
            else:
                print("[debug] %s" % message)
            self.__write_to_logfile("[debug] %s" % nocolor_message)

    def error(self, message):
        nocolor_message = re.sub(r"\x1b[\[]([0-9;]+)m", "", message)
        if self.config.no_colors:
            print("[error] %s" % nocolor_message)
        else:
            print("[\x1b[1;91merror\x1b[0m] %s" % message)
        self.__write_to_logfile("[error] %s" % nocolor_message)

    def __write_to_logfile(self, message):
        if self.logfile is not None:
            f = open(self.logfile, "a")
            f.write(message + "\n")
            f.close()
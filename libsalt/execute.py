#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
"""
Functions to execute native commands and get their output:
  - execCall
  - execCheck
  - execGetOutput
  - checkRoot
"""
from __future__ import print_function, unicode_literals, absolute_import

import subprocess
import sys
import os


def execCall(cmd, shell=True, env={'LANG': 'en_US'}):
  """
  Executes a command and return the exit code.
  The command is executed by default in a /bin/sh shell with en_US locale.
  The output of the command is not read. With some commands, it may hang if the output is not read when run in a shell.
  For this type of command, it is preferable to use execGetOutput even the return value is not read, or to use shell = False.
  """
  if shell and isinstance(cmd, list):
    cmd = ' '.join(cmd)
  return subprocess.call(cmd, shell=shell, env=env)


def execCheck(cmd, shell=True, env={'LANG': 'en_US'}):
  """
  Executes a command and return 0 if Ok or a subprocess.CalledProcessorError exception in case of error.
  The command is executed by default in a /bin/sh shell with en_US locale.
  """
  if shell and isinstance(cmd, list):
    cmd = ' '.join(cmd)
  return subprocess.check_call(cmd, shell=shell, env=env)


def execGetOutput(cmd, withError=False, shell=True, env={'LANG': 'en_US'}):
  """
  Executes a command and return its output in a list, line by line.
  In case of error, it returns a subprocess.CalledProcessorError exception.
  The command is executed by default in a /bin/sh shell with en_US locale.
  """
  DEVNULL = open(os.devnull, 'wb')
  stdErr = DEVNULL
  if withError:
    stdErr = subprocess.STDOUT
  if sys.version_info[0] > 2 or (sys.version_info[0] == 2 and sys.version_info[1] >= 7):  # ver >= 2.7
    if shell and isinstance(cmd, list):
      cmd = ' '.join(cmd)
    return subprocess.check_output(cmd, stderr=stdErr, shell=shell, env=env).splitlines()
  else:
    wrappedCmd = []
    if shell:
      wrappedCmd.append('sh')
      wrappedCmd.append('-c')
      if isinstance(cmd, list):
        wrappedCmd.append(' '.join(cmd))
      else:
        wrappedCmd.append(cmd)
    else:
      if isinstance(cmd, list):
        wrappedCmd = cmd
      else:
        wrappedCmd.append(cmd)
    p = subprocess.Popen(wrappedCmd, stdout=subprocess.PIPE, stderr=stdErr)
    output = p.communicate()[0]
    if p.returncode == 0:
      return output.splitlines()
    else:
      raise subprocess.CalledProcessError(returncode=p.returncode, cmd=cmd)


def checkRoot():
  """
  Raises an Exception if you run this code without root permissions
  """
  if os.getuid() != 0:
    raise Exception('You need root permissions.')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
"""
Functions to retrieve kernel parameters:
  - hasKernelParam
  - getKernelParamValue
"""
from __future__ import print_function, unicode_literals, absolute_import

import os


def hasKernelParam(param):
  """
  Defines if the kernel parameter param has been defined on the kernel command line or not
  """
  if os.path.exists('/proc/cmdline'):
    cmdline = open('/proc/cmdline', 'r').read().split()
    for chunk in cmdline:
      if param == chunk.split('=', 1)[0]:
        return True
  return False


def getKernelParamValue(param):
  """
  Returns the value of the kernel parameter, None if this param has no value and False if this param does not exist.
  """
  if os.path.exists('/proc/cmdline'):
    cmdline = open('/proc/cmdline', 'r').read().split()
    for chunk in cmdline:
      paramMap = chunk.split('=', 1)
      if param == paramMap[0]:
        if len(paramMap) > 1:
          return paramMap[1]
        else:
          return None
  return False

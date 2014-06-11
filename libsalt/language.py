#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
"""
Functions to handle locales and languages:
  - listAvailableLocales
  - getCurrentLocale
  - getDefaultLocale
  - setDefaultLocale
"""
from __future__ import print_function, unicode_literals, absolute_import

from .execute import *
import os
import glob
import locale
import re
import fileinput
import sys


def listAvailableLocales(mountPoint=None):
  """
  Returns a list of couples (name, title) for available utf8 locales on the system under 'mountPoint'.
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint is None:
    mountPoint = ''
  locales = []
  libdir = 'lib'
  if os.path.isdir('{0}/usr/lib64/locale'.format(mountPoint)):
    libdir = 'lib64'
  for path in sorted(glob.glob('{0}/usr/{1}/locale/*.utf8'.format(mountPoint, libdir))):
    locale = os.path.basename(path).rsplit('.', 1)[0]
    title = execGetOutput("strings {0}/LC_IDENTIFICATION | grep -i 'locale for'".format(path))[0]
    locales.append((locale, title))
  return locales


def getCurrentLocale():
  """
  Returns the current used locale in the current environment.
  """
  lang, enc = locale.getdefaultlocale()
  return "{0}.{1}".format(lang, re.sub(r'utf-8', r'utf8', enc.lower()))


def getDefaultLocale(mountPoint=None):
  """
  Returns the default locale as defined in /etc/profile.d/lang.c?sh
  """
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint is None:
    mountPoint = ''
  locale = None
  for f in ('lang.sh', 'lang.csh'):
    if not locale:
      for line in open('{0}/etc/profile.d/{1}'.format(mountPoint, f), 'rb').read().decode('utf8').splitlines():
        if line.startswith('export LANG='):
          locale = re.sub(r'export LANG=(.*)', r'\1', line)
          break
        elif line.startswith('setenv LANG '):
          locale = re.sub(r'setenv LANG (.*)', r'\1', line)
          break
  return locale


def setDefaultLocale(locale, mountPoint=None):
  """
  Set the default locale in the /etc/profile.d/lang.c?sh file
  """
  checkRoot()
  if mountPoint and not os.path.isdir(mountPoint):
    raise IOError("'{0}' does not exist or is not a directory.".format(mountPoint))
  if mountPoint is None:
    mountPoint = ''
  fi = fileinput.FileInput('{0}/etc/profile.d/lang.sh'.format(mountPoint), inplace=1)
  for line in fi:
    sys.stdout.write(re.sub(r'^(export LANG=).*', r'\1{0}'.format(locale), line))
  fi.close()
  fi = fileinput.FileInput('{0}/etc/profile.d/lang.csh'.format(mountPoint), inplace=1)
  for line in fi:
    sys.stdout.write(re.sub(r'^(setenv LANG ).*', r'\1{0}'.format(locale), line))
  fi.close()

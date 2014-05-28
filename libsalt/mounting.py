#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
"""
Help mounting/unmounting a filesystem.
Functions:
  - getMountPoint
  - isMounted
  - mountDevice
  - umountDevice
"""
from __future__ import print_function, unicode_literals, absolute_import

__copyright__ = 'Copyright 2011-2013, Salix OS'
__license__ = 'GPL2+'
from .execute import *
from .fs import getFsType
import os
import re
from stat import *

_tempMountDir = '/mnt/.tempSalt'


def getTempMountDir():
  return _tempMountDir


def getMountPoint(device):
  """
  Find the mount point to this 'device' or None if not mounted.
  """
  mountpoint = None
  path = os.path.abspath(device)
  for line in execGetOutput(['/bin/mount'], shell=False):
    p, _, mp, _ = line.split(' ', 3)  # 3 splits max, _ is discarded
    if os.path.islink(p):
      p = os.path.realpath(p)
    if p == path:
      mountpoint = mp
      break
  return mountpoint


def isMounted(device):
  """
  Same as os.path.ismount(path) but using a block device.
  """
  if getMountPoint(device):
    return True
  else:
    return False


def _deleteMountPoint(mountPoint):
  # delete the empty directory
  try:
    os.rmdir(mountPoint)
  except:
    pass
  # delete the temporary directory if not empty
  if os.path.isdir(_tempMountDir):
    try:
      os.rmdir(_tempMountDir)
    except:
      pass


def mountDevice(device, fsType=None, mountPoint=None):
  """
  Mount the 'device' of 'fsType' filesystem under 'mountPoint'.
  If 'mountPoint' is not specified, '{0}/device' will be used.
  Returns False if it fails or the mount point if it succeed.
  """.format(_tempMountDir)
  if not fsType:
    fsType = getFsType(re.sub(r'/dev/', '', device))
  if not fsType:
    return False
  autoMP = False
  if not mountPoint:
    mountPoint = '{0}/{1}'.format(_tempMountDir, os.path.basename(device))
    if os.path.exists(mountPoint):
      return False
    autoMP = True
  if not os.path.exists(mountPoint):
    try:
      os.makedirs(mountPoint)
    except os.error:
      pass
  ret = execCall(['mount', '-t', fsType, device, mountPoint], shell=False)
  if ret != 0 and autoMP:
    _deleteMountPoint(mountPoint)
  else:
    return mountPoint
  return ret == 0


def umountDevice(deviceOrPath, tryLazyUmount=True, deleteMountPoint=True):
  """
  Unmount the 'deviceOrPath' which could be a device or a mount point.
  If umount failed, try again with a lazyUmount if 'tryLazyUmount' is True.
  Will delete the mount point if 'deleteMountPoint' is True.
  Returns False if it fails.
  """
  if S_ISBLK(os.stat(deviceOrPath).st_mode):
    mountPoint = getMountPoint(deviceOrPath)
  else:
    mountPoint = deviceOrPath
  if mountPoint:
    ret = execCall(['umount', mountPoint], shell=False)
    if ret != 0:
       ret = execCall(['umount', '-l', mountPoint], shell=False)
    if ret == 0 and deleteMountPoint:
      _deleteMountPoint(mountPoint)
    return ret == 0
  else:
    return False

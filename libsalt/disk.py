#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
"""
Get information from the system disks and partitions.
For now it only handles (S/P)ATA disks and partitions, RAID and LVM are not supported yet.
MSDOS/GPT partition scheme is indicated if 'parted' is installed.
/proc and /sys should be mounted to retrieve information.
If the disk is GPT, will tell the GUID in the partition information.
For a MSDOS disk, the declared FS type is returned.
Functions:
  - getDisks
  - getDiskInfo
  - getPartitions
  - getSwapPartitions
  - getPartitionInfo
"""
from __future__ import print_function, unicode_literals, absolute_import

from .execute import *
from .fs import *
from .freesize import *
import glob
import re
import os
from stat import *


def getDisks():
  """
  Returns the disks devices (without /dev/) connected to the computer.
  RAID and LVM are not supported yet.
  """
  ret = []
  for l in open('/proc/partitions', 'r').read().splitlines():
    if re.search(r' sd[^0-9]+$', l):
      ret.append(re.sub(r'.*(sd.*)', r'\1', l))
  return ret


def getDiskInfo(diskDevice):
  """
  Returns a dictionary with the following disk device's info:
    - model: model name
    - size: size in bytes
    - sizeHuman: human readable size
    - removable: whether it is removable or not
    - type: either 'msdos' or 'gpt' if parted is installed, or None if not.
  diskDevice should no be prefixed with '/dev/'
  """
  if S_ISBLK(os.stat('/dev/{0}'.format(diskDevice)).st_mode) and os.path.exists('/sys/block/{0}'.format(diskDevice)):
    if os.path.exists('/sys/block/{0}/device/model'.format(diskDevice)):
      modelName = open('/sys/block/{0}/device/model'.format(diskDevice), 'r').read().strip()
    else:
      modelName = None
    blockSize = int(open('/sys/block/{0}/queue/logical_block_size'.format(diskDevice), 'r').read().strip())
    size = int(open('/sys/block/{0}/size'.format(diskDevice), 'r').read().strip()) * blockSize
    sizeHuman = getHumanSize(size)
    try:
      removable = int(open('/sys/block/{0}/removable'.format(diskDevice), 'r').read().strip()) == 1
    except:
      removable = False
    try:
      partType = execGetOutput("/usr/sbin/parted -m -s /dev/{0} print|sed -n '2p'|cut -d: -f6".format(diskDevice), shell=True)[0]
    except:
      partType = None
    return {'model': modelName, 'size': size, 'sizeHuman': sizeHuman, 'removable': removable, 'type': partType}
  else:
    return None


def getPartitions(diskDevice, skipExtended=True, skipSwap=True):
  """
  Returns partitions matching exclusion filters.
  """
  if S_ISBLK(os.stat('/dev/{0}'.format(diskDevice)).st_mode) and os.path.exists('/sys/block/{0}'.format(diskDevice)):
    parts = [p.replace('/sys/block/{0}/'.format(diskDevice), '') for p in glob.glob('/sys/block/{0}/{0}*'.format(diskDevice))]
    fsexclude = [False]
    if skipExtended:
      fsexclude.append('Extended')
    if skipSwap:
      fsexclude.append('swap')
    return [part for part in parts if getFsType(part) not in fsexclude]
  else:
    return None


def getSwapPartitions(devices=getDisks()):
  """
  Returns partition devices with Linux Swap type.
  """
  ret = []
  for diskDevice in devices:
    parts = [p.replace('/sys/block/{0}/'.format(diskDevice), '') for p in glob.glob('/sys/block/{0}/{0}*'.format(diskDevice))]
    ret.extend([part for part in parts if getFsType(part) == 'swap'])
  return ret


def getPartitionInfo(partitionDevice):
  """
  Returns a dictionary with the partition information:
    - fstype
    - label
    - size
    - sizeHuman
    - partId if sfdisk/sgdisk is installed or None otherwise.
  """
  checkRoot()
  if S_ISBLK(os.stat('/dev/{0}'.format(partitionDevice)).st_mode):
    fstype = getFsType(partitionDevice)
    label = getFsLabel(partitionDevice)
    diskDevice = re.sub(r'[0-9]*$', '', partitionDevice)
    if re.match(r'^.+[0-9]p$', diskDevice):
      diskDevice = diskDevice[:-1]
    blockSize = int(open('/sys/block/{0}/queue/logical_block_size'.format(diskDevice), 'r').read().strip())
    size = int(open('/sys/block/{0}/{1}/size'.format(diskDevice, partitionDevice), 'r').read().strip()) * blockSize
    sizeHuman = getHumanSize(size)
    partId = None
    try:
      partId = execGetOutput(r"/sbin/sfdisk --dump /dev/sda 2>/dev/null|sed -rn '\,^/dev/{0},{s/.*, Id= *([^,]+),?.*/\1/p}'".format(partitionDevice), shell=True)[0]
    except:
      pass
    return {'fstype': fstype, 'label': label, 'size': size, 'sizeHuman': sizeHuman, 'partId': partId}
  else:
    return None

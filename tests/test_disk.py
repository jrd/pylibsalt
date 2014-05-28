#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import, division
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import disk


@unittest.skipUnless(os.getuid() == 0, "root required")
class TestDisk(unittest.TestCase):
  def setUp(self):
    os.system('dd if=/dev/zero of=test_disk bs=1M count=50 >/dev/null 2>&1')
    os.system('parted -s test_disk mklabel msdos >/dev/null 2>&1')
    os.system('parted -s test_disk mkpart primary ext2 0 10M >/dev/null 2>&1')
    os.system('parted -s test_disk mkpart extended 10M 50M >/dev/null 2>&1')
    os.system('parted -s test_disk mkpart logical ext2 10M 30M >/dev/null 2>&1')
    os.system('parted -s test_disk mkpart logical linux-swap 30M 50M >/dev/null 2>&1')
    os.system('losetup -P /dev/loop7 test_disk')
    os.system('mkfs.ext2 -L test /dev/loop7p1 >/dev/null 2>&1')
    os.system('mkfs.ext2 -L test2 /dev/loop7p5 >/dev/null 2>&1')
    os.system('mkswap /dev/loop7p6 >/dev/null 2>&1')
    os.system('mkdir /tmp/loop7p1')
    os.system('mount /dev/loop7p1 /tmp/loop7p1')

  def tearDown(self):
    os.system('umount /tmp/loop7p1')
    os.system('rmdir /tmp/loop7p1')
    os.system('losetup -d /dev/loop7')
    os.system('rm -f test_disk')

  def test_get_disks(self):
    disks = disk.getDisks()
    self.assertGreater(len(disks), 0)
    self.assertEqual(disks[0], 'sda')

  def test_disk_info(self):
    diskInfo = disk.getDiskInfo('loop7')
    self.assertIsNone(diskInfo['model'])
    self.assertEqual(diskInfo['size'], 50 * 1024 * 1024)
    self.assertEqual(diskInfo['sizeHuman'], '50.0MB')
    self.assertFalse(diskInfo['removable'])

  def test_partition_info(self):
    self.assertEqual(len(disk.getPartitions('loop7')), 2)
    self.assertEqual(len(disk.getSwapPartitions(['loop7'])), 1)
    partInfo = disk.getPartitionInfo('loop7p1')
    self.assertEqual(partInfo['fstype'], 'ext2')
    self.assertEqual(partInfo['label'], 'test')
    size = 10 * 1000 * 1000 + 383 - 512 + 1
    self.assertEqual(partInfo['size'], size)
    self.assertEqual(partInfo['sizeHuman'], unicode(round(size / 1024 / 1024, 1)) + 'MB')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import freesize


@unittest.skipUnless(os.getuid() == 0, "root required")
class TestFreesize(unittest.TestCase):
  def setUp(self):
    os.system('dd if=/dev/zero of=test_disk bs=1M count=50 >/dev/null 2>&1')
    os.system('parted -s test_disk mklabel msdos >/dev/null 2>&1')
    os.system('parted -s test_disk mkpart primary ext2 0 10M >/dev/null 2>&1')
    os.system('parted -s test_disk mkpart extended 10M 50M >/dev/null 2>&1')
    os.system('parted -s test_disk mkpart logical ext2 10M 50M >/dev/null 2>&1')
    os.system('losetup -P /dev/loop7 test_disk')
    os.system('mkfs.ext2 /dev/loop7p1 >/dev/null 2>&1')
    os.system('mkfs.ext2 /dev/loop7p5 >/dev/null 2>&1')
    os.system('mkdir /tmp/loop7p1')
    os.system('mount /dev/loop7p1 /tmp/loop7p1')

  def tearDown(self):
    os.system('umount /tmp/loop7p1')
    os.system('rmdir /tmp/loop7p1')
    os.system('losetup -d /dev/loop7')
    os.system('rm -f test_disk')

  def test_human_size(self):
    self.assertEqual(freesize.getHumanSize(7923593216L), '7.4GB')

  def test_size_slash(self):
    stats = freesize.getSizes('/')
    self.assertGreater(stats['size'], 0)
    self.assertGreater(stats['free'], 0)
    self.assertGreater(stats['uuFree'], 0)
    self.assertGreater(stats['used'], 0)
    self.assertGreater(stats['uuUsed'], 0)

  def test_mounted_partition(self):
    part = '/dev/loop7p1'  # mounted partition
    stats = freesize.getSizes(part)
    self.assertGreater(stats['size'], 0)
    self.assertGreater(stats['free'], 0)
    self.assertGreater(stats['uuFree'], 0)
    self.assertGreater(stats['used'], 0)
    self.assertGreater(stats['uuUsed'], 0)

  def test_extended_partition(self):
    part = '/dev/loop7p2'  # extended partition (not a logical volume)
    stats = freesize.getSizes(part)
    self.assertGreater(stats['size'], 0)
    self.assertIsNone(stats['free'])
    self.assertIsNone(stats['uuFree'])
    self.assertIsNone(stats['used'])
    self.assertIsNone(stats['uuUsed'])

  def test_used_size(self):
    stats1 = freesize.getUsedSize('.')
    self.assertGreater(stats1['size'], 0)
    stats2 = freesize.getUsedSize('.', 524288)
    self.assertGreater(stats2['size'], 0)
    self.assertGreater(stats2['size'], stats1['size'])

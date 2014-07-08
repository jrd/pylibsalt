#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import execute, fs
from glob import glob


class TestFs(unittest.TestCase):
  def setUp(self):
    for ft in ('ext2', 'ext4', 'xfs', 'reiserfs', 'jfs', 'btrfs', 'ntfs', 'fat16', 'fat32', 'swap'):
      f = '{0}.fs'.format(ft)
      if ft == 'btrfs':
        size = 300  # btrfs minimum size is 256M
      else:
        size = 50
      execute.execCall(['dd', 'if=/dev/zero', 'of={0}'.format(f), 'bs=1M', 'count={0:d}'.format(size)], shell=False)

  def tearDown(self):
    for f in glob('*.fs'):
      os.unlink(f)

  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_fs_device(self):
    part = 'sda1'
    fstype = fs.getFsType(part)
    label = fs.getFsLabel(part)
    self.assertTrue(fstype)
    self.assertGreater(len(fstype), 0)
    self.assertTrue(label)
    self.assertGreater(len(label), 0)

  def test_fs_file(self):
    for ft in ('ext2', 'ext4', 'xfs', 'reiserfs', 'jfs', 'btrfs', 'ntfs', 'fat16', 'fat32', 'swap'):
      f = '{0}.fs'.format(ft)
      self.assertEqual(fs.makeFs(f, ft, 'test_{0}'.format(ft), True), 0)
      if ft in ('fat16', 'fat32'):
        expectedFt = 'vfat'
      else:
        expectedFt = ft
      self.assertEqual(fs.getFsType(f), expectedFt)
      self.assertEqual(fs.getFsLabel(f).upper(), 'test_{0}'.format(ft).upper())

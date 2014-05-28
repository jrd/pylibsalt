#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import fstab


class TestFstab(unittest.TestCase):
  def _create_fstab(self):
    fstab.createFsTab('.')
    self.assertTrue(os.path.exists('./etc/fstab'))

  def tearDown(self):
    if os.path.exists('./etc/fstab'):
      try:
        os.unlink('./etc/fstab')
        os.rmdir('./etc')
      except:
        pass

  def test_add_fstab_manual(self):
    self._create_fstab()
    fstab.addFsTabEntry('.', '/dev/sda1', '/', 'ext4', 'defaults', 1, 1)
    fstab.addFsTabEntry('.', '/dev/sda1', '/home', 'ext3', 'defaults', 1, 2)
    lines = open('./etc/fstab', 'r').read().splitlines()
    self.assertEqual(len(lines), 2)
    line1, line2 = lines
    dev, mp, fs, opts, dump, fsck = line1.split()
    self.assertEqual(dev, '/dev/sda1')
    self.assertEqual(mp, '/')
    self.assertEqual(fs, 'ext4')
    self.assertEqual(opts, 'defaults')
    self.assertEqual(dump, '1')
    self.assertEqual(fsck, '1')
    dev, mp, fs, opts, dump, fsck = line2.split()
    self.assertEqual(dev, '/dev/sda1')
    self.assertEqual(mp, '/home')
    self.assertEqual(fs, 'ext3')
    self.assertEqual(opts, 'defaults')
    self.assertEqual(dump, '1')
    self.assertEqual(fsck, '2')

  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_add_fstab_guess_fs(self):
    self._create_fstab()
    fstab.addFsTabEntry('.', '/dev/sda1', '/', 'ext4', 'defaults', 1, 1)
    fstab.addFsTabEntry('.', '/dev/sda1', '/root', None, None, 1, 2)
    lines = open('./etc/fstab', 'r').read().splitlines()
    self.assertEqual(len(lines), 2)
    line1, line2 = lines
    dev, mp, fs, opts, dump, fsck = line1.split()
    self.assertEqual(dev, '/dev/sda1')
    self.assertEqual(mp, '/')
    self.assertEqual(fs, 'ext4')
    self.assertEqual(opts, 'defaults')
    self.assertEqual(dump, '1')
    self.assertEqual(fsck, '1')
    dev, mp, fs, opts, dump, fsck = line2.split()
    self.assertEqual(dev, '/dev/sda1')
    self.assertEqual(mp, '/root')
    self.assertGreater(len(fs), 0)
    self.assertGreater(len(opts), 0)
    self.assertEqual(dump, '1')
    self.assertEqual(fsck, '2')

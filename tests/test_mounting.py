#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import mounting as m, execute, fs


@unittest.skipUnless(os.getuid() == 0, "root required")
class TestMounting(unittest.TestCase):
  def setUp(self):
    execute.execCall(['dd', 'if=/dev/zero', 'of=ext4.fs', 'bs=1M', 'count=50'], shell=False)
    fs.makeFs('ext4.fs', 'ext4', 'test ext4', True)

  def tearDown(self):
    os.system('umount -l ext4.fs 2>/dev/null')  # be sure it's umounted
    os.system('rm -r {0}'.format(m._tempMountDir))
    os.unlink('ext4.fs')

  def test_mounting(self):
    self.assertFalse(m.isMounted('ext4.fs'))
    self.assertIn('ext4.fs', m.mountDevice('ext4.fs'))
    self.assertTrue(m.isMounted('ext4.fs'))
    self.assertEqual(m.getMountPoint('ext4.fs'), '{0}/ext4.fs'.format(m._tempMountDir))
    self.assertTrue(m.umountDevice('ext4.fs'))
    self.assertFalse(m.isMounted('ext4.fs'))

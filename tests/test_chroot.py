#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import chroot


class TestChroot(unittest.TestCase):
  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_io_error(self):
    self.assertRaises(IOError, chroot.execChroot, None, '/bin/echo')
    self.assertRaises(IOError, chroot.execChroot, '/nonExistant', '/bin/echo')

  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_ls_ok(self):
    self.assertEqual(chroot.execChroot('/', ['/bin/echo', '-n']), 0)
    self.assertEqual(chroot.execChroot('/', "/bin/ls | grep -q '.'", shell=True), 0)

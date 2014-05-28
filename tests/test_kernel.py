#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import kernel


class TestKernel(unittest.TestCase):
  """
  It is supposed that the /proc/cmdline always have "ro" and "root=XXX" parameters.
  """

  def test_has_kernel_param(self):
    self.assertTrue(kernel.hasKernelParam('ro'))
    self.assertTrue(kernel.hasKernelParam('root'))
    self.assertFalse(kernel.hasKernelParam('nonexistant'))

  def test_get_kernel_param_value(self):
    self.assertNotEqual(kernel.getKernelParamValue('root'), '')
    self.assertIsNone(kernel.getKernelParamValue('ro'))
    self.assertFalse(kernel.getKernelParamValue('nonexistant'))

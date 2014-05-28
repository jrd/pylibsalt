#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import salt


class TestSalt(unittest.TestCase):
  def test_basic(self):
    with self.assertRaisesRegexp(Exception, 'Not in SaLT Live environment.'):
      salt.getSaLTVersion()

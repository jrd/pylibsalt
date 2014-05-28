#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import execute as ex
import subprocess


class TestExecute(unittest.TestCase):
  def test_call_ok(self):
    self.assertEqual(ex.execCall("ls >/dev/null"), 0)
    self.assertEqual(ex.execCall("ls -lh | grep -q '[.]'"), 0)
    self.assertEqual(ex.execCall(['echo', '-n'], shell=False), 0)

  def test_call_ko(self):
    self.assertEqual(ex.execCall("xyz 2>/dev/null"), 127)
    self.assertRaises(subprocess.CalledProcessError, ex.execCheck, "xyz")

  def test_exec_check(self):
    self.assertEqual(ex.execCheck("ls >/dev/null"), 0)

  def test_exec_get_output(self):
    self.assertEqual(ex.execGetOutput("pwd")[0].strip(), os.getcwd())

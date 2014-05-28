#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import keyboard as kb


class TestKeyboard(unittest.TestCase):
  def test_available_keymaps(self):
    keymaps = kb.listAvailableKeymaps()
    self.assertIsInstance(keymaps, list)
    self.assertGreater(len(keymaps), 0)
    keymaps = dict(keymaps)  # change it to dictionnary
    self.assertEqual(keymaps['fr-latin9'], 'azerty')

  def test_current_settings(self):
    keymap = kb.findCurrentKeymap()
    self.assertTrue(keymap)
    numlock = kb.isNumLockEnabledByDefault()
    self.assertIsInstance(numlock, bool)
    ibus = kb.isIbusEnabledByDefault()
    self.assertIsInstance(ibus, bool)

  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_set_settings(self):
    keymap = kb.findCurrentKeymap()
    numlock = kb.isNumLockEnabledByDefault()
    ibus = kb.isIbusEnabledByDefault()
    self.assertEqual(kb.setDefaultKeymap('fr-latin1'), 0)
    self.assertEqual(kb.findCurrentKeymap(), 'fr-latin1')
    self.assertEqual(kb.setNumLockDefault(True), 0)
    self.assertTrue(kb.isNumLockEnabledByDefault())
    self.assertEqual(kb.setIbusDefault(True), 0)
    self.assertTrue(kb.isIbusEnabledByDefault())
    # restore actual keyboard parameters
    kb.setDefaultKeymap(keymap)
    kb.setNumLockDefault(numlock)
    kb.setIbusDefault(ibus)

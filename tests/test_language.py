#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import language as l


class TestLanguage(unittest.TestCase):
  def test_get_settings(self):
    locales = l.listAvailableLocales()
    self.assertIsInstance(locales, list)
    self.assertGreater(len(locales), 0)
    self.assertIn('fr_FR', dict(locales))
    curlocale = l.getCurrentLocale()
    self.assertGreater(len(curlocale), 3)
    self.assertIn('.utf8', curlocale)
    deflocale = l.getDefaultLocale()
    self.assertGreater(len(deflocale), 3)
    self.assertIn('.utf8', deflocale)

  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_set_settings(self):
    deflocale = l.getDefaultLocale()
    l.setDefaultLocale('zu_ZA.utf8')
    locale = l.getDefaultLocale()
    self.assertEqual(locale, 'zu_ZA.utf8')
    l.setDefaultLocale(deflocale)

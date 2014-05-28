#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import timezone


class TestTimezone(unittest.TestCase):
  def test_get_settings(self):
    continents = timezone.listTZContinents()
    self.assertIsInstance(continents, list)
    self.assertGreater(len(continents), 0)
    self.assertIn('Europe', continents)
    cities = timezone.listTZCities('Europe')
    self.assertIsInstance(cities, list)
    self.assertGreater(len(cities), 0)
    self.assertIn('Paris', cities)
    tz = timezone.listTimeZones()
    self.assertIsInstance(tz, dict)
    self.assertGreater(len(tz), 0)
    self.assertIn('Europe', tz)
    self.assertIn('Paris', tz['Europe'])
    deftz = timezone.getDefaultTimeZone()
    self.assertIn('/', deftz)
    self.assertEqual(len(deftz.split('/')), 2)

  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_set_settings(self):
    deftz = timezone.getDefaultTimeZone()
    timezone.setDefaultTimeZone('Etc/Zulu')
    tz = timezone.getDefaultTimeZone()
    self.assertIn('/', tz)
    self.assertEqual(len(tz.split('/')), 2)
    self.assertEqual(tz, 'Etc/Zulu')
    timezone.setDefaultTimeZone(deftz)
    ntp = timezone.isNTPEnabledByDefault()
    self.assertIsInstance(ntp, bool)
    timezone.setNTPDefault(True)
    self.assertTrue(timezone.isNTPEnabledByDefault())
    timezone.setNTPDefault(False)
    self.assertFalse(timezone.isNTPEnabledByDefault())
    timezone.setNTPDefault(ntp)

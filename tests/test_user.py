#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et ai sta sts=2 sw=2 ts=2 tw=0:
from __future__ import print_function, unicode_literals, absolute_import
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from libsalt import user


class TestUser(unittest.TestCase):
  _testUser = '__test__'

  def tearDown(self):
    if self._testUser in open('/etc/passwd').read():
      try:
        user.deleteSystemUser(self._testUser)
      except:
        pass  # not a problem

  def test_list_users(self):
    users = user.listRegularSystemUsers()
    self.assertGreater(len(users), 0)

  @unittest.skipUnless(os.getuid() == 0, "root required")
  def test_create_user(self):
    self.assertEqual(user.createSystemUser(self._testUser, password='test'), 0)
    self.assertIn(self._testUser, user.listRegularSystemUsers())
    self.assertTrue(user.checkPasswordSystemUser(self._testUser, 'test', mountPoint='/'))
    self.assertFalse(user.checkPasswordSystemUser(self._testUser, 'test2'))
    self.assertEqual(user.deleteSystemUser(self._testUser), 0)
    self.assertNotIn(self._testUser, user.listRegularSystemUsers())
    self.assertEqual(user.createSystemUser(self._testUser, mountPoint='/./'), 0)  # to be different than '/' and to really force the chroot ;-)
    self.assertIn(self._testUser, user.listRegularSystemUsers())
    self.assertEqual(user.changePasswordSystemUser(self._testUser, 'test'), 0)
    self.assertTrue(user.checkPasswordSystemUser(self._testUser, 'test'))
    self.assertFalse(user.checkPasswordSystemUser(self._testUser, 'test3'))
    self.assertEqual(user.deleteSystemUser(self._testUser, mountPoint='/./'), 0)
    self.assertNotIn(self._testUser, user.listRegularSystemUsers())

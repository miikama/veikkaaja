"""Test whether the CI can access some basic API endpoints"""
import os
import unittest

from veikkaaja.veikkaus_client import VeikkausClient


class TestAccess(unittest.TestCase):
    """test access to API."""

    @unittest.skipIf('CI' in os.environ, "This is not currently run in Github CI.")
    def test_login(self):
        """Login is attempted upon client initialization"""

        client = VeikkausClient()
        self.assertIsNotNone(client.session)

"""Test common functionality"""
import unittest


class MyTestCase(unittest.TestCase):
    """Dummy Test Class"""

    def test_common(self):
        """Dummy Test Case"""
        self.assertTrue(True)  # pylint: disable=redundant-unittest-assert

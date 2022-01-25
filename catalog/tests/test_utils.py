# catalog/tests/test_utils.py
from datetime import date
from unittest import TestCase

from ..utils import format_date


class UtilsTestCase(TestCase):
    def test_format_date(self) -> None:
        self.assertEqual(format_date(date(2021, 1, 1)), "Jan 01, 2021")
        self.assertEqual(format_date(None), "")
        self.assertEqual(format_date(None, "N/A"), "N/A")

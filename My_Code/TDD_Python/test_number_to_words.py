import unittest
from number_to_words import number_to_words

class TestNums(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(number_to_words(0), "zero")

    def test_single_digits(self):
        self.assertEqual(number_to_words(1), "one")
        self.assertEqual(number_to_words(9), "nine")

    def test_teens(self):
        self.assertEqual(number_to_words(10), "ten")
        self.assertEqual(number_to_words(13), "thirteen")
        self.assertEqual(number_to_words(19), "nineteen")

    def test_tens(self):
        self.assertEqual(number_to_words(20), "twenty")
        self.assertEqual(number_to_words(45), "forty five")
        self.assertEqual(number_to_words(99), "ninety nine")

    def test_hundreds(self):
        self.assertEqual(number_to_words(100), "one hundred")
        self.assertEqual(number_to_words(342), "three hundred forty two")
        self.assertEqual(number_to_words(999), "nine hundred ninety nine")

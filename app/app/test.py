'''

sample test
'''

from django.test import SimpleTestCase

from . import calc


class CalcTests(SimpleTestCase):
    ''' Test addition '''
    def test_add_numbers(self):
        res = calc.add(3, 7)
        self.assertEqual(res, 10)

    def test_subtract_numbers(self):
        ''' Subtraction of numbers '''
        res = calc.subtract(8, 10)
        self.assertEqual(res, 2)

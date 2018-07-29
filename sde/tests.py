from django.test import TestCase


class TestUnitParsing(TestCase):
    def setUp(self):
        from .models import Unit
        self.nullunit = Unit(display_name=None)
        self.regular = Unit(display_name="ISK")
        self.enum = Unit(display_name="1=Male 2=Unisex 3=Female")


    def test_null_input(self):
        input = None
        self.assertEqual(self.nullunit.affix(input), None)
        self.assertEqual(self.regular.affix(input), None)
        self.assertEqual(self.enum.affix(input), None)


    def test_integer_input(self):
        input = 1
        self.assertEqual(self.nullunit.affix(input), "1")
        self.assertEqual(self.regular.affix(input), "1 ISK")
        self.assertEqual(self.enum.affix(input), "Male")
        self.assertEqual(self.enum.affix(4), "Invalid Enum: 4")
        

    def test_float_input(self):
        input = 4.5
        self.assertEqual(self.nullunit.affix(input), "4.5")
        self.assertEqual(self.regular.affix(input), "4.5 ISK")
        self.assertEqual(self.enum.affix(input), "Invalid Enum: 4.5")
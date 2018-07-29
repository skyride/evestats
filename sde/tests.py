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


    def test_special_types(self):
        from .models import Unit
        inverse_absolute = Unit(id=108)
        inverse_percent = Unit(id=109)
        inverse_modifier = Unit(id=111)

        self.assertEqual(inverse_absolute.affix(0.0), "100%")
        self.assertEqual(inverse_absolute.affix(0.2), "80%")
        self.assertEqual(inverse_absolute.affix(0.25), "75%")
        self.assertEqual(inverse_absolute.affix(0.5), "50%")
        self.assertEqual(inverse_absolute.affix(1.0), "0%")

        self.assertEqual(inverse_percent.affix(0.0), "-100%")
        self.assertEqual(inverse_percent.affix(0.2), "-80%")
        self.assertEqual(inverse_percent.affix(0.5), "-50%")
        self.assertEqual(inverse_percent.affix(1.0), "+0%")
        self.assertEqual(inverse_percent.affix(1.1), "+10%")
        self.assertEqual(inverse_percent.affix(1.25), "+25%")
        self.assertEqual(inverse_percent.affix(1.375), "+37.5%")
        self.assertEqual(inverse_percent.affix(2.0), "+100%")
        self.assertEqual(inverse_percent.affix(3.0), "+200%")

        self.assertEqual(inverse_modifier.affix(0.0), "100.0%")
        self.assertEqual(inverse_modifier.affix(0.1), "90.0%")
        self.assertEqual(inverse_modifier.affix(0.15), "85.0%")
        self.assertEqual(inverse_modifier.affix(0.2), "80.0%")
        self.assertEqual(inverse_modifier.affix(0.5), "50.0%")
        self.assertEqual(inverse_modifier.affix(0.125), "87.5%")
        self.assertEqual(inverse_modifier.affix(0.0), "100.0%")
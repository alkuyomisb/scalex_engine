import unittest
from scalex_toolkit import ScaleXToolkit


class TestGeneral(unittest.TestCase):
    stk = ScaleXToolkit()

    def test_clear_string(self):
        str1 = "  Incididunt \xa0elit /sint et \nexercitation mollit eu amet.    "
        str2 = "\xa0  Incididunt elit sint et\n exercitation /mollit eu amet.    \n"
        result = "Incididunt elit sint et exercitation mollit eu amet."

        self.assertEqual(self.stk.clear_string(str1), result)
        self.assertEqual(self.stk.clear_string(str2), result)

    def test_split_value_and_unit(self):
        self.assertEqual(self.stk.split_value_and_unit(
            "100 OMR"), {"value": "100", "unit": "OMR"})

        self.assertEqual(self.stk.split_value_and_unit(
            "100OMR"), {"value": "100", "unit": "OMR"})

        self.assertEqual(self.stk.split_value_and_unit(
            " 20  OMR "), {"value": "20", "unit": "OMR"})

        self.assertEqual(self.stk.split_value_and_unit(
            " OMR 300   "), {"value": "300", "unit": "OMR"})

        self.assertEqual(self.stk.split_value_and_unit(
            "150 MB"), {"value": "150", "unit": "MB"})

        self.assertEqual(self.stk.split_value_and_unit(
            " 3  GB "), {"value": "3", "unit": "GB"})

        self.assertEqual(self.stk.split_value_and_unit(
            " 600MB   "), {"value": "600", "unit": "MB"})


if __name__ == '__main__':
    unittest.main()

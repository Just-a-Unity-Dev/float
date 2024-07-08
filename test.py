import unittest
from classes.macro import do_macro


class MacroTests(unittest.TestCase):
    def test_macro_basic(self):
        result = do_macro("$0+3", ["1"])
        self.assertEqual(result.total, 4)

    def test_macro_rng(self):
        result = do_macro("$0+1", ["1d6"])
        self.assertGreaterEqual(result.total, 2)

    def test_macro_multiarg(self):
        result = do_macro("$0+$1+$2+$3+$4", ['1', '2', '3', '4', '5'])
        self.assertEqual(result.total, 15)
        result = do_macro("$0-$1+$2*$3/$4", ['1', '2', '3', '4', '5'])
        self.assertEqual(result.total, 1)

    def test_macro_double_rng(self):
        result = do_macro("$0+$1", ["1d6", "1d4"])
        self.assertGreaterEqual(result.total, 2)


if __name__ == '__main__':
    unittest.main()

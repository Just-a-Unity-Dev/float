import unittest
from classes.macro import do_macro


class MacroTests(unittest.TestCase):
    def test_macro_basic(self):
        result = do_macro("$0+3", ["1"])
        self.assertEqual(result.total, 4)


if __name__ == '__main__':
    unittest.main()

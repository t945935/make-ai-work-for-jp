import unittest
from app import make_label


class LabelTests(unittest.TestCase):
    def test_trim_name(self):
        self.assertEqual(make_label(" 林青 ", 2), "林青｜2 位")


if __name__ == "__main__":
    unittest.main()
import unittest
from fee import quote

class FeeTests(unittest.TestCase):
    def test_three_regular_tickets_receive_discount(self):
        self.assertEqual(quote("regular", 3), 810)

if __name__ == "__main__":
    unittest.main()

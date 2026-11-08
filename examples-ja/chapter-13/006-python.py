    def test_zero_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            quote("regular", 0)

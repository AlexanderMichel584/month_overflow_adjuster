import unittest
from datetime import date, datetime

from month_overflow_adjuster import add_months


class AddMonthsTest(unittest.TestCase):
    def test_jan_31_plus_one_month_clamps_to_february_end(self):
        self.assertEqual(add_months(date(2023, 1, 31), 1), date(2023, 2, 28))

    def test_leap_year_february_end(self):
        self.assertEqual(add_months(date(2024, 1, 31), 1), date(2024, 2, 29))

    def test_march_31_minus_one_month_clamps_to_february_end(self):
        self.assertEqual(add_months(date(2024, 3, 31), -1), date(2024, 2, 29))

    def test_day_preserved_when_target_month_is_long_enough(self):
        self.assertEqual(add_months(date(2023, 1, 15), 1), date(2023, 2, 15))

    def test_zero_months_is_identity(self):
        value = date(2023, 5, 31)
        self.assertEqual(add_months(value, 0), value)

    def test_year_boundary_forward(self):
        self.assertEqual(add_months(date(2023, 12, 15), 1), date(2024, 1, 15))

    def test_year_boundary_backward(self):
        self.assertEqual(add_months(date(2024, 1, 15), -1), date(2023, 12, 15))

    def test_large_forward_offset_clamps(self):
        # 2023-01-31 + 13 months lands on 2024-02-29.
        self.assertEqual(add_months(date(2023, 1, 31), 13), date(2024, 2, 29))

    def test_large_backward_offset_clamps(self):
        # 2024-03-31 - 13 months lands on 2023-02-28.
        self.assertEqual(add_months(date(2024, 3, 31), -13), date(2023, 2, 28))

    def test_datetime_preserves_time_components(self):
        value = datetime(2023, 1, 31, 23, 59, 59, 123456)
        self.assertEqual(
            add_months(value, 1),
            datetime(2023, 2, 28, 23, 59, 59, 123456),
        )

    def test_datetime_returns_datetime_type(self):
        result = add_months(datetime(2023, 1, 31, 12, 0), 1)
        self.assertIsInstance(result, datetime)

    def test_date_returns_date_type(self):
        result = add_months(date(2023, 1, 31), 1)
        self.assertIsInstance(result, date)
        self.assertNotIsInstance(result, datetime)

    def test_rejects_non_date(self):
        with self.assertRaises(TypeError):
            add_months("2023-01-31", 1)

    def test_rejects_non_int_months(self):
        with self.assertRaises(TypeError):
            add_months(date(2023, 1, 31), 1.0)

    def test_rejects_bool_months(self):
        with self.assertRaises(TypeError):
            add_months(date(2023, 1, 31), True)


if __name__ == "__main__":
    unittest.main()

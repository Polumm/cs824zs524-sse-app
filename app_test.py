import unittest
from app import process_query


class TestProcessQuery(unittest.TestCase):
    def test_name_query(self):
        self.assertEqual(process_query("What is your name?"), "cszs")

    def test_largest_number_query(self):
        self.assertEqual(
            process_query(
                "Which of the following numbers is the largest: 96, 77, 16?"
            ),
            "96",
        )
        self.assertEqual(
            process_query(
                "Which of the following numbers is the largest: 5, 27, 49?"
            ),
            "49",
        )

    def test_addition_query(self):
        self.assertEqual(process_query("What is 67 plus 26?"), "93")
        self.assertEqual(process_query("What is 2 plus 95?"), "97")

    def test_multiplication_query(self):
        self.assertEqual(process_query("What is 7 multiplied by 8?"), "56")
        self.assertEqual(process_query("What is 3 multiplied by 15?"), "45")

    def test_square_and_cube_query(self):
        self.assertEqual(
            process_query(
                "Which of the following numbers is both a square and a cube\
                : 4071, 4096, 1172, 64, 2500, 49, 2625?"
            ),
            "4096, 64",
        )


if __name__ == "__main__":
    unittest.main()

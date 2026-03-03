import unittest

from matrix_ops import (
    MatrixValidationError,
    add_matrices,
    multiply_matrices,
    subtract_matrices,
)


class MatrixOpsTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add_matrices([[1, 2], [3, 4]], [[4, 3], [2, 1]]), [[5, 5], [5, 5]])

    def test_subtraction(self):
        self.assertEqual(subtract_matrices([[5, 7]], [[2, 3]]), [[3, 4]])

    def test_multiplication(self):
        self.assertEqual(multiply_matrices([[1, 2, 3]], [[1], [2], [3]]), [[14]])

    def test_add_dimension_error(self):
        with self.assertRaises(MatrixValidationError):
            add_matrices([[1, 2]], [[1], [2]])

    def test_multiply_dimension_error(self):
        with self.assertRaises(MatrixValidationError):
            multiply_matrices([[1, 2]], [[1, 2]])


if __name__ == "__main__":
    unittest.main()

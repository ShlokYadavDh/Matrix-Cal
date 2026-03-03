"""Core matrix operations with mathematical rule validation."""

from __future__ import annotations

from typing import List

Matrix = List[List[float]]


class MatrixValidationError(ValueError):
    """Raised when a matrix is malformed or an operation is invalid."""



def validate_matrix(matrix: Matrix, name: str = "Matrix") -> None:
    if not matrix:
        raise MatrixValidationError(f"{name} must have at least one row.")

    if any(not row for row in matrix):
        raise MatrixValidationError(f"{name} must not contain empty rows.")

    row_length = len(matrix[0])
    if any(len(row) != row_length for row in matrix):
        raise MatrixValidationError(
            f"{name} is invalid: all rows must have the same number of columns."
        )



def shape(matrix: Matrix) -> tuple[int, int]:
    validate_matrix(matrix)
    return len(matrix), len(matrix[0])



def add_matrices(a: Matrix, b: Matrix) -> Matrix:
    validate_matrix(a, "Matrix A")
    validate_matrix(b, "Matrix B")

    if shape(a) != shape(b):
        raise MatrixValidationError(
            "Addition requires Matrix A and Matrix B to have the same dimensions."
        )

    return [[av + bv for av, bv in zip(ar, br)] for ar, br in zip(a, b)]



def subtract_matrices(a: Matrix, b: Matrix) -> Matrix:
    validate_matrix(a, "Matrix A")
    validate_matrix(b, "Matrix B")

    if shape(a) != shape(b):
        raise MatrixValidationError(
            "Subtraction requires Matrix A and Matrix B to have the same dimensions."
        )

    return [[av - bv for av, bv in zip(ar, br)] for ar, br in zip(a, b)]



def multiply_matrices(a: Matrix, b: Matrix) -> Matrix:
    validate_matrix(a, "Matrix A")
    validate_matrix(b, "Matrix B")

    a_rows, a_cols = shape(a)
    b_rows, b_cols = shape(b)

    if a_cols != b_rows:
        raise MatrixValidationError(
            "Multiplication requires columns in Matrix A to equal rows in Matrix B."
        )

    result: Matrix = [[0.0 for _ in range(b_cols)] for _ in range(a_rows)]
    for i in range(a_rows):
        for j in range(b_cols):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(a_cols))

    return result

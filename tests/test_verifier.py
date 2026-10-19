import pytest
from src.verifier import LinearAlgebraVerifier

def test_verify_determinant():
    # Матрица 3x3, det = -12
    matrix = [
        [2, 3, 1],
        [4, -1, 1],
        [5, 1, 1]
    ]
    assert LinearAlgebraVerifier.verify_determinant(matrix, -12) == True
    assert LinearAlgebraVerifier.verify_determinant(matrix, 10) == False

def test_verify_rank():
    matrix = [
        [1, 2, 3],
        [2, 4, 6],
        [1, 1, 1]
    ]
    assert LinearAlgebraVerifier.verify_rank(matrix, 2) == True
    assert LinearAlgebraVerifier.verify_rank(matrix, 3) == False

def test_verify_cramer():
    coeffs = [
        [2, 1],
        [1, -1]
    ]
    free = [5, 1]
    assert LinearAlgebraVerifier.verify_cramer(coeffs, free, [2.0, 1.0]) == True
    assert LinearAlgebraVerifier.verify_cramer(coeffs, free, [1.0, 1.0]) == False
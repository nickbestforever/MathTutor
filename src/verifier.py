import sympy as sp
from typing import Union, Dict, Any, List

class LinearAlgebraVerifier:
    """
    Mathematical answer verifier for linear algebra.
    Uses SymPy for precise symbolic computations.
    """

    @staticmethod
    def parse_matrix(data: Union[List[List[float]], str]) -> sp.Matrix:
        """Helper method to convert input data into a SymPy Matrix."""
        return sp.Matrix(data)

    @classmethod
    def verify_determinant(cls, user_matrix: List[List[float]], student_answer: float) -> bool:
        """1. Determinant calculation"""
        mat = cls.parse_matrix(user_matrix)
        correct_det = mat.det()
        return sp.simplify(correct_det - student_answer) == 0

    @classmethod
    def verify_matrix_multiplication(cls, matrix_a: List[List[float]], 
                                     matrix_b: List[List[float]], 
                                     student_answer: List[List[float]]) -> bool:
        """2. Matrix multiplication"""
        A = cls.parse_matrix(matrix_a)
        B = cls.parse_matrix(matrix_b)
        S = cls.parse_matrix(student_answer)
        correct_product = A * B
        return correct_product == S

    @classmethod
    def verify_inverse_matrix(cls, user_matrix: List[List[float]], 
                              student_answer: List[List[float]]) -> bool:
        """3. Inverse matrix"""
        A = cls.parse_matrix(user_matrix)
        S = cls.parse_matrix(student_answer)
        try:
            correct_inverse = A.inv()
            return correct_inverse == S
        except sp.NonInvertibleMatrixError:
            return False

    @classmethod
    def verify_matrix_equation(cls, data: Dict[str, Any], student_answer: List[List[float]]) -> bool:
        """
        4. Three types of matrix equations:
        Type 1: A * X = B  => X = A^(-1) * B
        Type 2: X * A = B  => X = B * A^(-1)
        Type 3: A * X * B = C => X = A^(-1) * C * B^(-1)
        """
        eq_type = data.get("equation_type")
        X = cls.parse_matrix(student_answer)
        
        try:
            if eq_type == "AX=B":
                A = cls.parse_matrix(data["matrix_a"])
                B = cls.parse_matrix(data["matrix_b"])
                correct_x = A.inv() * B
            elif eq_type == "XA=B":
                A = cls.parse_matrix(data["matrix_a"])
                B = cls.parse_matrix(data["matrix_b"])
                correct_x = B * A.inv()
            elif eq_type == "AXB=C":
                A = cls.parse_matrix(data["matrix_a"])
                B = cls.parse_matrix(data["matrix_b"])
                C = cls.parse_matrix(data["matrix_c"])
                correct_x = A.inv() * C * B.inv()
            else:
                return False
            return correct_x == X
        except Exception:
            return False

    @classmethod
    def verify_cramer(cls, coefficients: List[List[float]], 
                      free_terms: List[float], 
                      student_answer: List[float]) -> bool:
        """5. Cramer's rule for SLAE"""
        A = cls.parse_matrix(coefficients)
        B = cls.parse_matrix(free_terms)
        try:
            correct_sol = A.LUsolve(B) 
            student_sol = sp.Matrix(student_answer)
            if student_sol.cols == 1:
                student_sol = student_sol.T
            return correct_sol == student_sol.T or correct_sol == student_sol
        except Exception:
            return False

    @classmethod
    def verify_inverse_matrix_slae(cls, coefficients: List[List[float]], 
                                   free_terms: List[float], 
                                   student_answer: List[float]) -> bool:
        """6. SLAE via inverse matrix"""
        return cls.verify_cramer(coefficients, free_terms, student_answer)

    @classmethod
    def verify_rank(cls, user_matrix: List[List[float]], student_answer: int) -> bool:
        """7. Matrix rank calculation"""
        mat = cls.parse_matrix(user_matrix)
        correct_rank = mat.rank()
        return correct_rank == int(student_answer)

    @classmethod
    def verify_gauss_slae(cls, coefficients: List[List[float]], 
                          free_terms: List[float], 
                          student_answer: Any) -> bool:
        """8. Gaussian elimination for SLAE"""
        A = cls.parse_matrix(coefficients)
        B = cls.parse_matrix(free_terms)
        X = cls.parse_matrix(student_answer)
        try:
            return (A * X) == B
        except Exception:
            return False

    @classmethod
    def verify_homogeneous_slae(cls, coefficients: List[List[float]], 
                                student_basis: List[List[float]]) -> bool:
        """9. Fundamental Solution Set (FSS) for homogeneous SLAE"""
        A = cls.parse_matrix(coefficients)
        rows, cols = A.shape
        rank = A.rank()
        expected_nullity = cols - rank
        
        basis_vectors = [sp.Matrix(v) for v in student_basis]
        
        if len(basis_vectors) != expected_nullity:
            return False
            
        zero_vec = sp.zeros(rows, 1)
        for v in basis_vectors:
            if A * v != zero_vec:
                return False
                
        basis_matrix = sp.Matrix.hstack(*basis_vectors)
        if basis_matrix.rank() != expected_nullity:
            return False
            
        return True
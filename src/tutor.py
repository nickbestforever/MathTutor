import json
import os
from typing import Dict, Any, List, Optional
from src.verifier import LinearAlgebraVerifier

class TutorEngine:
    def __init__(self, task_bank_path: str = "task_bank.json"):
        self.tasks = self._load_tasks(task_bank_path)

    def _load_tasks(self, path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def evaluate_attempt(self, task: Dict[str, Any], student_input: Any) -> Dict[str, Any]:
        """
        Evaluates the student's answer using the verifier based on the task topic.
        Returns status, feedback message, and hint data.
        """
        topic = task["topic"]
        data = task["input_data"]
        is_correct = False

        try:
            # 1. Determinants
            if "Determinants" in topic:
                is_correct = LinearAlgebraVerifier.verify_determinant(
                    data["matrix"], float(student_input)
                )
            
            # 2. Matrix Multiplication
            elif "Matrix Multiplication" in topic:
                if isinstance(student_input, str):
                    rows = student_input.strip().split(";")
                    parsed_ans = [[float(val.strip()) for val in row.split(",")] for row in rows]
                else:
                    parsed_ans = student_input
                A = LinearAlgebraVerifier.parse_matrix(data["matrix_a"])
                B = LinearAlgebraVerifier.parse_matrix(data["matrix_b"])
                S = LinearAlgebraVerifier.parse_matrix(parsed_ans)
                is_correct = (A * B == S)

            # 3. Inverse Matrix
            elif "Inverse Matrix" in topic and "SLAE" not in topic:
                if isinstance(student_input, str):
                    rows = student_input.strip().split(";")
                    parsed_ans = [[float(val.strip()) for val in row.split(",")] for row in rows]
                else:
                    parsed_ans = student_input
                is_correct = LinearAlgebraVerifier.verify_inverse_matrix(data["matrix"], parsed_ans)

            # 4. Matrix Equations (AX=B, XA=B, AXB=C)
            elif "Matrix Equations" in topic:
                if isinstance(student_input, str):
                    rows = student_input.strip().split(";")
                    parsed_ans = [[float(val.strip()) for val in row.split(",")] for row in rows]
                else:
                    parsed_ans = student_input
                is_correct = LinearAlgebraVerifier.verify_matrix_equation(data, parsed_ans)

            # 5. Cramer's Rule
            elif "Cramer's Rule" in topic:
                if isinstance(student_input, str):
                    parsed_ans = [float(x.strip()) for x in student_input.split(",")]
                else:
                    parsed_ans = student_input
                is_correct = LinearAlgebraVerifier.verify_cramer(
                    data["coefficients"], data["free_terms"], parsed_ans
                )

            # 6. Inverse Matrix SLAE
            elif "Inverse Matrix SLAE" in topic:
                if isinstance(student_input, str):
                    parsed_ans = [float(x.strip()) for x in student_input.split(",")]
                else:
                    parsed_ans = student_input
                is_correct = LinearAlgebraVerifier.verify_inverse_matrix_slae(
                    data["coefficients"], data["free_terms"], parsed_ans
                )

            # 7. Matrix Rank
            elif "Matrix Rank" in topic:
                is_correct = LinearAlgebraVerifier.verify_rank(
                    data["matrix"], int(student_input)
                )

            # 8. Gaussian Elimination
            elif "Gaussian Elimination" in topic:
                if isinstance(student_input, str):
                    parsed_ans = [float(x.strip()) for x in student_input.split(",")]
                else:
                    parsed_ans = student_input
                is_correct = LinearAlgebraVerifier.verify_gauss_slae(
                    data["coefficients"], data["free_terms"], parsed_ans
                )

            # 9. Fundamental Solution Set (FSS)
            elif "Fundamental Solution Set" in topic:
                if isinstance(student_input, str):
                    vectors = student_input.strip().split(";")
                    parsed_ans = [[float(val.strip()) for val in v.split(",")] for v in vectors]
                else:
                    parsed_ans = student_input
                is_correct = LinearAlgebraVerifier.verify_homogeneous_slae(
                    data["matrix"], parsed_ans
                )
            else:
                return {"error": f"Unknown topic: {topic}"}
                
        except Exception as e:
            return {
                "is_correct": False,
                "message": f"Parsing error ({e}). Check the input format (e.g., matrices separated by ';', vectors by commas)."
            }

        return {
            "is_correct": is_correct,
            "message": "Correct! Great job." if is_correct else "Incorrect. Please check your calculations."
        }
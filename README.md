# MathTutor: A Verification-Guided Practice System for Linear Algebra

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-url.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MathTutor** is an open-source, verification-guided interactive practice environment tailored for linear algebra education. Built to prevent LLM hallucinations and calculation errors, MathTutor relies on an independent symbolic execution core powered by Python's `SymPy` library to ensure deterministic mathematical correctness.

## 📁 Repository Structure
- `src/` — Core mathematical verification engine (`verifier.py`) and tutoring session controller (`tutor.py`).
- `assets/images/` — Structured visual task conditions sorted by topics (`01/` to `09/`).
- `tests/` — Automated test suites (`pytest`) for validation.
- `task\_bank.json` — Comprehensive benchmark dataset of linear algebra problems with symbolic solutions.
- `app.py` — Streamlit-based web user interface.

## 🚀 Local Installation & Reproduction

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nickbestforever/MathTutor.git
   cd MathTutor

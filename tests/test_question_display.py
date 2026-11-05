"""Regression coverage for typography boundaries and program-content safety."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from question_display import display_issues, display_text, numeric_ascii, presentation_content


def example(code, language="cpp"):
    return {
        "id": "1.4.3-001", "module": "Module 1: Core Computer Science Fundamentals",
        "question": "Python 3. What is printed?" if language == "python" else
                    "Bash with GNU utilities. What is printed?" if language == "bash" else "What is printed?",
        "difficulty": "Easy", "correct_answer": "A", "explanation": "An example.",
        "options": {"A": "1", "B": "2", "C": "3", "D": "4"}, "code_snippet": code,
    }


class DisplayTests(unittest.TestCase):
    def test_bound_symbols(self):
        self.assertEqual(display_text("Theta(n^2) and Omega(n)"), "Θ(n²) and Ω(n)")

    def test_parameter_names_are_not_arbitrary_word_replacements(self):
        self.assertEqual(display_text("Pi holds Ri; the alphabet is unchanged."),
                         "Pi holds Ri; the alphabet is unchanged.")
        self.assertEqual(display_text("alpha=0.25; H0: mu!=mu0"), "α=0.25; H₀: μ≠μ₀")

    def test_inline_code_and_literals_remain_literal(self):
        value = 'Use `x >= 1` and the literal "Theta".'
        self.assertEqual(display_text(value), value)

    def test_fractional_powers_are_not_partly_rewritten(self):
        self.assertEqual(display_text("n^0.5 and n^12."), "n^0.5 and n¹².")
        self.assertEqual(numeric_ascii("2³ + √(4)"), "2**3 + sqrt(4)")

    def test_normalization_is_idempotent(self):
        value = "Theta(sqrt(n)); beta_hat^2; lambda>=0; Phi(1.96)"
        once = display_text(value)
        self.assertEqual(display_text(once), once)

    def test_cpp_indentation_is_safe_but_literal_changes_are_not(self):
        before = example('#include <iostream>\nint main(){std::cout<<"a b";}')
        after = deepcopy(before)
        after["code_snippet"] = '#include <iostream>\nint main() {\n    std::cout << "a b";\n}'
        self.assertEqual(presentation_content(before), presentation_content(after))
        after["code_snippet"] = after["code_snippet"].replace('"a b"', '"ab"')
        self.assertNotEqual(presentation_content(before), presentation_content(after))

    def test_python_uses_ast_equivalence(self):
        before = example("def f(x): return x + 1\nprint(f(2))", "python")
        after = deepcopy(before)
        after["code_snippet"] = "def f(x):\n    return x + 1\n\nprint(f(2))"
        self.assertEqual(presentation_content(before), presentation_content(after))
        after["code_snippet"] = after["code_snippet"].replace("x + 1", "x - 1")
        self.assertNotEqual(presentation_content(before), presentation_content(after))

    def test_shell_awk_formatting_preserves_printf_literals(self):
        before = example("printf 'a b\\n' | awk '{print $1}'", "bash")
        after = deepcopy(before)
        after["code_snippet"] = "printf 'a b\\n' |\n    awk '{\n        print $1\n    }'"
        self.assertEqual(presentation_content(before), presentation_content(after))
        after["code_snippet"] = after["code_snippet"].replace("a b", "ab")
        self.assertNotEqual(presentation_content(before), presentation_content(after))

    def test_sql_formatting_cannot_change_values(self):
        before = example("WITH T(x) AS (VALUES (1)) SELECT x FROM T;")
        after = deepcopy(before)
        after["code_snippet"] = "WITH\n    T(x) AS (\n        VALUES (1)\n    )\nSELECT x\nFROM T;"
        self.assertEqual(presentation_content(before), presentation_content(after))
        after["code_snippet"] = after["code_snippet"].replace("VALUES (1)", "VALUES (2)")
        self.assertNotEqual(presentation_content(before), presentation_content(after))

    def test_display_guard_handles_invalid_schema_and_invisible_characters(self):
        self.assertEqual(display_issues({}), [])
        q = example("int main() {}")
        q["question"] = "Theta(n)\u200b"
        self.assertGreaterEqual(len(display_issues(q)), 2)


if __name__ == "__main__":
    unittest.main()

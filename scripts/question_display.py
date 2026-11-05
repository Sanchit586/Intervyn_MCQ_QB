"""Renderer-independent mathematical typography and display-content signatures."""

import ast
import re
import shlex
import unicodedata

GREEK = {
    "Theta": "Θ", "theta": "θ", "Omega": "Ω", "omega": "ω",
    "alpha": "α", "Alpha": "α", "beta": "β", "gamma": "γ",
    "epsilon": "ε", "lambda": "λ", "sigma": "σ", "mu": "μ",
    "eta": "η", "Phi": "Φ",
}
GREEK_WORD = re.compile(r"\b(" + "|".join(GREEK) + r")(?=\b|_|[0-9])")
SUPERSCRIPT = str.maketrans("0123456789-+()nktT", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿᵏᵗᵀ")
SUBSCRIPT = str.maketrans("0123456789ijkn", "₀₁₂₃₄₅₆₇₈₉ᵢⱼₖₙ")
SUPERSCRIPT_REVERSE = {chr(value): chr(key) for key, value in SUPERSCRIPT.items()}
TOKEN = re.compile(
    r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|'
    r"'(?:\\.|''|[^'\\])*'|[\w]+|>>=|<<=|->|::|\+\+|--|"
    r"<=|>=|==|!=|&&|\|\||<<|>>|[^\s]"
)


def display_text(text):
    """Normalize math prose, preserving explicit inline code and quoted literals.

    Executable snippets must never be passed through this function. Pi is not
    a replacement: it denotes an indexed process in the deadlock questions.
    """
    def convert(value):
        value = GREEK_WORD.sub(lambda match: GREEK[match[0]], value)
        value = value.replace("β_hat", "β̂")
        value = re.sub(r"([αβγελσμθη])_([ijkn])\b", lambda m: m[1]+m[2].translate(SUBSCRIPT), value)
        value = re.sub(r"([αβγελσμθη])([0-9]+)\b", lambda m: m[1]+m[2].translate(SUBSCRIPT), value)
        value = re.sub(r"\bH([01])\b", lambda m: "H"+m[1].translate(SUBSCRIPT), value)
        value = re.sub(r"\bsqrt\s*(?=\()", "√", value)
        value = re.sub(r"\blog_?2\b", "log₂", value)
        value = re.sub(r"\bsum_([ij])\b", lambda m: "Σ"+m[1].translate(SUBSCRIPT), value)
        value = re.sub(r"(?<=[\w)])\^\((-?\d+)\)", lambda m: m[1].translate(SUPERSCRIPT), value)
        value = re.sub(r"(?<=[\w)\u0302])\^(-?\d+)(?!\w|\.\d)", lambda m: m[1].translate(SUPERSCRIPT), value)
        value = re.sub(r"(?<=[\w)])\^([nktT])\b", lambda m: m[1].translate(SUPERSCRIPT), value)
        value = value.replace("<->", "↔").replace("+/-", "±")
        value = value.replace("<=", "≤").replace(">=", "≥").replace("!=", "≠")
        value = re.sub(r"(?<=[A-Z0-9)])\s*->\s*(?=[A-Z0-9(])", " → ", value)
        return value

    # Explicit code spans and quoted strings are syntax/literal examples.
    pieces = re.split(r'(`[^`\n]*`|"[^"\n]*")', text)
    result = "".join(piece if i%2 else convert(piece) for i, piece in enumerate(pieces))
    return unicodedata.normalize("NFC", result).strip()


def numeric_ascii(text):
    """Convert displayed roots/powers back to parser syntax for numeric checks."""
    text = text.replace("√", "sqrt")
    return re.sub(
        r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿᵏᵗᵀ]+",
        lambda m: "**" + "".join(SUPERSCRIPT_REVERSE[c] for c in m[0]), text,
    )


def snippet_language(question):
    code = question.get("code_snippet") or ""
    if code.lstrip().startswith("#include"):
        return "cpp"
    if code.lstrip().startswith("public class Main"):
        return "java"
    if question["question"].startswith("Python 3"):
        return "python"
    if question["module"].startswith("Module 3:"):
        return "pseudocode"
    if re.match(r"^(WITH|SELECT)\b", code.lstrip()):
        return "sql"
    if question["question"].startswith("Bash with GNU utilities"):
        return "bash"
    return "reference"


def reference_text(code):
    # Give the confusion matrix an explicit row-label column. This also makes
    # the original table and its corrected display comparable in the audit.
    if ("Predicted negative" in code and "Actual negative: 90" in code
            and "Actual positive: 20" in code):
        return ("Actual class | Predicted negative | Predicted positive\n"
                "Negative | 90 | 10\nPositive | 20 | 30")
    return code


def tokens(code):
    return tuple(TOKEN.findall(code))


def display_issues(question):
    """Lightweight display checks, without formatter dependencies."""
    issues = []
    values = [(key, question.get(key)) for key in ("question", "explanation")]
    options = question.get("options")
    if isinstance(options, dict):
        values.extend((f"option {key}", value) for key, value in options.items())
    for name, value in values:
        if not isinstance(value, str):
            continue
        if display_text(value) != value:
            issues.append(f"{name}: mathematical text/whitespace needs display normalization")
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ufffd\ufeff\u200b\u00ad]", value):
            issues.append(f"{name}: contains an invalid/invisible display character")
        if any(line.rstrip() != line for line in value.splitlines()):
            issues.append(f"{name}: trailing whitespace")
    code = question.get("code_snippet")
    if isinstance(code, str):
        if "\t" in code or "\r" in code:
            issues.append("code_snippet: use spaces and LF line endings")
        if any(line.rstrip() != line for line in code.splitlines()):
            issues.append("code_snippet: trailing whitespace")
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ufffd\ufeff\u200b\u00ad]", code):
            issues.append("code_snippet: contains an invalid/invisible display character")
    return issues


def presentation_content(question):
    """Assess content equality while allowing documented display-only changes."""
    result = {key: question[key] for key in ("difficulty", "correct_answer")}
    for key in ("question", "explanation"):
        result[key] = " ".join(display_text(question[key]).split())
    result["options"] = {key: display_text(value) for key, value in question["options"].items()}
    code = question["code_snippet"]
    if code is None:
        result["code_snippet"] = None
        return result
    language = snippet_language(question)
    if language == "python":
        signature = ast.dump(ast.parse(code), include_attributes=False)
    elif language == "bash":
        # Only AWK program arguments may gain internal whitespace. printf
        # format strings and all other shell arguments must remain identical.
        signature = tuple(tokens(arg) if "{" in arg and "}" in arg else arg
                          for arg in shlex.split(code, comments=False))
    elif language in ("cpp", "java", "pseudocode", "sql"):
        signature = tokens(code)
    else:
        signature = tokens(display_text(reference_text(code)))
    result["code_snippet"] = signature
    return result

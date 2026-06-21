# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code to find all logical errors in `app.py`, then refactor the game logic functions from `app.py` into `logic_utils.py`, fix the scoring bug, generate edge-case tests, add professional docstrings, and enhance the game UI with Hot/Cold proximity feedback and a guess history table.

**What did the agent do?**

1. Read `app.py` and identified 6 logical bugs (scoring inconsistency, string conversion on even attempts, invalid guesses counting as attempts, history not clearing on new game, Hard mode attempt limit, hint suppression).
2. Copied the four game logic functions (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) from `app.py` into `logic_utils.py`, replacing the `NotImplementedError` stubs.
3. Fixed the `update_score` scoring bug in both `logic_utils.py` and `app.py` by removing the attempt-parity branch that rewarded +5 on even "Too High" attempts.
4. Generated 11 edge-case pytest tests in `tests/test_game_logic.py` targeting negative numbers, large values, whitespace, special characters, boundary values, and unknown difficulty.
5. Added Google-style docstrings and return type annotations to all functions in `logic_utils.py`, replaced bare `except Exception` with specific types, and fixed Python 3.9 type hint compatibility.
6. Added Hot/Cold proximity indicators and a guess history summary table to `app.py`.
7. Ran `pytest` after each change to verify all 33 tests passed.

**What did you have to verify or fix manually?**

- The agent initially used Python 3.10+ type hint syntax (`int | None`) which caused an import error on Python 3.9. It caught this from the pytest failure output and fixed it by adding `from __future__ import annotations` and using `Optional`/`Tuple` from `typing`.
- I had to review the existing test `test_too_high_on_even_attempt_increases_score` which asserted the old buggy behavior (score of 55). The agent updated it to assert the correct behavior (score of 45) and renamed it to `test_too_high_on_even_attempt_decreases_score`.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Negative numbers | "Identify three potential edge case inputs that might break the game" | `test_parse_guess_negative_number` — parses "-5" and checks it returns (-5) | Yes | Negative numbers parse as valid ints but are always outside the 1-based game range, so the game should handle them gracefully rather than crash. |
| Extremely large values | Same prompt | `test_parse_guess_extremely_large_number` — parses "999999999999" | Yes | Users could paste huge numbers; this verifies `int()` doesn't overflow or throw an unexpected error. |
| Whitespace-only input | Same prompt | `test_parse_guess_whitespace` — parses "   " and expects rejection | Yes | Whitespace looks empty but isn't caught by the `== ""` check, so `int()` must reject it. |
| Special characters | "Generate pytest cases that verify your game handles these inputs gracefully" | `test_parse_guess_special_characters` — parses "!@#$" | Yes | Non-numeric symbols should be caught by the except block, not crash the parser. |
| Zero | Same prompt | `test_parse_guess_zero` — parses "0" as valid int 0 | Yes | Zero is a valid integer but below the game's minimum range of 1; ensures it parses without error. |
| Negative decimal | Same prompt | `test_parse_guess_negative_decimal` — parses "-3.7" as -3 | Yes | Combines two edge cases (negative + decimal); truncation toward zero should work for negative floats. |
| Boundary low (1) | Same prompt | `test_check_guess_boundary_low` — checks guess=1, secret=1 is a Win | Yes | Lower boundary of every difficulty range; confirms exact match at the edge. |
| Boundary high (100) | Same prompt | `test_check_guess_boundary_high` — checks guess=100, secret=100 is a Win | Yes | Upper boundary of Hard mode; confirms exact match at the edge. |
| Negative guess comparison | Same prompt | `test_check_guess_negative_guess` — checks guess=-10 vs secret=50 | Yes | Ensures `check_guess` handles negative integers in comparisons without error. |
| Score going negative | Same prompt | `test_update_score_does_not_go_negative` — score 0 with "Too Low" gives -5 | Yes | Verifies the scoring function doesn't clamp at zero — negative scores are valid. |
| Unknown difficulty | Same prompt | `test_get_range_for_unknown_difficulty` — "Impossible" falls back to (1,100) | Yes | Confirms the default fallback works for unexpected difficulty strings. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Add professional-grade docstrings to every function in logic_utils.py. Then review the code for PEP 8 style compliance and apply suggestions.
```

**Linting output before:**

```
- No module docstring
- Functions had minimal one-line docstrings with no Args/Returns sections
- parse_guess used bare `except Exception` instead of specific exception types
- Type hints used Python 3.10+ syntax (int | None) incompatible with Python 3.9
- No return type annotations on any function
```

**Changes applied:**

- Added a module-level docstring to `logic_utils.py`
- Added Google-style docstrings with Args and Returns sections to all four functions
- Added return type annotations: `Tuple[int, int]`, `Tuple[bool, Optional[int], Optional[str]]`, `Tuple[str, str]`, `int`
- Replaced bare `except Exception` with `except (ValueError, OverflowError)` for specificity
- Added `from __future__ import annotations` and imported `Optional`, `Tuple` from `typing` for Python 3.9 compatibility

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

I asked both models to find and fix the scoring bug in `update_score` where "Too High" guesses on even-numbered attempts rewarded +5 points instead of penalizing.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude Code (Sonnet) | ChatGPT (GPT-4o) |
| **Response summary** | Identified the `attempt_number % 2 == 0` branch as the root cause and removed the parity check entirely so "Too High" always returns `current_score - 5`, matching "Too Low". | Suggested replacing the `+5` with `-5` inside the existing `if/else` structure, keeping the parity check but making both branches deduct points. |
| **More Pythonic?** | Yes — removed unnecessary branching, resulting in cleaner and simpler code. | No — kept the dead `if/else` branch even though both paths now do the same thing. |
| **Clearer explanation?** | Explained *why* the parity check was wrong (wrong guesses should never reward points) and showed the fix would make scoring symmetric with "Too Low". | Explained *what* to change (swap +5 to -5) but didn't address why the parity branch should be removed entirely. |

**Which did you prefer and why?**

I preferred Claude Code's approach because it simplified the code by removing the unnecessary `if attempt_number % 2 == 0` branch entirely rather than just patching the value inside it. This makes the intent clearer — all wrong guesses should penalize equally — and avoids leaving dead logic that could confuse future readers.

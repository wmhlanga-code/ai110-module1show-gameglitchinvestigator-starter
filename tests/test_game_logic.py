from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# --- check_guess tests ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_with_string_secret():
    # secret passed as string (happens on even attempts in the app)
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"


# --- parse_guess tests ---

def test_parse_guess_valid_number():
    ok, value, err = parse_guess("42")
    assert ok == True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok == False
    assert value is None

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok == False

def test_parse_guess_not_a_number():
    ok, value, err = parse_guess("hello")
    assert ok == False
    assert err == "That is not a number."

def test_parse_guess_decimal():
    ok, value, err = parse_guess("7.9")
    assert ok == True
    assert value == 7


# --- get_range_for_difficulty tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 100


# --- update_score tests ---

def test_win_on_first_attempt():
    new_score = update_score(0, "Win", 1)
    assert new_score == 90  # 100 - 10*1 = 90

def test_win_score_minimum_is_10():
    new_score = update_score(0, "Win", 20)
    assert new_score == 10  # minimum 10 points

def test_too_low_decreases_score():
    new_score = update_score(50, "Too Low", 1)
    assert new_score == 45

def test_too_high_on_odd_attempt_decreases_score():
    new_score = update_score(50, "Too High", 1)
    assert new_score == 45

def test_too_high_on_even_attempt_decreases_score():
    new_score = update_score(50, "Too High", 2)
    assert new_score == 45


# --- Bug-targeting tests ---

def test_too_high_should_always_penalize():
    """Too High should subtract points regardless of attempt parity."""
    score_odd = update_score(50, "Too High", 1)
    score_even = update_score(50, "Too High", 2)
    assert score_odd < 50, "Too High on odd attempt should decrease score"
    assert score_even < 50, "Too High on even attempt should decrease score, not reward +5"


def test_too_high_and_too_low_penalize_equally():
    """Both wrong-direction outcomes should apply the same penalty."""
    score_high = update_score(50, "Too High", 1)
    score_low = update_score(50, "Too Low", 1)
    assert score_high == score_low, "Too High and Too Low should have the same penalty"


def test_check_guess_string_secret_equality():
    """guess == secret should work even when secret is a string (even-attempt bug)."""
    outcome, _ = check_guess(42, "42")
    assert outcome == "Win", "Integer guess should match string secret of same value"


def test_check_guess_string_secret_too_high():
    """Directional hint should be correct when secret is passed as a string."""
    outcome, _ = check_guess(60, "50")
    assert outcome == "Too High"


def test_check_guess_string_secret_too_low():
    """Directional hint should be correct when secret is passed as a string."""
    outcome, _ = check_guess(40, "50")
    assert outcome == "Too Low"

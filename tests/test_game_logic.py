from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"


def test_hint_message_for_too_high_is_lower():
    # Regression: hint text was previously reversed
    result = check_guess(60, 50)
    assert result[1] == "📈 Go LOWER!"


def test_hint_message_for_too_low_is_higher():
    # Regression: hint text was previously reversed
    result = check_guess(40, 50)
    assert result[1] == "📉 Go HIGHER!"


def test_parse_guess_rejects_decimal_input():
    # Regression: decimal input was previously truncated to int
    ok, guess, err = parse_guess("12.2")
    assert ok is False
    assert guess is None
    assert err == "Enter a whole number."


def test_parse_guess_accepts_spaced_integer():
    # Regression: whitespace around valid numbers should be tolerated
    ok, guess, err = parse_guess("  42  ")
    assert ok is True
    assert guess == 42
    assert err is None


def test_parse_guess_rejects_blank_input():
    ok, guess, err = parse_guess("   ")
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_score_first_try_win_gets_100_points():
    # Regression: first attempt used to award 90 due to off-by-one
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 100


def test_score_second_try_win_gets_90_points():
    assert update_score(current_score=0, outcome="Win", attempt_number=2) == 90


def test_score_too_high_is_consistent_penalty():
    # Regression: too-high guesses used to sometimes add points
    assert update_score(current_score=20, outcome="Too High", attempt_number=2) == 15


def test_score_too_low_is_penalty():
    assert update_score(current_score=20, outcome="Too Low", attempt_number=3) == 15


def test_difficulty_ranges_are_correct():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_unknown_difficulty_defaults_to_hard_range():
    assert get_range_for_difficulty("Impossible") == (1, 100)



# /Users/pbajracharya1/Projects/Codepath_AI/ai110-module1show-gameglitchinvestigator-starter/.venv/bin/python -m pytest -q

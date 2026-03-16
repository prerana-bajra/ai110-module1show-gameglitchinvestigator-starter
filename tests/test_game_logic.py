from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    load_high_score,
    parse_guess,
    save_high_score,
    update_high_score,
    update_score,
)

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


def test_parse_guess_rejects_none_input():
    ok, guess, err = parse_guess(None)
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_parse_guess_rejects_text_input():
    ok, guess, err = parse_guess("hello")
    assert ok is False
    assert guess is None
    assert err == "Enter a whole number."


def test_score_first_try_win_gets_100_points():
    # Regression: first attempt used to award 90 due to off-by-one
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 100


def test_score_second_try_win_gets_90_points():
    assert update_score(current_score=0, outcome="Win", attempt_number=2) == 90


def test_score_late_win_uses_minimum_bonus():
    assert update_score(current_score=5, outcome="Win", attempt_number=20) == 15


def test_score_win_adds_to_existing_total():
    assert update_score(current_score=30, outcome="Win", attempt_number=3) == 110


def test_score_too_high_is_consistent_penalty():
    # Regression: too-high guesses used to sometimes add points
    assert update_score(current_score=20, outcome="Too High", attempt_number=2) == 15


def test_score_too_low_is_penalty():
    assert update_score(current_score=20, outcome="Too Low", attempt_number=3) == 15


def test_score_unknown_outcome_keeps_score_unchanged():
    assert update_score(current_score=20, outcome="Invalid", attempt_number=3) == 20


def test_difficulty_ranges_are_correct():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_unknown_difficulty_defaults_to_hard_range():
    assert get_range_for_difficulty("Impossible") == (1, 100)


def test_check_guess_string_inputs_can_still_win():
    result = check_guess("50", "50")
    assert result == ("Win", "🎉 Correct!")


def test_load_high_score_defaults_to_zero_for_missing_file(tmp_path):
    score_file = tmp_path / "high_score.json"
    assert load_high_score(score_file) == 0


def test_save_high_score_persists_value(tmp_path):
    score_file = tmp_path / "high_score.json"
    save_high_score(score_file, 85)
    assert load_high_score(score_file) == 85


def test_load_high_score_defaults_to_zero_for_invalid_json(tmp_path):
    score_file = tmp_path / "high_score.json"
    score_file.write_text("not valid json")
    assert load_high_score(score_file) == 0


def test_update_high_score_saves_new_best_score(tmp_path):
    score_file = tmp_path / "high_score.json"
    high_score, is_new = update_high_score(score_file, 90)
    assert high_score == 90
    assert is_new is True
    assert load_high_score(score_file) == 90


def test_update_high_score_keeps_existing_best_score(tmp_path):
    score_file = tmp_path / "high_score.json"
    save_high_score(score_file, 90)
    high_score, is_new = update_high_score(score_file, 75)
    assert high_score == 90
    assert is_new is False
    assert load_high_score(score_file) == 90



# /Users/pbajracharya1/Projects/Codepath_AI/ai110-module1show-gameglitchinvestigator-starter/.venv/bin/python -m pytest -q

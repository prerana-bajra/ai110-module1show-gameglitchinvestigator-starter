import json
from pathlib import Path
from typing import Optional, Tuple, Union


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """Return the inclusive number range for the selected difficulty.

    Args:
        difficulty: Difficulty label selected in the UI.

    Returns:
        A tuple ``(low, high)`` that defines the valid guess range.
    """
    # FIX: Reordered difficulty ranges with Copilot so Hard has the widest range.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: Optional[str]) -> Tuple[bool, Optional[int], Optional[str]]:
    """Validate and parse a raw text guess into an integer.

    Args:
        raw: Raw user input from the text field.

    Returns:
        A tuple ``(ok, guess_int, error_message)`` where:
        - ``ok`` is ``True`` when parsing succeeds.
        - ``guess_int`` is the parsed integer guess when valid, otherwise ``None``.
        - ``error_message`` contains a user-facing validation message when invalid.
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()

    if raw == "":
        return False, None, "Enter a guess."

    # FIX: Kept strict integer parsing after AI review to reject decimal guesses cleanly.
    try:
        value = int(raw)
    except ValueError:
        return False, None, "Enter a whole number."

    return True, value, None


def check_guess(
    guess: Union[int, str],
    secret: Union[int, str],
) -> Tuple[str, str]:
    """Compare a guess to the secret number and produce outcome feedback.

    Args:
        guess: Player guess, normally an integer but also supports string fallback.
        secret: Secret value for the current round.

    Returns:
        A tuple ``(outcome, message)`` where ``outcome`` is one of
        ``"Win"``, ``"Too High"``, or ``"Too Low"``, and ``message`` is a
        player-facing hint string.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Flipped hint directions with Copilot after reproducing the reversed-hint bug.
    try:
        if guess > secret:
            return "Too High", "📈 Go LOWER!"
        else:
            return "Too Low", "📉 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go LOWER!"
        return "Too Low", "📉 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Return the updated score after applying one guess outcome.

    Args:
        current_score: Score before applying the current guess result.
        outcome: Guess result label returned by ``check_guess``.
        attempt_number: 1-based index of the current attempt.

    Returns:
        The new score after applying win bonus or incorrect-guess penalty.
    """
    # FIX: Award more points for earlier wins, with a 10-point minimum bonus.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points
    # FIX: Consistent update in score regardless of the attempt number
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def load_high_score(file_path: Union[str, Path]) -> int:
    """Load the best score from JSON storage.

    Args:
        file_path: Path to the high score JSON file.

    Returns:
        Stored high score as an integer, or ``0`` when the file is missing,
        unreadable, malformed, or does not contain a valid integer score.
    """
    path = Path(file_path)

    if not path.exists():
        return 0

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0

    high_score = data.get("high_score", 0)
    if isinstance(high_score, int) and not isinstance(high_score, bool):
        return high_score
    return 0


def save_high_score(file_path: Union[str, Path], score: int) -> None:
    """Persist a high score value to JSON storage.

    Args:
        file_path: Destination JSON file path.
        score: Score value to persist.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"high_score": score}, indent=2), encoding="utf-8")


def update_high_score(file_path: Union[str, Path], score: int) -> Tuple[int, bool]:
    """Update persistent high score when a new score exceeds the previous best.

    Args:
        file_path: Path to the high score JSON file.
        score: Latest completed game score.

    Returns:
        A tuple ``(high_score, is_new_high_score)`` where ``high_score`` is the
        resulting stored best score and ``is_new_high_score`` indicates whether
        the provided score replaced the previous best.
    """
    current_high_score = load_high_score(file_path)

    if score > current_high_score:
        save_high_score(file_path, score)
        return score, True

    return current_high_score, False

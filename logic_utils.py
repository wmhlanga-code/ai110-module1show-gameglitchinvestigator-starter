"""Core game logic for the Glitchy Guesser number guessing game."""

from __future__ import annotations

from typing import Optional, Tuple


def get_range_for_difficulty(difficulty: str) -> Tuple[int, int]:
    """Return the (low, high) inclusive guess range for a given difficulty.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple of (low, high) integers defining the valid guess range.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """Parse raw user input into a validated integer guess.

    Args:
        raw: The raw string from the text input field.

    Returns:
        A tuple of (ok, guess_int, error_message) where ok is True
        if parsing succeeded, guess_int is the parsed value or None,
        and error_message describes the failure or is None on success.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, OverflowError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret) -> Tuple[str, str]:
    """Compare the player's guess to the secret number.

    Args:
        guess: The player's parsed integer guess.
        secret: The secret number (may be int or str due to app quirks).

    Returns:
        A tuple of (outcome, message) where outcome is one of
        "Win", "Too High", or "Too Low".
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📈 Go LOWER!"
        else:
            return "Too Low", "📉 Go HIGHER!"
    except TypeError:
        s = int(secret)
        if guess == s:
            return "Win", "🎉 Correct!"
        if guess > s:
            return "Too High", "📈 Go LOWER!"
        return "Too Low", "📉 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate the new score based on the guess outcome.

    Args:
        current_score: The player's score before this guess.
        outcome: The result from check_guess ("Win", "Too High", "Too Low").
        attempt_number: Which attempt this is (1-based).

    Returns:
        The updated score. Wins earn 100 - 10 * attempt (min 10).
        Wrong guesses deduct 5 points.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

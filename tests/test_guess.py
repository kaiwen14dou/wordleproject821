"""Testing guess function from wordle."""

import pytest

from wordle import Feedback, Wordle


def test_correct_guess_wins() -> None:
    """Return all GREEN feedback and sets game as won when guess is correct."""
    game = Wordle(secret_word="apple")
    feedback = game.guess("apple")
    assert feedback == [Feedback.GREEN] * 5
    assert game.is_won
    assert game.is_over


def test_max_attempts_loses() -> None:
    """Test 2 wrong attempts."""
    game = Wordle(secret_word="apple", max_attempts=2)
    game.guess("zebra")
    game.guess("crane")
    assert not game.is_won
    assert game.is_over


def test_invalid_guess_raises() -> None:
    """Test for invalid guess."""
    game = Wordle(secret_word="apple")
    with pytest.raises(ValueError):
        game.guess("a2c")

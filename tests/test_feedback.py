"""Testing feedbacks in letters."""

from wordle import Wordle


def test_partial_feedback_internal() -> None:
    """Testing feedbacks."""
    game = Wordle(secret_word="plant")
    result = game._generate_feedback("plate")
    assert result == "GGGY_"


def test_allcorrect() -> None:
    """Testing feedback when it is all correct."""
    game = Wordle(secret_word="plant")
    result = game._generate_feedback("plant")
    assert result == "GGGGG"

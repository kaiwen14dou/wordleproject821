"""Testing feedbacks in letters."""

from wordle import Feedback, Wordle


def test_partial_feedback_internal() -> None:
    """Test feedback when some letters are correct and others are not."""
    game = Wordle(secret_word="plant")
    result = game._generate_feedback("plate")
    expected = [
        Feedback.GREEN,  # p
        Feedback.GREEN,  # l
        Feedback.GREEN,  # a
        Feedback.YELLOW,  # t is in plant, but wrong position
        Feedback.GRAY,  # e not in plant
    ]
    assert result == expected


def test_allcorrect() -> None:
    """Test feedback when the guess is entirely correct."""
    game = Wordle(secret_word="plant")
    result = game._generate_feedback("plant")
    assert result == [Feedback.GREEN] * 5


def test_feedback_repeated_letters() -> None:
    """Feedback with repeated letters in guess ('sassy' vs 'spasm')."""
    game = Wordle(secret_word="spasm")
    result = game._generate_feedback("sassy")
    expected = [
        Feedback.GREEN,  # s (correct spot)
        Feedback.YELLOW,  # a (wrong spot)
        Feedback.GRAY,  # s (already matched once)
        Feedback.GREEN,  # s (correct spot)
        Feedback.GRAY,  # y (not in word)
    ]
    assert result == expected

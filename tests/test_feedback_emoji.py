"""Testing feedback converting to emoji."""

from wordle import Wordle


def test_feedback_to_emoji() -> None:
    """Testing the string is converting to emoji correctly."""
    assert Wordle.feedback_to_emoji("G_YG_") == "🟩⬜🟨🟩⬜"

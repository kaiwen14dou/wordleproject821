"""Testing feedback converting to emoji."""

import pytest

from wordle import Feedback, Wordle


def test_feedback_to_emoji_mixed() -> None:
    """Test conversion of mixed feedback list to emojis."""
    feedback = [
        Feedback.GREEN,
        Feedback.GRAY,
        Feedback.YELLOW,
        Feedback.GREEN,
        Feedback.GRAY,
    ]
    assert Wordle.feedback_to_emoji(feedback) == "🟩⬜🟨🟩⬜"


def test_feedback_to_emoji_empty() -> None:
    """Test conversion of empty feedback list."""
    assert Wordle.feedback_to_emoji([]) == ""

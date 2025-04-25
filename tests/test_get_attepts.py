"""Testing the get attmept is correct."""

from wordle import Wordle


def test_get_attempts() -> None:
    """Test that attempts list stores (guess, feedback) correctly."""
    game = Wordle(secret_word="candy")
    result = game.guess("zebra")
    assert game.attempts == [("zebra", result)]

"""Testing the get attmept is correct."""

from wordle import Wordle


def test_get_attempts() -> None:
    """Testing the attmept is correct."""
    game = Wordle(secret_word="candy")
    game.guess("zebra")
    attempts = game.get_attempts()
    assert len(attempts) == 1
    assert attempts[0][0] == "zebra"
    assert len(attempts[0][1]) == 5  # feedback string

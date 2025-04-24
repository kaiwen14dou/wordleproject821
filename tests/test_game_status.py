"""Testing game status function is correct."""

from wordle import Wordle


def test_game_status_in_progress() -> None:
    """Testing game status when it is in progress."""
    game = Wordle(secret_word="candy")
    assert game.game_status() == "In Progress"


def test_game_status_won() -> None:
    """Testing game status is won."""
    game = Wordle(secret_word="candy")
    game.guess("candy")
    assert game.game_status() == "Won"


def test_game_status_lost() -> None:
    """Testing game status is lost."""
    game = Wordle(secret_word="candy", max_attempts=1)
    game.guess("zebra")
    assert game.game_status() == "Lost. The word was 'candy'"

"""Generate a new game called wordle."""

from collections import Counter
from enum import Enum


class Feedback(Enum):
    """A class to define feedback."""

    GREEN = "G"
    YELLOW = "Y"
    GRAY = "_"


class Wordle:
    """A class to represent the Wordle game logic.

    Attributes:
        secret_word (str): The 5-letter target word to guess.
        max_attempts (int): The maximum number of allowed guesses.
        attempts (list[tuple[str, str]]): A list of guesses and their
        corresponding feedback.
        is_won (bool): Whether the game has been won.
        is_over (bool): Whether the game is over (won or max attempts reached).
    """

    def __init__(self, secret_word: str, max_attempts: int = 6) -> None:
        """Initialize the Wordle game.

        Args:
            secret_word (str): The word to be guessed; must be 5 lowercase
            alphabetic characters.
            max_attempts (int): The number of guesses allowed (default is 6).

        Raises:
            ValueError: If the secret word is not a valid 5-letter word.
        """
        if len(secret_word) != 5 or not secret_word.isalpha():
            raise ValueError(
                "Secret word must be a 5-letter alphabetic string."
            )
        self.secret_word: str = secret_word.lower()
        self.max_attempts: int = max_attempts
        self.attempts: list[tuple[str, list[Feedback]]] = []
        self.is_won: bool = False
        self.is_over: bool = False

    def guess(self, word: str) -> list[Feedback]:
        """Submit a guess and receive feedback on letter correctness and.

        positions.

        Args:
            word (str): A 5-letter guess.

        Returns:
            list[Feedback]:  'G' for correct, 'Y'
            for wrong position, '_' for incorrect).

        Raises:
            Exception: If the game is already over.
            ValueError: If the guess is not a valid 5-letter alphabetic string.
        """
        word = word.lower()
        if self.is_over:
            raise Exception("Game over. No more guesses allowed.")
        if len(word) != 5 or not word.isalpha():
            raise ValueError("Guess must be a 5-letter alphabetic string.")

        feedback = self._generate_feedback(word)
        self.attempts.append((word, feedback))

        if word == self.secret_word:
            self.is_won = True
            self.is_over = True
        elif len(self.attempts) >= self.max_attempts:
            self.is_over = True

        return feedback

    def _generate_feedback(self, guess: str) -> list[Feedback]:
        """Generate feedback for a given guess compared to the secret word.

        Args:
            guess (str): The guessed word.

        Returns:
            list[Feedback]: Feedback composed of 'G', 'Y', and '_' characters.
        """
        feedback = [Feedback.GRAY] * 5
        secret_temp = list(self.secret_word)

        # First pass: correct position
        for i in range(5):
            if guess[i] == secret_temp[i]:
                feedback[i] = Feedback.GREEN
                secret_temp[i] = "*"

        # Count remaining letters (only non-green ones)
        remaining_letters = Counter(c for c in secret_temp if c is not None)

        # Second pass: correct letter, wrong position
        for i in range(5):
            if (
                feedback[i] == Feedback.GRAY
                and guess[i] in remaining_letters
                and remaining_letters[guess[i]] > 0
            ):
                feedback[i] = Feedback.YELLOW
                remaining_letters[guess[i]] -= 1

        return feedback

    @staticmethod
    def feedback_to_emoji(feedback: list[Feedback]) -> str:
        """Give the emoji feedbacks."""
        mapping = {
            Feedback.GREEN: "🟩",
            Feedback.YELLOW: "🟨",
            Feedback.GRAY: "⬜",
        }
        return "".join(mapping[f] for f in feedback)

    def game_status(self) -> str:
        """Get the current game status.

        Returns:
            str: "Won", "Lost. The word was 'xxxxx'", or "In Progress".
        """
        if self.is_won:
            return "Won"
        elif self.is_over:
            return f"Lost. The word was '{self.secret_word}'"
        return "In Progress"

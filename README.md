# Wordle

## Introduction 

PyWordle is a terminal-based implementation of the classic Wordle game in Python. It supports core game logic, emoji-style feedback, repeated letter handling, and a comprehensive set of unit tests.

## Project Features

- Clean and modular game logic via a `Wordle` class
- Accurate feedback for guesses using `Feedback` enums (`GREEN`, `YELLOW`, `GRAY`)
- Emoji output for visual feedback: 🟩 (correct), 🟨 (misplaced), ⬜ (wrong)
- Full set of unit tests for functionality, edge cases, and input validation
- Terminal-based gameplay with `run_game.py`

## Game Rules

- The secret word is always 5 letters long.
- You have a maximum of 6 attempts to guess the secret word.
- Each guess must be a valid 5-letter English word from the provided dictionary.
- After each guess, you receive feedback:
  - 🟩 Green: correct letter in the correct position
  - 🟨 Yellow: correct letter in the wrong position
  - ⬜ Gray: letter not in the word at all
- Repeated letters are handled carefully: each letter in the secret word can only be matched once per guess.


## How to Play in Terminal

### Prerequisites
Python 3.11 is required. 

### Installation Steps
Install required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

From the project root, run:

   ```bash
   python run_game.py
   ```

This launches a game session using a randomly selected secret word from word_doc.txt. Type your guess and press Enter. You have 6 tries to guess the word.

To exit the game at any time, type: `exit`


## Core Class: Wordle

### Key Methods

- `guess(word: str) -> list[Feedback]` — submit a guess and get structured feedback as a list of enums
- `feedback_to_emoji(feedback: list[Feedback]) -> str` — convert enum feedback to emoji visuals
- `game_status() -> str` — returns game outcome: "Won", "Lost. The word was '____'", or "In Progress"

### Error Handling

- Raises `ValueError` for invalid guesses (e.g. wrong length or characters)
- Raises `Exception` if guesses are submitted after the game is over


## Running Tests
All tests use `pytest`. To run them:

   ```bash
   pytest tests/
   ```

Make sure `pytest` is installed:

   ```sh
   pip install pytest
   ```

## Test Coverage Summary

We test the following scenarios:

- ✅ Emoji feedback generation using enums
- ✅ Handling of repeated letters
- ✅ Full match (correct guess)
- ✅ Game status: in progress, win, and loss
- ✅ Attempt logging and feedback tracking
- ✅ Input validation and error handling

Run `pytest -v` for detailed results.

## Authors

- Keru Zhou
- Kaiwen Lu

We hope you enjoy playing PyWordle as much as we enjoyed building it 🎉

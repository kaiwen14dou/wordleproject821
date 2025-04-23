"""Running the game in terminal."""

import os
import random
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from wordle import Wordle

with open("data/word_doc.txt") as f:
    word_list: list[str] = [line.strip().lower() for line in f]

secret_word: str = random.choice(word_list)

game = Wordle(secret_word)

print("🎉 Welcome to Wordle!")
print("🔤 Guess the 5-letter secret word within 6 tries.")
print("🟩 = correct letter in the correct spot")
print("🟨 = correct letter in the wrong spot")
print("⬜ = letter not in the word at all")
print("💡 Valid guesses must be real 5-letter words from the dictionary.\n")
print("Type 'exit' to quit.\n")

while not game.is_over:
    guess = input("👉 Your guess: ").strip().lower()

    if guess == "exit":
        print("👋 Exiting the game. Goodbye!")
        sys.exit(0)

    try:
        feedback = game.guess(guess)

        print("🟩🟨⬜ Feedback:", Wordle.feedback_to_emoji(feedback))
        print(f"📊 Attempts left: {game.max_attempts - len(game.attempts)}\n")

    except (ValueError, Exception) as e:
        print("❌", e)


print("\n📢 Game Over:", game.game_status())
print("📝 All attempts:")

for i, (word, fb) in enumerate(game.get_attempts(), start=1):
    print(f"Round {i}: {word.upper()} → {Wordle.feedback_to_emoji(fb)}")

sys.exit(0 if game.is_won else 2)

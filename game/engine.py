from pathlib import Path
from datetime import datetime
from game.ascii_art import STATES


class HangmanGame:
    MAX_WRONG = 6

    def __init__(self, word: str):
        self.word = word.lower()
        self.progress = ['_' if c.isalpha() else c for c in self.word]
        self.guessed = []
        self.wrong_guesses = []
        self.wrong_count = 0
        self.won = False
        self.score = 0
        self.history = []

    def guess_letter(self, ch: str):
        ch = ch.lower()
        if not ch.isalpha() or len(ch) != 1:
            return 'invalid'
        if ch in self.guessed:
            return 'repeat'
        self.guessed.append(ch)
        if ch in self.word:
            for i, c in enumerate(self.word):
                if c == ch:
                    self.progress[i] = ch
            self.history.append((ch, 'Correct'))
            if '_' not in self.progress:
                self.won = True
            return 'correct'
        else:
            self.wrong_count += 1
            self.wrong_guesses.append(ch)
            self.history.append((ch, 'Wrong'))
            return 'wrong'

    def guess_full_word(self, guess: str):
        guess = guess.lower().strip()
        if guess == self.word:
            self.progress = list(self.word)
            self.won = True
            self.history.append((guess, 'CorrectFull'))
            return True
        else:
            self.wrong_count += 1
            self.wrong_guesses.append(guess)
            self.history.append((guess, 'WrongFull'))
            return False

    def current_ascii(self):
        idx = min(self.wrong_count, self.MAX_WRONG)
        return STATES[idx]

    def compute_score(self):
        base = len([c for c in self.word if c.isalpha()]) * 10
        remaining = max(0, self.MAX_WRONG - self.wrong_count)
        bonus = remaining * 5
        penalty = self.wrong_count * 5
        self.score = max(0, base + bonus - penalty)
        return self.score

    def play(self, display, log_path: Path):
        with log_path.open('a', encoding='utf-8') as f:
            f.write(f"Selected word (hidden): {self.word}\nWord length: {len(self.word)}\n\n")

        display.show_new_word(len(self.word))

        while True:
            display.show_state(' '.join(self.progress), self.guessed, self.MAX_WRONG - self.wrong_count, self.current_ascii())
            choice = display.prompt_guess()

            if choice.lower() == 'quit':
                display.say_goodbye()
                break
            if choice.lower() == 'guess':
                full = display.prompt_full_guess()
                correct = self.guess_full_word(full)
                with log_path.open('a', encoding='utf-8') as f:
                    f.write(f"Full-word guess: {full} -> {'Correct' if correct else 'Wrong'}\n")
                if correct:
                    display.show_message(f"Correct! The word is: {self.word}")
                    break
            else:
                res = self.guess_letter(choice)
                with log_path.open('a', encoding='utf-8') as f:
                    f.write(f"Guess: {choice} -> {res}\n")
                if res == 'invalid':
                    display.show_message('Please enter a single alphabetic character.')
                elif res == 'repeat':
                    display.show_message(f"You've already guessed '{choice}'.")
                elif res == 'correct':
                    display.show_message('Correct!')
                elif res == 'wrong':
                    display.show_message('Wrong!')

            if self.won:
                display.show_message(f"You win! Word: {self.word}")
                self.compute_score()
                display.show_message(f"Points earned this round: {self.score}")
                break

            if self.wrong_count >= self.MAX_WRONG:
                display.show_message(f"You lost. The word was: {self.word}")
                self.score = 0
                break

"""Entry point for the Hangman game. Keeps top-level flow only."""
from pathlib import Path
from game.wordlist import WordList
from game.engine import HangmanGame
from ui.display import Display
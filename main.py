"""Entry point for the Hangman game. Keeps top-level flow only."""
from pathlib import Path
from game.wordlist import WordList
from game.engine import HangmanGame
from ui.display import Display
def main():
    base = Path(__file__).parent
    words_dir = base / "words"
    logs_dir = base / "game_log"

    wlist = WordList(words_dir)
    display = Display()

    total_stats = wlist.load_or_init_stats(logs_dir)

    while True:
        display.show_welcome()
        category = display.prompt_category(wlist.available_categories())
        word = wlist.pick_word(category)
        game = HangmanGame(word)
        log_folder, log_path = wlist.create_new_game_log_folder(logs_dir)

        game.play(display, log_path)

        total_stats['games_played'] += 1
        if game.won:
            total_stats['wins'] += 1
            total_stats['total_score'] += game.score
        else:
            total_stats['losses'] += 1

        wlist.save_stats(total_stats, logs_dir)

        display.show_stats(total_stats)

        if not display.ask_play_again():
            display.say_goodbye()
            break


if __name__ == "__main__":
    main()

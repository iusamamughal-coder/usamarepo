class Display:
     def show_welcome(self):
        print('\nWelcome to Hangman!\n')

     def prompt_category(self, categories):
        print('Choose a category: ' + ', '.join(categories))
        print("Type nothing to choose from all words.")
        choice = input('Category: ').strip()
        return choice if choice else None
    
     def prompt_category(self, categories):
        print('Choose a category: ' + ', '.join(categories))
        print("Type nothing to choose from all words.")
        choice = input('Category: ').strip()
        return choice if choice else None

     def show_new_word(self, length):
        print(f"\nNew word selected (length {length})\n")

     def show_state(self, progress, guessed, remaining, art):
        print('\n' + art)
        print('\nProgress: ' + progress)
        print('Guessed letters: ' + ', '.join(guessed))
        print(f'Remaining attempts: {remaining}\n')

     def prompt_guess(self):
        return input("Enter a letter (or type 'guess' to guess full word, 'quit' to exit): ").strip()

     def prompt_full_guess(self):
        return input('Enter your full-word guess: ').strip()

     def show_message(self, msg):
        print(msg)

     def ask_play_again(self):
        ans = input('\nPlay again? (y/n): ').strip().lower()
        return ans == 'y'

     def say_goodbye(self):
        print('\nThanks for playing! Goodbye.\n')

     def show_stats(self, stats):
        games = stats.get('games_played', 0)
        wins = stats.get('wins', 0)
        losses = stats.get('losses', 0)
        total_score = stats.get('total_score', 0)
        win_rate = (wins / games * 100) if games else 0
        avg = (total_score / games) if games else 0
        print(f"\nGames played: {games}  Wins: {wins}  Losses: {losses}  Win rate: {win_rate:.2f}%")
        print(f"Total score: {total_score}  Average score per game: {avg:.2f}\n")


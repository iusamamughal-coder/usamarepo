This file contains the folowing contents which are explained in their respective section

    1. How to run the game
    2. Wordlist format and categories used
    3. Scoring method
    4. How logs are saved

1. How to run the game:
    Following procedure should be used to run the gama

        1. Open Anaconda Powershell Prompt

        2. Go to the Hang_Man game directry by changing the current directry with the help of cd command.
        For example if the hang_man game folder is present on the deckstop the paste the folder directry next to cd command like cd "C:\Users\SiliCon\Desktop\hangman game"

        3. After changing the directry run main.py file by writing following command
                        python main.py

        This will stat the game in the terminal.

        4. Once the game is started, it will ask the player to select any one of the catagory of the word from animal, science, programming or country. When the player will select the catagory, it will display the dashes for each letter in the word to be guessed. It will ask to guess either full word which can be enter by writting guess and giving the whole word or single letter on each try.
        There are total six chances which allow you to give wrong letters which are not in the word. Each time the wrong letter is given the hangman parts start to appear and your chances start to reduce one at each time. Player can quit game anytime by writting quit.
        Once all letters are guessed correcly, the games ends and 
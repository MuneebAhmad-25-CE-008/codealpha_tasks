# Add this at the top with your other imports
import os
import time

def display_hangman(incorrect_guesses):
    """
    Display the hangman ASCII art based on number of incorrect guesses.
    
    Args:
        incorrect_guesses: Number of incorrect guesses made
    
    Returns:
        String containing the hangman ASCII art
    """
    stages = [
        # Final state: complete hangman (6 incorrect guesses)
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        # 5 incorrect guesses
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     /
           -
        """,
        # 4 incorrect guesses
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |
           -
        """,
        # 3 incorrect guesses
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |
           -
        """,
        # 2 incorrect guesses
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |
           -
        """,
        # 1 incorrect guess
        """
           --------
           |      |
           |      O
           |
           |
           |
           -
        """,
        # Initial state: no incorrect guesses
        """
           --------
           |      |
           |
           |
           |
           |
           -
        """
    ]
    return stages[6 - incorrect_guesses]

def display_game_header():
    """
    Display the game header with decorative elements.
    """
    print("\n")
    print("=" * 50)
    print("🎮 HANGMAN GAME 🎮".center(50))
    print("=" * 50)
    print("\n")

def display_game_status(secret_word, guessed_letters, incorrect_guesses, max_guesses):
    """
    Display the current game status including the hangman, word state, and guesses.
    
    Args:
        secret_word: The word to be guessed
        guessed_letters: Set of letters that have been guessed
        incorrect_guesses: Number of incorrect guesses made
        max_guesses: Maximum allowed incorrect guesses
    """
    clear_screen()
    display_game_header()
    
    # Display hangman
    print(display_hangman(incorrect_guesses))
    print("\n")
    
    # Display word state
    word_state = display_game_state(secret_word, guessed_letters)
    print(f"Word: {word_state}")
    
    # Display guessed letters in a formatted way
    sorted_guesses = sorted(guessed_letters)
    print("\nGuessed letters:", end=" ")
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        if letter in sorted_guesses:
            print(f"\033[92m{letter}\033[0m", end=" ")  # Green for guessed letters
        else:
            print("_", end=" ")
    
    # Display remaining guesses
    remaining = max_guesses - incorrect_guesses
    print(f"\n\nRemaining guesses: {remaining}")
    print(f"{'❤️ ' * remaining}{'💔 ' * incorrect_guesses}")
    print("\n")

def display_win_message(word, turns_taken):
    """
    Display a decorated win message.
    
    Args:
        word: The word that was correctly guessed
        turns_taken: Number of turns taken to win
    """
    print("\n")
    print("🎉" * 20)
    print("\nCONGRATULATIONS! YOU WIN! 🏆\n".center(50))
    print(f"The word was: {word}".center(50))
    print(f"You got it in {turns_taken} turns!".center(50))
    print("\n")
    print("🎉" * 20)
    print("\n")

def display_lose_message(word):
    """
    Display a decorated lose message.
    
    Args:
        word: The word that wasn't guessed
    """
    print("\n")
    print("💀" * 20)
    print("\nGAME OVER - Better luck next time! 😢\n".center(50))
    print(f"The word was: {word}".center(50))
    print("\n")
    print("💀" * 20)
    print("\n")

# Modify your play_hangman function to use these new display functions:

def play_hangman():
    """
    Main function to run the Hangman game with enhanced visual display.
    """
    try:
        word_list = load_words()
        secret_word = random.choice(word_list).lower()
        max_incorrect_guesses = 6
        incorrect_guesses = 0
        guessed_letters = set()
        turns_taken = 0
        
        display_game_status(secret_word, guessed_letters, incorrect_guesses, max_incorrect_guesses)
        
        while incorrect_guesses < max_incorrect_guesses:
            try:
                guess = input("Enter your guess: ").lower()
                turns_taken += 1
                
                is_valid, message = validate_guess(guess, guessed_letters)
                if not is_valid:
                    print(f"\n{message}")
                    time.sleep(1)
                    display_game_status(secret_word, guessed_letters, incorrect_guesses, max_incorrect_guesses)
                    continue
                
                guessed_letters.add(guess)
                
                if guess in secret_word:
                    if all(letter in guessed_letters for letter in secret_word):
                        display_game_status(secret_word, guessed_letters, incorrect_guesses, max_incorrect_guesses)
                        display_win_message(secret_word, turns_taken)
                        return True
                else:
                    incorrect_guesses += 1
                
                display_game_status(secret_word, guessed_letters, incorrect_guesses, max_incorrect_guesses)
                
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"\nError processing guess: {str(e)}")
                time.sleep(1)
        
        display_lose_message(secret_word)
        return False
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        return False
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        return False
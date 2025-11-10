import random
import sys
import os
import time

def load_words():
    """
    Load words from the words.txt file.
    If the file doesn't exist, fall back to default words.
    
    Returns:
        list: A list of words for the game
    """
    default_words = ["python", "hangman", "computer", "programming", "developer"]
    try:
        # Try to read from words.txt in the same directory as the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        words_path = os.path.join(script_dir, 'words.txt')
        
        with open(words_path, 'r') as file:
            words = [word.strip().lower() for word in file.readlines() if word.strip()]
            # Verify we have valid words
            if not words:
                raise ValueError("Words file is empty")
            return words
    except (FileNotFoundError, IOError, ValueError) as e:
        # Log the error and fall back to default words
        print(f"Warning: Could not load words.txt ({str(e)})")
        print("Using default word list...")
        time.sleep(2)  # Give user time to read the message
        return default_words

def validate_guess(guess, guessed_letters):
    """
    Validate user's guess with improved error handling.
    
    Args:
        guess: The user's guess input
        guessed_letters: Set of previously guessed letters
    
    Returns:
        tuple: (is_valid, message)
    """
    if not guess:
        return False, "Please enter a letter."
    
    if len(guess) != 1:
        return False, "Please enter a single letter."
    
    if not guess.isalpha():
        return False, "Please enter a letter, not a number or special character."
    
    if guess in guessed_letters:
        return False, f"You already guessed '{guess}'. Try a different letter."
    
    return True, ""

def display_game_state(word, guessed_letters):
    """
    Display the current state of the word with guessed letters revealed
    and underscores for letters not yet guessed.
    
    Args:
        word: The secret word to guess
        guessed_letters: Set of letters that have been guessed
    
    Returns:
        String representation of the current word state
    """
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def clear_screen():
    """
    Clear the console screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def play_hangman():
    """
    Main function to run the Hangman game.
    Handles game loop, user input, and win/lose conditions.
    
    Returns:
        Boolean indicating whether player wants to play again
    """
    try:
        # Load words from file
        word_list = load_words()
        
        # Randomly select a word from the list
        secret_word = random.choice(word_list).lower()
        
        # Initialize game variables
        max_incorrect_guesses = 6
        incorrect_guesses = 0
        guessed_letters = set()
        
        # Display welcome message
        clear_screen()
        print("=" * 40)
        print("Welcome to Hangman!")
        print("=" * 40)
        print(f"The word has {len(secret_word)} letters.")
        print(f"You have {max_incorrect_guesses} incorrect guesses allowed.\n")
        
        # Main game loop
        while incorrect_guesses < max_incorrect_guesses:
            # Display current game state
            print(f"Word: {display_game_state(secret_word, guessed_letters)}")
            print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
            print(f"Remaining guesses: {max_incorrect_guesses - incorrect_guesses}\n")
            
            try:
                # Get player input with timeout
                guess = input("Guess a letter: ").lower()
                
                # Validate the guess
                is_valid, message = validate_guess(guess, guessed_letters)
                if not is_valid:
                    print(f"\n{message}\n")
                    time.sleep(1)  # Give user time to read error message
                    continue
                
                # Add the guess to guessed letters
                guessed_letters.add(guess)
                
                # Check if the guess is correct
                if guess in secret_word:
                    print(f"\nGood guess! '{guess}' is in the word.\n")
                    
                    # Check for win
                    if all(letter in guessed_letters for letter in secret_word):
                        print("=" * 40)
                        print(f"Congratulations! You Win!")
                        print(f"The word was: {secret_word}")
                        print("=" * 40)
                        return True
                else:
                    incorrect_guesses += 1
                    print(f"\nSorry, '{guess}' is not in the word.\n")
                
                time.sleep(0.5)  # Short pause for better game flow
                clear_screen()
                
            except KeyboardInterrupt:
                raise  # Re-raise to be caught by outer try/except
            
            except Exception as e:
                print(f"\nAn error occurred while processing your guess: {str(e)}")
                time.sleep(1)
                continue
        
        # Game over - player lost
        print("=" * 40)
        print("Game Over - You Lose!")
        print(f"The word was: {secret_word}")
        print("=" * 40)
        return False
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        return False
        
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        return False

def main():
    """
    Main entry point for the game.
    Handles replay functionality and ensures console stays open.
    """
    try:
        while True:
            # Play one round of the game
            game_result = play_hangman()
            
            # Ask if player wants to play again
            print("\nWould you like to play again?")
            while True:
                try:
                    play_again = input("Enter 'y' for yes or 'n' for no: ").lower()
                    if play_again in ['y', 'yes', 'n', 'no']:
                        break
                    print("Please enter 'y' or 'n'")
                except Exception:
                    print("Invalid input. Please enter 'y' or 'n'")
            
            if play_again not in ['y', 'yes']:
                print("\nThank you for playing Hangman! Goodbye!")
                break
            
            clear_screen()
    
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
    
    finally:
        # Keep console window open when running as .exe
        print("\nPress Enter to exit...")
        input()

# Entry point
if __name__ == "__main__":
    main()

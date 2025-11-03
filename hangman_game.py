import random
import sys


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


def is_word_guessed(word, guessed_letters):
    """
    Check if all letters in the word have been guessed.
    
    Args:
        word: The secret word to guess
        guessed_letters: Set of letters that have been guessed
    
    Returns:
        Boolean indicating whether the word is completely guessed
    """
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True


def play_hangman():
    """
    Main function to run the Hangman game.
    Handles game loop, user input, and win/lose conditions.
    
    Returns:
        Boolean indicating whether player wants to play again
    """
    # Predefined list of words to choose from
    word_list = ["python", "hangman", "computer", "programming", "developer"]
    
    # Randomly select a word from the list
    secret_word = random.choice(word_list).lower()
    
    # Initialize game variables
    max_incorrect_guesses = 6
    incorrect_guesses = 0
    guessed_letters = set()
    
    # Display welcome message
    print("=" * 40)
    print("Welcome to Hangman!")
    print("=" * 40)
    print(f"The word has {len(secret_word)} letters.")
    print(f"You have {max_incorrect_guesses} incorrect guesses allowed.\n")
    
    # Main game loop - continues until win or lose condition is met
    while incorrect_guesses < max_incorrect_guesses:
        # Display current state of the word
        print(f"Word: {display_game_state(secret_word, guessed_letters)}")
        print(f"Guessed letters: {sorted(guessed_letters) if guessed_letters else 'None'}")
        print(f"Remaining guesses: {max_incorrect_guesses - incorrect_guesses}\n")
        
        # Get player input
        guess = input("Guess a letter: ").lower()
        
        # Validate input - must be a single letter
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.\n")
            continue
        
        # Check if letter was already guessed
        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.\n")
            continue
        
        # Add the guess to the set of guessed letters
        guessed_letters.add(guess)
        
        # Check if the guess is correct
        if guess in secret_word:
            print(f"Good guess! '{guess}' is in the word.\n")
            
            # Check if the player has won
            if is_word_guessed(secret_word, guessed_letters):
                print("=" * 40)
                print(f"Congratulations! You Win!")
                print(f"The word was: {secret_word}")
                print("=" * 40)
                return True
        else:
            # Incorrect guess - increment counter
            incorrect_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.\n")
    
    # If loop exits, player has run out of guesses
    print("=" * 40)
    print("Game Over - You Lose!")
    print(f"The word was: {secret_word}")
    print("=" * 40)
    return True


def main():
    """
    Main entry point for the game.
    Handles replay functionality and ensures console stays open.
    """
    try:
        while True:
            # Play one round of the game
            play_hangman()
            
            # Ask if player wants to play again
            print("\nWould you like to play again?")
            play_again = input("Enter 'y' for yes or 'n' for no: ").lower()
            
            if play_again != 'y' and play_again != 'yes':
                print("\nThank you for playing Hangman! Goodbye!")
                break
            
            # Clear screen effect with newlines
            print("\n" * 2)
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nGame interrupted. Thanks for playing!")
    
    except Exception as e:
        # Catch any unexpected errors
        print(f"\nAn error occurred: {e}")
    
    finally:
        # Keep console window open when running as .exe
        input("\nPress Enter to exit...")


# Entry point - run the game when script is executed
if __name__ == "__main__":
    main()

import random
import sys
import os
import time
import socket

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.
    """
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path is None:
        # Use the directory of this script as the base in development
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_words():
    """
    Load words from assets/words.txt (or words.txt). Fallback to default list.
    """
    default_words = ["python", "hangman", "computer", "programming", "developer"]
    try:
        possible_paths = [
            get_resource_path(os.path.join("assets", "words.txt")),
            get_resource_path("words.txt"),
            os.path.join(os.path.dirname(__file__), "..", "assets", "words.txt"),
        ]
        for words_path in possible_paths:
            if words_path and os.path.exists(words_path):
                with open(words_path, "r", encoding="utf-8") as f:
                    words = [w.strip().lower() for w in f.readlines() if w.strip()]
                    if words:
                        return words
        raise FileNotFoundError("words.txt not found in expected locations")
    except Exception as e:
        print(f"Warning: Could not load words.txt ({e})")
        print("Using default word list...")
        time.sleep(1)
        return default_words

def clear_screen():
    """Clear the console screen in a cross-platform way."""
    os.system("cls" if os.name == "nt" else "clear")

def display_game_state(word, guessed_letters):
    """
    Return the current masked word state (e.g. 'p _ t h o n').
    """
    return " ".join((c if c in guessed_letters else "_") for c in word)

def display_hangman(incorrect_guesses):
    stages = [
        # 6 incorrect (final)
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / \
           -
        """,
        # 5
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     /
           -
        """,
        # 4
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |      |
           -
        """,
        # 3
        """
           --------
           |      |
           |      O
           |     \|
           |      |
           |      |
           -
        """,
        # 2
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |      |
           -
        """,
        # 1
        """
           --------
           |      |
           |      O
           |
           |
           |
           -
        """,
        # 0
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
    # clamp index to [0,6]
    idx = max(0, min(6, 6 - incorrect_guesses))
    return stages[idx]

def display_game_header():
    print("\n" + "=" * 50)
    print(" HANGMAN GAME ".center(50))
    print("=" * 50 + "\n")

def display_game_status(secret_word, guessed_letters, incorrect_guesses, max_guesses):
    """
    Show the hangman ASCII art, the masked word, guessed letters and remaining guesses.
    """
    clear_screen()
    display_game_header()
    print(display_hangman(incorrect_guesses))
    print()  
    # FIXED: call display_game_state (previously called display_game_status recursively)
    word_state = display_game_state(secret_word, guessed_letters)
    print(f"Word: {word_state}\n")
    sorted_guesses = sorted(guessed_letters)
    if sorted_guesses:
        print("Guessed letters:", ", ".join(sorted_guesses))
    else:
        print("Guessed letters: None")
    remaining = max_guesses - incorrect_guesses
    print(f"\nRemaining guesses: {remaining}\n")

def display_win_message(word, turns_taken):
    print("\n" + "🎉" * 8)
    print("CONGRATULATIONS! YOU WIN!")
    print(f"The word was: {word}")
    print(f"You got it in {turns_taken} turns!")
    print("🎉" * 8 + "\n")

def display_lose_message(word):
    print("\n" + "💀" * 8)
    print("GAME OVER - Better luck next time!")
    print(f"The word was: {word}")
    print("💀" * 8 + "\n")

# Single-instance guard to prevent multiple copies from running
_singleton_socket = None

def ensure_single_instance(port=65432):
    """
    Try to bind to localhost:port. If bind fails, another instance is running.
    Keep the socket open so the OS prevents others from binding.
    """
    global _singleton_socket
    if _singleton_socket:
        return True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(("127.0.0.1", port))
        s.listen(1)
        _singleton_socket = s
        return True
    except OSError:
        # Another instance is running
        return False


def validate_guess(raw_guess, guessed_letters):
    """
    Validate the user's guess.

    Returns:
      (False, error_message) on invalid input
      (True, processed_guess) on success (processed_guess is a single lowercase letter)
    """
    if raw_guess is None:
        return False, "Please enter a letter."
    guess = str(raw_guess).strip()
    if not guess:
        return False, "Please enter a letter."
    if len(guess) != 1:
        return False, "Please enter a single letter."
    if not guess.isascii() or not guess.isalpha():
        return False, "Please enter a letter from A-Z."
    guess = guess.lower()
    if guess in guessed_letters:
        return False, f"You already guessed '{guess}'. Try a different letter."
    return True, guess


def play_hangman():
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
                raw = input("Enter your guess: ")
                is_valid, result = validate_guess(raw, guessed_letters)
                if not is_valid:
                    print("\n" + result + "\n")
                    time.sleep(1)
                    display_game_status(secret_word, guessed_letters, incorrect_guesses, max_incorrect_guesses)
                    continue

                # Only increment turns for valid guesses
                turns_taken += 1
                guess = result  # processed single lowercase letter
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
                print(f"\nError processing guess: {e}\n")
                time.sleep(1)
                display_game_status(secret_word, guessed_letters, incorrect_guesses, max_incorrect_guesses)

        display_lose_message(secret_word)
        return False

    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        return False
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return False


def main():
    # Prevent multiple instances from running simultaneously
    if not ensure_single_instance():
        print("Another instance of Hangman is already running. Exiting.")
        time.sleep(2)
        try:
            sys.exit(0)
        except SystemExit:
            return

    try:
        while True:
            play_hangman()
            print("\nWould you like to play again?")
            while True:
                k = input("Enter 'y' for yes or 'n' for no: ").strip().lower()
                if k in ("y", "yes", "n", "no"):
                    break
                print("Please enter 'y' or 'n'")
            if k not in ("y", "yes"):
                print("\nThank you for playing Hangman! Goodbye!")
                break
            clear_screen()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    finally:
        print("\nPress Enter to exit...")
        try:
            input()
        except Exception:
            pass

if __name__ == "__main__":
    main()
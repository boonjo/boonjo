from wiki import get_page, find_short_path, get_page_links_with_cache
import random
import warnings
from bs4 import GuessedAtParserWarning
# Suppress BeautifulSoup parser warnings
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)
import nltk
import spacy

def main():
    print("\n\n🥓 Welcome to WikiBacon! 🥓\n")
    print("In this game, we start from a random Wikipedia page, and then we compete to see who can name a page that is *farthest away* from the original page.\n")
    print("Ready to play? Hit Enter to start, or type 'q' to quit")
    cmd = input()
    if cmd == "q":
        return
    
    with open("dictionary.txt", "r") as f:
        common_words = f.read().splitlines()

    # random.seed(42) Removing this for true randomness

    def get_well_connected_page():
        """Choose pages that are more likely to be well-connected"""
        for _ in range(5):  # Try up to 5 times
            word = random.choice(common_words)
            page = get_page(word)
            if page and len(get_page_links_with_cache(page.title)) > 50:  # Well-connected
                return page
        return get_page(random.choice(common_words))  # Fallback

    while True:

        # Start Page
        while True:
            start_word = random.choice(common_words)
            start_page = get_page(start_word)
            if start_page:
                break
        print(f"The starting page is: {start_page.title}\n")
        print(f"Summary: {start_page.summary[:500]}...\n")

        # Computer Page
        while True:
            computer_page = get_well_connected_page()
            if computer_page:
                break
        print(f"The computer's page is: {computer_page.title}\n")
        print(f"Summary: {computer_page.summary[:500]}...\n")

        # User Page
        print("What would you like your page to be page?")
        user_page_name = input().strip()
        user_page = get_page(user_page_name)
        if not user_page:
            print("Couldn't find that page. Please try again.\n")
            continue
        print(f"Your page is: {user_page.title}\n")
        print(f"Summary: {user_page.summary[:500]}...\n")

        # Paths
        print("Calculating Bacon paths...\n")

        computer_path = find_short_path(start_page, computer_page)
        if computer_path:
            print("Computer's path:")
            print(f"\n -> ".join(computer_path))
            print(f"Length: {len(computer_path)}\n")
        else:
            print("Computer's path: None found (timeout)\n")

        user_path = find_short_path(start_page, user_page)
        if user_path:
            print("Your path:")
            print(f"\n -> ".join(user_path))
            print(f"Length: {len(user_path)}\n")
        else:
            print("Your path: None found (timeout)\n")

        # Winner
        if computer_path and user_path:
            if len(computer_path) > len(user_path):
                print("I win!")
            elif len(computer_path) < len(user_path):
                print("You win!")
            else:
                print("It's a tie!")
        elif user_path:
            print("You win by default — I couldn’t find a path!")
        elif computer_path:
            print("I win by default — you couldn’t find a path!")
        else:
            print("Nobody wins this round...")

        # Replay
        print("\n\nPlay again? Hit Enter for another round, or type 'q' to quit")
        cmd = input()
        if cmd == "q":
            print("\n🥓 Thanks for playing! 🥓\n")
            print("WikiBacon is not affiliated with Wikipedia or the Wikimedia Foundation. To donate to Wikipedia and support their vision of an open internet that makes games like this possible, please visit https://donate.wikimedia.org/\n")
            return

if __name__ == "__main__":
    main()
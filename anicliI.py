import json
import os
import subprocess

def fetch_anime_data():
    """Fetches anime data by running scrape.py and returns it as a list."""
    try:
        process = subprocess.run(['python', 'scrape.py'], capture_output=True, text=True, check=True)
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running scrape.py: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def display_menu(options, selected_index):
    """Displays the menu with the current selection highlighted."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"> {option}")
        else:
            print(f"  {option}")

def search_anime(anime_data):
    """Allows the user to search for anime titles."""
    search_term = input("Enter anime name to search: ").strip().lower()
    if not search_term:
        return
    
    matching_anime = [item for item in anime_data if search_term in item['text'].lower()]
    
    if matching_anime:
        print("\nMatching anime:")
        for item in matching_anime:
            print(f"- {item['text']}")
    else:
        print("\nNo matching anime found.")
    input("Press Enter to continue...")

def main():
    """Main function to run the CLI application."""
    anime_data = fetch_anime_data()
    if not anime_
        return

    options = ["Search"]
    selected_index = 0

    while True:
        display_menu(options, selected_index)

        key = input()
        if key == '\x1b[A':  # Up arrow
            selected_index = (selected_index - 1) % len(options)
        elif key == '\x1b[B':  # Down arrow
            selected_index = (selected_index + 1) % len(options)
        elif key == '\r':  # Enter key
            if options[selected_index] == "Search":
                search_anime(anime_data)
        elif key == '\x03': # Ctrl+C
            break

if __name__ == "__main__":
    main()

import json
import os
import subprocess
import inquirer

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
    if not anime_data:
        return

    options = ["Search"]
    questions = [
        inquirer.List('action',
                      message="What do you want to do?",
                      choices=options,
                      ),
    ]
    while True:
        clear_terminal()
        answers = inquirer.prompt(questions)
        if answers:
            if answers['action'] == "Search":
                search_anime(anime_data)
        else:
            break

if __name__ == "__main__":
    main()

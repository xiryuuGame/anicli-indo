import json
import os
import subprocess
import inquirer
import random

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
        choices = [f"{item['text']}" for item in matching_anime]
        questions = [
            inquirer.List('selected_anime',
                          message="Select an anime for episodes:",
                          choices=choices,
                          ),
        ]
        answers = inquirer.prompt(questions)
        if answers:
            selected_anime_text = answers['selected_anime']
            selected_anime = next((item for item in matching_anime if item['text'] == selected_anime_text), None)
            if selected_anime:
                clear_terminal()
                print(f"Fetching episodes for: {selected_anime['text']}")
                try:
                    process = subprocess.run(['python', 'scrape.py', selected_anime['link']], capture_output=True, text=True, check=True)
                    episode_data = json.loads(process.stdout)
                    if episode_data:
                        episode_choices = [f"{ep['text']}" for ep in episode_data]
                        episode_questions = [
                            inquirer.List('selected_episode',
                                          message="Select an episode:",
                                          choices=episode_choices,
                                          ),
                        ]
                        episode_answers = inquirer.prompt(episode_questions)
                        if episode_answers:
                            selected_episode_text = episode_answers['selected_episode']
                            selected_episode = next((ep for ep in episode_data if ep['text'] == selected_episode_text), None)
                            if selected_episode:
                                clear_terminal()
                                print("\n\n\n")
                                print(" " * int(os.get_terminal_size().columns / 2 - len("SEDANG MENYIAPKAN VIDEO...") / 2) + "SEDANG MENYIAPKAN VIDEO...")
                                user_agents = [
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Edg/120.0.2210.144",
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 SeaMonkey/2.57",
                                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
                                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
                                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 OPR/106.0.0.0",
                                ]
                                user_agent = random.choice(user_agents)
                                try:
                                    process = subprocess.run(['python', 'scrape.py', selected_anime['link'], selected_episode['link'], user_agent], capture_output=True, text=True, check=True)
                                    video_data = json.loads(process.stdout)
                                    if video_data and video_data.get('video_link'):
                                        video_link = video_data['video_link']
                                        mpv_command = [
                                            "mpv",
                                            f"{video_link}",
                                            "--user-agent=" + user_agent,
                                            '--http-header-fields="Referer: https://youtube.googleapis.com/"',
                                            '--http-header-fields="Accept: */*"',
                                            '--http-header-fields="Accept-Encoding: identity;q=1, *;q=0"',
                                            '--http-header-fields="Sec-Fetch-Dest: video"',
                                            '--http-header-fields="Sec-Fetch-Mode: no-cors"',
                                            '--http-header-fields="Sec-Fetch-Site: cross-site"',
                                        ]
                                        subprocess.run(mpv_command)
                                        with open("link.txt", "w") as f:
                                            f.write(video_link)
                                    else:
                                        print("No video link found.")
                                        input("Press Enter to continue...")
                                except subprocess.CalledProcessError as e:
                                    print(f"Error running scrape.py: {e}")
                                    input("Press Enter to continue...")
                                except json.JSONDecodeError as e:
                                    print(f"Error decoding JSON: {e}")
                                    input("Press Enter to continue...")
                    else:
                        print("No episodes found.")
                        input("Press Enter to continue...")
                except subprocess.CalledProcessError as e:
                    print(f"Error running scrape.py: {e}")
                    input("Press Enter to continue...")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    input("Press Enter to continue...")
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

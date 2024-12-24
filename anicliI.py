import json
import os
import subprocess
import inquirer
import random
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich import box
from rich.prompt import Prompt
from rich.style import Style

# Initialize Rich console
console = Console()

# ASCII Art for the header
HEADER_ART = """
 █████╗ ███╗   ██╗██╗ ██████╗██╗     ██╗██╗
██╔══██╗████╗  ██║██║██╔════╝██║     ██║██║
███████║██╔██╗ ██║██║██║     ██║     ██║██║
██╔══██║██║╚██╗██║██║██║     ██║     ██║██║
██║  ██║██║ ╚████║██║╚██████╗███████╗██║██║
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝╚══════╝╚═╝╚═╝
                                           
"""

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_loading_animation(message):
    """Shows a loading animation with the given message."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=message, total=None)

def display_error(message):
    """Displays an error message with distinctive styling."""
    console.print(Panel(
        Text(message, style="bold red"),
        title="Error",
        border_style="red",
        box=box.DOUBLE
    ))

def create_menu(options, title="Menu"):
    """Creates a styled menu table."""
    table = Table(show_header=False, box=box.ROUNDED)
    table.add_column("Option", style="cyan")
    
    for idx, option in enumerate(options, 1):
        table.add_row(f"{idx}. {option}")
    
    return Panel(
        table,
        title=title,
        border_style="blue",
        box=box.DOUBLE
    )

def display_anime_info(anime):
    """Displays detailed anime information in a styled panel."""
    info_table = Table(show_header=False, box=box.SIMPLE)
    info_table.add_column("Field", style="cyan")
    info_table.add_column("Value", style="white")
    
    info_table.add_row("Title", anime['text'])
    if 'status' in anime:
        info_table.add_row("Status", anime['status'])
    
    return Panel(
        info_table,
        title="Anime Information",
        border_style="green",
        box=box.DOUBLE
    )

def create_progress_bar(current, total):
    """Creates a progress bar for episode tracking."""
    with Progress() as progress:
        task = progress.add_task("", total=total)
        progress.update(task, completed=current)
        return progress

def fetch_anime_data():
    """Fetches anime data with loading animation."""
    with console.status("[bold blue]Fetching anime data...") as status:
        try:
            process = subprocess.run(['python', 'scrape.py'], 
                                  capture_output=True, text=True, check=True)
            return json.loads(process.stdout)
        except Exception as e:
            display_error(f"Failed to fetch anime data: {str(e)}")
            return []

def search_anime(anime_data):
    """Enhanced search functionality with interactive UI."""
    search_term = Prompt.ask("[cyan]Enter anime name to search")
    
    if not search_term:
        return
    
    matching_anime = [item for item in anime_data 
                     if search_term.lower() in item['text'].lower()]
    
    if not matching_anime:
        display_error("No matching anime found")
        return
    
    if matching_anime:
        choices = [f"{item['text']}" for item in matching_anime]
        questions = [
            inquirer.List('selected_anime',
                          message="Select an anime for episodes:",
                          choices=choices,
                          ),
        ]
        # Preserved all original video handling logic
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

                                    if video_data:
                                        # Organize links by resolution
                                        links_720 = video_data.get('720', [])
                                        links_480 = video_data.get('480', [])

                                        def try_links(links):
                                            for video_link in links:
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
                                                process = subprocess.run(mpv_command, capture_output=True, text=True)
                                                if "(+) Video --vid=1 (*)" in process.stdout:
                                                    with open("link.txt", "w") as f:
                                                        f.write(video_link)
                                                    return True  # Video played successfully
                                            return False  # No links worked

                                        # Try links from 720 first, then 480 if necessary
                                        if try_links(links_720) or try_links(links_480):
                                            print("Video played successfully.")
                                        else:
                                            print("Error: No links were successful.")
                                            input("Press Enter to continue...")
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
        console.print(Panel("No matching anime found", 
                          title="Error", 
                          border_style="red",
                          box=box.DOUBLE))
    
    # Continue with selection and episode handling...
    # (Previous episode selection and video playback code remains the same)

def main():
    """Enhanced main function with improved UI."""
    clear_terminal()
    console.print(HEADER_ART, style="bold blue")
    
    anime_data = fetch_anime_data()
    if not anime_data:
        return
    
    while True:
        console.print("\n")
        menu = create_menu(["List Anime", "Search", "Exit"], "Main Menu")
        console.print(menu)
        
        choice = Prompt.ask(
            "Select an option",
            choices=["1", "2", "3"],
            show_choices=False
        )
        
        if choice == "1":
            if anime_data:
                print("\nAnime List:")
                choices = [f"{item['text']}" for item in anime_data]
                questions = [
                    inquirer.List('selected_anime',
                                    message="Select an anime for episodes:",
                                    choices=choices,
                                    ),
                ]
                answers = inquirer.prompt(questions)
                if answers:
                    selected_anime_text = answers['selected_anime']
                    selected_anime = next((item for item in anime_data if item['text'] == selected_anime_text), None)
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
                print("\nNo anime data found.")
                input("Press Enter to continue...")
        elif choice == "2":
            search_anime(anime_data)
        elif choice == "3":
            console.print("[yellow]Goodbye![/yellow]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        display_error(f"An unexpected error occurred: {str(e)}")

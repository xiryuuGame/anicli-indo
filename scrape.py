import subprocess
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_anime_list(url):
    """
    Scrapes a list of anime titles and links from a given URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        None. Prints the extracted links and text to the terminal.
    """
    try:
        # Use curl to fetch the webpage content
        process = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
        html_content = process.stdout

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the anime list items
        anime_list_items = soup.select('#main > div.listpst > div > div.listttl > ul > li > a')

        anime_data = []
        for item in anime_list_items:
            link = item['href']
            text = item.get_text(strip=True)
            anime_data.append({"link": link, "text": text})

        print(json.dumps(anime_data, indent=4))

    except subprocess.CalledProcessError as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def scrape_video_link(url):
    """
    Scrapes the video link from a given episode URL using Playwright.

    Args:
        url (str): The URL of the episode page to scrape.

    Returns:
        str: The video link, or None if not found.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            video_element = page.query_selector("#oframeplayerjs > pjsdiv:nth-child(3) > video")
            if video_element:
                video_link = video_element.get_attribute("src")
                browser.close()
                print(json.dumps({"video_link": video_link}, indent=4))
                return video_link
            else:
                browser.close()
                print(json.dumps({"video_link": None}, indent=4))
                return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def scrape_episode_list(url):
    """
    Scrapes a list of episode titles and links from a given anime URL.

    Args:
        url (str): The URL of the anime page to scrape.

    Returns:
        None. Prints the extracted episode links and text to the terminal.
    """
    try:
        # Use curl to fetch the webpage content
        process = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
        html_content = process.stdout

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all the episode list items
        episode_list_items = soup.select('#infoarea > div > div.whites.lsteps.widget_senction > div.lstepsiode.listeps > ul > li > div.epsleft > span.lchx > a')

        episode_data = []
        for item in episode_list_items:
            link = item['href']
            text = item.get_text(strip=True)
            episode_data.append({"link": link, "text": text})

        print(json.dumps(episode_data, indent=4))

    except subprocess.CalledProcessError as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if len(sys.argv) > 2:
            episode_url = sys.argv[2]
            scrape_video_link(episode_url)
        else:
            scrape_episode_list(url)
    else:
        url = "https://samehadaku.click/daftar-anime-2/?list"
        scrape_anime_list(url)

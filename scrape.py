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
        anime_list_items = soup.select('ul > li > a.hodebgst')

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
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-popup-blocking",
                    "--block-new-web-contents",
                ],
            )
            page = browser.new_page()
            page.goto(url)
            page.evaluate("document.querySelectorAll('.box_item_ads_popup').forEach(el => el.remove());")
            page.click(".m480p")
            page.wait_for_timeout(500)
            page.wait_for_function("""
                () => {
                    const options = document.querySelectorAll('.m480p li a, .m720p li a');
                    for (const option of options) {
                        if (option.offsetParent !== null) {
                            return true;
                        }
                    }
                    return false;
                }
            """)

            preferred_link = None
            quality_options = page.query_selector_all(".m720p li a, .m480p li a")
            
            if quality_options:
                for option in quality_options:
                    if option.text_content() in ["desudesu", "desudesu2", "otakustream", "otakuplay", "desudrive", "ondesuhd", "ondesu3", "updesu", "playdesu"]:
                        if ".m720p" in option.locator.selector:
                            preferred_link = option
                            break
                        elif not preferred_link:
                            preferred_link = option
                if preferred_link:
                    preferred_link.click()
                    page.wait_for_timeout(500)
                    page.wait_for_selector("#oframeplayerjs > pjsdiv:nth-child(3) > video")
                    video_element = page.query_selector("#oframeplayerjs > pjsdiv:nth-child(3) > video")
                    if video_element:
                        video_link = video_element.get_attribute("src")
                        browser.close()
                        return {"video_link": video_link}
            browser.close()
            return {"video_link": None}
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
        episode_list_items = soup.select('#venkonten > div.venser > div:nth-child(8) > ul > li > span:nth-child(1) > a')

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
            video_data = scrape_video_link(episode_url)
            print(json.dumps(video_data, indent=4))
        else:
            scrape_episode_list(url)
    else:
        url = "https://otakudesu.cloud/anime-list/"
        scrape_anime_list(url)

import subprocess
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

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

        # Remove elements containing "iklan"
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup.find_all(text=lambda text: text and "iklan" in text.lower()):
            element.extract()

        # Parse the HTML content with BeautifulSoup
        # soup = BeautifulSoup(html_content, 'html.parser')

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

def scrape_video_link(url, user_agent):
    """
    Scrapes the video link from a given episode URL using Playwright.

    Args:
        url (str): The URL of the episode page to scrape.

    Returns:
        dict: A dictionary containing the video link or an error message.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=[f'--user-agent={user_agent}'])
            context = browser.new_context(user_agent=user_agent)  # New browser context to isolate session
            page = context.new_page()

            # Handle popup windows and close them automatically
            context.on("page", lambda popup: popup.close())

            # Navigate to the episode page
            page.goto(url)

            # Remove ads if they exist
            page.evaluate("""
                document.querySelectorAll('.box_item_ads_popup, .ads-container, .ads').forEach(el => el.remove());
            """)

            # Wait for the .m480p button and click it
            page.wait_for_selector(".m480p", timeout=5000)

            with page.expect_popup() as popup_info:
                page.click(".m480p")  # Trigger the click
            popup_info.value.close()  # Ensure popup is closed

            # Wait for the preferred quality links to appear
            page.wait_for_function("""
                () => document.querySelectorAll('.m480p li a, .m720p li a').length > 0
            """, timeout=5000)

            # Select preferred quality link
            quality_buttons = page.query_selector_all(".m720p li a")
            preferred_link = None
            
            videoLink = {"720": [], "480": []}  # Inisialisasi dictionary untuk menyimpan link video

            # Scrape untuk resolusi 720p
            quality_buttons_720 = page.query_selector_all(".m720p li a")
            for button in quality_buttons_720:
                text = button.text_content().strip().lower()
                if text in ["desudesu", "desudesu2", "otakustream", "otakuplay", "ondesuhd", "ondesu3", "updesu", "playdesu", "otakuwatchhd2", "otakuwatch2", "moedesuhd", "moedesu", "odesu", "odesu2", "desudrive"]:
                    button.click()
                    time.sleep(1.5)  # Tunggu proses load

                    iframe = page.wait_for_selector("#pembed > div > iframe", timeout=10000)
                    if iframe:
                        frame = iframe.content_frame()
                        if frame:
                            frame.wait_for_selector("video", timeout=10000)
                            video_element = frame.query_selector("video")
                            if video_element:
                                video_link = video_element.get_attribute("src")
                                if video_link:
                                    videoLink["720"].append(video_link)  # Tambahkan link video 720p
                                    page.click(".m480p")  # Trigger the click

            # Scrape untuk resolusi 480p
            quality_buttons_480 = page.query_selector_all(".m480p li a")
            for button in quality_buttons_480:
                text = button.text_content().strip().lower()
                if text in ["desudesu", "desudesu2", "otakustream", "otakuplay", "ondesuhd", "ondesu3", "updesu", "playdesu", "otakuwatchhd2", "otakuwatch2", "moedesuhd", "moedesu", "odesu", "odesu2", "desudrive"]:
                    button.click()
                    time.sleep(1.5)  # Tunggu proses load

                    iframe = page.wait_for_selector("#pembed > div > iframe", timeout=10000)
                    if iframe:
                        frame = iframe.content_frame()
                        if frame:
                            frame.wait_for_selector("video", timeout=10000)
                            video_element = frame.query_selector("video")
                            if video_element:
                                video_link = video_element.get_attribute("src")
                                if video_link:
                                    videoLink["480"].append(video_link)  # Tambahkan link video 480p
                                    page.click(".m480p")  # Trigger the click

            # Periksa hasil
            if not videoLink["720"] and not videoLink["480"]:
                return {"error": "Tidak ada video link yang ditemukan."}

            # Simpan ke file JSON
            with open("link.json", "w") as f:
                f.write(json.dumps(videoLink, indent=4))

            return videoLink

    except Exception as e:
        return {"error": str(e)}

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

        # Remove elements containing "iklan"
        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup.find_all(text=lambda text: text and "iklan" in text.lower()):
            element.extract()

        # Parse the HTML content with BeautifulSoup
        # soup = BeautifulSoup(html_content, 'html.parser')

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
            if len(sys.argv) > 3:
                user_agent = sys.argv[3]
                video_data = scrape_video_link(episode_url, user_agent)
                print(json.dumps(video_data, indent=4))
            else:
                print(json.dumps({"error": "User-agent is missing."}))
        else:
            scrape_episode_list(url)
    else:
        url = "https://otakudesu.cloud/anime-list/"
        scrape_anime_list(url)

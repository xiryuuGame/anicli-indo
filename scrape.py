import subprocess
from bs4 import BeautifulSoup

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

        # Extract and print the link and text for each item
        for item in anime_list_items:
            link = item['href']
            text = item.get_text(strip=True)
            print(f"Link: {link}, Text: {text}")

    except subprocess.CalledProcessError as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    url = "https://samehadaku.click/daftar-anime-2/?list"
    scrape_anime_list(url)

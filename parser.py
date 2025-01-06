import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_level1_links(base_url, section_class):
    """
    Extracts Level 1 links from the specified section of the given base URL.

    :param base_url: URL of the webpage to scrape for Level 1 links.
    :param section_class: Class name of the section containing the links.
    :return: List of Level 1 links (absolute URLs).
    """
    logging.info(f"Fetching Level 1 links from {base_url}...")
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        section = soup.find('td', class_=section_class)
        if section:
            links = section.find_all('a')
            level1_links = [urljoin(base_url, link.get('href')) for link in links if link.get('href')]
            logging.info(f"Found {len(level1_links)} Level 1 links.")
            return level1_links
        else:
            logging.warning(f"No section with class '{section_class}' found.")
            return []
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {base_url}: {e}")
        return []

def extract_links_from_page(url, link_selector):
    """
    Extracts links from a given URL based on the specified CSS selector.

    :param url: URL of the webpage to scrape.
    :param link_selector: CSS selector for the links to extract.
    :return: List of links extracted from the page.
    """
    logging.info(f"Extracting links from {url} using selector '{link_selector}'...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rows with the class "text"
        rows = soup.find_all('tr', class_='text')
        links = []
        for row in rows:
            td_elements = row.find_all('td')
            if len(td_elements) >= 4:  # Ensure there are enough <td> elements
                link_td = td_elements[3]  # Links appear in the 4th <td> (index 3)
                link_tags = link_td.find_all('a')
                for tag in link_tags:
                    href = tag.get('href')
                    if href:
                        links.append(urljoin(url, href))  # Ensure the link is absolute

        logging.info(f"Found {len(links)} links on {url}.")
        return links
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return []


def save_links_to_file(links, filename):
    """
    Saves a list of links to a file.

    :param links: List of links to save.
    :param filename: Name of the file to save the links.
    """
    try:
        with open(filename, "w") as f:

            filtered_links = [link for link in links if not link.endswith('#en')] #filters links that contain #en

            for link in filtered_links:
                f.write(link + "\n")
        logging.info(f"Saved {len(links)} links to {filename}.")
    except IOError as e:
        logging.error(f"Failed to save links to {filename}: {e}")

def main():
    # Configuration
    level1_base_url = "https://histodb11.usz.ch/pages/liste_praep_organ.html"
    section_class = "subtitel de"
    link_selector = "table.tcontent tr.text.de td:nth-child(2)"
    output_file = "all_links.txt"

    # Step 1: Get Level 1 links
    level1_links = get_level1_links(level1_base_url, section_class)

    # Step 2: Extract secondary links from each Level 1 page
    all_links = []
    for idx, level1_link in enumerate(level1_links, start=1):
        logging.info(f"Processing Level 1 link {idx}/{len(level1_links)}: {level1_link}")
        secondary_links = extract_links_from_page(level1_link, link_selector)
        all_links.extend(secondary_links)

    # Step 3: Save all collected links to a file
    save_links_to_file(all_links, output_file)

if __name__ == "__main__":
    main()

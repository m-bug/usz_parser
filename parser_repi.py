import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def extract_filtered_links(url, pattern):
    try:
        # call website
        response = requests.get(url)
        response.raise_for_status()

        # parse content
        soup = BeautifulSoup(response.text, 'html.parser')

        # collect and filter links
        links = []
        for a_tag in soup.find_all('a', href=True):
            absolute_link = urljoin(url, a_tag['href'])
            # filter by pattern
            if re.search(pattern, absolute_link):
                links.append(absolute_link)

        return links

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
        return []

# website
url = "https://histodb11.usz.ch/pages/rep_inhalt.html"

# search pattern: link with "r_"
pattern = r"/r_"
filtered_links = extract_filtered_links(url, pattern)

# Open the file in write mode to empty it before writing
with open("repi_links.txt", "w") as f:
    for link in filtered_links:
        f.write(link+"\n")

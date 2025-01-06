import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def extract_filtered_links(url, pattern):
    try:
        # call webside
        response = requests.get(url)
        response.raise_for_status()

        # pars content
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

# webside
url = "https://histodb11.usz.ch/pages/rep_inhalt.html"

# pattern: link with "r_" or "ra_"
pattern = r"/(r_|ra_)" 
filtered_links = extract_filtered_links(url, pattern)


with open("repi_links.txt", "a") as f:
    for link in filtered_links:
        f.write(link+"\n")

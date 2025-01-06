import random
import webbrowser
from urllib.parse import urlparse

def extract_slide_name_from_url(url):
    """
    Extracts the slide name from the given URL.
    Example URL: https://histodb11.usz.ch/pages/R_IV_1.html -> returns "IV_1.html"
    """
    answer_url = urlparse(url)
    slide_name = answer_url.path.split('/')[-1].replace('r_', '')
    return slide_name

def build_answer_url(slide_name):
    """
    Builds the result URL using the slide name.
    """
    BASE_URL = "https://histodb11.usz.ch/pages/s_"
    return BASE_URL + slide_name

def main():
    # Read all links from the file
    with open('repi_links.txt', 'r') as file:
        links = file.readlines()

    # Choose a random link
    random_link = random.choice(links).strip()

    # Extract slide name from the page URL
    slide_name = extract_slide_name_from_url(random_link)

    # Build the answer URL
    answer_url = build_answer_url(slide_name)

    print(f"Opening image from URL: {answer_url}")

    # Open the random link and answer url in the default web browser
    webbrowser.open(answer_url, new=2)
    webbrowser.open(random_link, new=2)  # 'new=2' opens in a new tab, if possible

if __name__ == "__main__":
    main()

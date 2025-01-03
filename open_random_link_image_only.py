import random
import webbrowser
from urllib.parse import urlparse

def extract_image_name_from_url(url):
    """
    Extracts the image name from the given URL.
    Example URL: https://histodb11.usz.ch/pages/A_IV_1.html -> returns "A_IV_1"
    """
    parsed_url = urlparse(url)
    image_name = parsed_url.path.split('/')[-1].replace('.html', '')
    return image_name

def build_image_url(image_name):
    """
    Builds the image-only URL using the image name.
    """
    BASE_URL = "https://histodb11.usz.ch/olat/img_zif.php?img="
    return BASE_URL + image_name

def main():
    # Read all links from the file
    with open('all_links.txt', 'r') as file:
        links = file.readlines()

    # Choose a random link
    random_link = random.choice(links).strip()

    # Extract image name from the page URL
    image_name = extract_image_name_from_url(random_link)

    # Build the image-only URL
    image_url = build_image_url(image_name)

    print(f"Opening image from URL: {image_url}")

    # Open the image URL in the default web browser
    webbrowser.open(image_url, new=2)  # 'new=2' opens in a new tab, if possible

if __name__ == "__main__":
    main()

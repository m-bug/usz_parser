import random
import requests
from PIL import Image
from io import BytesIO

def fetch_image_from_url(url):
    """
    Fetches an image from the given URL and returns a PIL Image object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except requests.RequestException as e:
        print(f"Error fetching image from {url}: {e}")
        return None

def display_image(img):
    """
    Displays the given PIL Image object.
    """
    if img:
        img.show()
    else:
        print("No image to display.")

def main():
    # Read all links from the file
    with open('all_links.txt', 'r') as file:
        links = file.readlines()

    # Choose a random link
    random_link = random.choice(links).strip()

    # Fetch and display the image
    img = fetch_image_from_url(random_link)
    display_image(img)

if __name__ == "__main__":
    main()

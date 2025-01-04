import random
import webbrowser
from urllib.parse import urlparse
import keyboard  # To detect key presses

def extract_image_name_from_url(url):
    """
    Extracts the image name from the given URL.
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

def load_links(file_path):
    """
    Loads all links from a file.
    """
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def save_visited_link(link, visited_file):
    """
    Appends a visited link to the visited_links.txt file.
    """
    with open(visited_file, 'a') as file:
        file.write(link + '\n')

def load_visited_links(visited_file):
    """
    Loads all visited links from the visited_links.txt file.
    """
    try:
        with open(visited_file, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def browse_next_link():
    """
    Selects the next random link and opens it in the browser.
    """
    # File paths
    all_links_file = 'all_links.txt'
    visited_links_file = 'visited_links.txt'

    # Load links
    all_links = load_links(all_links_file)
    visited_links = load_visited_links(visited_links_file)

    # Get unvisited links
    unvisited_links = [link for link in all_links if link not in visited_links]

    # Reset if all links are visited
    if not unvisited_links:
        print("All links have been visited. Resetting...")
        unvisited_links = all_links
        with open(visited_links_file, 'w') as file:
            file.truncate(0)  # Clear the file

    # Choose a random link from unvisited links
    random_link = random.choice(unvisited_links)

    # Extract image name and build image URL
    image_name = extract_image_name_from_url(random_link)
    image_url = build_image_url(image_name)

    print(f"Opening image from URL: {image_url}")

    # Open the image URL in the default web browser
    webbrowser.open(image_url, new=2)  # 'new=2' opens in a new tab, if possible

    # Save the link to visited_links.txt
    save_visited_link(random_link, visited_links_file)

def main():
    print("Press 'Space' to browse the next random link. Press 'Ctrl+C' to exit.")
    while True:
        # Wait for the Space key to be pressed
        keyboard.wait('space')
        browse_next_link()

if __name__ == "__main__":
    main()


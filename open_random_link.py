import webbrowser
import random

def open_random_link_from_file(filename):
    """
    Opens a random link from the provided file in the default web browser.

    :param filename: The path to the file containing the links.
    """
    try:
        with open(filename, 'r') as file:
            links = file.readlines()
        
        if links:
            # Strip any extra whitespace or newlines from the links
            links = [link.strip() for link in links]
            
            # Select a random link
            selected_link = random.choice(links)
            print(f"Opening: {selected_link}")
            
            # Open the link in the default web browser
            webbrowser.open(selected_link)
        else:
            print("No links found in the file.")
    
    except IOError as e:
        print(f"Failed to read the file: {e}")

if __name__ == "__main__":
    # Specify the path to your all_links.txt file
    file_path = "all_links.txt"
    open_random_link_from_file(file_path)

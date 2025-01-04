import random
import os
from urllib.parse import urlparse
import webbrowser
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


def generate_html(image_url, solution_text):
    """
    Generates an HTML file with an iframe and additional solution text.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Study Tool</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}
            iframe {{
                width: 90%;
                height: 70vh;
                border: 2px solid #ccc;
                margin-top: 20px;
            }}
            .solution {{
                margin-top: 20px;
                padding: 10px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                max-width: 90%;
            }}
            .solution.hidden {{
                display: none;
            }}
        </style>
    </head>
    <body>
        <h1>Study Tool</h1>
        <iframe src="{image_url}" frameborder="0"></iframe>
        <div class="solution hidden" id="solution">
            <h2>Solution</h2>
            <p>{solution_text}</p>
        </div>
        <button onclick="toggleSolution()">Show Solution</button>
        <script>
            function toggleSolution() {{
                const solutionDiv = document.getElementById('solution');
                if (solutionDiv.classList.contains('hidden')) {{
                    solutionDiv.classList.remove('hidden');
                }} else {{
                    solutionDiv.classList.add('hidden');
                }}
            }}
        </script>
    </body>
    </html>
    """
    html_file = "study_tool.html"
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    return html_file


def browse_next_link():
    """
    Selects the next random link, generates an HTML file, and opens it in the browser.
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

    # Generate a custom HTML file
    solution_text = f"Solution for {image_name}"  # Customize as needed
    html_file = generate_html(image_url, solution_text)

    print(f"Opening study tool for image: {image_name}")

    # Open the generated HTML file in the default browser
    webbrowser.open(f"file://{os.path.abspath(html_file)}", new=2)  # 'new=2' opens in a new tab, if possible

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

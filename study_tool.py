import random
import os
from urllib.parse import urlparse
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

# File paths
ALL_LINKS_FILE = 'all_links.txt'
ALL_REPI_LINKS_FILE = 'repi_links.txt'
VISITED_LINKS_FILE = 'visited_links.txt'
VISITED_REPI_LINKS_FILE = 'visited_repi_links.txt'
HTML_FILE = 'study_tool.html'
BASE_URL = "https://histodb11.usz.ch/olat/img_zif.php?img="
BASE_REPI_URL = "https://histodb11.usz.ch/pages/s_"


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
    return BASE_URL + image_name

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
    return BASE_REPI_URL + slide_name


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


def generate_html(random_image_url, original_link, random_repi_link, answer_url):
    """
    Generates an HTML file with two buttons and a refresh option.
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
                padding: 20px;
                text-align: center;
                background-color: #f4f7f6;
            }}
            h1 {{
                color: #333;
                font-size: 2rem;
                margin-bottom: 20px;
            }}
            button {{
                margin: 20px;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
            .message {{
                font-size: 18px;
                color: green;
                margin-top: 20px;
            }}
            .loading {{
                font-size: 18px;
                color: #888;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Study Tool: Guess the Image</h1>
        <p>Click a button below to view the image and the solution.</p>
        <div>
            <button onclick="window.open('{random_image_url}', '_blank')">View Random Image</button>
            <button onclick="window.open('{original_link}', '_blank')">View Solution</button>
        </div>
        <button onclick="refreshPage()">Get Another Random Link</button>
        <div id="loading" class="loading"></div>
        <div id="message" class="message" style="display: none;">Random Link Updated!</div>

        <h1>Study Tool: Guess the Repi Image</h1>
        <p>Click a button below to view the image and the solution.</p>
        <div>
            <button onclick="window.open('{random_repi_link}', '_blank')">View Random Repi Image</button>
            <button onclick="window.open('{answer_url}', '_blank')">View Solution</button>
        </div>
        <button onclick="refreshPage()">Get Another Random Repi Link</button>
        <div id="loading" class="loading"></div>
        <div id="message" class="message" style="display: none;">Random Link Updated!</div>

        <script>
            function refreshPage() {{
                document.getElementById('loading').innerText = 'Loading...';
                document.getElementById('message').style.display = 'none';

                fetch('/refresh')
                    .then(response => response.text())
                    .then(data => {{
                        document.body.innerHTML = data;
                    }});
            }}
        </script>
    </body>
    </html>
    """
    with open(HTML_FILE, 'w', encoding='utf-8') as file:
        file.write(html_content)


def browse_next_link():
    """
    Selects the next random link, generates an HTML file.
    """
    # Load links
    all_links = load_links(ALL_LINKS_FILE)
    visited_links = load_visited_links(VISITED_LINKS_FILE)
    all_repi_links = load_links(ALL_REPI_LINKS_FILE)
    visited_repi_links = load_visited_links(VISITED_REPI_LINKS_FILE)

    # Get unvisited links
    unvisited_links = [link for link in all_links if link not in visited_links]
    unvisited_repi_links = [link for link in all_repi_links if link not in visited_repi_links]

    # Reset if all links are visited
    if not unvisited_links:
        print("All links have been visited. Resetting...")
        unvisited_links = all_links
        with open(VISITED_LINKS_FILE, 'w') as file:
            file.truncate(0)  # Clear the file
    if not unvisited_repi_links:
        print("All repi links have been visited. Resetting...")
        unvisited_repi_links = all_repi_links
        with open(VISITED_REPI_LINKS_FILE, 'w') as file:
            file.truncate(0)  # Clear the file

    # Choose a random link from unvisited links
    random_link = random.choice(unvisited_links)
    random_repi_link = random.choice(unvisited_repi_links)

    # Extract image name and build image-only URL
    image_name = extract_image_name_from_url(random_link)
    random_image_url = build_image_url(image_name)

    # Extract slide name from the page URL and Build the answer URL
    slide_name = extract_slide_name_from_url(random_repi_link)
    answer_url = build_answer_url(slide_name)

    # Generate a custom HTML file
    generate_html(random_image_url, random_link, random_repi_link, answer_url)

    print(f"Generated HTML for image: {image_name}")

    # Save the link to visited_links.txt
    save_visited_link(random_link, VISITED_LINKS_FILE)
    save_visited_link(random_repi_link, VISITED_REPI_LINKS_FILE)


def start_server():
    """
    Starts an HTTP server to serve the HTML file.
    """
    class CustomHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/refresh":
                browse_next_link()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(HTML_FILE, 'r', encoding='utf-8') as file:
                    self.wfile.write(file.read().encode('utf-8'))
            else:
                super().do_GET()

    server = HTTPServer(('localhost', 8000), CustomHandler)
    print("Starting server at http://localhost:8000")
    server.serve_forever()


def main():
    # Generate the first random HTML
    browse_next_link()

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Open the HTML file in the browser
    webbrowser.open("http://localhost:8000/study_tool.html", new=2)  # Open in a new tab

    # Wait for user input
    print("Press 'Ctrl+C' to exit.")
    try:
        while True:
            pass  # Keep script running
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()

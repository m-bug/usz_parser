import random
import os
from urllib.parse import urlparse
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import os
import sys
import re

def get_base_path():
    """
    Get the base path where the script or executable is running.
    """
    if getattr(sys, 'frozen', False):  # Check if the script is running as a frozen executable
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# File paths
BASE_PATH = get_base_path()

ALL_LINKS_FILE = os.path.join(BASE_PATH, 'all_links.txt')
ALL_REPI_LINKS_FILE = os.path.join(BASE_PATH, 'repi_links.txt')
VISITED_LINKS_FILE = os.path.join(BASE_PATH, 'visited_links.txt')
VISITED_REPI_LINKS_FILE = os.path.join(BASE_PATH, 'visited_repi_links.txt')
HTML_FILE = os.path.join(BASE_PATH, 'study_tool.html')

# some URL's
BASE_URL = "https://histodb11.usz.ch/olat/img_zif.php?img="
BASE_REPI_URL = "https://histodb11.usz.ch/pages/s_"


def extract_image_name_from_url(url):
    """
    Extracts the image name from the given URL. Handles exceptions for specific cases.
    """
    # Mapping of exceptions
    exception_map = {
        "s_vii_30": "np_i_1",
        "s_vii_31": "np_i_2",
        "s_vii_32": "np_i_3",
        "s_vii_33": "np_ii_1",
        "s_vii_34": "np_ii_2",
        "s_vii_35a": "np_ii_3a",
        "s_vii_35b": "np_ii_3b",
        "s_vii_35c": "np_ii_3c",
        "s_vii_36": "np_ii_4",
        "s_vii_37": "np_ii_5",
        "s_vii_38": "np_ii_6",
        "s_vii_39": "np_iii_1",
        "s_vii_40": "np_iii_2",
        "s_vii_41": "np_iii_3",
        "s_vii_42": "np_iii_4",
        "s_vii_43": "np_iii_5",
        "s_vii_44": "np_iii_6",
    }

    # Extract the image name as per the general rule
    parsed_url = urlparse(url)
    image_name = parsed_url.path.split('/')[-1].replace('.html', '')

    print(image_name)

    # Check if the image name has an exception
    return exception_map.get(image_name, image_name)


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
    sanitized_link = re.sub(r'(\d)[a-zA-Z]+(?=\.html)', r'\1', slide_name)
    print(sanitized_link)
    return sanitized_link

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


def refresh_image_section():
    """
    Refreshes the random image section.
    """
    all_links = load_links(ALL_LINKS_FILE)
    visited_links = load_visited_links(VISITED_LINKS_FILE)
    unvisited_links = [link for link in all_links if link not in visited_links]

    if not unvisited_links:
        print("Resetting image links...")
        unvisited_links = all_links
        with open(VISITED_LINKS_FILE, 'w') as file:
            file.truncate(0)

    random_link = random.choice(unvisited_links)
    
    image_name = extract_image_name_from_url(random_link)
    random_image_url = build_image_url(image_name)
    print(random_image_url)
    print(random_link)
    
    random_link = random_link.replace('/s_h', '/h')
    random_link = random_link.replace('/s_s', '/s')
    
    
    save_visited_link(random_link, VISITED_LINKS_FILE)

    # Update the HTML
    generate_html(random_image_url, random_link, None, None)


def refresh_repi_section():
    """
    Refreshes the random repi section.
    """
    all_repi_links = load_links(ALL_REPI_LINKS_FILE)
    visited_repi_links = load_visited_links(VISITED_REPI_LINKS_FILE)
    unvisited_repi_links = [link for link in all_repi_links if link not in visited_repi_links]

    if not unvisited_repi_links:
        print("Resetting repi links...")
        unvisited_repi_links = all_repi_links
        with open(VISITED_REPI_LINKS_FILE, 'w') as file:
            file.truncate(0)

    random_repi_link = random.choice(unvisited_repi_links)
    slide_name = extract_slide_name_from_url(random_repi_link)
    answer_url = build_answer_url(slide_name)

    save_visited_link(random_repi_link, VISITED_REPI_LINKS_FILE)

    # Update the HTML
    generate_html(None, None, random_repi_link, answer_url)


def generate_html(image_section_url, solution_section_url, repi_image_url, repi_solution_url):
    """
    Generates an HTML file with independent sections for each link type.
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
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                text-align: center;
                background-color: #f4f7f6;
            }}

            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 20px;
            }}

            .card {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 100%;
            }}

            .card h1 {{
                color: #333;
                font-size: 1.5rem;
                margin-bottom: 10px;
            }}

            .card p {{
                color: #666;
                font-size: 1rem;
                margin-bottom: 20px;
            }}

            .button-group {{
                display: flex;
                justify-content: space-around;
                gap: 10px;
                flex-wrap: wrap;
            }}

            button {{
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
            }}

            button:hover {{
                background-color: #0056b3;
                transform: translateY(-2px);
            }}

            button i {{
                font-size: 1.2rem;
            }}

            @media (max-width: 600px) {{
                .card {{
                    width: 90%;
                }}

                button {{
                    flex: 1 1 auto;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <h1>Study Tool: Guess the Image</h1>
                <p>Click a button below to view the image and the solution.</p>
                <div class="button-group">
                    <button onclick="window.open('{image_section_url}', '_blank')">
                        <i>📷</i> View Random Image
                    </button>
                    <button onclick="window.open('{solution_section_url}', '_blank')">
                        <i>🔍</i> View Solution
                    </button>
                    <button onclick="refreshImage()">
                        <i>🔄</i> Refresh Image
                    </button>
                </div>
            </div>

            <div class="card">
                <h1>Study Tool: Guess the Repi Image</h1>
                <p>Click a button below to view the image and the solution.</p>
                <div class="button-group">
                    <button id="repiImageButton" onclick="window.open('{repi_image_url}', '_blank')">
                        <i>📷</i> View Random Repi Image
                    </button>
                    <button id="repiSolutionButton" onclick="window.open('{repi_solution_url}', '_blank')">
                        <i>🔍</i> View Solution
                    </button>
                    <button onclick="refreshRepi()">
                        <i>🔄</i> Refresh Repi
                    </button>
                </div>
            </div>
        </div>
        <div id="loading" class="loading" style="display: none;">Loading...</div>
        <div id="message" class="message" style="display: none;">Random Link Updated!</div>

        <script>
    function refreshImage() {{
        fetch('/refresh_image')
            .then(response => response.json())
            .then(data => {{
                // Update the button or display for the random image link
                const imageButton = document.querySelector('.button-group button:first-child');
                const solutionButton = document.querySelector('.button-group button:nth-child(2)');

                // Check if the image button exists and update its onclick link
                if (imageButton) {{
                    imageButton.setAttribute('onclick', `window.open('${{data.image_url}}', '_blank')`);
                }}

                // Check if the solution button exists and update its onclick link
                if (solutionButton) {{
                    solutionButton.setAttribute('onclick', `window.open('${{data.solution_url}}', '_blank')`);
                }}
            }})
            .catch(() => {{
                alert('Failed to refresh image!');
            }});
    }}


    function refreshRepi() {{
        fetch('/refresh_repi')
            .then(response => response.json())
            .then(data => {{
                const repiImageButton = document.getElementById('repiImageButton');
                const repiSolutionButton = document.getElementById('repiSolutionButton');
                if (repiImageButton) {{
                    repiImageButton.setAttribute('onclick', `window.open('${{data.repi_url}}', '_blank')`);
                }}
                if (repiSolutionButton) {{
                    repiSolutionButton.setAttribute('onclick', `window.open('${{data.solution_url}}', '_blank')`);
                }}
            }})
            .catch(() => {{
                alert('Failed to refresh repi!');
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
            if self.path == "/refresh_image":
                refresh_image_section()
                all_links = load_links(ALL_LINKS_FILE)
                visited_links = load_visited_links(VISITED_LINKS_FILE)
                unvisited_links = [link for link in all_links if link not in visited_links]

                if not unvisited_links:
                    unvisited_links = all_links

                random_link = random.choice(unvisited_links)
                image_name = extract_image_name_from_url(random_link)
                random_image_url = build_image_url(image_name)

                # Assuming solution URL is linked to the same random link
                # slide_name = extract_slide_name_from_url(random_link)
                solution_url = random_link

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"image_url": "{random_image_url}", "solution_url": "{solution_url}"}}'.encode('utf-8'))

            elif self.path == "/refresh_repi":
                refresh_repi_section()
                all_repi_links = load_links(ALL_REPI_LINKS_FILE)
                visited_repi_links = load_visited_links(VISITED_REPI_LINKS_FILE)
                unvisited_repi_links = [link for link in all_repi_links if link not in visited_repi_links]

                if not unvisited_repi_links:
                    unvisited_repi_links = all_repi_links

                random_repi_link = random.choice(unvisited_repi_links)
                slide_name = extract_slide_name_from_url(random_repi_link)
                repi_solution_url = build_answer_url(slide_name)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(f'{{"repi_url": "{random_repi_link}", "solution_url": "{repi_solution_url}"}}'.encode('utf-8'))

            elif self.path == "/study_tool.html":
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

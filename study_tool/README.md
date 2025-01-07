# Study Tool

This tool helps you study by showing random links to images and solutions. It creates a simple HTML interface for interaction.


## File Structure

Make sure the following files are in the same directory:

```
study_tool
│
├── all_links.txt
├── repi_links.txt
├── visited_links.txt        # Created at runtime
├── visited_repi_links.txt   # Created at runtime
├── study_tool.html          # Created at runtime
├── study_tool.app           # Generated executable
├── README.md
```

## Building the Application   
Following instructions demonstrate how to build the application for different platforms.

### Prerequisites

1. Install **Python 3.8+** from [python.org](https://www.python.org/).
2. Install dependencies:
   ```bash
   pip install pyinstaller requests beautifulsoup4
   ```

### For Windows (.exe)
1. Open a terminal and navigate to the folder:

```bash
cd path/to/study_tool
```

2. Create the executable:

```bash
pyinstaller --onefile study_tool.py
```

3. The `.exe` file will be located in `dist/study_tool.exe`.

4. Build a folder, which consists of following files:

```
study_tool
│
├── all_links.txt
├── repi_links.txt
├── visited_links.txt        
├── visited_repi_links.txt   
├── study_tool.html          
├── study_tool.app           
├── README.md
```

5. Share this folder as an archive (.zip file).

### For macOS (.app)
1. Open a terminal and navigate to the folder:

```bash
cd path/to/study_tool
```

2. Create the executable:

```bash
pyinstaller --onefile --windowed study_tool.py
```

3. The `.app` file will be located in `dist/study_tool.app`.

4. Build a folder, which consists of following files:

```
study_tool
│
├── all_links.txt
├── repi_links.txt
├── visited_links.txt
├── visited_repi_links.txt
├── study_tool.html
├── study_tool.app [GENERATED]
├── README.md
```

5. Share this folder as an archive (.zip file)

## Running the Application   
Following instructions demonstrate how to run the application for different platforms.

1. Place at least the following files in the same directory as the executable:

```
study_tool
│
├── all_links.txt
├── repi_links.txt
```

2. Launch the application:

* On Windows: Double-click study_tool.exe.
* On macOS: Double-click study_tool.app.
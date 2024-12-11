# Web Crawl Application

A Python-based web crawler that uses `BeautifulSoup` (bs4) for parsing and extracting data from websites. This application is ideal for small-scale data scraping and research projects, enabling efficient data collection and export.

## Features

- **HTML Parsing**: Utilizes `BeautifulSoup` to parse and extract specific data from web pages.
- **Customizable Targeting**: Define target URLs and patterns to scrape specific sections of a website.
- **Export Options**: Save scraped data in formats like CSV or JSON for easy analysis.
- **Error Handling**: Includes basic mechanisms to handle missing pages and connection issues.

## Prerequisites

Ensure you have Python 3.8 or higher installed.

Install the required libraries:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/web-crawl-application.git
   cd web-crawl-application
   ```

2. Define the URLs and tags to scrape in the `config` section of the script.

3. Run the application:

   ```bash
   python web_crawler.py
   ```

4. Exported data will be saved in the `output` directory as a CSV or JSON file.

## Example

Scrape all `<h1>` tags from a website:

```python
from bs4 import BeautifulSoup
import requests

url = "https://example.com"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    headers = [h1.text for h1 in soup.find_all("h1")]
    print(headers)
```

## Contributions

Contributions are welcome! Feel free to fork this repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/en/latest/)

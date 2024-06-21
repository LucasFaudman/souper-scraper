# SouperScraper

> A simple web scraper base that combines BeautifulSoup and Selenium to scrape dynamic websites.


## Setup
1. Install with pip
```bash
pip install souperscraper
```

2. Download the appropriate [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your Chrome version using [getchromedriver.py](https://github.com/LucasFaudman/souper-scraper/blob/main/src/souperscraper/getchromedriver.py) (command below) or manually from the [ChromeDriver website](https://sites.google.com/a/chromium.org/chromedriver/downloads).
> To find your Chrome version, go to [`chrome://settings/help`](chrome://settings/help) in your browser.
```bash
getchromedriver
```

3. Create a new SouperScaper object using the path to your ChromeDriver
```python
from souperscraper import SouperScraper

scraper = SouperScraper('/path/to/your/chromedriver')
```

4. Start scraping using BeautifulSoup and/or Selenium methods
```python
scraper.goto('https://github.com/LucasFaudman')

# Use BeautifulSoup to search for and extract content
# by accessing the scraper's 'soup' attribute
# or with the 'soup_find' / 'soup_find_all' methods
repos = scraper.soup.find_all('span', class_='repo')
for repo in repos:
    repo_name = repo.text
    print(repo_name)

# Use Selenium to interact with the page such as clicking buttons
# or filling out forms by accessing the scraper's
# find_element_by_* / find_elements_by_* / wait_for_* methods
repos_tab = scraper.find_element_by_css_selector("a[data-tab-item='repositories']")
repos_tab.click()

search_input = scraper.wait_for_visibility_of_element_located_by_id('your-repos-filter')
search_input.send_keys('souper-scraper')
search_input.submit()
```

## BeautifulSoup Reference
- [Quick Start](https://beautiful-soup-4.readthedocs.io/en/latest/#quick-start)
- [Types of Objects](https://beautiful-soup-4.readthedocs.io/en/latest/#kinds-of-objects)
- [The BeautifulSoup object](https://beautiful-soup-4.readthedocs.io/en/latest/#beautifulsoup)
- [Navigating the HTML tree](https://beautiful-soup-4.readthedocs.io/en/latest/#navigating-the-tree)
- [Searching for HTML Elements](https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree)
- [Modifying the tree](https://beautiful-soup-4.readthedocs.io/en/latest/#modifying-the-tree)

## Selenium Reference
- [Quick Start](https://selenium-python.readthedocs.io/getting-started.html)
- [Navigating the Web](https://selenium-python.readthedocs.io/getting-started.html#)
- [Locating HTML Elements](https://selenium-python.readthedocs.io/locating-elements.html)
- [Interacting with HTML elements on the page](https://selenium-python.readthedocs.io/navigating.html#interacting-with-the-page)
- [Filling in Forms](https://selenium-python.readthedocs.io/navigating.html#filling-in-forms)
- [Waiting (for page to load, element to be visible, etc)](https://selenium-python.readthedocs.io/waits.html)
- [Full Webdriver API Reference](https://selenium-python.readthedocs.io/api.html)

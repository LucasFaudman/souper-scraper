# SouperScraper

> A simple web scraper base that combines BeautifulSoup and Selenium to scrape dynamic websites.


## Setup
1. Install the required packages
```bash
pip3 install selenium beautifulsoup4 requests
```

2. Download the appropriate [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your Chrome version using [get_chrome_driver.py](https://github.com/LucasFaudman/souper-scraper/blob/main/src/souperscraper/getchromedriver.py)
```bash
python3 souper-scraper/src/souperscraper/get_chrome_driver.py
```

3. Create a new SouperScaper object using path to your ChromeDriver
```python
from souper_scraper import SouperScraper

scraper = SouperScraper(executable_path='/path/to/your/chromedriver')
```

4. Start scraping using BeautifulSoup and/or Selenium methods
```python
scraper.goto('https://github.com/LucasFaudman')

# Use BeautifulSoup to search for and extract content by accessing the scraper's 'soup' attribute or with the 'soup_find' / 'soup_find_all' methods
repos = scraper.soup.find_all('span', class_='repo')
for repo in repos:
    repo_name = repo.text
    print(repo_name)

# Use Selenium to interact with the page such as clicking buttons or filling out forms by accessing the scraper's find_element_by_* / find_elements_by_* / wait_for_* methods
repos_tab = scraper.find_element_by_css_selector("a[data-tab-item='repositories']")
repos_tab.click()

search_input = scraper.wait_for_visibility_of_element_located_by_id('your-repos-filter')
search_input.send_keys('souper-scraper')
search_input.submit()
```

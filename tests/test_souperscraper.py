import pytest
from souperscraper import SouperScraper, WebDriverException
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from bs4 import Tag
from pathlib import Path
from time import time

DEFAULT_CHROMEDRIVER_PATH = list(filter(Path.is_file, (Path.home() / ".chromedriver").rglob("chromedriver")))[0]

scraper = SouperScraper(executable_path=DEFAULT_CHROMEDRIVER_PATH, save_dynamic_methods=False)


@pytest.fixture
def selenium_test_html_static(tmpdir):
    test_html = """
<html>
<body>
<style>
.information {
  background-color: white;
  color: black;
  padding: 10px;
}
</style>
<h2>Contact Selenium</h2>

<form action="/action_page.php">
  <input type="radio" name="gender" value="m" />Male &nbsp;
  <input type="radio" name="gender" value="f" />Female <br>
  <br>
  <label for="fname">First name:</label><br>
  <input class="information" type="text" id="fname" name="fname" value="Jane"><br><br>
  <label for="lname">Last name:</label><br>
  <input class="information" type="text" id="lname" name="lname" value="Doe"><br><br>
  <label for="newsletter">Newsletter:</label>
  <input type="checkbox" name="newsletter" value="1" /><br><br>
  <input type="submit" value="Submit">
</form>

<p>To know more about Selenium, visit the official page
<a href ="https://www.selenium.dev">Selenium Official Page</a>
</p>
<div id="vegetableSnippet">
    <ol id="vegetables">
      <li class="potatoes">...</li>
      <li class="onions">...</li>
      <li class="tomatoes"><span>Tomato is a Vegetable</span>...</li>
    </ol>
    <ul id="fruits">
      <li class="bananas">...</li>
      <li class="apples">...</li>
      <li class="tomatoes"><span>Tomato is a Fruit</span>...</li>
    </ul>
</div>
</body>
</html>
"""
    # Write the HTML content to a file in the temporary directory
    html_file_path = tmpdir.join("test_page.html")
    html_file_path.write(test_html)

    # Return the URL of the HTML page
    return f"file://{html_file_path}"


@pytest.fixture
def selenium_test_html_dynamic(tmpdir):
    test_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Contact Selenium</title>
</head>
<body>
<style>
.information {
  background-color: white;
  color: black;
  padding: 10px;
}
</style>
<h2>Contact Selenium</h2>

<div id="formContainer"></div>

<p>To know more about Selenium, visit the official page
<a href ="https://www.selenium.dev">Selenium Official Page</a>
</p>

<script>
setTimeout(function() {
  var formContainer = document.getElementById('formContainer');
  var formHTML = `
    <form action="/action_page.php">
      <input type="radio" name="gender" value="m" />Male &nbsp;
      <input type="radio" name="gender" value="f" />Female <br>
      <br>
      <label for="fname">First name:</label><br>
      <input class="information" type="text" id="fname" name="fname" value="Jane"><br><br>
      <label for="lname">Last name:</label><br>
      <input class="information" type="text" id="lname" name="lname" value="Doe"><br><br>
      <label for="newsletter">Newsletter:</label>
      <input type="checkbox" name="newsletter" value="1" /><br><br>
      <input type="submit" value="Submit">
    </form>
  `;
  formContainer.innerHTML = formHTML;
}, 5000);
</script>

<div id="vegetableSnippet"></div>
<script>
// Function to display the snippet
function displaySnippet() {
  var snippetHTML = `
    <ol id="vegetables">
      <li class="potatoes">...</li>
      <li class="onions">...</li>
      <li class="tomatoes"><span>Tomato is a Vegetable</span>...</li>
    </ol>
    <ul id="fruits">
      <li class="bananas">...</li>
      <li class="apples">...</li>
      <li class="tomatoes"><span>Tomato is a Fruit</span>...</li>
    </ul>
  `;

  var snippetContainer = document.getElementById('vegetableSnippet');
  snippetContainer.innerHTML = snippetHTML;
}

// Function to remove the snippet
function removeSnippet() {
  var snippetContainer = document.getElementById('vegetableSnippet');
  snippetContainer.innerHTML = '';
}

// Alternate between displaying and removing the snippet every 5 seconds
var displayInterval = setInterval(function() {
  displaySnippet();
  setTimeout(removeSnippet, 2000);
}, 5000);

</script>

</body>
</html>

"""
    # Write the HTML content to a file in the temporary directory
    html_file_path = tmpdir.join("test_page.html")
    html_file_path.write(test_html)

    # Return the URL of the HTML page
    return f"file://{html_file_path}"


def test_goto():
    scraper.goto("https://www.example.com/")
    assert scraper.current_url == "https://www.example.com/"
    assert scraper.current_title == "Example Domain"


def test_goto_sleep():
    start = time()
    scraper.goto("https://www.example.com/", sleep_secs=3)
    end = time()
    assert end - start >= 3


def test_get_soup():
    scraper.goto("https://www.example.com/")
    soup = scraper.soup
    assert isinstance((title := soup.find("title")), Tag) and title.string == "Example Domain"


def test_new_tab():
    scraper.goto("https://google.com")
    scraper.new_tab("https://www.example.com/")
    assert len(scraper.tabs) == 2
    assert scraper.current_url == "https://www.example.com/"
    assert scraper.current_title == "Example Domain"


def test_find_element_by(selenium_test_html_static):
    if selenium_test_html_static:
        scraper.goto(selenium_test_html_static)
    assert scraper.find_element_by_class_name("information").get_attribute("value") == "Jane"
    assert scraper.find_element_by_css_selector("input#fname").get_attribute("value") == "Jane"
    assert scraper.find_element_by_id("fname").get_attribute("value") == "Jane"
    assert scraper.find_element_by_name("fname").get_attribute("value") == "Jane"
    assert (
        scraper.find_element_by_link_text("Selenium Official Page").get_attribute("href") == "https://www.selenium.dev/"
    )
    assert scraper.find_element_by_partial_link_text("Selenium").get_attribute("href") == "https://www.selenium.dev/"
    assert scraper.find_element_by_tag_name("h2").text == "Contact Selenium"
    assert scraper.find_element_by_xpath("//input[@id='fname']").get_attribute("value") == "Jane"


def test_find_elements_by(selenium_test_html_static=None):
    if selenium_test_html_static:
        scraper.goto(selenium_test_html_static)
    assert (found_elements := scraper.find_elements_by_class_name("information"))[0].get_attribute(
        "value"
    ) == "Jane" and len(found_elements) == 2
    assert (found_elements := scraper.find_elements_by_css_selector("input#fname"))[0].get_attribute(
        "value"
    ) == "Jane" and len(found_elements) == 1
    assert (found_elements := scraper.find_elements_by_id("fname"))[0].get_attribute("value") == "Jane" and len(
        found_elements
    ) == 1
    assert (found_elements := scraper.find_elements_by_name("fname"))[0].get_attribute("value") == "Jane" and len(
        found_elements
    ) == 1
    assert (found_elements := scraper.find_elements_by_link_text("Selenium Official Page"))[0].get_attribute(
        "href"
    ) == "https://www.selenium.dev/" and len(found_elements) == 1
    assert (found_elements := scraper.find_elements_by_partial_link_text("Selenium"))[0].get_attribute(
        "href"
    ) == "https://www.selenium.dev/" and len(found_elements) == 1
    assert (found_elements := scraper.find_elements_by_tag_name("h2"))[0].text == "Contact Selenium" and len(
        found_elements
    ) == 1
    assert (found_elements := scraper.find_elements_by_xpath("//input[@id='fname']"))[0].get_attribute(
        "value"
    ) == "Jane" and len(found_elements) == 1


def test_wait_for_element(selenium_test_html_dynamic):
    scraper.goto(selenium_test_html_dynamic)
    scraper.wait_until_presence_of_element_located_by_tag_name("form", timeout=6)
    test_find_element_by(None)
    scraper.wait_for_visibility_of_element_located_by_id("vegetableSnippet", timeout=6)
    assert scraper.find_element_by_id("vegetableSnippet").is_displayed() == True
    assert scraper.find_element_by_tag_name("ol").is_displayed() == True
    assert scraper.find_element_by_tag_name("ul").is_displayed() == True
    assert len(scraper.find_elements_by_tag_name("li")) == 6

    scraper.wait_for_invisibility_of_element_located_by_id("vegetableSnippet", timeout=6)


def test_try_wrapper_methods(selenium_test_html_static):
    scraper.goto(selenium_test_html_static)
    with pytest.raises(WebDriverException) as e:
        scraper.find_element_by_class_name("nonexistent")
        assert isinstance(e, NoSuchElementException)

    non_elm = scraper.try_find_element_by_class_name("nonexistent")
    assert non_elm == None

    with pytest.raises(JavascriptException) as e:
        # Only NoSuchElementException is ignored so JavascriptException should be raised
        scraper.try_execute_script("<invalid JS>", ignore_exceptions=NoSuchElementException)
        assert isinstance(e, JavascriptException)

    with pytest.raises(JavascriptException) as e:
        # Try with tuple of exceptions
        scraper.try_execute_script("<invalid JS>", ignore_exceptions=(NoSuchElementException,))
        assert isinstance(e, JavascriptException)

    # No exceptions should be raised since JavascriptException
    # is a subclass of WebDriverException (the default ignored exception)
    bad_js = scraper.try_execute_script("<invalid JS>")
    assert bad_js == None


def test_save_dynamic_methods(selenium_test_html_static):
    scraper.goto(selenium_test_html_static)

    # Test with save_dynamic_methods = False
    # Each call should return a new method
    # Methods should not be saved
    scraper.save_dynamic_methods = False
    dynamic_method_getattr_call1 = scraper.find_elements_by_class_name
    dynamic_method_getattr_call2 = scraper.find_elements_by_class_name
    assert id(dynamic_method_getattr_call1) != id(dynamic_method_getattr_call2)
    assert "find_elements_by_class_name" not in dir(scraper)

    # Test with save_dynamic_methods = True
    # Each call should return the same method
    # Methods should be saved
    scraper.save_dynamic_methods = True
    dynamic_method_getattr_call1 = scraper.find_elements_by_class_name
    dynamic_method_getattr_call2 = scraper.find_elements_by_class_name
    assert id(dynamic_method_getattr_call1) == id(dynamic_method_getattr_call2)
    assert "find_elements_by_class_name" in dir(scraper)


@pytest.mark.parametrize(
    "user_agent",
    [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "SOME ARBITRARY USER AGENT STRING",
    ],
)
def test_user_agent(user_agent):
    scraper = SouperScraper(executable_path=DEFAULT_CHROMEDRIVER_PATH, user_agent=user_agent)

    scraper.goto("https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
    ua_elm = scraper.wait_for_visibility_of_element_located_by_id("detected_value")
    assert ua_elm.text.strip('"') == user_agent == scraper.user_agent

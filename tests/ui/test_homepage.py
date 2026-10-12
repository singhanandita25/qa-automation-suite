# test_homepage.py — a completely separate test file
# It uses the same driver fixture from conftest.py, with no import at all.
# Run it with:   pytest test_homepage.py -v

# 4.Two more test cases

def test_homepage_title(driver):
    driver.get("https://www.python.org")
    assert driver.title == "Welcome to Python.org"


def test_about_page_loads(driver):
    driver.get("https://www.python.org/about/")
    assert "/about/" in driver.current_url

# test_search_v2.py — the same test, now using a Page Object
# Notice: no By, no find_element, no locators. Just steps.
# Run it with:   pytest test_search_v2.py -v

# 3. One test case — steps + expected result

from home_page import HomePage


def test_search_goes_to_results_page(driver):
    home = HomePage(driver)

    home.open()                    #Read the middle three lines out loud: open the home page, search for "selenium", check we're on the results page. 
    home.search("selenium")

    assert "/search/" in driver.current_url

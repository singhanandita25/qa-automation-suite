# home_page.py — the Page Object for python.org's home page
# All the locators and actions for this page live here. Tests never see a locator.

# Where things are on the screen, and what you can do there

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:

    URL = "https://www.python.org"

    # --- locators: the page's "contacts list" ---
    SEARCH_BOX = (By.ID, "id-search-field")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- actions: what a user can do on this page ---
    def open(self):
        self.driver.get(self.URL)

    def search(self, term):
        box = self.driver.find_element(*self.SEARCH_BOX)
        box.send_keys(term)
        box.send_keys(Keys.RETURN)
        self.wait.until(EC.url_contains("/search/"))

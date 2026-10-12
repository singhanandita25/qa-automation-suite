# conftest.py — shared fixtures for every test in this folder
# pytest finds this file automatically. No test file needs to import it.
#
#   pytest            -> headless (fast, no windows)
#   pytest --headed   -> visible browser (for watching / debugging)

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    """Teach pytest a new command line option: --headed"""
    parser.addoption(
        "--headed",
        action="store_true",
        help="run the tests with a visible browser window",
    )


@pytest.fixture
def driver(request):
    options = Options()  #	pick up a blank order form

    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")    #tick the box: "don't show a window"

    d = webdriver.Chrome(options=options)    # SETUP
    yield d                                  # the test runs here
    d.quit()                                 # TEARDOWN - always runs

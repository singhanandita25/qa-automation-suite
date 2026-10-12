# test_search_terms.py — the same test, but the data now lives in a CSV
# Add a row to search_terms.csv and you get another test. No Python changes.
# Run it with:   pytest selenium_suite/test_search_terms.py -v

import csv
import pathlib
import pytest
from home_page import HomePage


def load_terms():
    path = pathlib.Path(__file__).parent / "search_terms.csv"
    terms = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            terms.append(row["term"])
    return terms


@pytest.mark.parametrize("term", load_terms())
def test_search_works_for(driver, term):
    home = HomePage(driver)

    home.open()
    home.search(term)

    assert term in driver.current_url

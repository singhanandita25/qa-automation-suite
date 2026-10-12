# QA Automation Suite

![tests](https://github.com/singhanandita25/qa-automation-suite/actions/workflows/tests.yml/badge.svg)

A UI test suite built with Selenium and pytest, structured with the Page Object
Model and running headless in GitHub Actions on every push.

The tests run against [python.org](https://www.python.org) — a public site, chosen
deliberately so anyone can clone this repo and run the suite without credentials or
a private environment.

## What it covers

- Navigation and page titles
- Search: entering a term, waiting for the results page, verifying the result
- The same search test run against multiple inputs loaded from a CSV

## Running it

```bash
pip install -r requirements.txt

pytest tests/ui -v            # headless
pytest tests/ui -v --headed   # watch the browser, for debugging
```

An HTML report:

```bash
pytest tests/ui --html=report.html --self-contained-html
```

## Structure

```
tests/ui/
├── conftest.py          browser fixture: setup, teardown, --headed flag
├── home_page.py         page object: all locators and page actions
├── test_search_v2.py    search test, via the page object
├── test_search_terms.py data-driven search tests
├── test_homepage.py     navigation tests
└── search_terms.csv     test data
```

## Design decisions

**Page Object Model.** Locators live in `home_page.py` and nowhere else. The tests
contain no `By.ID` and no `find_element` — they call methods like `home.search()`.
When a locator changes, one file changes rather than every test that touches that
element.

**Explicit waits, never `sleep`.** Waits use `WebDriverWait` with an expected
condition, so a test waits for the state it needs rather than a fixed number of
seconds. A fixed sleep is simultaneously too slow on a fast machine and too short
on a slow one, which is the most common cause of flaky UI tests.

**Waits belong in the page object, not the test.** `search()` isn't finished when
Enter is pressed — it's finished when the results page has loaded. The page object
owns that, so a method always leaves the page in a usable state before returning.

**A fixture for the browser.** Setup and teardown live in `conftest.py`, so the
browser is quit even when a test fails. The fixture runs per test, which keeps
tests independent — no test inherits state from the one before it.

**Data-driven via `parametrize`.** Search terms come from `search_terms.csv` and
each one becomes a separate test with its own pass/fail result and the input in
its name. A loop inside a single test would fail as one unit and hide which input
broke. Adding a test case means adding a CSV row, not editing Python.

**Headless by default.** The CI runner has no display, so headless is what makes
the suite runnable there at all. The `--headed` flag is kept for local debugging.
On network-bound tests the speed difference is small — the point is portability,
not performance.

**Paths resolved relative to the test file.** The CSV is located with
`pathlib.Path(__file__).parent`, so the suite runs correctly regardless of the
working directory it's invoked from.

## CI

`.github/workflows/tests.yml` runs on every push and pull request: check out the
code, install Python, install dependencies, run the suite. A failing test fails the
build, so a regression is caught on the commit that introduced it.

## What I would do next

- **More pages.** One page object is enough to demonstrate the pattern, not enough
  to show how it scales. A second page would also force a decision about shared
  behaviour — a `BasePage` for common actions.
- **Screenshot on failure.** A pytest hook capturing a screenshot when a test fails
  would make CI failures diagnosable without reproducing them locally.
- **Cross-browser.** Currently Chrome only. Parametrising the driver fixture over
  Chrome and Firefox would catch browser-specific issues.
- **A real application.** python.org is stable and public, which makes it a good
  demo target but a poor test of the suite — it has no login, no forms with
  validation, and no state to clean up between tests.

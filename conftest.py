import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load = load_dotenv()

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    #options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window
    driver.implicitly_wait(int(os.getenv("IMPLICIT_WAIT", 10)))

    yield driver
    driver.quit()

@pytest.fixture(scope = "session")
def base_url():
    return os.getenv("BASE_URL", "https://www.saucedemo.com")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Saves a screenshot of the browser window if a test fails.

    This implementation of pytest_runtest_makereport is a hook that runs after each test
    has finished. If the test failed, it saves a screenshot of the browser to the
    "screenshots" directory in the current working directory. The screenshot is saved with
    the name "<test_name>_failed.png". If the test did not fail, no screenshot is saved.

    The test name is obtained from the test item object, which is an instance of
    `_pytest.nodes.Item`.

    This hook is marked with `tryfirst=True` to ensure it runs before other hooks. This
    allows the hook to capture any exceptions that occur during teardown, which would
    otherwise be lost if another hook were to run first.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs["driver"]
            if driver:
                screenshot_dir = "screenshots"
                os.markedirs(screenshot_dir, exist_ok=True)
                screenshot_path = f"{screenshot_dir}/{item.name}_failed.png"
                driver.save_screenshot(screenshot_path)
                print(f"\n💥 Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Failed to save screenshot: {e}")
import pytest
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from pages.login_page import LoginPage

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

def pytest_addoption(parser):
    """Add a command-line option to specify the browser."""
    parser.addoption("--browser", action="store", default="chrome", help="Choose browser: chrome, firefox, edge.")

@pytest.fixture
def driver(request):
    """Fixture to initialize and return the browser driver based on the user."""
    browser_name = request.config.getoption("--browser")

    logger.info("Starting WebDriver...")

    if browser_name == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser_name == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser_name == "edge":
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        raise ValueError(f"Unsupported browser: {browser_name}.")

    driver.maximize_window()

    yield driver

    logger.info("Quitting WebDriver...")
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to take a screenshot when a test fails and attach it to Allure reports."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"reports/screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved: {screenshot_path}")

            # Attach screenshot to Allure report
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

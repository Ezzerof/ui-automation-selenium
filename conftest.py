import pytest
import allure
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

@pytest.fixture
def driver():
    """Fixture to initialize and quit WebDriver."""
    logger.info("Starting WebDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
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

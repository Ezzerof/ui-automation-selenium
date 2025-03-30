import pytest
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
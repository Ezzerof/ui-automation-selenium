import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)

class LoginPage:
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        """Opens the Swag Lab login page."""
        logger.info("Opening Swag Lab login page...")
        self.driver.get("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        """Fills in the login form and submit it."""
        logger.info(f"Attempting to log in with username: {username}.")
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
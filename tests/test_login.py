import allure
import pytest
from selenium.webdriver import Keys

from tests.conftest import driver
from utils.config_loader import load_config
from utils.credentials_fetcher import get_credentials

config = load_config()

@allure.feature("Login Feature")
@allure.story("Valid Login")
def test_login_with_valid_credential(driver, login_page):
    """Test login functionality with correct username and password."""

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter valid credentials and submit the login form"):
        login_page.login(get_credentials("valid_username"), get_credentials("valid_password"))

    with allure.step("Verify that user is redirected to the inventory page"):
        assert "inventory.html" in driver.current_url, "Login failed: Inventory page not loaded."

@allure.feature("Login Feature")
@allure.story("Whitespace Trimming in Credentials")
@pytest.mark.xfail(reason="App does not trim input fields.")
def test_login_with_whitespace(driver, login_page):
    """Test login with leading/trailing spaces in credentials."""

    username = f"  {get_credentials("valid_username")}  "
    password = f"  {get_credentials("valid_password")}  "

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter credentials with leading/trailing whitespace"):
        login_page.login(username, password)

    with allure.step("Verify that user is redirected to the inventory page"):
        assert "inventory.html" in driver.current_url, "Login failed: App may not trim input."


@allure.feature("Login Feature")
@allure.story("Login using Enter key")
def test_login_with_enter_key(driver, login_page):
    """Test login by pressing Enter key instead of clicking the button."""

    username = get_credentials("valid_username")
    password = get_credentials("valid_password")

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter valid credentials and hit Enter key"):
        login_page.username_input.send_keys(username)
        login_page.password_input.send_keys(password + Keys.ENTER)

    with allure.step("Verify that user is redirected to the inventory page"):
        assert "inventory.html" in driver.current_url, "Login failed using Enter key."

@allure.feature("Login Feature")
@allure.story("Login using invalid username")
def test_login_with_invalid_username(driver, login_page):
    """Test login with invalid username and a valid password."""

    username = get_credentials("invalid_username")
    password = get_credentials("valid_password")

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter invalid username and valid password"):
        login_page.username_input.send_keys(username)
        login_page.password_input.send_keys(password + Keys.ENTER)

    with allure.step("Verify that error message appears"):
        assert "Epic sadface: Username and password do not match any user in this service" in login_page.error_message

@allure.feature("Login Feature")
@allure.story("Login using invalid password")
def test_login_with_invalid_password(driver, login_page):
    """Test login with invalid password and a valid username."""

    username = get_credentials("valid_username")
    password = get_credentials("invalid_password")

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter valid username and invalid password"):
        login_page.username_input.send_keys(username)
        login_page.password_input.send_keys(password + Keys.ENTER)

    with allure.step("Verify that error message appears"):
        assert "Epic sadface: Username and password do not match any user in this service" in login_page.error_message

@allure.feature("Login Feature")
@allure.story("Login using invalid credentials")
def test_login_with_invalid_credentials(driver, login_page):
    """Test login with invalid credentials."""

    username = get_credentials("invalid_username")
    password = get_credentials("invalid_password")

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter invalid username and password"):
        login_page.username_input.send_keys(username)
        login_page.password_input.send_keys(password + Keys.ENTER)

    with allure.step("Verify that error message appears"):
        assert "Epic sadface: Username and password do not match any user in this service" in login_page.error_message

@allure.feature("Login Feature")
@allure.story("Login using empty username")
def test_login_with_empty_username(driver, login_page):
    """Test login with empty username and valid password."""

    password = get_credentials("valid_password")

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter valid password"):
        login_page.password_input.send_keys(password + Keys.ENTER)

    with allure.step("Verify that error message appears"):
        assert "Epic sadface: Username is required" in login_page.error_message

@allure.feature("Login Feature")
@allure.story("Login using empty password")
def test_login_with_empty_password(driver, login_page):
    """Test login with valid username and empty password."""

    username = get_credentials("valid_username")

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Enter valid username"):
        login_page.username_input.send_keys(username + Keys.ENTER)

    with allure.step("Verify that error message appears"):
        assert "Epic sadface: Password is required" in login_page.error_message

@allure.feature("Login Feature")
@allure.story("Login using both fields empty")
def test_login_with_empty_fields(driver, login_page):
    """Test login using both credential fields empty."""

    with allure.step("Open Swag Labs login page"):
        login_page.open()

    with allure.step("Hit Enter key to submit empty form"):
        login_page.username_input.send_keys(Keys.ENTER)

    with allure.step("Verify that error message appears"):
        assert "Epic sadface: Username is required" in login_page.error_message
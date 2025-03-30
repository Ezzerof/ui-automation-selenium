import pytest
from pages.login_page import LoginPage
from conftest import driver

@pytest.mark.parametrize("username, password", [
    ("standard_user", "secret_sauce"), # Valid credentials
    ("locked_out_user", "secret_sauce") # Locked-out user
])
def test_login(driver, username, password):
    """Open the Login Page, fill in credentials and submit."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    if username == "standard_user":
        assert "inventory.html" in driver.current_url # Successful login
    elif username == "locked_out_user":
        error_message = driver.find_element("xpath", "//h3[@data-test='error']").text
        assert "Epic sadface" in error_message # Expected failure message


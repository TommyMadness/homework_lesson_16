import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene import Browser, Config, be
from dotenv import load_dotenv
from utils import attach

DEFAULT_BROWSER_VERSION = "127.0"


def pytest_addoption(parser):
    parser.addoption("--browser_version", default=DEFAULT_BROWSER_VERSION)
    parser.addoption(
        "--remote",
        action="store_true",
        default=False,
        help="Run tests remotely via Selenoid",
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function")
def chrome_options():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    return options


@pytest.fixture(scope="function")
def setup_browser(request, chrome_options):
    remote = request.config.getoption("--remote")
    browser_version = request.config.getoption("--browser_version")
    browser_version = browser_version if browser_version else DEFAULT_BROWSER_VERSION

    if remote:
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
            },
        }
        chrome_options.capabilities.update(selenoid_capabilities)

        login = os.getenv("LOGIN")
        password = os.getenv("PASSWORD")

        driver = webdriver.Remote(
            command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
            options=chrome_options,
        )
    else:
        driver = webdriver.Chrome(options=chrome_options)

    browser = Browser(Config(driver=driver, base_url="https://www.cian.ru"))

    yield browser

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    if remote:
        attach.add_video(browser)

    browser.quit()


@pytest.fixture
def close_popup(setup_browser):
    """Фикстура для закрытия всплывающего окна после загрузки страницы."""

    def _close():
        with allure.step("Закрываем всплывающее окно, если оно появилось"):
            popup_close_button = setup_browser.element("button[title='Закрыть']")
            if popup_close_button.matching(be.visible):
                popup_close_button.click()

    return _close

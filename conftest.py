import os

import allure
import pytest
from selenium import webdriver

# Адрес приложения. По умолчанию — опубликованная версия на GitHub Pages.
# Для локальной проверки: TASKFLOW_URL=http://127.0.0.1:5500/index.html pytest
BASE_URL = os.getenv("TASKFLOW_URL", "https://a160lkn.github.io/TaskFlow/")


@pytest.fixture
def driver():
    """Открывает браузер перед тестом и закрывает после."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,900")

    # Запуск без окна браузера: HEADLESS=1 pytest
    # Дополнительные флаги нужны для серверов и CI (например, GitHub Actions)
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def app(driver):
    """Открывает приложение и возвращает его Page Object."""
    from pages.taskflow_page import TaskFlowPage

    return TaskFlowPage(driver, BASE_URL).open()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Если тест упал, прикрепляет скриншот к Allure-отчёту."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG,
            )

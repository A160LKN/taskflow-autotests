from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def testid(value):
    """Локатор по атрибуту data-testid."""
    return By.CSS_SELECTOR, f'[data-testid="{value}"]'


class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_visible(self, locator):
        """Дождаться, пока элемент появится, и вернуть его."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Дождаться, пока элемент станет кликабельным, и нажать."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        """Дождаться поля, очистить его и ввести текст."""
        field = self.wait_for_visible(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator):
        """Текст элемента."""
        return self.driver.find_element(*locator).text

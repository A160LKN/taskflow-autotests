import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, testid


class TaskFlowPage(BasePage):

    # Форма
    TASK_INPUT = testid("task-input")
    PRIORITY_SELECT = testid("task-priority")
    ADD_BUTTON = testid("add-button")
    FORM_ERROR = testid("form-error")

    # Список задач
    TASK_ITEMS = testid("task-item")
    TASK_TITLES = testid("task-title")
    EDIT_INPUT = testid("task-edit-input")
    EMPTY_STATE = testid("empty-state")
    EMPTY_TEXT = (By.ID, "empty-text")

    # Фильтры и поиск
    SEARCH = testid("search")

    # Статистика
    PROGRESS_TEXT = testid("progress-text")
    PROGRESS_PERCENT = testid("progress-percent")
    COUNTER = testid("counter")
    CLEAR_DONE = testid("clear-done")

    # Уведомление
    TOAST = testid("toast")
    TOAST_UNDO = testid("toast-undo")

    # Настройки
    LANG_TOGGLE = testid("lang-toggle")
    THEME_TOGGLE = testid("theme-toggle")

    def __init__(self, driver, url):
        super().__init__(driver)
        self.url = url

    # ---------- Навигация ----------

    @allure.step("Открыть приложение TaskFlow")
    def open(self):
        self.driver.get(self.url)
        self.wait_for_visible(self.TASK_INPUT)
        return self

    @allure.step("Обновить страницу")
    def refresh(self):
        self.driver.refresh()
        self.wait_for_visible(self.TASK_INPUT)

    # ---------- Добавление ----------

    @allure.step("Добавить задачу «{title}» с приоритетом {priority}")
    def add_task(self, title, priority="medium"):
        self.type_text(self.TASK_INPUT, title)
        Select(self.driver.find_element(*self.PRIORITY_SELECT)).select_by_value(priority)
        self.click(self.ADD_BUTTON)

    @allure.step("Получить текст ошибки формы")
    def get_error_text(self):
        self.wait.until(lambda d: d.find_element(*self.FORM_ERROR).text != "")
        return self.text_of(self.FORM_ERROR)

    # ---------- Список ----------

    def _task(self, index):
        """Задача по порядковому номеру (0 — первая сверху)."""
        return self.driver.find_elements(*self.TASK_ITEMS)[index]

    @allure.step("Получить названия задач")
    def get_task_titles(self):
        # textContent, а не .text: Selenium возвращает в .text только видимый текст,
        # а новая задача появляется с анимацией прозрачности (opacity от 0 до 1)
        return [el.get_attribute("textContent") for el in self.driver.find_elements(*self.TASK_TITLES)]

    @allure.step("Дождаться, что в списке {count} задач(и)")
    def wait_for_tasks_count(self, count):
        self.wait.until(lambda d: len(d.find_elements(*self.TASK_ITEMS)) == count)

    @allure.step("Получить приоритет задачи №{index}")
    def get_priority_badge(self, index):
        return self._task(index).find_element(*testid("task-priority-badge")).text

    @allure.step("Отметить задачу №{index}")
    def toggle_task(self, index):
        # Сам чекбокс прозрачный и лежит поверх нарисованной рамки,
        # поэтому кликаем по обёртке <label>, внутри которой он находится
        self._task(index).find_element(By.CLASS_NAME, "task__check-wrap").click()

    @allure.step("Проверить, выполнена ли задача №{index}")
    def is_task_done(self, index):
        return self._task(index).find_element(*testid("task-checkbox")).is_selected()

    @allure.step("Удалить задачу №{index}")
    def delete_task(self, index):
        self._task(index).find_element(*testid("task-delete")).click()

    @allure.step("Переименовать задачу №{index} в «{new_title}»")
    def edit_task(self, index, new_title):
        title = self._task(index).find_element(*testid("task-title"))
        ActionChains(self.driver).double_click(title).perform()
        field = self.wait_for_visible(self.EDIT_INPUT)
        # Текст в поле уже выделен — новый ввод его заменит
        field.send_keys(new_title + Keys.ENTER)
        self.wait.until(EC.invisibility_of_element_located(self.EDIT_INPUT))

    @allure.step("Получить текст пустого списка")
    def get_empty_text(self):
        # В блоке есть ещё иконка ✓, поэтому читаем только абзац с сообщением
        self.wait_for_visible(self.EMPTY_STATE)
        return self.driver.find_element(*self.EMPTY_TEXT).get_attribute("textContent")

    # ---------- Уведомление ----------

    @allure.step("Проверить, что показано уведомление об удалении")
    def is_toast_visible(self):
        return self.wait_for_visible(self.TOAST).is_displayed()

    @allure.step("Нажать «Отменить» в уведомлении")
    def undo_delete(self):
        self.click(self.TOAST_UNDO)

    # ---------- Фильтры и поиск ----------

    @allure.step("Выбрать фильтр «{name}»")
    def set_filter(self, name):
        self.click(testid(f"filter-{name}"))

    @allure.step("Найти «{text}»")
    def search(self, text):
        self.type_text(self.SEARCH, text)

    # ---------- Статистика ----------

    @allure.step("Дождаться прогресса «{text}»")
    def wait_for_progress(self, text):
        self.wait.until(EC.text_to_be_present_in_element(self.PROGRESS_TEXT, text))

    @allure.step("Дождаться процента «{percent}»")
    def wait_for_percent(self, percent):
        self.wait.until(lambda d: d.find_element(*self.PROGRESS_PERCENT).text == percent)

    @allure.step("Получить счётчик задач")
    def get_counter_text(self):
        return self.text_of(self.COUNTER)

    @allure.step("Проверить, доступна ли кнопка «Удалить выполненные»")
    def is_clear_done_enabled(self):
        return self.driver.find_element(*self.CLEAR_DONE).is_enabled()

    @allure.step("Удалить выполненные задачи")
    def clear_completed(self):
        self.click(self.CLEAR_DONE)

    # ---------- Настройки ----------

    @allure.step("Переключить язык")
    def switch_language(self):
        self.click(self.LANG_TOGGLE)

    @allure.step("Получить текст кнопки добавления")
    def get_add_button_text(self):
        return self.text_of(self.ADD_BUTTON)

    @allure.step("Переключить тему")
    def toggle_theme(self):
        self.click(self.THEME_TOGGLE)

    @allure.step("Получить текущую тему")
    def get_theme(self):
        return self.driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme")

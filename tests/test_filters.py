import allure
import pytest


@allure.epic("TaskFlow")
@allure.feature("Фильтры и поиск")
class TestFilters:

    @pytest.fixture(autouse=True)
    def prepare_tasks(self, app):
        """Перед каждым тестом: три задачи, одна из них выполнена."""
        app.add_task("Купить молоко")
        app.add_task("Позвонить маме")
        app.add_task("Купить хлеб")
        app.wait_for_tasks_count(3)
        app.toggle_task(0)  # «Купить хлеб» — выполнена
        self.app = app

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Фильтр «{filter_name}» показывает нужные задачи")
    @pytest.mark.parametrize(
        "filter_name, expected_titles",
        [
            ("active", ["Позвонить маме", "Купить молоко"]),
            ("done", ["Купить хлеб"]),
            ("all", ["Купить хлеб", "Позвонить маме", "Купить молоко"]),
        ],
    )
    def test_filter(self, filter_name, expected_titles):
        self.app.set_filter(filter_name)

        self.app.wait_for_tasks_count(len(expected_titles))
        assert self.app.get_task_titles() == expected_titles

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Поиск находит задачи по части названия без учёта регистра")
    def test_search(self):
        self.app.search("КУПИТЬ")

        self.app.wait_for_tasks_count(2)
        assert self.app.get_task_titles() == ["Купить хлеб", "Купить молоко"]

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Если ничего не найдено, показывается сообщение")
    def test_search_not_found(self):
        self.app.search("несуществующая")

        self.app.wait_for_tasks_count(0)
        assert self.app.get_empty_text() == "Ничего не найдено"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("«Удалить выполненные» удаляет только выполненные задачи")
    def test_clear_completed(self):
        assert self.app.is_clear_done_enabled()

        self.app.clear_completed()

        self.app.wait_for_tasks_count(2)
        assert self.app.get_task_titles() == ["Позвонить маме", "Купить молоко"]
        assert not self.app.is_clear_done_enabled()

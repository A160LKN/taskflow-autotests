import allure
import pytest


@allure.epic("TaskFlow")
@allure.feature("Задачи")
class TestTasks:

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Задача добавляется в список")
    def test_add_task(self, app):
        app.add_task("Купить молоко")

        app.wait_for_tasks_count(1)
        assert app.get_task_titles() == ["Купить молоко"]
        assert app.get_counter_text() == "1 задача в работе"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Новая задача появляется вверху списка")
    def test_new_task_on_top(self, app):
        app.add_task("Первая задача")
        app.add_task("Вторая задача")

        app.wait_for_tasks_count(2)
        assert app.get_task_titles() == ["Вторая задача", "Первая задача"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("У задачи отображается выбранный приоритет")
    def test_task_priority(self, app):
        app.add_task("Срочный отчёт", priority="high")

        app.wait_for_tasks_count(1)
        assert app.get_priority_badge(0) == "Высокий"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Ошибка при добавлении: {case_name}")
    @pytest.mark.parametrize(
        "case_name, title, expected_error",
        [
            ("Пустое название", "", "Введите название задачи"),
            ("Только пробелы", "   ", "Введите название задачи"),
            ("Слишком короткое", "ab", "Минимум 3 символа"),
        ],
        ids=["empty", "spaces", "too_short"],
    )
    def test_validation(self, app, case_name, title, expected_error):
        app.add_task(title)

        assert app.get_error_text() == expected_error
        assert app.get_task_titles() == []

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("HTML-код в названии отображается как текст (защита от XSS)")
    def test_xss_shown_as_text(self, app):
        app.add_task("<b>жирный</b>")

        app.wait_for_tasks_count(1)
        assert app.get_task_titles() == ["<b>жирный</b>"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Отметка выполнения обновляет прогресс и счётчик")
    def test_complete_task(self, app):
        app.add_task("Сделать зарядку")
        app.add_task("Прочитать книгу")
        app.wait_for_tasks_count(2)

        app.toggle_task(0)

        assert app.is_task_done(0)
        app.wait_for_progress("Выполнено 1 из 2")
        app.wait_for_percent("50%")
        assert app.get_counter_text() == "1 задача в работе"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Задача редактируется двойным кликом")
    def test_edit_task(self, app):
        app.add_task("Купить молоко")
        app.wait_for_tasks_count(1)

        app.edit_task(0, "Купить хлеб")

        assert app.get_task_titles() == ["Купить хлеб"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление задачи и отмена удаления")
    def test_delete_and_undo(self, app):
        app.add_task("Временная задача")
        app.wait_for_tasks_count(1)

        app.delete_task(0)

        app.wait_for_tasks_count(0)
        assert app.is_toast_visible()

        app.undo_delete()

        app.wait_for_tasks_count(1)
        assert app.get_task_titles() == ["Временная задача"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Задачи сохраняются после обновления страницы")
    def test_tasks_persist_after_refresh(self, app):
        app.add_task("Не потеряться")
        app.wait_for_tasks_count(1)

        app.refresh()

        app.wait_for_tasks_count(1)
        assert app.get_task_titles() == ["Не потеряться"]

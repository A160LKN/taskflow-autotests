import allure


@allure.epic("TaskFlow")
@allure.feature("Настройки")
class TestSettings:

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Переключение языка на английский и обратно")
    def test_switch_language(self, app):
        assert app.get_add_button_text() == "Добавить"

        app.switch_language()
        assert app.get_add_button_text() == "Add"

        app.switch_language()
        assert app.get_add_button_text() == "Добавить"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Счётчик задач переводится вместе с интерфейсом")
    def test_counter_translated(self, app):
        app.add_task("Learn English")
        app.wait_for_tasks_count(1)

        app.switch_language()

        assert app.get_counter_text() == "1 task in progress"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Переключение темы")
    def test_toggle_theme(self, app):
        # Тема по умолчанию зависит от настроек системы, поэтому
        # проверяем, что она меняется на противоположную
        initial = app.get_theme()
        expected = "light" if initial == "dark" else "dark"

        app.toggle_theme()

        assert app.get_theme() == expected

    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Тема и язык сохраняются после обновления страницы")
    def test_settings_persist(self, app):
        initial_theme = app.get_theme()

        app.toggle_theme()
        app.switch_language()
        app.refresh()

        assert app.get_theme() != initial_theme
        assert app.get_add_button_text() == "Add"

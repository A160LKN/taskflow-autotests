# TaskFlow Autotests

[![UI tests](https://github.com/A160LKN/taskflow-autotests/actions/workflows/tests.yml/badge.svg)](https://github.com/A160LKN/taskflow-autotests/actions/workflows/tests.yml)

UI-автотесты для моего приложения [TaskFlow](https://github.com/A160LKN/TaskFlow) — трекера задач на HTML, CSS и JavaScript.

**Тестируемое приложение:** https://a160lkn.github.io/TaskFlow/

**Allure-отчёт последнего прогона:** https://a160lkn.github.io/taskflow-autotests/

## Стек

- Python 3.10+
- Selenium WebDriver 4
- pytest
- Allure Report

## Что проверяется — 21 тест

**Задачи**
- добавление задачи и порядок в списке;
- приоритет задачи;
- валидация (параметризованный тест): пустое название, только пробелы, слишком короткое;
- защита от XSS: HTML-код в названии отображается как текст;
- отметка выполнения, прогресс-бар и счётчик;
- редактирование двойным кликом;
- удаление и отмена удаления;
- сохранение задач после обновления страницы.

**Фильтры и поиск**
- фильтры «Все / Активные / Выполненные» (параметризованный тест);
- поиск без учёта регистра и сообщение «Ничего не найдено»;
- удаление выполненных задач.

**Настройки**
- переключение языка RU/EN и перевод счётчика;
- переключение темы;
- сохранение темы и языка после обновления страницы.

## Особенности

- паттерн **Page Object**;
- локаторы по атрибутам **`data-testid`**, которые я заложил в приложение специально для автотестов;
- **явные ожидания** вместо `time.sleep`;
- каждый тест запускается в чистом браузере — тесты не зависят друг от друга;
- **Allure-отчёт** с шагами и скриншотом при падении;
- запуск без окна браузера (headless) для серверов и CI;
- **CI на GitHub Actions**: тесты запускаются при каждом изменении и раз в день по расписанию, Allure-отчёт публикуется на GitHub Pages.

## Структура

```
├── pages
│   ├── base_page.py       — общие методы и локатор по data-testid
│   └── taskflow_page.py   — Page Object приложения
├── tests
│   ├── test_tasks.py      — задачи
│   ├── test_filters.py    — фильтры и поиск
│   └── test_settings.py   — язык и тема
├── conftest.py            — фикстуры браузера и приложения, скриншот при падении
├── pytest.ini
└── requirements.txt
```

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# тесты против опубликованного приложения
pytest

# тесты против локальной версии (например, VS Code Live Server)
TASKFLOW_URL=http://127.0.0.1:5500/index.html pytest

# без окна браузера
HEADLESS=1 pytest

# Allure-отчёт
allure serve allure-results
```

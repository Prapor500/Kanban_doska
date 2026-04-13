import os
import time
import uuid

import pytest

playwright = pytest.importorskip(
    "playwright.sync_api",
    reason="Install playwright to run frontend UI tests",
)

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


BASE_URL = os.getenv("FRONTEND_BASE_URL")

pytestmark = [pytest.mark.frontend]
if not BASE_URL:
    pytestmark.append(
        pytest.mark.skip(reason="Set FRONTEND_BASE_URL to run frontend UI tests")
    )


EMAIL_SELECTORS = [
    "input[name='email']",
    "input[type='email']",
    "input[placeholder*='mail' i]",
]
PASSWORD_SELECTORS = [
    "input[name='password']",
    "input[type='password']",
    "input[placeholder*='парол' i]",
    "input[placeholder*='password' i]",
]
CONFIRM_PASSWORD_SELECTORS = [
    "input[name='confirmPassword']",
    "input[name='password_confirmation']",
    "input[placeholder*='подтверж' i]",
    "input[placeholder*='confirm' i]",
]
LOGIN_BUTTON_SELECTORS = [
    "button:has-text('Войти')",
    "button:has-text('Login')",
    "button[type='submit']",
]
REGISTER_BUTTON_SELECTORS = [
    "button:has-text('Зарегистрироваться')",
    "button:has-text('Register')",
    "button:has-text('Создать аккаунт')",
    "button[type='submit']",
]
LOGIN_LINK_SELECTORS = [
    "a:has-text('Войти')",
    "a:has-text('Login')",
]
REGISTER_LINK_SELECTORS = [
    "a:has-text('Регистрация')",
    "a:has-text('Register')",
    "a:has-text('Создать аккаунт')",
]
LOGOUT_SELECTORS = [
    "button:has-text('Выйти')",
    "button:has-text('Logout')",
    "[data-testid='logout']",
]
CREATE_BOARD_BUTTON_SELECTORS = [
    "button:has-text('Создать доску')",
    "button:has-text('Create board')",
    "button:has-text('Новая доска')",
    "[data-testid='create-board']",
]
BOARD_NAME_SELECTORS = [
    "input[name='boardName']",
    "input[name='name']",
    "input[placeholder*='доск' i]",
    "input[placeholder*='board' i]",
]
ADD_COLUMN_BUTTON_SELECTORS = [
    "button:has-text('Добавить колонку')",
    "button:has-text('Add column')",
    "[data-testid='add-column']",
]
COLUMN_NAME_SELECTORS = [
    "input[name='columnName']",
    "input[name='name']",
    "input[placeholder*='колонк' i]",
    "input[placeholder*='column' i]",
]
ADD_TASK_BUTTON_SELECTORS = [
    "button:has-text('Добавить задачу')",
    "button:has-text('Add task')",
    "[data-testid='add-task']",
]
TASK_TITLE_SELECTORS = [
    "input[name='title']",
    "input[placeholder*='назван' i]",
    "input[placeholder*='title' i]",
]
TASK_DESCRIPTION_SELECTORS = [
    "textarea[name='description']",
    "textarea[placeholder*='описан' i]",
    "textarea[placeholder*='description' i]",
]
SAVE_BUTTON_SELECTORS = [
    "button:has-text('Сохранить')",
    "button:has-text('Save')",
    "button:has-text('Создать')",
    "button:has-text('Create')",
    "button[type='submit']",
]
ERROR_SELECTORS = [
    "[role='alert']",
    ".error",
    ".alert-error",
    ".form-error",
    "text=Неверный",
    "text=Ошибка",
    "text=Invalid",
    "text=Error",
]
AUTHENTICATED_SELECTORS = [
    "button:has-text('Создать доску')",
    "button:has-text('Create board')",
    "button:has-text('Выйти')",
    "button:has-text('Logout')",
    "[data-testid='board-list']",
]


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=os.getenv("PLAYWRIGHT_HEADLESS", "1") != "0"
        )
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(base_url=BASE_URL, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    yield page
    context.close()


def _visible_locator(page, selectors, timeout=3500):
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return locator
        except PlaywrightTimeoutError:
            continue
    raise AssertionError(f"Visible element not found for selectors: {selectors}")


def _try_visible_locator(page, selectors, timeout=1200):
    for selector in selectors:
        locator = page.locator(selector).first
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return locator
        except PlaywrightTimeoutError:
            continue
    return None


def _click_any(page, selectors, timeout=3500):
    _visible_locator(page, selectors, timeout=timeout).click()


def _fill_any(page, selectors, value, timeout=3500):
    field = _visible_locator(page, selectors, timeout=timeout)
    field.fill(value)
    return field


def _text_locator(page, text, timeout=3500):
    locator = page.locator(f"text={text}").first
    locator.wait_for(state="visible", timeout=timeout)
    return locator


def _goto_login(page):
    for path in ("/login", "/auth/login", "/"):
        page.goto(path, wait_until="domcontentloaded")
        if _try_visible_locator(page, EMAIL_SELECTORS):
            return
        login_link = _try_visible_locator(page, LOGIN_LINK_SELECTORS)
        if login_link:
            login_link.click()
            if _try_visible_locator(page, EMAIL_SELECTORS):
                return
    raise AssertionError("Login form was not found in the frontend app")


def _goto_register(page):
    for path in ("/register", "/auth/register", "/signup", "/"):
        page.goto(path, wait_until="domcontentloaded")
        if _try_visible_locator(page, EMAIL_SELECTORS):
            register_link = _try_visible_locator(page, REGISTER_LINK_SELECTORS, timeout=600)
            if register_link:
                register_link.click()
            return
        register_link = _try_visible_locator(page, REGISTER_LINK_SELECTORS)
        if register_link:
            register_link.click()
            if _try_visible_locator(page, EMAIL_SELECTORS):
                return
    raise AssertionError("Registration form was not found in the frontend app")


def _wait_until_authenticated(page):
    if _try_visible_locator(page, AUTHENTICATED_SELECTORS, timeout=5000):
        return
    raise AssertionError("Authenticated UI state was not detected")


def _register_user(page, email, password):
    _goto_register(page)
    _fill_any(page, EMAIL_SELECTORS, email)
    _fill_any(page, PASSWORD_SELECTORS, password)
    confirm_field = _try_visible_locator(page, CONFIRM_PASSWORD_SELECTORS, timeout=700)
    if confirm_field:
        confirm_field.fill(password)
    _click_any(page, REGISTER_BUTTON_SELECTORS)
    page.wait_for_load_state("networkidle")


def _login_user(page, email, password):
    _goto_login(page)
    _fill_any(page, EMAIL_SELECTORS, email)
    _fill_any(page, PASSWORD_SELECTORS, password)
    _click_any(page, LOGIN_BUTTON_SELECTORS)
    page.wait_for_load_state("networkidle")
    _wait_until_authenticated(page)


def _logout_user(page):
    _click_any(page, LOGOUT_SELECTORS)
    page.wait_for_load_state("networkidle")
    _visible_locator(page, EMAIL_SELECTORS)


def _create_board(page, board_name):
    _click_any(page, CREATE_BOARD_BUTTON_SELECTORS)
    _fill_any(page, BOARD_NAME_SELECTORS, board_name)
    _click_any(page, SAVE_BUTTON_SELECTORS)
    page.wait_for_load_state("networkidle")
    _text_locator(page, board_name)


def _add_column(page, column_name):
    _click_any(page, ADD_COLUMN_BUTTON_SELECTORS)
    _fill_any(page, COLUMN_NAME_SELECTORS, column_name)
    _click_any(page, SAVE_BUTTON_SELECTORS)
    page.wait_for_load_state("networkidle")
    _text_locator(page, column_name)


def _add_task(page, title, description="UI automation task"):
    _click_any(page, ADD_TASK_BUTTON_SELECTORS)
    _fill_any(page, TASK_TITLE_SELECTORS, title)
    description_field = _try_visible_locator(page, TASK_DESCRIPTION_SELECTORS, timeout=700)
    if description_field:
        description_field.fill(description)
    _click_any(page, SAVE_BUTTON_SELECTORS)
    page.wait_for_load_state("networkidle")
    _text_locator(page, title)


def _edit_task_title(page, old_title, new_title):
    _text_locator(page, old_title).click()
    title_field = _visible_locator(page, TASK_TITLE_SELECTORS)
    title_field.fill(new_title)
    _click_any(page, SAVE_BUTTON_SELECTORS)
    page.wait_for_load_state("networkidle")
    _text_locator(page, new_title)


def _column_container(page, column_name):
    selectors = [
        f"[data-testid='column']:has-text('{column_name}')",
        f".kanban-column:has-text('{column_name}')",
        f".column:has-text('{column_name}')",
        f"section:has-text('{column_name}')",
        f"div:has-text('{column_name}')",
    ]
    return _visible_locator(page, selectors, timeout=5000)


def _drag_task_to_column(page, task_title, column_name):
    task = _text_locator(page, task_title)
    target_column = _column_container(page, column_name)
    task.drag_to(target_column)
    page.wait_for_load_state("networkidle")
    target_column.locator(f"text={task_title}").first.wait_for(state="visible", timeout=5000)


def _unique_credentials(prefix):
    suffix = f"{int(time.time())}-{uuid.uuid4().hex[:6]}"
    return f"{prefix}-{suffix}@example.com", "Secret123!"


def test_frontend_login_with_invalid_password_shows_error(page):
    email, password = _unique_credentials("frontend-login")
    _register_user(page, email, password)

    logout_button = _try_visible_locator(page, LOGOUT_SELECTORS, timeout=1500)
    if logout_button:
        logout_button.click()
        page.wait_for_load_state("networkidle")

    _goto_login(page)
    _fill_any(page, EMAIL_SELECTORS, email)
    _fill_any(page, PASSWORD_SELECTORS, "WrongPassword123!")
    _click_any(page, LOGIN_BUTTON_SELECTORS)
    page.wait_for_load_state("networkidle")
    _visible_locator(page, ERROR_SELECTORS, timeout=5000)


def test_frontend_protected_route_redirects_to_login(page):
    for path in ("/boards", "/dashboard", "/projects"):
        page.goto(path, wait_until="domcontentloaded")
        if _try_visible_locator(page, EMAIL_SELECTORS, timeout=1500):
            return
        if "login" in page.url.lower():
            return
    raise AssertionError("Protected route did not redirect to login")


def test_frontend_can_create_board_and_columns(page):
    email, password = _unique_credentials("frontend-board")
    _register_user(page, email, password)
    _login_user(page, email, password)

    board_name = f"Test Board {uuid.uuid4().hex[:6]}"
    _create_board(page, board_name)
    _add_column(page, "To Do")
    _add_column(page, "Done")


def test_frontend_logout_returns_user_to_login(page):
    email, password = _unique_credentials("frontend-logout")
    _register_user(page, email, password)
    _login_user(page, email, password)
    _logout_user(page)


def test_frontend_can_edit_task_and_move_it_between_columns(page):
    email, password = _unique_credentials("frontend-task")
    _register_user(page, email, password)
    _login_user(page, email, password)

    board_name = f"Board {uuid.uuid4().hex[:6]}"
    original_title = f"Task {uuid.uuid4().hex[:4]}"
    updated_title = f"Task updated {uuid.uuid4().hex[:4]}"

    _create_board(page, board_name)
    _add_column(page, "To Do")
    _add_column(page, "In Progress")
    _add_task(page, original_title)
    _edit_task_title(page, original_title, updated_title)
    _drag_task_to_column(page, updated_title, "In Progress")

# Инструкция по запуску тестов проекта Kanban

В проекте используются современные инструменты: **uv** для Python (Backend) и **npm** для Vite/React (Frontend).

## 1. Подготовка окружения (выполняется один раз)

### Бэкенд (Python/FastAPI)
```powershell
cd Kanban_doska
# Создание виртуального окружения и синхронизация зависимостей
uv venv
uv sync
# Установка инструментов тестирования (если еще не установлены)
uv add --dev pytest pytest-asyncio playwright httpx
# Установка браузеров для UI-тестов
uv run playwright install
```

### Фронтенд (React/Vite)
```powershell
cd Kanban_frontend
npm install
```

---

## 2. Запуск тестов

### А. API-тесты бэкенда (Логика и БД)
Эти тесты проверяют серверную часть через SQLite (без браузера).
```powershell
cd Kanban_doska
uv run pytest -m "not frontend"
```

### Б. UI-тесты / E2E (Интерфейс)
Требуют запущенного фронтенда. Тесты имитируют действия пользователя в браузере.

1. **Запустите фронтенд** (в одном терминале):
   ```powershell
   cd Kanban_frontend
   npm run dev
   ```
2. **Запустите UI-тесты** (во втором терминале):
   ```powershell
   cd Kanban_doska
   $env:FRONTEND_BASE_URL="http://localhost:5173"; uv run pytest -m frontend
   ```

---

## 3. Запуск приложения для разработки

**Backend:**
```powershell
cd Kanban_doska
uv run uvicorn src.main:app --reload
```

**Frontend:**
```powershell
cd Kanban_frontend
npm run dev
```

---

## Полезные команды pytest
* `uv run pytest -v` — подробный вывод.
* `uv run pytest --lf` — запустить только упавшие тесты.
* `uv run pytest -s` — видеть `print()` в консоли.

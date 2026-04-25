# ♟ Chess Coach Agent Bot

Telegram-бот-тренер по шахматным дебютам на основе LLM-агента.  
Подбирает дебюты под уровень игрока, показывает реальную статистику из Lichess и находит обучающие видео на YouTube.

---

## Возможности

- **Подбор дебюта** — агент рекомендует 1–2 дебюта под рейтинг и цвет фигур игрока
- **Разбор конкретного дебюта** — объясняет идею, показывает основные ходы
- **Статистика Lichess** — реальные данные: процент побед, количество партий, топ продолжения
- **Поиск видео** — находит обучающие ролики на YouTube (по релевантности или по дате)
- **Общие вопросы** — отвечает на шахматные вопросы из собственных знаний
- **Память диалога** — сохраняет историю переписки в рамках сессии для каждого чата

---

## Стек технологий

| Слой | Технология |
|---|---|
| Язык | Python 3.13+ |
| Telegram | [aiogram](https://github.com/aiogram/aiogram) 3.x |
| LLM | OpenAI-совместимый API (по умолчанию — [OpenRouter](https://openrouter.ai)) |
| Веб-поиск | [Tavily API](https://tavily.com) |
| Шахматная статистика | [Lichess Opening Explorer API](https://lichess.org/api#tag/Opening-Explorer) |
| Видео | [YouTube Data API v3](https://developers.google.com/youtube/v3) |
| HTTP-клиент | httpx |
| Конфигурация | pydantic-settings |

---

## Архитектура

```
src/
├── main.py               # Точка входа: запуск бота и DI зависимостей
├── core/
│   └── config.py         # Настройки из .env (pydantic-settings)
├── agent/
│   ├── agent.py          # Агентный цикл: вызов LLM + обработка tool calls
│   ├── prompts.py        # Системный промпт с алгоритмом работы агента
│   └── schemas.py        # JSON-схемы инструментов для LLM (function calling)
├── bot/
│   └── handlers.py       # Обработчики Telegram-команд и сообщений
├── contracts/
│   └── tool_results.py   # TypedDict-контракты для инструментов
└── tools/
    ├── web_search.py      # Tavily: веб-поиск
    ├── opening_stats.py   # Lichess: статистика дебюта
    └── video_search.py    # YouTube: поиск видео
```

Агент работает по схеме **ReAct-loop**: на каждом шаге LLM либо вызывает один из трёх инструментов, либо формирует финальный ответ. Максимальное число итераций — 10.

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <repo-url>
cd chess-coach-agent-bot-master/app
```

### 2. Установить зависимости

Проект использует [Poetry](https://python-poetry.org/):

```bash
pip install poetry
poetry install
```

### 3. Настроить окружение

Скопируй `example.env` в `.env` и заполни все переменные:

```bash
cp example.env .env
```

```env
BOT_TOKEN=          # Токен Telegram-бота (от @BotFather)
API_KEY=            # API-ключ для LLM (OpenRouter или другой провайдер)
LLM_MODEL=inclusionai/ling-2.6-1t:free   # Модель (можно заменить на любую OpenAI-совместимую)
BASE_URL=https://openrouter.ai/api/v1    # Base URL провайдера
TAVILY_API_KEY=     # Ключ Tavily для веб-поиска
YOUTUBE_API_KEY=    # Ключ YouTube Data API v3
LICHESS_API_TOKEN=  # Токен Lichess (нужен для Opening Explorer)
```

### 4. Запустить бота

```bash
poetry run python -m src.main
```

---

## Получение API-ключей

| Сервис | Где получить |
|---|---|
| Telegram Bot Token | [@BotFather](https://t.me/BotFather) → `/newbot` |
| OpenRouter API Key | [openrouter.ai/keys](https://openrouter.ai/keys) |
| Tavily API Key | [app.tavily.com](https://app.tavily.com) |
| YouTube Data API v3 | [Google Cloud Console](https://console.cloud.google.com) → APIs & Services |
| Lichess API Token | [lichess.org/account/oauth/token](https://lichess.org/account/oauth/token) (scope: не требуется) |

---

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Начать диалог (сбрасывает историю) |
| `/help` | Список возможностей бота |
| `/reset` | Очистить историю текущего чата |

Любое другое сообщение передаётся агенту. Примеры запросов:

```
Какой дебют учить? Рейтинг 900, играю белыми.
Расскажи про Сицилианскую защиту.
Найди последнее видео GothamChess.
Что такое гамбит?
```

---

## Инструменты агента

### `web_search(query)`
Поиск в интернете через Tavily. Используется для нахождения UCI-ходов дебюта и подбора рекомендаций.

### `get_opening_stats(opening_name, moves)`
Запрашивает статистику из Lichess Opening Explorer по UCI-ходам дебюта. Возвращает процент побед белых/чёрных/ничьих, количество партий и топ-3 продолжения. Фильтрует партии рейтинга 1000–1600 в форматах blitz, rapid, classical.

### `find_video(query, order)`
Ищет видео через YouTube Data API. Параметр `order`: `relevance` (по умолчанию) или `date` (для поиска новых видео). Возвращает до 3 результатов.

---

## Требования

- Python 3.13–3.14
- Poetry ≥ 2.0

---

## Зависимости
- "pydantic (>=2.4.1,<2.13)",
- "aiogram (>=3.27.0,<4.0.0)",
- "openai (>=2.32.0,<3.0.0)",
- "pydantic-settings (>=2.14.0,<3.0.0)",
- "tavily-python (>=0.7.23,<0.8.0)"

---

## Разработка

Линтинг кода через [Ruff](https://docs.astral.sh/ruff/):

```bash
poetry run ruff check src/
poetry run ruff format src/
```
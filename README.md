# Компьютерный магазин «Pixel» 🖥️

Веб-приложение управления компьютерным магазином.
Работает в **Docker без X11** и любых GUI-зависимостей.

## Стек

| Компонент | Технология |
|-----------|-----------|
| HTTP-сервер | FastAPI + uvicorn |
| БД | SQLite |
| Фронтенд | HTML5 + CSS3 + Vanilla JS |
| Контейнер | Docker / Docker Compose |

## Быстрый старт

### Docker (рекомендуется — работает везде)

```bash
docker compose up --build
# Открыть http://localhost:8000
```

### Локально

```bash
make install    # создать .venv и установить зависимости
make run        # http://localhost:8000
```

## Тесты

```bash
make test       # все тесты (pytest)
make coverage   # с отчётом покрытия
```

## Функциональность

| Страница | Возможности |
|----------|------------|
| 📊 Дашборд | Выручка 30 дн., средний чек, ТОП-5 товаров, рейтинг сотрудников, выручка по категориям |
| 📦 Товары | Каталог, поиск, фильтр по категории, сортировка, пополнение склада |
| 🛒 Заказы | Создание чека, детальный просмотр, оплата, отмена, фильтр по статусу |
| 📉 Отчёты | Критические остатки, сводка всех чеков |
| 👥 Клиенты | Список, добавление нового клиента |
| 👔 Сотрудники | Список штата |
| 🏭 Поставщики | Список поставщиков |

## API

| Группа | Эндпоинты |
|--------|----------|
| Products | GET `/api/products/`, `/available`, `/low-stock`, `/search`, `/by-category/{id}` · POST `/restock` |
| Orders | GET `/`, `/unpaid`, `/{id}` · POST `/`, `/{id}/pay`, `/{id}/cancel` |
| Analytics | GET `/summary`, `/top-products`, `/monthly-revenue`, `/order-sums`, `/employee-efficiency`, `/revenue-by-category` |
| Customers | GET/POST `/api/customers/` |
| Employees | GET `/api/employees/` |
| Suppliers | GET `/api/suppliers/` |
| Categories | GET `/api/categories/` |

Swagger UI: **http://localhost:8000/docs**

## Структура репозитория

```
pixel-web/
├── app/
│   ├── main.py            # FastAPI + middleware
│   ├── dependencies.py    # DB dependency
│   ├── routers/           # products, orders, analytics, customers, employees, suppliers, categories
│   ├── static/css/        # reset, vars, layout, components, responsive
│   ├── static/js/         # api.js, ui.js, app.js, pages/
│   └── templates/         # index.html (SPA)
├── packages/core/         # бизнес-логика (без FastAPI)
│   ├── database.py        # подключение, схема, демо-данные
│   ├── products.py        # товары, остатки
│   ├── orders.py          # заказы, оплата, отмена
│   ├── analytics.py       # отчёты и агрегаты
│   ├── customers.py
│   ├── employees.py
│   ├── suppliers.py
│   └── categories.py
├── tests/                 # pytest (core + HTTP)
├── Dockerfile
├── compose.yaml
└── Makefile
```

## Makefile

```
make install      создать окружение
make run          сервер разработки
make test         pytest
make coverage     отчёт покрытия
make docker-build собрать образ
make compose-up   запустить в Docker
make compose-down остановить
make doks         проверить наличие документации
make clean        удалить кэши
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|-----------|-------------|----------|
| `SHOP_DB_PATH` | `shop.db` | Путь к SQLite-базе данных |

---

## PyPi

Core business logic for Pixel computer store management system.

https://test.pypi.org/project/pixel-shop-core/0.1.0/

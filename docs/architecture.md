# Архитектура - Компьютерный магазин «Pixel» (Web)

## Стек

| Слой | Технология |
|------|-----------|
| HTTP-сервер | FastAPI + uvicorn |
| Шаблоны | Jinja2 (один HTML-файл, SPA) |
| Фронтенд | Vanilla JS + Fetch API |
| Хранилище | SQLite (файл в Docker volume) |
| Контейнер | Docker / Docker Compose |

## Структура проекта

```
pixel-web/
├── app/
│   ├── main.py            # FastAPI app, подключение роутеров
│   ├── dependencies.py    # DB-зависимость (get_db)
│   ├── routers/           # Один файл = один ресурс
│   │   ├── products.py    # GET/POST /api/products
│   │   ├── orders.py      # GET/POST /api/orders
│   │   ├── analytics.py   # GET /api/analytics
│   │   ├── customers.py   # GET/POST /api/customers
│   │   └── employees.py   # GET /api/employees
│   ├── static/
│   │   ├── css/           # reset, vars, layout, components
│   │   └── js/
│   │       ├── api.js     # fetch-обёртка
│   │       ├── ui.js      # toast, modal, rub, navigate
│   │       ├── app.js     # bootstrap, sidebar
│   │       └── pages/     # products, orders, analytics, ...
│   └── templates/
│       └── index.html     # SPA-оболочка
├── packages/core/         # Бизнес-логика (нет зависимости от FastAPI)
│   ├── database.py
│   ├── products.py
│   ├── orders.py
│   ├── analytics.py
│   ├── customers.py
│   └── employees.py
├── tests/                 # pytest + httpx TestClient
├── Dockerfile
├── compose.yaml
└── Makefile
```

## Поток запроса

```
Браузер → GET /api/products/
  └→ FastAPI router products.py
      └→ packages.core.products.get_all(conn)
          └→ SQLite SELECT
              └→ JSON response → JS рендерит таблицу
```

## 🗺️ Варианты использования (Use-Cases)

Диаграмма вариантов использования описывает ключевые сценарии взаимодействия пользователей с системой компьютерного магазина "Pixel".

[Диаграмма Use-Case](docs/diagrams/use-cases.png)

Исходник диаграммы в редактируемом векторном формате сохранен в репозитории по пути: `docs/diagrams/use-cases.drawio`.
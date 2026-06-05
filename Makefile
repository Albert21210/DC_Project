.DEFAULT_GOAL := help
PYTHON      ?= python3
VENV        ?= .venv
PY          := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
PYTEST      := $(VENV)/bin/pytest
UV          := $(VENV)/bin/uvicorn

help:
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*##"};{printf "  \033[36m%-18s\033[0m %s\n",$$1,$$2}'

venv:           ## Создать виртуальное окружение
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv   ## Установить зависимости и локальные пакеты
	$(PIP) install -r requirements.txt -r requirements-dev.txt
	$(PIP) install -e ./packages/core  ## Фиксируем установку переиспользуемого компонента

run:            ## Запустить сервер разработки локально (http://localhost:8000)
	$(UV) app.main:app --reload --host 0.0.0.0 --port 8000

test:           ## Запустить тесты
	$(PYTEST) tests/ -v

coverage:       ## Тесты с отчётом покрытия
	$(PYTEST) tests/ --cov=packages/core --cov-report=term-missing

lint:           ## Проверка стиля кода (flake8)
	$(VENV)/bin/flake8 app/ packages/ --max-line-length=100

docker-build:   ## Собрать Docker-образ приложения
	docker build -t pixel-shop:latest .

compose-up:     ## Запустить всё окружение через Docker Compose
	docker compose up --build -d

compose-logs:   ## Посмотреть логи контейнеров
	docker compose logs -f

compose-down:   ## Остановить контейнеры
	docker compose down

reset-db:       ## Полный сброс базы данных и очистка Docker томов (С чистого листа)
	docker compose down -v
	rm -rf .coverage htmlcov/

clean:          ## Удалить кэши разработки и временные файлы
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/ .pytest_cache/
	@echo "Локальный кэш очищен."

.PHONY: help venv install run test coverage lint docker-build compose-up compose-logs compose-down reset-db clean
.DEFAULT_GOAL := help

PYTHON      ?= python
VENV        ?= .venv
PY          := $(VENV)/Scripts/python.exe
PIP         := $(VENV)/Scripts/pip.exe
PYTEST      := $(VENV)/Scripts/pytest.exe
UV          := $(VENV)/Scripts/uvicorn.exe

help:
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*##"};{printf "  \033[36m%-18s\033[0m %s\n",$$1,$$2}'

venv:           ## Создать виртуальное окружение
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --upgrade pip

install: venv   ## Установить зависимости
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install -r requirements-dev.txt

run:            ## Запустить сервер разработки (http://localhost:8000)
	$(UV) app.main:app --reload --host 0.0.0.0 --port 8000

test:           ## Запустить тесты
	$(PY) -m pytest tests/ -v -p no:warnings

coverage:       ## Тесты с отчётом покрытия
	$(PY) -m pytest tests/ --cov=packages/core --cov-report=term-missing

doks:     ## Проверить наличие документации
	@echo "========================================="
	@echo "Checking documentation..."
	@echo "========================================="
	@echo ""
	@echo "[Project documentation]"
	@if [ -f "README.md" ]; then \
		echo "  [OK]   README.md exists"; \
	else \
		echo "  [MISS] README.md MISSING"; \
	fi
	@if [ -f "docs/api.md" ]; then \
		echo "  [OK]   docs/api.md exists"; \
	else \
		echo "  [MISS] docs/api.md MISSING"; \
	fi
	@if [ -f "docs/architecture.md" ]; then \
		echo "  [OK]   docs/architecture.md exists"; \
	else \
		echo "  [MISS] docs/architecture.md MISSING"; \
	fi
	@echo ""
	@echo "[Test documentation]"
	@if [ -d "tests" ] && [ $$(ls -1 tests/test_*.py 2>/dev/null | wc -l) -gt 0 ]; then \
		echo "  [OK]   Tests found ($$(ls -1 tests/test_*.py 2>/dev/null | wc -l) test files)"; \
	else \
		echo "  [MISS] No test files found"; \
	fi
	@echo ""
	@echo "========================================="
	@FAIL=0; \
	if [ ! -f "README.md" ]; then FAIL=1; fi; \
	if [ ! -f "docs/api.md" ]; then FAIL=1; fi; \
	if [ ! -f "docs/architecture.md" ]; then FAIL=1; fi; \
	if [ $$FAIL -eq 0 ]; then \
		echo "  STATUS: All documentation is complete!"; \
	else \
		echo "  STATUS: Some documentation files are missing."; \
	fi
	@echo "========================================="

docker-build:   ## Собрать Docker-образ
	docker build -t pixel-shop:latest .

compose-up:     ## Запустить через Docker Compose
	docker compose up --build -d

compose-logs:   ## Посмотреть логи контейнеров
	docker compose logs -f

compose-down:   ## Остановить контейнеры
	docker compose down

reset-db:       ## Сброс БД и Docker томов
	docker compose down -v
	rm -rf .coverage htmlcov/

clean:          ## Удалить временные файлы
	rm -rf $(VENV)
	rm -rf .coverage htmlcov/ .pytest_cache/ dist/ *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

.PHONY: help venv install run test coverage docs-check docker-build compose-up compose-logs compose-down reset-db clean

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

run:            ## Запустить сервер
	$(UV) app.main:app --reload --host 0.0.0.0 --port 8000

test:           ## Запустить тесты
	$(PY) -m pytest tests/ -v

coverage:       ## Тесты с отчётом покрытия
	$(PY) -m pytest tests/ --cov=packages/core --cov-report=term-missing

clean:          ## Удалить временные файлы
	rm -rf $(VENV)
	rm -rf .coverage htmlcov/ .pytest_cache/ dist/ *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

.PHONY: help venv install run test coverage clean

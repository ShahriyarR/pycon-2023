ifdef OS
	PYTHON ?= .venv/Scripts/python.exe
	TYPE_CHECK_COMMAND ?= echo Pytype package doesn't support Windows OS
else
	PYTHON ?= .venv/bin/python
	TYPE_CHECK_COMMAND ?= ${PYTHON} -m pytype --config=pytype.cfg src
endif

SETTINGS_FILENAME = pyproject.toml

.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: clean_pyc clean_pycache ## Clean all PYC in the system

.PHONY: clean_pyc
clean_pyc: ## Cleans all *.pyc in the system
	find . -type f -name "*.pyc" -delete || true

.PHONY: clean_pycache
clean_pycache: ## Removes the __pycaches__
	find . -type d -name "*__pycache__*" -delete


install:
	${PYTHON} -m flit install --env --deps=production

install-dev:
	${PYTHON} -m flit install -s --env --deps=develop --symlink

install-flit:
	${PYTHON} -m pip install flit==3.8.0

.PHONY: run
run: ## Starts the local server with production settings
	ESMERALD_SETTINGS_MODULE=src.blog.configs.development.settings.DevelopmentAppSettings ${PYTHON} -m blog.serve

.PHONY: test
test: ## Runs the local tests with nose
	ESMERALD_SETTINGS_MODULE=src.blog.configs.testing.settings.TestingAppSettings ${PYTHON} -m pytest -s $(TESTONLY)

migrations:
	${PYTHON} -m saffier --app src.blog.main:app makemigrations

migrate:
	${PYTHON} -m saffier --app src.blog.main:app migrate

format:
	${PYTHON} -m isort src tests --force-single-line-imports --settings-file ${SETTINGS_FILENAME}
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	${PYTHON} -m black src tests --config ${SETTINGS_FILENAME}
	${PYTHON} -m isort src tests --settings-file ${SETTINGS_FILENAME}

lint:
	${PYTHON} -m flake8 --toml-config ${SETTINGS_FILENAME} --max-complexity 5 --max-cognitive-complexity=6 src
	${PYTHON} -m black src tests --check --diff --config ${SETTINGS_FILENAME}
	${PYTHON} -m isort src tests --check --diff --settings-file ${SETTINGS_FILENAME}

secure:
	${PYTHON} -m bandit -r src --config ${SETTINGS_FILENAME}
	pip-audit .
	${PYTHON} -m safety check

ifndef VERBOSE
.SILENT:
endif
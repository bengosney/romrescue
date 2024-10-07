.PHONY: help clean test install all init css js assets watch
.DEFAULT_GOAL := install
.PRECIOUS: requirements.%.in

HOOKS=$(.git/hooks/pre-commit)
REQS=$(wildcard requirements.*.txt)

SYSTEM_PYTHON_VERSION:=$(shell ls /usr/bin/python* | grep -Eo '[0-9]+\.[0-9]+' | sort -V | tail -n 1)
PYTHON_VERSION:=$(shell python --version | cut -d " " -f 2)
UV_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/uv
PIP_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pip
WHEEL_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/wheel
PRE_COMMIT_PATH:=.direnv/python-$(PYTHON_VERSION)/bin/pre-commit

CSS_INPUTS:=$(wildcard assets/css/*.css)
CSS_OUTPUTS:=$(patsubst assets/css/%.css,romrescue/static/css/%.min.css,$(CSS_INPUTS))
ALL_CSS:=$(shell find assets/css -type f -name '*.css')

JS_INPUTS:=$(wildcard assets/js/*.ts)
JS_OUTPUTS:=$(patsubst assets/js/%.ts,romrescue/static/js/%.min.js,$(JS_INPUTS))
ALL_JS:=$(shell find assets/js -type f -name '*.ts')

COG_FILES:=$(shell find assets/css -type f -name '*.css' -exec grep -l "\[\[\[cog" {} \;)

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@

.git: .gitignore
	git init

.pre-commit-config.yaml: | $(PRE_COMMIT_PATH) .git
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/.pre-commit-config.yaml > $@
	pre-commit autoupdate
	@touch $@

pyproject.toml: | $(UV_PATH)
	curl https://gist.githubusercontent.com/bengosney/f703f25921628136f78449c32d37fcb5/raw/pyproject.toml > $@
	$(UV_PATH) pip install toml
	@touch $@

requirements.%.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	@python -m uv pip compile --generate-hashes -q --extra $* -o $@ $(filter-out $<,$^)

requirements.txt: $(UV_PATH) pyproject.toml
	@echo "Builing $@"
	@python -m uv pip compile --generate-hashes -q -o $@ $(filter-out $<,$^)

.direnv: .envrc
	@touch $@ $^

.git/hooks/pre-commit: .git $(PRE_COMMIT_PATH) .pre-commit-config.yaml
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python$(SYSTEM_PYTHON_VERSION)" > $@
	@touch -d '+1 minute' $@
	@false

$(UV_PATH): $(PIP_PATH) $(WHEEL_PATH)
	python -m pip install uv
	@touch $@

$(PIP_PATH): .direnv
	python -m pip install --upgrade pip
	@touch $@

$(WHEEL_PATH): $(PIP_PATH)
	python -m pip install wheel
	@touch $@

$(PRE_COMMIT_PATH): $(UV_PATH)
	$(UV_PATH) pip install pre-commit

init: .direnv $(UV_PATH) requirements.txt requirements.dev.txt .git/hooks/pre-commit ## Initalise a enviroment
	@python -m pip install --upgrade pip

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata

reset:
	rm -rf pyproject.toml src uv.lock .pre-commit-config.yaml requirements*.txt .gitignore .venv

node_modules: package.json package-lock.json
	npm install

romrescue/static/css/%.min.css: assets/css/%.css $(ALL_CSS)
	npx lightningcss --minify --bundle --targets ">= 0.25%" $< -o $@

css: $(CSS_OUTPUTS)

romrescue/static/js/%.min.js: assets/js/%.ts $(ALL_JS)
	npx esbuild $< --bundle --minify --outfile=$@

js: $(JS_OUTPUTS)

assets: css js ## Build assets

install: installpython node_modules

installpython: $(UV_PATH) requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $(filter-out $<,$^)"
	$(UV_PATH) pip sync $(filter-out $<,$^)

watch: ## Watch assets for changes
	@echo "Watching assets"
	$(MAKE) assets
	@while inotifywait -qr -e close_write assets; do \
		$(MAKE) assets; \
	done

cog: $(COG_FILES)
	@for file in $^; do \
		cog -rc $$file; \
	done

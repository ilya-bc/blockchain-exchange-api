#################################################################################
# This Makefile is self-documented
# Use ## before target to provide a description
#################################################################################
.DEFAULT_GOAL := help

SHELL = /bin/bash

# Set context for execution of sphinx build
PIPENV_EXISTS=$(shell which pipenv || echo 0 )
ifeq ($(PIPENV_EXISTS), 0)
    PYTHON = python3
else
    PYTHON = pipenv run python
endif

#################################################################################
# INSTALL/SETUP COMMANDS                                                        #
#################################################################################
.PHONY: install install-dev

## Install this package
install:
	pipenv --python 3.7
	pipenv install .

## Install this package in editable mode with packages required for development
install-dev:
	pipenv --python 3.7
	pipenv install -e '.[dev]'
	pipenv install twine --dev

## Build for PyPi
build: clean clean-build
	$(PYTHON) setup.py sdist bdist_wheel

## Upload to PyPi Test server
upload-test-pypi: build
	$(PYTHON) -m twine upload --repository testpypi dist/*


#################################################################################
# CLEAN COMMANDS                                                                #
#################################################################################
.PHONY: clean clean-build clean-test clean-all

## Remove Python file artifacts
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

## Remove build artifacts
clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

## Remove test and coverage artifacts
clean-test:
	find . -name '*.coverage' -exec rm -f {} +
	find . -name '*.coverage.*' -exec rm -f {} +
	rm -rf .tox/
	rm -rf htmlcov/
	rm -rf .reports/
	rm -rf .pytest_cache

## Remove all build, test, coverage and Python artifacts
clean-all: clean clean-build clean-test


#################################################################################
# MISC                                                                          #
#################################################################################
.PHONY: update-readme-toc

define README_TOC_TITLE
Table of Contents
-----------------
Generated with [DocToc](https://github.com/thlorenz/doctoc)

Last Update: $(shell date +%Y-%m-%d)
endef
export README_TOC_TITLE
## Update table of contents for the main README. Requires 'doctoc' to be installed
update-readme-toc:
	doctoc --github --title "$${README_TOC_TITLE}" README.md


#################################################################################
# For self-documenting of Makefile: use '##' before target to provide a description
#
# References:
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
# https://github.com/drivendata/cookiecutter-data-science/blob/master/%7B%7B%20cookiecutter.repo_name%20%7D%7D/Makefile
#
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
#
#################################################################################
.PHONY: help

## Show this message
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=25 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

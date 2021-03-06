.PHONY: requirements environment clean test timetest archive

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = declorations
USER := $(whoami)

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## DUMP Python Dependencies [not real requirements, though]
requirements:
	conda env export > environment.yml

## Set up python interpreter environment
environment:
	conda env create -f environment.yml
	@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"

## Delete all compiled Python files
clean:
	find . -name "*.pyc" -exec rm {} \;

## Test
test:
	python -m nose;

## Test with timer
timetest:
	python -m nose --with-timer --timer-top-n 10

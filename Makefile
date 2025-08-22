# Clever – tab-free Makefile (delegates to scripts/dev.sh)
SHELL := /bin/bash
HOST ?= 0.0.0.0
PORT ?= 5000

.PHONY: setup run test urls doctor clean-venv

setup:     ; @HOST=$(HOST) PORT=$(PORT) bash scripts/dev.sh setup
run:       ; @HOST=$(HOST) PORT=$(PORT) bash scripts/dev.sh run
test:      ; @HOST=$(HOST) PORT=$(PORT) bash scripts/dev.sh test
urls:      ; @HOST=$(HOST) PORT=$(PORT) bash scripts/dev.sh urls
doctor:    ; @HOST=$(HOST) PORT=$(PORT) bash scripts/dev.sh doctor
clean-venv:; @bash scripts/dev.sh clean-venv

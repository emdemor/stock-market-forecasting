-include .env

export

PROJECT_NAME = stock_prediction
PACKAGE_NAME = stock_prediction

PWD := $(shell pwd)
JUPYTER_IMAGE := $(PROJECT_NAME)_jupyter:latest

DOCKER_IMG := $(PROJECT_NAME):latest
DOCKER_ENV := --env-file .env

DOCKER_RUN := docker run --rm -t

PYTEST := python -B -m pytest

build:
	docker build -f docker/Dockerfile -t $(DOCKER_IMG) .

start: build
	$(DOCKER_RUN) $(DOCKER_ENV) -i $(DOCKER_IMG)

shell: build
	$(DOCKER_RUN) $(DOCKER_ENV) -i --entrypoint=/bin/bash $(DOCKER_IMG)

clean:
	docker images -q $(PROJECT_NAME)* | xargs -I {} docker rmi -f {}

mypy: build
	$(DOCKER_RUN) $(DOCKER_IMG) mypy src tests

flake: build
	$(DOCKER_RUN) $(DOCKER_IMG) flake8 src tests

bandit: build
	$(DOCKER_RUN) $(DOCKER_IMG) bandit src tests

format:
	black src tests

lint: mypy flake bandit

check:
	$(DOCKER_RUN) $(DOCKER_IMG) $(PYTEST) tests/unit

build-jupyter:
	docker build -f docker/Dockerfile.jupyter -t $(JUPYTER_IMAGE) .

start-jupyter: build-jupyter
	docker run $(DOCKER_ENV) -p 8888:8888 -v $(PWD):/app $(JUPYTER_IMAGE) &
	sleep 5
	xdg-open http://localhost:8888/lab

.PHONY: all test clean
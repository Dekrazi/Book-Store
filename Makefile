.ONESHELL:

.DEFAULT_GOAL := run

PYTHON = env/bin/python
PIP = env/bin/pip
IMAGE = dekrazi/book-store
TAG = latest

env/bin/activate: requirements.txt
	python3 -m venv env
	chmod +x env/bin/activate
	. ./env/bin/activate && $(PIP) install -r requirements.txt

env: env/bin/activate

run: env
	. ./env/bin/activate && $(PYTHON) manage.py runserver

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf env

docker-login:
	@echo -n "Docker Username: "; \
	read DOCKER_LOGIN_USERNAME; \
	echo -n "Docker Password: "; \
	stty -echo; \
	read DOCKER_LOGIN_PASSWORD; \
	stty echo; \
	echo ""; \
	echo "Logging in to Docker registry..."; \
	docker login -u $$DOCKER_LOGIN_USERNAME -p $$DOCKER_LOGIN_PASSWORD $(DOCKER_LOGIN_REGISTRY); \
	echo "Docker login successful."


docker-build:
	docker build . -t ${IMAGE}:${TAG}

docker-push: docker-login
	docker push ${IMAGE}:${TAG}

docker-clean:
	docker rmi ${IMAGE}:${TAG}



.PHONY: env run docker-build docker-push docker-clean clean

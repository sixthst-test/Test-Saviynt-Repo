buildenv?=dev
include buildenv/$(buildenv)

CLUSTER=FederationECS
NAME=hello-api
PYPACKAGE_NAME=hello_api

DOCKER_REGISTRY=sstp.jfrog.io/sstp-docker-images
CONTAINER_REPO=$(DOCKER_REGISTRY)/$(NAME)
# Consider getting rid of this variable and always having VERSION available as an environment variable
PYPROJECT_VERSION=$(shell poetry version --short)
FAMILY=HelloApi
LOG_GROUP=/fargate/$(FAMILY)
LOG_STREAM_PREFIX=$(NAME)
ROLE=$(FAMILY)ServiceRole


update-service: build/task.json
	aws ecs register-task-definition --cli-input-json file://build/task.json
	aws ecs update-service \
		--cluster $(CLUSTER) \
		--service $(FAMILY)Service \
		--task-definition $(FAMILY) \
		--desired-count 2 \
		--propagate-tags TASK_DEFINITION

build/task.json: task.json.in
	mkdir -p build
	export \
		CONTAINER_REPO=$(CONTAINER_REPO) \
		VERSION=$(VERSION) \
		LOG_GROUP=$(LOG_GROUP) \
		LOG_STREAM_PREFIX=$(LOG_STREAM_PREFIX) \
		FAMILY=$(FAMILY) \
		ROLE=$(ROLE) \
		ACCOUNT=$(ACCOUNT) \
		LOGURU_LEVEL=$(LOGURU_LEVEL) \
		SSTP_ENVIRONMENT=$(SSTP_ENVIRONMENT) \
		HONEYCOMB_DATASET=$(HONEYCOMB_DATASET) \
		AWS_EMF_NAMESPACE=$(AWS_EMF_NAMESPACE) \
		AWS_EMF_LOG_GROUP_NAME=$(AWS_EMF_LOG_GROUP_NAME) \
		ARTIFACTORY_SECRET_NAME=$(ARTIFACTORY_SECRET_NAME) \
		HONEYCOMB_SECRET_NAME=$(HONEYCOMB_SECRET_NAME) \
		OTEL_SDK_DISABLED=$(OTEL_SDK_DISABLED) \
	&& cat task.json.in | envsubst > build/task.json

clean:
	rm -rf build

build/venv: poetry.lock pyproject.toml
	python -m venv build/venv
	. build/venv/bin/activate && \
		poetry install && \
		touch build/venv

run: build/venv
	OTEL_SDK_DISABLED=true build/venv/bin/uvicorn $(PYPACKAGE_NAME).__main__:app  --reload

unit-test: build/venv
	OTEL_SDK_DISABLED=true ./build/venv/bin/pytest tests/ --cov $(PYPACKAGE_NAME)

lint: build/venv
	build/venv/bin/ruff check src/ --exit-zero
	build/venv/bin/pylint src/ tests --output-format=parseable --exit-zero

mypy: build/venv
	build/venv/bin/mypy --check-untyped-defs src/

static-analysis: lint mypy

format: build/venv
	. ./build/venv/bin/activate && \
		ruff check src/ --select I,E,W --fix --exit-zero && \
		black src/ tests/

docker-scan:
	docker scan $(NAME)

docker-build:
	docker build . \
		--build-arg PIP_INDEX_URL=${PIP_INDEX_URL} \
		--build-arg POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_USERNAME=${POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_USERNAME} \
		--build-arg POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_PASSWORD=${POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_PASSWORD} \
		--tag $(NAME):$(PYPROJECT_VERSION)

docker-run: docker-build
	docker run -d \
		--name $(NAME) \
		--env DEV_MODE=docker \
		--env LOG_FORMAT=notJSON \
		--platform=linux/amd64 \
		--interactive --tty \
		--rm \
		--publish 8000:80 $(NAME):$(VERSION)

docker-push:
	docker tag $(NAME):$(PYPROJECT_VERSION) $(CONTAINER_REPO):$(PYPROJECT_VERSION)
	docker push $(CONTAINER_REPO):$(PYPROJECT_VERSION)

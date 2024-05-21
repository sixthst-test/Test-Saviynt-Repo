FROM --platform=linux/amd64 sstp.jfrog.io/sstp-docker-images/python:3.11.7-slim-builder AS builder

WORKDIR /app

ARG PIP_INDEX_URL
ENV PIP_INDEX_URL=$PIP_INDEX_URL
RUN pip install --upgrade pip==23.1

RUN python -m venv venv
COPY . .

ARG POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_USERNAME
ARG POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_PASSWORD
ENV POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_USERNAME=$POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_USERNAME
ENV POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_PASSWORD=$POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_PASSWORD

RUN . venv/bin/activate && \
    poetry install --without dev

FROM --platform=linux/amd64 sstp.jfrog.io/sstp-docker-images/python:3.11.7-slim AS runtime
COPY --from=builder /app /app
WORKDIR /app

ENV GUNICORN_PORT=80
CMD ["venv/bin/python", "-m" , "hello_api"]

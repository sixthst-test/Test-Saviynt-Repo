# hello-api

Minimal example of a working, Dockerized Python FastAPI app that is deployable to our Fargate clusters.
See corresponding AWS infra instantiation in
[this block in infra-federation](https://github.com/sixthst/infra-federation/blob/806be598e6a2ee04408c746c74ea5e0d295c3d26/cdk/app.py#L33-L51)
For launching a new repository, please see additional documentation located here: [Operationalize A Service]([text](https://sixthstreet-prod.atlassian.net/wiki/spaces/SSI/pages/2475655179/Operationalize+A+Service))

## Getting Started

### Use as a Template

To use this repository as a template for your own project, in GitHub.com, navigate to the main page of this repository. Above the file list, click Use this template. Select Create a new repository.
In your new repository, go to Settings > Collaborators and Teams > Manage Access, and then add SSTP-GithubServiceUser as an admin. While there, also give your github team access.
Once you have the repository, the first step is to find and replace all occurrences of hello api with your service. It's recommended to keep the dashes, underscores or camel casing consistent to avoid issues when deploying.

### Prerequisites

- A Unixy dev environment, such as Mac OS, WSL, or Linux
- Docker
- Your local python/pip is configured to pull packages from our Artifactory. See the [JFrog Artifactory](https://sixthstreet-prod.atlassian.net/wiki/spaces/DO/pages/2333310991/JFrog+Artifactory+Setup) section in the setup guide.
- Python - refer the version specified in `Dockerfile` which should match the version specified in `pyproject.toml`.
- [Poetry](https://python-poetry.org/docs/#installing-with-pipx) - refer to `poetry.lock` for the exact version.
  - The following environment variables should be configured to your Artifactory credentials:

    ```sh
    $ env | grep ^POETRY
    POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_USERNAME=username@sixthstreet.com
    POETRY_HTTP_BASIC_SSTP_ARTIFACTORY_PASSWORD=***
    ```

### Quick start

1. Use `make` to install dependencies and run the app locally

   ```sh
    make run
   ```

1. The OpenAPI docs can be accessed at [http://localhost:8000](http://localhost:8000).

### Manual Setup / Run

1. Setup virtual environment and install dependencies using poetry:

    ```sh
    [~/hello-api] $ python3 -m venv venv --prompt hello-api
    [~/hello-api] $ source ./venv/bin/activate
    (hello-api) [~/hello-api] $ poetry install
    Installing dependencies from lock file

    Package operations: 36 installs, 0 updates, 0 removals

    • Installing idna (3.4)
    [...]
    • Installing uvicorn (0.21.1)

    Installing the current project: hello-api (1.0.0)
    ```

1. Run the API process using uvicorn. Using the `--reload` option will refresh the process automatically on any change in the source or dependencies. This is the simplest way to run & debug the app locally (using CLI or VSCode).

    ```sh
    (hello-api) [~/hello-api] $ uvicorn hello_api:app  --reload
    INFO:     Will watch for changes in these directories: ['~/hello-api']
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [57639] using StatReload
    INFO:     Started server process [57641]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ```

    - The alternate way to run is to use `gunicorn`, as shown below. This is how the app is run on deployment.

        ```sh
        (hello-api) [~/hello-api] $ LOG_FORMAT='' python -m hello_api
        2023-04-10 10:19:48.075 | INFO     | logging:callHandlers:1706 - Starting gunicorn 20.1.0 - {'application': 'hello-api', 'request_id': '', 'trace_id': '', 'instance_id': UUID('884d2d8f-8aee-4785-950d-b0af671b8aba')}
        2023-04-10 10:19:48.076 | INFO     | logging:callHandlers:1706 - Listening at: http://0.0.0.0:8000 (57984) - {'application': 'hello-api', 'request_id': '', 'trace_id': '', 'instance_id': UUID('884d2d8f-8aee-4785-950d-b0af671b8aba')}
        [...]
        2023-04-10 10:19:48.262 | INFO     | logging:callHandlers:1706 - Application startup complete. - {'application': 'hello-api', 'request_id': '', 'trace_id': '', 'instance_id': UUID('884d2d8f-8aee-4785-950d-b0af671b8aba')}
        ```

### Adding new dependencies

Since poetry is used to manage the project's dependencies, you should use the [CLI](https://python-poetry.org/docs/cli/) to add dependencies.

Runtime dependencies can be added as shown:

```sh
(hello-api) [~/hello-api] $ poetry add httpx
Using version ^0.24.0 for httpx

Updating dependencies
Resolving dependencies...
Resolving dependencies... (2.3s)

Writing lock file

Package operations: 3 installs, 0 updates, 0 removals

  • Installing certifi (2022.12.7)
  • Installing httpcore (0.17.0)
  • Installing httpx (0.24.0)
```

Development dependencies (such as pytest or mypy) can be added as shown:

```sh
(hello-api) [~/hello-api] $ poetry add mypy --group=dev
Using version ^1.2.0 for mypy

Updating dependencies
Resolving dependencies... (0.1s)

Writing lock file

Package operations: 1 install, 0 updates, 0 removals

  • Installing mypy (1.2.0)
```

Both `pyproject.toml` and `poetry.lock` should be checked in to ensure consistency between development & deployments.

### Make targets for local development

- Run unit tests

    ```sh
    make unit-test
    ```

- Run static analysis (PyLint & mypy)

    ```sh
    make static-analysis
    ```

- Build and run the Docker image

    ```sh
    make docker-build
    make docker-run
    ```

- Format the code to our standards

    ```sh
    make format
    ```

### Other make targets

These are used by the CI/CD machinery and would seldom be used directly by a developer

Push the docker image up to Artifactory, our private Docker registry

```sh
make docker-push
```

Update the running service with the latest image

```sh
make update-service
```

### Opentelemetry

By default, Opentelemetry tracing and metrics export is configured. If you want to disable, please pass in

```shell
OTEL_SDK_DISABLED=true
```

*Note:* This requires you to run the app with your `venv` and `uvicorn hello_api:app  --reload` instead of `make run` since that uses Docker.

This will prevent the warning log messages to the console.
However, in case you wanted to see the traces that were being published, start up the docker compose file set up for
local development for otel like so

```shell
docker-compose -f docker-compose-otel.yaml up
```

This will stop the connection error warning messages.

- Jaeger can be accessed at <http://localhost:16686>
- Prometheus can be accessed at <http://localhost:8889/metrics>


## REFERENCES

1. [Poetry Repositories](https://python-poetry.org/docs/repositories/)
1. [PIPX](https://pypa.github.io/pipx/)

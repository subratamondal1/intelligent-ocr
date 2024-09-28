<h1> <center>Optical Character Recognition (OCR)</center> </h1>

---

# Makefile Commands

The `Makefile` provides a set of common commands to manage the development and deployment workflow for the project. Below is a list of the available commands and their purposes.

## Installation
To set up the Python environment and install the required packages:

```bash
make install
```

This command will:
- Upgrade `pip`.
- Install all packages specified in `requirements.txt`.

## Linting
To lint the codebase and automatically fix issues based on the configuration in `pyproject.toml`:

```bash
make lint
```

This command uses **Ruff** to:
- Check for code quality issues.
- Apply fixes according to the settings in `pyproject.toml`.

## Formatting
To format code according to the rules specified in `pyproject.toml`:

```bash
make format
```

This command utilizes **Ruff** to:
- Format all Python files based on the styles defined in `pyproject.toml`.

## Testing
To run tests and ensure the code is functioning as expected:

```bash
make test
```

This command will:
- Execute the test suite for the project.
- Ensure code coverage meets the desired threshold.

> **Note**: Ensure that the test runner and any required configurations are set up properly for smooth execution.

## Building Docker Image
To build a Docker image for the application:

```bash
make build
```

This command will:
- Package the application into a Docker container.
- Use a `Dockerfile` to create the image.

## Running Docker Container
To run the Docker container created from the image:

```bash
make run
```

This command will:
- Start a Docker container based on the built image.
- Run the application in an isolated environment.

## Deployment
To set up Azure deployment with Docker:

```bash
make deploy
```

This command will:
- Authenticate with Azure.
- Deploy the Docker container to the specified Azure service.

---
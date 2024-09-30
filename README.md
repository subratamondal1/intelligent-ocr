<h1> <center>Optical Character Recognition (OCR)</center> </h1>

---

<img src="assets/images/MeraMaster OCR.png"/>

---

# Makefile Commands

The `Makefile` provides a set of common commands to manage the development and deployment workflow for the project. Below is a list of the available commands and their purposes.

```Makefile
install:
	# Install Package Installer for Python
	pip install --upgrade pip && pip install -r requirements.txt

lint:
	# Lint Code with Ruff using pyproject.toml
	ruff check . --fix --config pyproject.toml

format:
	# Format Code with Ruff Formatter using pyproject.toml
	ruff format . --config pyproject.toml

test:
	# Test Code

build:
	# Build Docker Image
	
run:
	# Run Docker Container
	
deploy:
	# Azure Deployment Setup with Docker
```

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

# Continuous Integration with GitHub Actions

This project uses GitHub Actions to automate CI workflows, including installing dependencies, linting code, running tests, and building a Docker container.

## Workflow Overview

The CI workflow is triggered on **push** and **pull request** events, except for changes in certain files (`*.lock`, `*.toml`, and `README.md`), which are ignored.

### Workflow File: `.github/workflows/ci.yml`

```yaml
name: OCR

on:
  push:
    paths-ignore:
      - "**/*.lock"
      - "**/*.toml"
      - "**/README.md"

  pull_request:
    paths-ignore:
      - "**/*.lock"
      - "**/*.toml"
      - "**/README.md"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: 3.12
          cache: 'pip'

      - name: Install dependencies
        run: make install

      - name: Lint code with ruff
        run: make lint

      - name: Format code with ruff
        run: make format

      - name: Test with pytest
        run: make test

      - name: Build Docker Container
        run: make build
```

## Job Details

The workflow is divided into a series of steps, each responsible for a different part of the CI process:

### 1. **Checkout Code**
```yaml
- uses: actions/checkout@v4
```
This step checks out the repository code to the runner environment.

### 2. **Set Up Python Environment**
```yaml
- name: Set up Python 3.12
  uses: actions/setup-python@v5
  with:
    python-version: 3.12
    cache: 'pip'
```
Uses `actions/setup-python@v5` to install and set up Python 3.12. Pip caching is enabled to speed up the installation of dependencies.

### 3. **Install Dependencies**
```yaml
- name: Install dependencies
  run: make install
```
Installs all necessary dependencies for the project using the `make install` command.

### 4. **Lint Code**
```yaml
- name: Lint code with ruff
  run: make lint
```
Uses `ruff` to check for code quality and linting issues, with the command `make lint`.

### 5. **Format Code**
```yaml
- name: Format code with ruff
  run: make format
```
Formats the code using `ruff`, ensuring a consistent style throughout the codebase.

### 6. **Run Tests**
```yaml
- name: Test with pytest
  run: make test
```
Runs the test suite using `pytest` to ensure that the code is functioning as expected.

### 7. **Build Docker Container**
```yaml
- name: Build Docker Container
  run: make build
```
Builds a Docker image of the application using the `make build` command.

This CI workflow helps ensure code quality, consistent formatting, and that all tests pass before any changes are merged into the main codebase. 

---
# API Test Automation Framework

A robust, production-ready API test automation framework built with Python, Pytest, and the Requests library. This framework demonstrates professional software engineering practices including reusable components, comprehensive test coverage, data-driven testing, and CI/CD integration.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running Tests](#running-tests)
- [Generating Test Reports](#generating-test-reports)
- [Design Decisions](#design-decisions)
- [CI/CD Integration](#cicd-integration)
- [ Extending the Framework](#extending-the-framework)

## Overview

This API testing framework provides a scalable foundation for testing RESTful APIs with a focus on maintainability, readability, and comprehensive coverage. It leverages Pytest's powerful features including fixtures, parametrization, and custom plugins to create a professional-grade test automation solution.

The framework is designed with a clean architecture that separates test logic from implementation details, making it easy to maintain and extend as API requirements evolve.

## Features

- **Reusable API Client**: Custom APIClient class wrapping Requests library with built-in logging and error handling
- **Data-Driven Testing**: Pytest parametrization for testing multiple payload variations
- **JSON Schema Validation**: Validates API responses against defined schemas
- **Comprehensive Error Handling**: Custom APIError exceptions for robust test validation
- **Code Quality**: Ruff linter for Python code style and quality checks
- **CI/CD Ready**: GitHub Actions and Jenkins pipeline configurations included
- **Professional Reporting**: HTML and Allure reports with pytest-html and allure-pytest
- **Clean Architecture**: Separation of concerns with utilities, config, and test directories

## Project Structure

```
api-testing-framework/
├── .github/
│   └── workflows/
│       └── api-tests.yml          # GitHub Actions CI/CD pipeline
├── config/
│   ├── __init__.py                 # Package initializer
│   └── settings.json              # API configuration (base URL, timeout, headers)
├── tests/
│   ├── __init__.py                 # Package initializer
│   └── test_post_api.py           # Comprehensive test suite
├── utilities/
│   ├── __init__.py                 # Package initializer
│   └── api_helpers.py             # APIClient class and configuration loader
├── reports/
│   └── .gitkeep                   # Directory for generated reports
├── .gitignore                      # Git ignore rules
├── Jenkinsfile                     # Jenkins CI/CD pipeline
├── conftest.py                     # Pytest configuration and fixtures
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

### Directory Descriptions

| Directory/File | Purpose |
|----------------|---------|
| `config/` | Configuration files for API endpoints, timeouts, and headers |
| `tests/` | Pytest test files organized by feature/module |
| `utilities/` | Reusable helper classes and functions |
| `reports/` | Generated test reports and logs |
| `conftest.py` | Pytest configuration, fixtures, and hooks |

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git for version control

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd api-testing-framework
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and update with your configuration:

```bash
cp .env.example .env
```

Edit `.env` with your API configuration:

```env
BASE_URL=https://jsonplaceholder.typicode.com
TIMEOUT=30
RETRIES=3
CONTENT_TYPE=application/json
```

The `.env` file is included in `.gitignore` to protect sensitive information.

The installed packages include:

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.0+ | Testing framework |
| requests | 2.28.0+ | HTTP client for API calls |
| pytest-html | 4.0.0+ | HTML report generation |
| pytest-reportlog | 1.0.0+ | Test result logging |
| pytest-xdist | 3.0.0+ | Parallel test execution |
| allure-pytest | 2.11.0+ | Allure report generation |
| jsonschema | 4.20.0+ | JSON schema validation |
| responses | 0.21.0+ | API mocking for testing |

## Running Tests

### Basic Test Execution

Run all tests in the test suite:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run tests with detailed tracebacks:

```bash
pytest -v --tb=short
```

### Parallel Test Execution

Run tests in parallel using pytest-xdist with 4 workers:

```bash
pytest -n 4 -v
```

The number of workers can be adjusted based on your machine's CPU cores:

```bash
pytest -n auto      # Automatically use all available cores
pytest -n 2         # Use 2 workers
pytest -n 8         # Use 8 workers (for powerful machines)
```

Parallel execution provides:

- **Faster Test Execution**: Tests run concurrently across multiple processes
- **Better Resource Utilization**: Leverages multiple CPU cores
- **Scalable Testing**: Ideal for large test suites

Note: Some tests may not be suitable for parallel execution due to shared state. The framework uses session-scoped fixtures to minimize conflicts.

### Run Specific Tests

Run a specific test file:

```bash
pytest tests/test_post_api.py
```

Run tests matching a pattern:

```bash
pytest -k "create"    # Run tests with "create" in name
pytest -k "Post"      # Run tests in TestPostEndpoint class
```

Run a specific test method:

```bash
pytest tests/test_post_api.py::TestPostEndpoint::test_create_post_returns_correct_status_code
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--base-url` | Override the base URL from config |
| `--timeout` | Set custom request timeout in seconds |
| `-v` | Verbose output |
| `-k` | Filter tests by keyword |
| `-x` | Stop on first failure |
| `--maxfail=N` | Stop after N failures |

## Generating Test Reports

### HTML Report

Generate a self-contained HTML report with all test results:

```bash
pytest --html=reports/report.html --self-contained-html
```

The HTML report includes:

- Test summary (passed, failed, skipped, errors)
- Detailed test execution times
- Environment information
- Interactive filtering and sorting

### JSON Report Log

Generate a JSON log file for programmatic analysis:

```bash
pytest --reportlog=reports/log.json
```

### Allure Report

Generate a comprehensive interactive test report using Allure:

```bash
pytest -v --alluredir=allure-results
allure generate allure-results --output reports/allure-report --clean
```

Or run tests and generate the report in one command:

```bash
pytest -n 4 -v --alluredir=allure-results && allure generate allure-results --output reports/allure-report --clean
```

#### Installing Allure CLI

The `allure-pytest` package provides the Pytest plugin, but you need the Allure CLI to generate reports:

**Windows (using Chocolatey):**
```bash
choco install allure
```

**macOS (using Homebrew):**
```bash
brew install allure
```

**Linux (using wget):**
```bash
wget https://github.com/allure-framework/allure2/releases/download/2.28.0/allure-2.28.0.zip -O /tmp/allure.zip
unzip /tmp/allure.zip -d /opt/
ln -sf /opt/allure-2.28.0/bin/allure /usr/bin/allure
```

**Docker:**
```bash
docker run --rm -v $(pwd):/allure-results allure/2.28.0 generate allure-results --output /allure-report --clean
```

The Allure report includes:

- **Interactive Dashboard**: Visual test execution summary with charts and statistics
- **Test Structure**: Hierarchical view of test cases, classes, and modules
- **Step-by-Step Execution**: Detailed breakdown of each test with all assertions
- **Attachments**: Screenshots, logs, and other artifacts
- **Flaky Test Detection**: Identifies tests with inconsistent results
- **Timeline View**: Visual representation of test execution order and duration

### Combining Commands

Run tests and generate multiple reports:

```bash
pytest -v --html=reports/report.html --self-contained-html --reportlog=reports/log.json --alluredir=allure-results
```

For parallel execution with Allure:

```bash
pytest -n 4 -v --alluredir=allure-results
allure generate allure-results --output reports/allure-report --clean
```

## Design Decisions

### API Client Pattern

**Why a custom APIClient class?**

While the Requests library is powerful, directly using `requests.get()`, `requests.post()`, etc. throughout test files leads to:

1. **Code Duplication**: Common patterns like header management and error handling repeated across tests
2. **Tight Coupling**: Tests directly dependent on Requests implementation details
3. **Maintenance Burden**: Changing authentication, headers, or error handling requires updates across all tests

**Our Solution:**

The `APIClient` class provides:

- **Single Responsibility**: HTTP operations centralized in one class
- **Consistent Behavior**: Standardized logging, error handling, and headers
- **Easy Testing**: Mockable interface for unit testing
- **Cleaner Tests**: Tests focus on test logic, not HTTP mechanics

```python
# Instead of this in every test:
response = requests.get(url, headers=headers, timeout=timeout)
response.raise_for_status()
data = response.json()

# We write this:
data = api_client.get("/endpoint")
```

### Pytest Parametrization for Data-Driven Testing

**Why parametrize tests?**

1. **Test Coverage**: Validate multiple payload variations with minimal code
2. **Maintainability**: Add new test cases by updating data, not writing new tests
3. **Readability**: Clear separation of test logic and test data
4. **Efficiency**: Single test method runs multiple times with different inputs

**Implementation:**

```python
VALID_POST_PAYLOADS = [
    {"title": "First", "body": "Content", "userId": 1},
    {"title": "Second", "body": "More content", "userId": 2},
    # ... more payloads
]

@pytest.mark.parametrize("payload", VALID_POST_PAYLOADS)
def test_create_post_with_different_payloads(self, api_client, payload):
    response = api_client.post("/posts", json=payload)
    assert response["title"] == payload["title"]
```

This pattern tests 5 different payloads with a single test method, generating 5 separate test results in the report.

### JSON Schema Validation

**Why validate against schemas?**

API contracts can change, and schema validation provides:

1. **Contract Enforcement**: Ensures API response matches expected structure
2. **Regression Detection**: Catches unexpected field additions/removals
3. **Documentation**: Schemas serve as living documentation
4. **Type Safety**: Validates field types (string, integer, boolean, etc.)

**Implementation:**

```python
POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"}
    },
    "required": ["userId", "id", "title", "body"]
}

validate(instance=response, schema=POST_SCHEMA)
```

### Configuration Management

**Why externalize configuration?**

- **Environment Flexibility**: Run tests against dev, staging, or prod without code changes
- **CI/CD Compatibility**: Override values via environment variables or pipeline parameters
- **Team Collaboration**: Shared configuration with optional overrides

**Implementation:**

```json
{
  "base_url": "https://jsonplaceholder.typicode.com",
  "timeout": 30,
  "retries": 3,
  "headers": {
    "Content-Type": "application/json"
  }
}
```

Command line options allow runtime overrides:

```bash
pytest --base-url https://staging-api.example.com
```

### Parallel Test Execution

**Why use parallel execution?**

Test suites can grow large over time, and sequential execution becomes a bottleneck. Pytest-xdist provides:

- **Reduced Feedback Loop**: Tests complete faster, enabling rapid iteration
- **Resource Optimization**: Uses multiple CPU cores effectively
- **Scalable Testing**: Scales from local development to CI/CD environments

**Implementation:**

```bash
pytest -n 4           # 4 workers for balanced performance
pytest -n auto        # Auto-detect optimal worker count
```

The framework uses session-scoped fixtures to ensure parallel tests don't interfere with each other.

## CI/CD Integration

### GitHub Actions

The `.github/workflows/api-tests.yml` file defines a workflow that:

- Runs on push and pull request to `main` and `master` branches
- Sets up Python 3.11 environment
- Installs dependencies from `requirements.txt`
- Sets environment variables from GitHub Secrets (BASE_URL, TIMEOUT, etc.)
- Executes the test suite with parallel execution (4 workers)
- Generates Allure and HTML reports
- Uploads reports as artifacts (retained for 30 days)

### Jenkins Pipeline

The `Jenkinsfile` defines a declarative pipeline with stages:

1. **Checkout**: Retrieve source code
2. **Install Dependencies**: Setup Python environment and install packages
3. **Install Allure CLI**: Download and install Allure for report generation
4. **Run Tests**: Execute pytest with parallel execution (4 workers)
5. **Generate Allure Report**: Create and archive Allure report
6. **Generate HTML Report**: Create and archive HTML report

Environment variables can be set in Jenkins credentials or pipeline configuration.

## Extending the Framework

### Adding New Tests

1. Create a new file in `tests/` following the naming convention `test_*.py`
2. Import required fixtures and utilities
3. Write test classes and methods following the existing patterns

### Adding New Endpoints

1. Add JSON schemas for new endpoints in `tests/test_endpoints.py`
2. Create test methods using the `api_client` fixture
3. Follow existing test patterns for validation

### Adding Custom Utilities

Add reusable helper functions in `utilities/`:

```python
def validate_email_format(email):
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def generate_unique_id():
    """Generate a unique identifier for test data."""
    return str(uuid.uuid4())[:8]
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and add tests
3. Run the test suite: `pytest -v`
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Open a Pull Request

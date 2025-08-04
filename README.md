# Python Playwright Test Suite

## Overview
This project automates smoke test scenarios for given website (https://epam.com/careers in this case) using Playwright with Python.

## Features
- Search and filter test scenarios
- Mobile/responsive view validation
- Allure report integration
- Docker-ready + GitHub Actions CI

## Detailed Test Running Guide

### Basic Test Execution

1. Run all tests:
```bash
pytest --alluredir=allure-results
```

2. View the report:
```bash
allure serve allure-results
```

### Running Tests by Severity
The tests are marked with different severity levels using Allure. You can run tests based on their severity:

```bash
# Run only critical tests
pytest --alluredir=allure-results -v -k "severity='critical'"

# Run only normal severity tests
pytest --alluredir=allure-results -v -k "severity='normal'"

# Run both critical and normal tests
pytest --alluredir=allure-results -v -k "severity in ['critical', 'normal']"
```

### Running Tests by Feature
Tests are organized by features. You can run specific features:

```bash
# Run only job filter tests
pytest --alluredir=allure-results -v -k "feature='Job Filters'"

# Run only search functionality tests
pytest --alluredir=allure-results -v -k "feature='Job Search'"

# Run only responsive design tests
pytest --alluredir=allure-results -v -k "feature='Responsive Design'"
```

### Running Tests by Story
Each feature contains multiple stories. Run specific test stories:

```bash
# Run only location filter tests
pytest --alluredir=allure-results -v -k "story='Filter by location'"

# Run only job type filter tests
pytest --alluredir=allure-results -v -k "story='Filter by job type'"
```

### Running Specific Test Files
Run tests from specific files:

```bash
# Run only filter tests
pytest tests/test_filters.py --alluredir=allure-results

# Run only search tests
pytest tests/test_search_jobs.py --alluredir=allure-results

# Run only responsiveness tests
pytest tests/test_responsiveness.py --alluredir=allure-results
```

### Additional pytest Options

1. Run tests in parallel:
```bash
pytest -n auto --alluredir=allure-results
```

2. Run tests with detailed output:
```bash
pytest -v --alluredir=allure-results
```

3. Show extra test summary info:
```bash
pytest -ra --alluredir=allure-results
```

4. Stop on first failure:
```bash
pytest -x --alluredir=allure-results
```

5. Show local variables in tracebacks:
```bash
pytest -l --alluredir=allure-results
```

### Allure Report Options

1. Generate report without serving:
```bash
allure generate allure-results -o allure-report
```

2. Serve existing report:
```bash
allure serve allure-results
```

3. Clean previous results:
```bash
rm -rf allure-results/* && pytest --alluredir=allure-results
```

### Docker Execution

1. Run all tests in Docker:
```bash
docker-compose up --build
```

2. Run specific tests in Docker:
```bash
docker-compose run --rm tests pytest tests/test_filters.py --alluredir=allure-results
```

3. Run by severity in Docker:
```bash
docker-compose run --rm tests pytest -v -k "severity='critical'" --alluredir=allure-results
```

### Environment Variables
You can customize test execution using environment variables:

```bash
# Run tests against different environment
ENVIRONMENT=staging pytest --alluredir=allure-results

# Run tests with different viewport
VIEWPORT_WIDTH=1920 VIEWPORT_HEIGHT=1080 pytest --alluredir=allure-results

# Run tests with specific browser
BROWSER=firefox pytest --alluredir=allure-results
```

### Debugging Options

1. Run tests in debug mode:
```bash
pytest --pdb --alluredir=allure-results
```

2. Run with print statements visible:
```bash
pytest -s --alluredir=allure-results
```

3. Show extra pytest info:
```bash
pytest -v --alluredir=allure-results --setup-show
```

### Test Categories in the Project

1. Severity Levels:
- CRITICAL: Core functionality tests
- NORMAL: Regular feature tests
- MINOR: Nice-to-have feature tests

2. Features:
- Job Filters
- Job Search
- Responsive Design

3. Stories:
- Filter by location
- Filter by job type
- Search for QA positions
- Search with invalid input
- Mobile responsiveness
- Validate job card content

## Tips for Test Execution

1. Always clean allure-results before a fresh test run:
```bash
rm -rf allure-results/* && pytest --alluredir=allure-results
```

2. For debugging, combine options:
```bash
pytest -v -s --pdb --alluredir=allure-results
```

3. For CI/CD, use:
```bash
pytest --alluredir=allure-results --junitxml=report.xml
```

4. For development:
```bash
pytest -v -s --alluredir=allure-results --lf  # runs last failed tests
```
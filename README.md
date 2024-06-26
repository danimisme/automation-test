# Automation API Testing

## Overview
This project provides automated testing capabilities for RESTful APIs using Python, pytest, and requests. It includes test cases for CRUD operations (Create, Read, Update, Delete) on user data using the public API from https://gorest.co.in/.

## Setup
1. **Clone repository:**
   ```sh
   git clone https://github.com/danimisme/automation-test
   ```

2. **Install Pipenv if not installed:**
    ```sh
   pip install pipenv
   ```

3. **Install project dependencies:**
    ```sh
   pipenv install
   ```
   
3. **Create a config.json file and add your authorization token:**
    ```sh
    {
      "baseUrl": "https://gorest.co.in/public/v2",
      "token": "YOUR_TOKEN"
    }
   ```
   
## Run Test
**To run tests and generate an HTML report:**
   ```sh
   pipenv run pytest --html=report.html
   ```

## Structure
   ```
      project/
      ├── tests/
      │   └── api_test.py
      ├── config.json
      ├── Pipfile
      └── Pipfile.lock
   ```
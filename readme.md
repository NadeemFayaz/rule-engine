# Rule Engine with Abstract Syntax Tree (AST)

This project implements a simple rule engine that uses Abstract Syntax Tree (AST) to evaluate user eligibility based on attributes such as age, department, income, and spend.

## Features

- Define complex conditional rules.
- Combine rules dynamically.
- Evaluate rules against user data.
- Expose functionality through a Flask-based API.
- Simple UI for rule creation.

## How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Start the Flask API:
python api/app.py

3. Open `frontend/index.html` in a browser.

## API Endpoints

- `POST /create_rule`: Create a rule from a rule string.
- `POST /combine_rules`: Combine multiple rules.
- `POST /evaluate_rule`: Evaluate a rule against user attributes.

## Example Rules

- `"age > 30 AND department = 'Sales'"`
- `"age < 25 OR income > 50000"`


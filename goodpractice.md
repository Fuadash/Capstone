# Python and Git Good Practices

## 1. Function Documentation and Type Hints

Always include docstrings and type hints for functions:

```python
def calculate_total(price: float, tax_rate: float = 0.1) -> float:
    """Calculate total price including tax.
    
    Args:
        price: Base price of item
        tax_rate: Tax rate as decimal (default 0.1)
    
    Returns:
        Total price including tax
    """
    return price * (1 + tax_rate)
```

## 2. Variable Naming

Use descriptive names and snake_case:

```python
# Good
customer_count = 150
total_revenue = 25000.50

# Bad
c = 150
tr = 25000.50
```

## 3. Constants

Use UPPER_CASE for constants:

```python
MAX_RETRY_ATTEMPTS = 3
DATABASE_TIMEOUT = 30
```

## 4. Error Handling

Handle exceptions appropriately:

```python
def read_file(filename: str) -> str:
    """Read file content safely."""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found")
```

## 5. List Comprehensions

Use for simple transformations:

```python
# Good
squares = [x**2 for x in range(10)]
filtered_data = [item for item in data if item > 0]

# Avoid complex nested comprehensions
```

## 6. Context Managers

Always use `with` for file operations:

```python
with open('data.txt', 'r') as file:
    content = file.read()
```

## 7. Class Structure

Follow proper class conventions:

```python
class DataProcessor:
    """Process customer data."""
    
    def __init__(self, data_source: str) -> None:
        self.data_source = data_source
    
    def process(self) -> dict:
        """Process the data and return results."""
        return {"status": "processed"}
```

## 8. Import Organization

Group imports properly:

```python
# Standard library
import os
from typing import List, Dict

# Third-party
import pandas as pd
import numpy as np

# Local imports
from .utils import helper_function
```

## 9. Boolean Comparisons

Be explicit with boolean checks:

```python
# Good
if items:  # Check if list is not empty
if value is None:
if flag is True:

# Avoid
if len(items) > 0:
if value == None:
```

## 10. String Formatting

Use f-strings for readability:

```python
name = "Alice"
age = 30
message = f"Hello {name}, you are {age} years old"
```

## 11. Git Best Practices

### Commit Messages
> - Use clear, descriptive commit messages:
> - One feature per commit, if the message contains the word "and" then it should be 2 commits
> - Prefix a commit with the type of commit:
> - - fix: bugfix
> - - feat:  new feature
> - - docs: doc change
> - - perf: performance improvement
> - - test: adds or modifies tests
> - - refactor: code change that doesnt change functionality
> - - style: change that doesnt change the meaning of the code (whitespace, comments, formatting, etc)
```bash
# Good
git commit -m "feat: Add data validation for customer records"
git commit -m "fix: Fix SQL query timeout in database connection"
git commit -m "docs: Update README with setup instructions"

# Bad
git commit -m "fix"
git commit -m "updates"
git commit -m "Added this feature and fixed this bug"
```

### Branch Naming
Use descriptive branch names:

```bash
# Good
git checkout -b feature/customer-analysis
git checkout -b bugfix/database-connection
git checkout -b hotfix/critical-data-error

# Bad
git checkout -b temp
git checkout -b my-branch
```

### Workflow
Follow a clean workflow:

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/new-analysis

# 3. Make changes and commit frequently
git add .
git commit -m "Add initial data extraction logic"

# 4. Push and create pull request
git push origin feature/new-analysis
```

### .gitignore
Always include relevant files:

```gitignore
# Python
__pycache__/
*.pyc
.env
venv/

# Jupyter
.ipynb_checkpoints/

# Data files
*.csv
*.json
data/

# IDE
.vscode/
.idea/
```
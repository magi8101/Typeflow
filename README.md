# 🌊 TypeFlow

**Because Life's Too Short for TypeError Exceptions!**

<div align="center">
  <img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Python Versions">
  <img src="https://img.shields.io/badge/version-0.13.6-brightgreen.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</div>

```python
from typeflow import flow, TypeFlowContext

with TypeFlowContext():
    answer = flow(42) + " is the answer to everything"  # Works like magic! 🪄
    print(answer)  # "42 is the answer to everything"
```

<details id="run-output-1">
  <summary>Output</summary>
  
  ```
  42 is the answer to everything
  ```
</details>

## What is TypeFlow?

TypeFlow is a Python package that makes type conversion seamless and painless. Say goodbye to those annoying `TypeError: can only concatenate str (not "int") to str` exceptions that haunt your dreams!

## Why Do I Need This in My Life?

Ever tried to:

- Add a number to a string?
- Concatenate a list with text?
- Do math with values from JSON or CSV files without checking types?

TypeFlow handles all these scenarios with grace, so you can focus on building cool stuff instead of writing repetitive type conversion code.

## Why Use TypeFlow?

### 🚀 Boost Development Speed

- **Write Less Code**: No more manual type checking and conversion
- **Reduce Bugs**: Eliminate an entire class of type-related errors
- **Faster Prototyping**: Focus on features, not type compatibility

### 🛡️ Improve Code Quality

- **More Readable Code**: Express your intent clearly without conversion noise
- **Easier Maintenance**: Less code means less to maintain
- **Better Error Handling**: Consistent approach to type conversion issues

### 💪 Handle Real-World Challenges

- **Messy Input Data**: Process API responses with inconsistent types
- **Form Data**: Handle form submissions where all values are strings
- **CSV/JSON Imports**: Process tabular data without type headaches
- **Database Results**: Work with query results that might return mixed types
- **Configuration Files**: Parse config values without type validation

### 🎓 Great for Learning

- **Perfect for Beginners**: Remove frustrating type errors that discourage new Python programmers
- **Educational Tool**: Learn about Python's type system in a forgiving environment
- **Teaching Aid**: Explain type conversion without getting bogged down in details

TypeFlow strikes the perfect balance between Python's dynamic nature and the safety of strong typing. It respects the "principle of least surprise" while adding powerful capabilities to your code.

## Installation

```bash
pip install typeflow
```

<p align="center">
  <a href="https://pypi.org/project/typeflow/"><img src="https://img.shields.io/badge/pypi-v0.13.6-blue.svg" alt="PyPI Version"></a>
  <a href="https://github.com/magi8101/typeflow/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
  <a href="https://github.com/magi8101/typeflow"><img src="https://img.shields.io/badge/python-3.6+-orange.svg" alt="Python Versions"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/magi8101/typeflow/main/docs/assets/demo.gif" alt="TypeFlow Demo" width="650">
</p>

<h1>current version:0.13.6</h1>

## Quick Start Guide

TypeFlow offers multiple ways to handle type conversions based on your needs:

```python
from typeflow import flow, TypeFlowContext, with_typeflow

# Method 1: Use flow() directly - the most explicit approach
result1 = flow(42) + " unicorns"
print(result1)  # "42 unicorns"

# Method 2: Use TypeFlowContext for a block of code
with TypeFlowContext():
    # Remember to wrap values with flow() inside the context
    num = flow(123)
    text = " in context"
    result2 = num + text
    print(result2)  # "123 in context"

# Method 3: Use decorator for functions
@with_typeflow
def make_sandwich(bread, fillings):
    # Arguments are auto-wrapped - no need for flow()
    return bread + fillings

print(make_sandwich("Wheat bread with ", 3))  # "Wheat bread with 3"
```

<details id="run-output-2">
  <summary>Output</summary>
  
  ```
  42 unicorns
  123 in context
  Wheat bread with 3
  ```
</details>

## 🧰 API Reference

### Core Functions

#### `flow(value)`

Wraps any value in a TypeFlow type for seamless operations. This is the foundation of TypeFlow.

```python
num = flow(42)
text = flow("answer")
print(num + text)  # "42answer"

# Works with all major types
list_flow = flow([1, 2, 3])
print(list_flow + " items")  # "1, 2, 3 items"
```

<details id="run-output-3">
  <summary>Output</summary>
  
  ```
  42answer
  1, 2, 3 items
  ```
</details>

#### `enable()` and `disable()`

Controls TypeFlow globally - use with caution.

```python
from typeflow import enable, disable

# Enable TypeFlow globally (affects new objects created after enabling)
enable()

# Create new variables using built-in constructors
new_int = int(42)
text = " answers"
print(new_int + text)  # "42 answers"

# Disable when done to restore normal Python behavior
disable()
```

<details id="run-output-4">
  <summary>Output</summary>
  
  ```
  42 answers
  ```
</details>

Note: When using `enable()`, use the built-in constructors (`int()`, `str()`, etc.) to create values that can properly handle mixed operations.

### Context Managers

#### `TypeFlowContext(verbose=None, raise_errors=None)`

Creates a safe playground where TypeFlow is active.

```python
with TypeFlowContext(verbose=True):  # See what's happening under the hood
    # Use flow() to wrap existing values
    result = flow([1, 2, 3]) + " items in cart"
    print(result)

    # Or create new values with type constructors inside the context
    new_value = int(456)
    print(new_value + " is a new value")
```

<details id="run-output-5">
  <summary>Output</summary>
  
  ```
  typeflow - INFO - Converting list to string for concatenation with string: [1, 2, 3] -> '1, 2, 3'
  1, 2, 3 items in cart
  typeflow - INFO - Converting int to string for concatenation with string: 456 -> '456'
  456 is a new value
  ```
</details>

### Decorators

#### `@with_typeflow(verbose=None, raise_errors=None, auto_flow=True)`

Makes functions automatically handle mixed types.

```python
# Arguments are automatically wrapped with flow()
@with_typeflow
def calculate_total(quantity, price, coupon=0):
    # All arguments are pre-wrapped, so operations just work
    return "Total: $" + (quantity * price) - coupon

print(calculate_total(3, 9.99, 5))  # "Total: $24.97"

# For manual control, disable auto_flow
@with_typeflow(auto_flow=False)
def manual_calculate(a, b):
    # Here you need to use flow() manually
    return flow(a) * flow(b)

print(manual_calculate(5, "6"))  # Will convert "6" to a number and multiply
```

<details id="run-output-6">
  <summary>Output</summary>
  
  ```
  Total: $24.97
  30
  ```
</details>

### Configuration

#### `configure(verbose=None, raise_errors=None, log_level=None)`

Customize TypeFlow's behavior to your liking.

```python
from typeflow import configure, flow
import logging

# Set up verbose logging to see what TypeFlow is doing
configure(verbose=True, log_level=logging.INFO)

# Try a conversion that requires type handling
result = flow(42) + " magic beans"
print(result)

# Be strict and raise errors on conversion problems
configure(raise_errors=True)
```

<details id="run-output-7">
  <summary>Output</summary>
  
  ```
  typeflow - INFO - Converting int to string for concatenation with string: 42 -> '42'
  42 magic beans
  ```
</details>

### Custom Converters

#### `register_converter(target_type, source_type, converter_function)`

Teach TypeFlow how to handle your custom classes.

```python
from typeflow import register_converter, flow, TypeFlowContext

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

# Register how to convert Person to string
register_converter('str', Person, lambda p: f"{p.name} ({p.age})")
register_converter('int', Person, lambda p: p.age)

with TypeFlowContext():
    person = Person("Alice", 30)
    # Now you can do string concatenation with a Person
    greeting = flow("Hello, ") + person  # "Hello, Alice (30)"
    print(greeting)

    # And numeric operations using the age
    age_in_months = flow(person) * 12  # 360
    print(f"Age in months: {age_in_months}")
```

<details id="run-output-8">
  <summary>Output</summary>
  
  ```
  Hello, Alice (30)
  Age in months: 360
  ```
</details>

## Real-World Examples

### Data Processing

```python
from typeflow import flow

# Mixed data from a CSV file or API
user_data = [
    {"id": "1001", "visits": 5, "active": "true"},
    {"id": 1002, "visits": "12", "active": 1},
    {"id": 1003, "visits": None, "active": "false"}
]

# Process without worrying about types
def process_user(user):
    activity_score = flow(user["visits"]) * (1 if flow(user["active"]) else 0.5)
    return f"User {user['id']} has a score of {activity_score}"

for user in user_data:
    print(process_user(user))
```

<details id="run-output-9">
  <summary>Output</summary>
  
  ```
  User 1001 has a score of 5.0
  User 1002 has a score of 12.0
  User 1003 has a score of 0.0
  ```
</details>

### Form Input Processing

```python
from typeflow import with_typeflow

# Input values from a web form
form_data = {
    "quantity": "3",
    "price": 24.99,
    "discount": "5",
    "is_member": "true"
}

@with_typeflow
def calculate_order(quantity, price, discount=0, is_member=False):
    subtotal = quantity * price
    member_discount = subtotal * 0.1 if is_member else 0
    return subtotal - discount - member_discount

total = calculate_order(
    form_data["quantity"],
    form_data["price"],
    form_data["discount"],
    form_data["is_member"]
)
print(f"Order total: ${total:.2f}")
```

<details id="run-output-10">
  <summary>Output</summary>
  
  ```
  Order total: $62.47
  ```
</details>

## Command-Line Interface

TypeFlow comes with a simple command-line interface:

```bash
# Show version information
typeflow --version

# Enable TypeFlow globally
typeflow --enable

# Enable with verbose mode
typeflow --enable --verbose

# Disable TypeFlow
typeflow --disable
```

<details id="run-output-11">
  <summary>Output</summary>
  
  ```
  TypeFlow version 0.13.6
  
  # When enabling:
  TypeFlow has been enabled globally
  
  # When disabling:
  TypeFlow has been disabled globally
  ```
</details>

## Limitations

- Currently, TypeFlow works best when explicitly wrapping values with `flow()`. Global `enable()` works but requires creating new values using type constructors.
- Due to Python's immutable built-in types, patching existing values directly isn't possible in all cases.
- Performance impact is minimal for most operations, but may be noticeable in tight loops with many conversions.

## Uploading to PyPI

If you've made improvements to TypeFlow and want to share them with the world, here's how to upload your package to PyPI:

### 1. Prepare your package

Make sure your package structure is correct:

```
TypeFlow/
├── typeflow/
│   ├── __init__.py
│   ├── core.py
│   └── ...
├── setup.py
├── README.md
└── LICENSE
```

### 2. Install build tools

```bash
pip install build twine
```

### 3. Build distribution packages

From the project root directory, run:

```bash
python -m build
```

This creates distribution packages in the `dist/` directory.

### 4. Upload to PyPI

#### Test PyPI first (recommended)

```bash
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

#### Upload to production PyPI

```bash
python -m twine upload dist/*
```

You'll need to provide your PyPI username and password or API token.

### 5. Verify installation

```bash
# From test PyPI
pip install --index-url https://test.pypi.org/simple/ typeflow

# From production PyPI
pip install typeflow
```

<details id="run-output-pypi">
  <summary>Example Output</summary>
  
  ```
  Uploading distributions to https://upload.pypi.org/legacy/
  Uploading typeflow-0.13.6-py3-none-any.whl
  100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 21.3/21.3 kB • 00:00 • ?
  Uploading typeflow-0.13.6.tar.gz
  100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 19.4/19.4 kB • 00:00 • ?
  
  View at: https://pypi.org/project/typeflow/0.13.6/
  ```
</details>

## Publishing with GitHub Actions

TypeFlow uses GitHub Actions for automated publishing to PyPI. To set up your own fork for publishing:

1. **Create a PyPI API token**:

   - Go to https://pypi.org/manage/account/
   - Create an API token with the scope limited to your project

2. **Set up GitHub repository**:

   - In your repository, go to Settings > Environments
   - Create a new environment named `pypi`
   - Add a secret called `PYPI_API_TOKEN` with your PyPI token value

3. **Set up PyPI Trusted Publisher**:

   - In PyPI project settings, add a new "Trusted Publisher"
   - Configure with these values:
     - **PyPI Project Name**: typeflow
     - **Owner**: your GitHub username or organization name
     - **Repository name**: typeflow
     - **Workflow name**: publish.yml
     - **Environment name**: pypi

4. **Publish a new version**:
   - Update version in `setup.py`
   - Create a new GitHub Release
   - The workflow will automatically publish to PyPI

This implements modern OIDC authentication between GitHub and PyPI, eliminating the need for long-lived API tokens.

## Philosophy

TypeFlow follows the "batteries included" and "it should just work" philosophy of Python, tackling one of the few remaining pain points in Python's smooth developer experience.

---

<div align="center">
  <img src="https://img.shields.io/badge/Built_with_❤️_by-Magi_Sharma-ff69b4" alt="Built with love">
  <p><i>"In Python, we trust; with TypeFlow, we flow."</i></p>
</div>

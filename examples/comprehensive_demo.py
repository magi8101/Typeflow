"""
Comprehensive demo script showcasing all TypeFlow features.
"""

import logging
from typeflow import (
    flow, TypeFlowContext, with_typeflow, enable, disable, configure,
    register_converter
)

def section_header(title):
    """Print a section header."""
    print(f"\n{'=' * 40}")
    print(f"  {title}")
    print(f"{'=' * 40}")

# Configure TypeFlow for better logging
configure(verbose=True, log_level=logging.INFO)

print("\n🌊 TYPEFLOW DEMONSTRATION 🌊")
print("A comprehensive showcase of TypeFlow's capabilities\n")

# SECTION 1: Basic Usage with flow()
section_header("1. BASIC USAGE WITH FLOW()")
print("The flow() function explicitly wraps values for type conversion:")

# Basic flow examples
str_result = flow(42) + " answers"
list_result = flow([1, 2, 3]) + " items"
dict_result = flow({"name": "TypeFlow"}) + " is awesome"
print(f"Int + String: {str_result}")
print(f"List + String: {list_result}")
print(f"Dict + String: {dict_result}")

print("\nChaining operations:")
# Fix: Make sure each operation involves at least one flow object
step1 = flow(10) * flow(5)  # This gives 50 as a FlowInt
step2 = flow(step1) + " = "  # Convert to "50 = "
complex_result = step2 + flow(50)  # Add the final "50"
print(f"10 * 5 + ' = ' + 50: {complex_result}")

# Alternatively, more concise approach with proper parentheses
alternate_result = flow(10 * 5) + " = " + flow(50)
print(f"Alternative approach: {alternate_result}")

# SECTION 2: TypeFlowContext
section_header("2. USING TYPEFLOWCONTEXT")
print("The TypeFlowContext creates a controlled environment for type conversion:")

with TypeFlowContext():
    # Explicitly wrap existing variables with flow()
    num = flow(123)
    text = " in context"
    result = num + text
    print(f"Using flow(): {result}")
    
    # Create new variables with the built-in constructors
    # (these use our enhanced types while in the context)
    int_val = int(456)  # This will be a FlowInt
    str_val = str(" is a FlowStr")  # This will be a FlowStr
    addition = int_val + str_val
    print(f"Using constructors: {addition}")

print("\nAfter exiting the context, automatic conversion is disabled.")

# SECTION 3: Function Decorator
section_header("3. FUNCTION DECORATOR")
print("The @with_typeflow decorator enables automatic type conversion in functions:")

@with_typeflow
def combine(a, b, c=None):
    if c is None:
        return a + b
    return a + b + c

print(f"Combining string + int: {combine('Answer: ', 42)}")
print(f"Combining three values: {combine(10, ' + ', 20)}")

@with_typeflow(auto_flow=False)
def manual_combine(a, b):
    # Need to use flow() manually with auto_flow=False
    return flow(a) + flow(b)

print(f"Manual decoration: {manual_combine(99, ' manual')}")

# SECTION 4: Global Enable/Disable
section_header("4. GLOBAL ENABLE/DISABLE")
print("Global enabling affects ALL operations in the program:")

print("Before enable:")
try:
    before_result = 789 + " global"
    print(f"Result: {before_result}")
except TypeError as e:
    print(f"Expected error: {e}")

# Enable globally
print("\nEnabling TypeFlow globally...")
enable()

# Operations should now work with new variables created after enable()
try:
    # New variable using int() constructor will be FlowInt
    new_int = int(789)
    global_int_str = new_int + " global"
    print(f"Int + String: {global_int_str}")
    
    # New variable using list() constructor will be FlowList
    new_list = list([1, 2, 3])
    global_list_str = new_list + " in a list"
    print(f"List + String: {global_list_str}")
    
    # This also works with flow() of course
    global_dict_str = flow({"key": "value"}) + " in a dict"
    print(f"Dict + String: {global_dict_str}")
    
    # Complex operations work with explicit flow()
    global_complex = flow(5 + 10) + " equals " + flow(15)
    print(f"Complex operation: {global_complex}")
    
    print("\nNote: After enable(), new variables created with type constructors")
    print("will have TypeFlow's enhanced behavior, but existing literals or")
    print("variables need explicit flow() wrapping.")
except Exception as e:
    print(f"Error: {e}")

# Disable globally
print("\nDisabling TypeFlow...")
disable()

print("After disable:")
try:
    after_result = 999 + " after disable"
    print(f"Result: {after_result}")
except TypeError as e:
    print(f"Expected error: {e}")

# SECTION 5: Custom Converters
section_header("5. CUSTOM CONVERTERS")
print("Register custom converters for your own types:")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return f"Person({self.name}, {self.age})"

# Register converters for the Person class
register_converter('str', Person, lambda p: f"{p.name} (age {p.age})")
register_converter('int', Person, lambda p: p.age)
register_converter('bool', Person, lambda p: p.age >= 18)

# Use the converters
person = Person("Alice", 30)

with TypeFlowContext():
    # String conversion
    person_str = "Hello, " + flow(person)
    print(f"Person to string: {person_str}")
    
    # Int conversion
    person_age = flow(person) * 2
    print(f"Person's age doubled: {person_age}")
    
    # Boolean conversion (is adult?)
    is_adult = "Is adult: " + flow(flow(person))
    print(f"Boolean conversion: {is_adult}")
    print("---------------------------------------")
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

print("\n🌊 TYPEFLOW DEMONSTRATION COMPLETED 🌊")

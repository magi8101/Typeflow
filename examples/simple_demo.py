"""
Simple demo script that shows TypeFlow's core functionality
"""

import sys
from typeflow import flow, TypeFlowContext, with_typeflow, enable, disable, configure

print("===== TypeFlow Simple Demo =====")

# Part 1: Using flow() directly - Always Works
print("\n1. Using flow() directly:")
result1 = flow(42) + " answers"
result2 = flow([1, 2, 3]) + " items"
print(f"Int + String: {result1}")
print(f"List + String: {result2}")

# Part 2: Using TypeFlowContext
print("\n2. Using TypeFlowContext:")
with TypeFlowContext():
    # Method 1: Use flow() to explicitly wrap existing variables
    num = flow(123)  # Explicitly wrap with flow()
    text = " in context"
    result = num + text  # This works because num is a flow object
    print(f"Method 1 - Explicit flow(): {result}")
    
    # Method 2: Use flow() for all variables inside context
    new_num = flow(456)  # Need to use flow() even for new variables
    new_text = flow(" created inside context")
    new_result = new_num + new_text
    print(f"Method 2 - All flow objects: {new_result}")
    
    # Method 3: Alternative approach with explicit type conversion
    another_result = str(789) + " with explicit conversion"
    print(f"Method 3 - Explicit conversion: {another_result}")

# Part 3: Using the decorator
print("\n3. Using @with_typeflow decorator:")
@with_typeflow
def combine(a, b):
    return a + b

mixed_result = combine(456, " decorated")
print(f"Decorator result: {mixed_result}")

# Part 4: Global enable/disable
print("\n4. Demonstrating global enable/disable:")
# Test the initial state
print("Before enabling:")
try:
    before_result = 789 + " global"
    print(f"Result: {before_result}")
except TypeError as e:
    print(f"Expected error: {e}")

# Now enable it globally
print("\nEnabling TypeFlow globally...")
enable()

# Try again
try:
    # Should work now with auto conversion
    global_result = 789 + " global"
    print(f"After enable: {global_result}")
    
    # Try with list too
    list_result = [1, 2, 3] + " global items"
    print(f"List + String: {list_result}")
except Exception as e:
    print(f"Error after enable: {e}")

# Disable again
print("\nDisabling TypeFlow...")
disable()

# Verify it's disabled
print("After disabling:")
try:
    after_result = 999 + " after disable"
    print(f"Result: {after_result}")
except TypeError as e:
    print(f"Expected error (TypeFlow is disabled): {e}")

print("\n===== Demo Completed =====")

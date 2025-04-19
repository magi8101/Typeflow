"""
Demo script for TypeFlow package.
"""

from typeflow import flow, TypeFlowContext, with_typeflow, enable, disable, configure
import logging

# Configure with simpler settings
configure(verbose=False, log_level=logging.WARNING)

print("===== TypeFlow Demo =====")

# First, let's try the basic Python behavior
print("\n1. Normal Python Behavior:")
try:
    result = 123 + "456"
    print(f"This won't work: {result}")
except TypeError as e:
    print(f"Expected error: {e}")

# Use manual flow conversion - always works
print("\n2. Using manual flow conversion:")
result1 = flow(42) + " unicorns"
result2 = flow([1, 2, 3]) + " items"
print(f"Int + String: {result1}")
print(f"List + String: {result2}")

# Use the decorator with simplified approach
print("\n3. Using with_typeflow decorator:")
@with_typeflow
def make_sandwich(bread, fillings):
    return bread + fillings  # Args are auto-converted by decorator

print(f"Function result: {make_sandwich('Wheat bread with ', 3)}")

# Test global enable/disable
print("\n4. Using global enable/disable:")
print("Before enable: ", end="")
try:
    test = 123 + "456"
    print("Worked (unexpected)")
except TypeError:
    print("Fails as expected")

print("\nEnabling TypeFlow globally...")
# Enable globally - use direct approach
enable()

try:
    # Test basic type mixing without flow()
    int_str = 42 + " is the answer"
    print(f"Int + String: {int_str}")
    
    # List concatenation
    list_str = [1, 2, 3] + " items"
    print(f"List + String: {list_str}")

except Exception as e:
    print(f"Error: {e}")
finally:
    print("\nDisabling TypeFlow...")
    disable()

print("\nAfter disable: ", end="")
try:
    result = 42 + " answers"
    print("Still works (unexpected)")
except TypeError:
    print("Back to normal Python behavior")

print("\n===== Demo completed =====")


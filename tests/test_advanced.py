"""
Advanced tests for TypeFlow.
"""

import unittest
import logging
import sys

# Import typeflow directly
import typeflow

class TestAdvancedFeatures(unittest.TestCase):
    """Test advanced TypeFlow features."""
    
    def setUp(self):
        """Set up test environment."""
        # Make sure TypeFlow is disabled before each test
        typeflow.disable()
        # Reset configuration
        typeflow.configure(verbose=False, log_level=logging.WARNING)
    
    def tearDown(self):
        """Clean up after each test."""
        # Make sure TypeFlow is disabled after each test
        typeflow.disable()
        # Reset configuration
        typeflow.configure(verbose=False, log_level=logging.WARNING)
    
    def test_verbose_mode(self):
        """Test verbose mode."""
        # This test is mainly to ensure verbose mode doesn't break anything
        typeflow.configure(verbose=True, log_level=logging.INFO)
        
        # Need to create Flow objects directly since we're testing TypeFlow
        with typeflow.TypeFlowContext():
            num = typeflow.flow(42)
            text = typeflow.flow("answer")
            result = num + text
            self.assertEqual(result, "42answer")
    
    def test_custom_converters(self):
        """Test custom converters."""
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age
            
            def __repr__(self):
                return f"Person({self.name}, {self.age})"
        
        # Register custom converters for Person
        typeflow.register_converter('str', Person, lambda p: f"{p.name} ({p.age})")
        typeflow.register_converter('int', Person, lambda p: p.age)
        typeflow.register_converter('float', Person, lambda p: float(p.age))
        typeflow.register_converter('bool', Person, lambda p: p.age > 18)
        
        with typeflow.TypeFlowContext():
            person = Person("Alice", 30)
            greeting = typeflow.flow("Hello, ")
            
            # String concatenation - must use flow objects
            self.assertEqual(greeting + person, "Hello, Alice (30)")
            
            # Numeric operations - need to use the int converter
            num = typeflow.flow(12)
            person_age = typeflow.get_converter('int').to_int(person)  # Get the age (30)
            self.assertEqual(person_age * 12, 360)  # 30 * 12
            
            # Boolean operations - directly use the bool converter
            is_adult = typeflow.get_converter('bool').to_bool(person)  # True for age > 18
            self.assertEqual(is_adult, True)  # Person is adult (age > 18)
    
    def test_error_handling(self):
        """Test error handling."""
        # With default error handling (silent)
        with typeflow.TypeFlowContext():
            # This should convert to string even though it's not ideal
            dict_obj = typeflow.flow({"complex": "data"})
            list_obj = typeflow.flow([1, 2, 3])
            result = dict_obj + list_obj
            self.assertTrue(isinstance(result, str))
        
        # With error raising enabled
        with typeflow.TypeFlowContext(raise_errors=True):
            # Simple cases should still work
            num = typeflow.flow(42)
            text = typeflow.flow("answer")
            self.assertEqual(num + text, "42answer")
            
            # But complex cases might raise errors
            try:
                # Create a custom type that has no conversion logic
                class ComplexCustom:
                    pass
                
                complex_obj = ComplexCustom()
                list_obj = typeflow.flow([1, 2, 3])
                
                # This should fail with TypeError since we have no converter
                with self.assertRaises(TypeError):
                    typeflow.get_converter('int').to_int(complex_obj)
            except Exception as e:
                self.fail(f"Test failed due to unexpected error: {e}")
    
    def test_nested_contexts(self):
        """Test nested context managers."""
        with typeflow.TypeFlowContext():
            num = typeflow.flow(42)
            text1 = typeflow.flow("outer")
            self.assertEqual(num + text1, "42outer")
            
            with typeflow.TypeFlowContext(verbose=True):
                text2 = typeflow.flow("inner")
                self.assertEqual(num + text2, "42inner")
            
            text3 = typeflow.flow("outer again")
            self.assertEqual(num + text3, "42outer again")
    
    def test_complex_operations(self):
        """Test more complex operations."""
        with typeflow.TypeFlowContext():
            # Nested structures
            dict_obj = typeflow.flow({"users": [{"name": "Alice"}, {"name": "Bob"}]})
            text = typeflow.flow(" data")
            result = dict_obj + text
            self.assertTrue(isinstance(result, str))
            
            # Multiple operations - proper way to chain operations
            # First add numbers, then convert to string and append
            num1 = 5  # regular int
            num2 = 10  # regular int
            sum_num = typeflow.flow(num1 + num2)  # flow int with value 15
            text = typeflow.flow("items")
            list_obj = typeflow.flow([1, 2, 3])
            
            # Now chain the operations correctly
            result = sum_num + text + list_obj
            # The list is represented as "[1, 2, 3]" in the string output
            self.assertEqual(result, "15items[1, 2, 3]")
            
            # Mixed operations
            num = typeflow.flow(5)
            text = typeflow.flow("x")
            num3 = typeflow.flow(3)
            result = (num + text) * num3
            self.assertEqual(result, "5x5x5x")

if __name__ == "__main__":
    unittest.main()
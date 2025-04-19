"""
Advanced tests for TypeFlow.
"""

import unittest
import logging
from typeflow import (
    configure, TypeFlowContext, register_converter, 
    with_typeflow, enable, disable
)

class TestAdvancedFeatures(unittest.TestCase):
    """Test advanced TypeFlow features."""
    
    def setUp(self):
        """Set up test environment."""
        # Make sure TypeFlow is disabled before each test
        disable()
        # Reset configuration
        configure(verbose=False, log_level=logging.WARNING)
    
    def tearDown(self):
        """Clean up after each test."""
        # Make sure TypeFlow is disabled after each test
        disable()
        # Reset configuration
        configure(verbose=False, log_level=logging.WARNING)
    
    def test_verbose_mode(self):
        """Test verbose mode."""
        # This test is mainly to ensure verbose mode doesn't break anything
        configure(verbose=True, log_level=logging.INFO)
        
        with TypeFlowContext():
            result = 42 + "answer"
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
        register_converter('str', Person, lambda p: f"{p.name} ({p.age})")
        register_converter('int', Person, lambda p: p.age)
        register_converter('float', Person, lambda p: float(p.age))
        register_converter('bool', Person, lambda p: p.age > 18)
        
        with TypeFlowContext():
            person = Person("Alice", 30)
            
            # String concatenation
            self.assertEqual("Hello, " + person, "Hello, Alice (30)")
            
            # Numeric operations
            self.assertEqual(person * 12, 360)  # 30 * 12
            
            # Boolean operations
            self.assertEqual(person + False, True)  # True + False = 1 (True)
    
    def test_error_handling(self):
        """Test error handling."""
        # With default error handling (silent)
        with TypeFlowContext():
            # This should convert to string even though it's not ideal
            result = {"complex": "data"} + [1, 2, 3]
            self.assertTrue(isinstance(result, str))
        
        # With error raising enabled
        with TypeFlowContext(raise_errors=True):
            # Simple cases should still work
            self.assertEqual(42 + "answer", "42answer")
            
            # But complex cases might raise errors
            with self.assertRaises(TypeError):
                import cmath
                complex(1, 2) + [1, 2, 3]
    
    def test_nested_contexts(self):
        """Test nested context managers."""
        with TypeFlowContext():
            self.assertEqual(42 + "outer", "42outer")
            
            with TypeFlowContext(verbose=True):
                self.assertEqual(42 + "inner", "42inner")
            
            self.assertEqual(42 + "outer again", "42outer again")
    
    def test_complex_operations(self):
        """Test more complex operations."""
        with TypeFlowContext():
            # Nested structures
            result = {"users": [{"name": "Alice"}, {"name": "Bob"}]} + " data"
            self.assertTrue(isinstance(result, str))
            
            # Multiple operations
            result = 5 + 10 + "items" + [1, 2, 3]
            self.assertEqual(result, "15items1, 2, 3")
            
            # Mixed operations
            result = (5 + "x") * 3
            self.assertEqual(result, "5x5x5x")

if __name__ == "__main__":
    unittest.main()
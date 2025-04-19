"""
Basic tests for TypeFlow.
"""

import unittest
import sys
from typeflow import enable, disable, TypeFlowContext, with_typeflow, flow, configure

class TestBasicOperations(unittest.TestCase):
    """Test basic TypeFlow operations."""
    
    def setUp(self):
        """Set up test environment."""
        # Make sure TypeFlow is disabled before each test
        disable()
    
    def tearDown(self):
        """Clean up after each test."""
        # Make sure TypeFlow is disabled after each test
        disable()
    
    def test_global_enable(self):
        """Test global enablement."""
        try:
            # Explicitly enable TypeFlow
            enable()
            
            # String concatenation with different types
            self.assertEqual("The answer is " + 42, "The answer is 42")
            self.assertEqual(42 + " is the answer", "42 is the answer")
            
            # List concatenation with string
            self.assertEqual([1, 2, 3] + "test", "1, 2, 3test")
            self.assertEqual("test" + [1, 2, 3], "test1, 2, 3")
            
            # Boolean addition with float
            self.assertEqual(True + 5.0, 6.0)
            self.assertEqual(5.0 + False, 5.0)
        finally:
            # Always disable even if test fails
            disable()
        
        # Should raise TypeError now
        with self.assertRaises(TypeError):
            "Back to normal: " + 42
    
    def test_context_manager(self):
        """Test context manager."""
        # Should raise TypeError outside context
        with self.assertRaises(TypeError):
            2 + "ad"
        
        # Should work inside context
        with TypeFlowContext():
            self.assertEqual(2 + "ad", "2ad")
            self.assertEqual([1, 2, 3] + "test", "1, 2, 3test")
            self.assertEqual({"a": 1} + [1, 2, 3], {"a": 1, 0: 1, 1: 2, 2: 3})
            self.assertEqual(True + 5.0, 6.0)
        
        # Should raise TypeError again outside context
        with self.assertRaises(TypeError):
            2 + "ad"
    
    def test_decorator(self):
        """Test decorator."""
        @with_typeflow
        def process_data(value, suffix):
            return value + suffix
        
        # Should work with any types
        self.assertEqual(process_data(42, "!"), "42!")
        self.assertEqual(process_data([1, 2, 3], "test"), "1, 2, 3test")
        self.assertEqual(process_data(True, 5), 6)
    
    def test_flow_function(self):
        """Test flow function."""
        # Convert values to TypeFlow types
        num = flow(42)
        text = flow("hello")
        lst = flow([1, 2, 3])
        
        # Should handle mixed operations
        self.assertEqual(num + text, "42hello")
        self.assertEqual(lst + text, "1, 2, 3hello")
        self.assertEqual(num + [4, 5, 6], "424, 5, 6")

if __name__ == "__main__":
    unittest.main()
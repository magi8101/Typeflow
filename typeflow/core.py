"""
Core functionality for TypeFlow package.
"""

import builtins
import functools
import inspect
import logging
import sys
import threading
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional, TypeVar, cast

from .config import get_config
from .types import (
    FlowBool, FlowDict, FlowFloat, FlowInt, FlowList, FlowStr, flow,
    _original_bool, _original_dict, _original_float, _original_int, 
    _original_list, _original_str
)

logger = logging.getLogger("typeflow")

# Thread-local storage for tracking enabled state
_local = threading.local()

# Initialize thread-local variables
def _init_local():
    if not hasattr(_local, "enabled"):
        _local.enabled = False
    if not hasattr(_local, "depth"):
        _local.depth = 0

_init_local()

def is_enabled() -> bool:
    """Check if TypeFlow is currently enabled."""
    _init_local()
    return _local.enabled

def enable() -> None:
    """
    Enable automatic type conversion globally.
    
    This replaces built-in types with TypeFlow's enhanced versions
    that automatically handle type conversion during operations.
    """
    _init_local()
    if _local.enabled:
        logger.debug("TypeFlow is already enabled")
        return
    
    # Mark as enabled first to avoid recursion issues
    _local.enabled = True
    
    # Replace built-in types with our enhanced versions
    # This is the only mechanism we need - no patching of operators
    builtins.str = FlowStr
    builtins.int = FlowInt
    builtins.float = FlowFloat
    builtins.list = FlowList
    builtins.dict = FlowDict
    builtins.bool = FlowBool
    
    logger.info("TypeFlow enabled globally")

def disable() -> None:
    """
    Disable automatic type conversion globally.
    
    This restores the original built-in types.
    """
    _init_local()
    if not _local.enabled:
        logger.debug("TypeFlow is not enabled")
        return
    
    # Restore original built-in types
    builtins.str = _original_str
    builtins.int = _original_int
    builtins.float = _original_float
    builtins.list = _original_list
    builtins.dict = _original_dict
    builtins.bool = _original_bool
    
    # Mark as disabled after cleanup
    _local.enabled = False
    logger.info("TypeFlow disabled globally")

class TypeFlowContext:
    """
    Context manager for scoped automatic type conversion.
    
    Example:
        with TypeFlowContext():
            result = 2 + "ad"  # Works without error
    """
    
    def __init__(self, verbose: bool = None, raise_errors: bool = None):
        """
        Initialize the context manager.
        
        Args:
            verbose: If True, log information about type conversions.
                    If None, use the global configuration.
            raise_errors: If True, raise errors for conversions that fail.
                         If None, use the global configuration.
        """
        self.verbose = verbose
        self.raise_errors = raise_errors
        _init_local()
        self.was_enabled = _local.enabled
        self.original_config = None
    
    def __enter__(self):
        _init_local()
        
        # Track context depth to handle nested contexts
        _local.depth += 1
        
        # Save and update configuration
        config = get_config()
        self.original_config = {
            'verbose': config.verbose,
            'raise_errors': config.raise_errors
        }
        
        # Update configuration if specified
        if self.verbose is not None:
            config.verbose = self.verbose
        if self.raise_errors is not None:
            config.raise_errors = self.raise_errors
        
        # Always enable TypeFlow within the context
        enable()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        _init_local()
        _local.depth = max(0, _local.depth - 1)
        
        # Restore original configuration
        if self.original_config:
            config = get_config()
            config.verbose = self.original_config['verbose']
            config.raise_errors = self.original_config['raise_errors']
        
        # Only disable TypeFlow if this is the outermost context
        if _local.depth == 0 and not self.was_enabled:
            disable()

F = TypeVar('F', bound=Callable[..., Any])

def with_typeflow(func: Optional[F] = None, *, verbose: bool = None, raise_errors: bool = None, auto_flow: bool = True) -> F:
    """
    Decorator for functions with automatic type conversion.
    
    Example:
        @with_typeflow
        def my_function(num, text):
            return num + text  # Works without explicit flow() calls
    
    Args:
        func: The function to decorate
        verbose: If True, log information about type conversions
        raise_errors: If True, raise errors for conversions that fail
        auto_flow: If True, automatically wrap function arguments with flow()
    """
    def decorator(f: F) -> F:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            from .types import flow  # Import flow function directly here to avoid circular imports
            
            with TypeFlowContext(verbose=verbose, raise_errors=raise_errors):
                # If auto_flow is enabled, wrap all arguments with flow()
                if auto_flow:
                    args = tuple(flow(arg) for arg in args)
                    kwargs = {key: flow(value) for key, value in kwargs.items()}
                return f(*args, **kwargs)
        return cast(F, wrapper)
    
    if func is None:
        return decorator
    return decorator(func)
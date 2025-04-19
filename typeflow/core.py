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
    FlowBool, FlowDict, FlowFloat, FlowInt, FlowList, FlowStr, 
    _original_bool, _original_dict, _original_float, _original_int, 
    _original_list, _original_str
)

logger = logging.getLogger("typeflow")

# Thread-local storage for tracking enabled state
_local = threading.local()
_local.enabled = False
_local.depth = 0

def is_enabled() -> bool:
    """Check if TypeFlow is currently enabled."""
    return getattr(_local, "enabled", False)

def enable() -> None:
    """
    Enable automatic type conversion globally.
    
    This replaces built-in types with TypeFlow's enhanced versions
    that automatically handle type conversion during operations.
    """
    if is_enabled():
        logger.debug("TypeFlow is already enabled")
        return
    
    # Replace built-in types with our enhanced versions
    builtins.str = FlowStr
    builtins.int = FlowInt
    builtins.float = FlowFloat
    builtins.list = FlowList
    builtins.dict = FlowDict
    builtins.bool = FlowBool
    
    _local.enabled = True
    logger.info("TypeFlow enabled globally")

def disable() -> None:
    """
    Disable automatic type conversion globally.
    
    This restores the original built-in types.
    """
    if not is_enabled():
        logger.debug("TypeFlow is not enabled")
        return
    
    # Restore original built-in types
    builtins.str = _original_str
    builtins.int = _original_int
    builtins.float = _original_float
    builtins.list = _original_list
    builtins.dict = _original_dict
    builtins.bool = _original_bool
    
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
        self.was_enabled = is_enabled()
        self.original_config = None
    
    def __enter__(self):
        _local.depth = getattr(_local, "depth", 0) + 1
        
        # Save original configuration if this is the outermost context
        if _local.depth == 1:
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
        
        if not is_enabled():
            enable()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        _local.depth = max(0, getattr(_local, "depth", 1) - 1)
        
        # Restore original configuration if this is the outermost context
        if _local.depth == 0 and self.original_config:
            config = get_config()
            config.verbose = self.original_config['verbose']
            config.raise_errors = self.original_config['raise_errors']
        
        # Only disable if we were the ones who enabled it
        if not self.was_enabled and _local.depth == 0:
            disable()

F = TypeVar('F', bound=Callable[..., Any])

def with_typeflow(func: Optional[F] = None, *, verbose: bool = None, raise_errors: bool = None) -> F:
    """
    Decorator for functions with automatic type conversion.
    
    Example:
        @with_typeflow
        def my_function():
            return 2 + "ad"  # Works without error
    """
    def decorator(f: F) -> F:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with TypeFlowContext(verbose=verbose, raise_errors=raise_errors):
                return f(*args, **kwargs)
        return cast(F, wrapper)
    
    if func is None:
        return decorator
    return decorator(func)
"""
Configuration module for TypeFlow.
"""

import logging
import threading
from dataclasses import dataclass
from typing import Dict, Optional

logger = logging.getLogger("typeflow")

@dataclass
class Config:
    """Configuration for TypeFlow."""
    verbose: bool = False
    raise_errors: bool = False
    log_level: int = logging.WARNING

# Thread-local storage for configuration
_local = threading.local()

def get_config() -> Config:
    """Get the current configuration."""
    if not hasattr(_local, "config"):
        _local.config = Config()
        
        # Configure logging based on initial settings
        _configure_logging(_local.config.log_level)
    
    return _local.config

def _configure_logging(level: int) -> None:
    """Configure logging with the specified level."""
    logger.setLevel(level)
    
    # Add a handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

def configure(verbose: Optional[bool] = None, raise_errors: Optional[bool] = None, 
              log_level: Optional[int] = None) -> None:
    """
    Configure TypeFlow settings.
    
    Args:
        verbose: If True, log information about type conversions
        raise_errors: If True, raise errors for conversions that fail
        log_level: Logging level (e.g., logging.INFO, logging.DEBUG)
    """
    config = get_config()
    
    if verbose is not None:
        config.verbose = verbose
    
    if raise_errors is not None:
        config.raise_errors = raise_errors
    
    if log_level is not None:
        config.log_level = log_level
        _configure_logging(log_level)
"""
Type conversion functionality for TypeFlow.
"""

import datetime
import decimal
import logging
import uuid
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

logger = logging.getLogger("typeflow")

# Type for conversion functions
T = TypeVar('T')
ConversionFunc = Callable[[Any], T]

class ConversionRegistry:
    """Registry for type conversion functions."""
    
    def __init__(self):
        self._str_converters: Dict[type, ConversionFunc] = {}
        self._int_converters: Dict[type, ConversionFunc] = {}
        self._float_converters: Dict[type, ConversionFunc] = {}
        self._bool_converters: Dict[type, ConversionFunc] = {}
        self._list_converters: Dict[type, ConversionFunc] = {}
        self._dict_converters: Dict[type, ConversionFunc] = {}
        
        # Cache for performance
        self._str_cache: Dict[type, str] = {}
        self._int_cache: Dict[type, int] = {}
        self._float_cache: Dict[type, float] = {}
        self._bool_cache: Dict[type, bool] = {}
        
        self._register_default_converters()
    
    def _register_default_converters(self) -> None:
        """Register default conversion functions for common types."""
        # String converters
        self.register_str(str, lambda x: x)
        self.register_str(int, str)
        self.register_str(float, str)
        self.register_str(bool, lambda x: "True" if x else "False")
        self.register_str(list, lambda x: ", ".join(str(item) for item in x))
        self.register_str(tuple, lambda x: ", ".join(str(item) for item in x))
        self.register_str(set, lambda x: "{" + ", ".join(str(item) for item in x) + "}")
        self.register_str(dict, lambda x: ", ".join(f"{k}: {v}" for k, v in x.items()))
        self.register_str(datetime.datetime, lambda x: x.isoformat())
        self.register_str(datetime.date, lambda x: x.isoformat())
        self.register_str(datetime.time, lambda x: x.isoformat())
        self.register_str(bytes, lambda x: x.decode('utf-8', errors='replace'))
        self.register_str(bytearray, lambda x: x.decode('utf-8', errors='replace'))
        self.register_str(type(None), lambda x: "None")
        self.register_str(uuid.UUID, str)
        self.register_str(decimal.Decimal, str)
        
        # Integer converters
        self.register_int(int, lambda x: x)
        self.register_int(str, lambda x: int(x.strip()))
        self.register_int(float, int)
        self.register_int(bool, int)
        self.register_int(bytes, lambda x: int(x.decode('utf-8', errors='replace').strip()))
        self.register_int(bytearray, lambda x: int(x.decode('utf-8', errors='replace').strip()))
        self.register_int(decimal.Decimal, int)
        
        # Float converters
        self.register_float(float, lambda x: x)
        self.register_float(int, float)
        self.register_float(str, lambda x: float(x.strip()))
        self.register_float(bool, float)
        self.register_float(bytes, lambda x: float(x.decode('utf-8', errors='replace').strip()))
        self.register_float(bytearray, lambda x: float(x.decode('utf-8', errors='replace').strip()))
        self.register_float(decimal.Decimal, float)
        
        # Boolean converters
        self.register_bool(bool, lambda x: x)
        self.register_bool(int, lambda x: bool(x))
        self.register_bool(float, lambda x: bool(x))
        self.register_bool(str, lambda x: x.lower() in ('true', 'yes', 'y', '1', 'on'))
        self.register_bool(list, lambda x: bool(x))
        self.register_bool(dict, lambda x: bool(x))
        self.register_bool(type(None), lambda x: False)
        
        # List converters
        self.register_list(list, lambda x: x)
        self.register_list(tuple, list)
        self.register_list(set, list)
        self.register_list(str, lambda x: [x])
        self.register_list(int, lambda x: [x])
        self.register_list(float, lambda x: [x])
        self.register_list(bool, lambda x: [x])
        self.register_list(dict, lambda x: list(x.items()))
        
        # Dict converters
        self.register_dict(dict, lambda x: x)
        self.register_dict(list, lambda x: {i: v for i, v in enumerate(x)})
        self.register_dict(tuple, lambda x: {i: v for i, v in enumerate(x)})
    
    def register_str(self, type_: Type, converter: ConversionFunc) -> None:
        """Register a conversion function for converting to string."""
        self._str_converters[type_] = converter
        # Clear cache for this type
        if type_ in self._str_cache:
            del self._str_cache[type_]
    
    def register_int(self, type_: Type, converter: ConversionFunc) -> None:
        """Register a conversion function for converting to integer."""
        self._int_converters[type_] = converter
        # Clear cache for this type
        if type_ in self._int_cache:
            del self._int_cache[type_]
    
    def register_float(self, type_: Type, converter: ConversionFunc) -> None:
        """Register a conversion function for converting to float."""
        self._float_converters[type_] = converter
        # Clear cache for this type
        if type_ in self._float_cache:
            del self._float_cache[type_]
    
    def register_bool(self, type_: Type, converter: ConversionFunc) -> None:
        """Register a conversion function for converting to boolean."""
        self._bool_converters[type_] = converter
        # Clear cache for this type
        if type_ in self._bool_cache:
            del self._bool_cache[type_]
    
    def register_list(self, type_: Type, converter: ConversionFunc) -> None:
        """Register a conversion function for converting to list."""
        self._list_converters[type_] = converter
    
    def register_dict(self, type_: Type, converter: ConversionFunc) -> None:
        """Register a conversion function for converting to dictionary."""
        self._dict_converters[type_] = converter
    
    def _get_converter(self, type_: Type, converters: Dict[type, ConversionFunc]) -> Optional[ConversionFunc]:
        """Get the conversion function for a specific type."""
        # Direct match
        if type_ in converters:
            return converters[type_]
        
        # Check for subclass matches
        for registered_type, converter in converters.items():
            if issubclass(type_, registered_type):
                # Cache this result for future lookups
                converters[type_] = converter
                return converter
        
        return None
    
    def to_str(self, value: Any) -> str:
        """Convert a value to a string."""
        if value is None:
            return "None"
        
        value_type = type(value)
        
        # Check cache first
        if value_type in self._str_cache:
            return self._str_cache[value_type]
        
        # Get converter
        converter = self._get_converter(value_type, self._str_converters)
        
        if converter:
            try:
                result = converter(value)
                return result
            except Exception as e:
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"Error converting {value_type.__name__} to string: {e}")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to string: {e}") from e
                
                # Fallback to default str()
                return str(value)
        else:
            # Fallback to default str()
            return str(value)
    
    def to_int(self, value: Any) -> int:
        """Convert a value to an integer."""
        if value is None:
            return 0
        
        value_type = type(value)
        
        # Check cache first
        if value_type in self._int_cache:
            return self._int_cache[value_type]
        
        # Get converter
        converter = self._get_converter(value_type, self._int_converters)
        
        if converter:
            try:
                result = converter(value)
                return result
            except Exception as e:
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"Error converting {value_type.__name__} to integer: {e}")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to integer: {e}") from e
                
                # Fallback to 0
                return 0
        else:
            # Try default int() or fallback to 0
            try:
                return int(value)
            except (TypeError, ValueError):
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"No converter found for {value_type.__name__} to integer, using 0")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to integer") from None
                
                return 0
    
    def to_float(self, value: Any) -> float:
        """Convert a value to a float."""
        if value is None:
            return 0.0
        
        value_type = type(value)
        
        # Check cache first
        if value_type in self._float_cache:
            return self._float_cache[value_type]
        
        # Get converter
        converter = self._get_converter(value_type, self._float_converters)
        
        if converter:
            try:
                result = converter(value)
                return result
            except Exception as e:
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"Error converting {value_type.__name__} to float: {e}")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to float: {e}") from e
                
                # Fallback to 0.0
                return 0.0
        else:
            # Try default float() or fallback to 0.0
            try:
                return float(value)
            except (TypeError, ValueError):
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"No converter found for {value_type.__name__} to float, using 0.0")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to float") from None
                
                return 0.0
    
    def to_bool(self, value: Any) -> bool:
        """Convert a value to a boolean."""
        if value is None:
            return False
        
        value_type = type(value)
        
        # Check cache first
        if value_type in self._bool_cache:
            return self._bool_cache[value_type]
        
        # Get converter
        converter = self._get_converter(value_type, self._bool_converters)
        
        if converter:
            try:
                result = converter(value)
                return result
            except Exception as e:
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"Error converting {value_type.__name__} to boolean: {e}")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to boolean: {e}") from e
                
                # Fallback to False
                return False
        else:
            # Try default bool() or fallback to False
            try:
                return bool(value)
            except (TypeError, ValueError):
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"No converter found for {value_type.__name__} to boolean, using False")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to boolean") from None
                
                return False
    
    def to_list(self, value: Any) -> list:
        """Convert a value to a list."""
        if value is None:
            return []
        
        value_type = type(value)
        
        # Get converter
        converter = self._get_converter(value_type, self._list_converters)
        
        if converter:
            try:
                return converter(value)
            except Exception as e:
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"Error converting {value_type.__name__} to list: {e}")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to list: {e}") from e
                
                # Fallback to empty list
                return []
        else:
            # Try default list() or fallback to [value]
            try:
                return list(value)
            except (TypeError, ValueError):
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"No converter found for {value_type.__name__} to list, using [value]")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to list") from None
                
                return [value]
    
    def to_dict(self, value: Any) -> dict:
        """Convert a value to a dictionary."""
        if value is None:
            return {}
        
        value_type = type(value)
        
        # Get converter
        converter = self._get_converter(value_type, self._dict_converters)
        
        if converter:
            try:
                return converter(value)
            except Exception as e:
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"Error converting {value_type.__name__} to dict: {e}")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to dict: {e}") from e
                
                # Fallback to empty dict
                return {}
        else:
            # Try default dict() or fallback to {0: value}
            try:
                return dict(value)
            except (TypeError, ValueError):
                from .config import get_config
                config = get_config()
                
                if config.verbose:
                    logger.warning(f"No converter found for {value_type.__name__} to dict, using {0: value}")
                
                if config.raise_errors:
                    raise TypeError(f"Cannot convert {value_type.__name__} to dict") from None
                
                return {0: value}

# Global conversion registry
_registry = ConversionRegistry()

def register_converter(target_type: str, source_type: Type, converter: ConversionFunc) -> None:
    """
    Register a custom converter for a specific type.
    
    Args:
        target_type: The target type ('str', 'int', 'float', 'bool', 'list', 'dict')
        source_type: The source type to convert from
        converter: A function that converts instances of the source type to the target type
    """
    if target_type == 'str':
        _registry.register_str(source_type, converter)
    elif target_type == 'int':
        _registry.register_int(source_type, converter)
    elif target_type == 'float':
        _registry.register_float(source_type, converter)
    elif target_type == 'bool':
        _registry.register_bool(source_type, converter)
    elif target_type == 'list':
        _registry.register_list(source_type, converter)
    elif target_type == 'dict':
        _registry.register_dict(source_type, converter)
    else:
        raise ValueError(f"Unknown target type: {target_type}")

def get_converter(target_type: str) -> ConversionRegistry:
    """
    Get the converter registry for a specific target type.
    
    Args:
        target_type: The target type ('str', 'int', 'float', 'bool', 'list', 'dict')
    
    Returns:
        The conversion registry
    """
    return _registry
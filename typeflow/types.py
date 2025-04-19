"""
Enhanced type implementations for TypeFlow.
"""

import builtins
import logging
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union, cast

logger = logging.getLogger("typeflow")

# Store original built-in types
_original_str = builtins.str
_original_int = builtins.int
_original_float = builtins.float
_original_list = builtins.list
_original_dict = builtins.dict
_original_bool = builtins.bool

# Type variables for generic methods
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class FlowStr(str):
    """Enhanced string class that handles operations with different types."""
    
    def __add__(self, other: Any) -> 'FlowStr':
        """Handle string concatenation with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, str):
            return FlowStr(super().__add__(other))
        
        try:
            # Convert other to string
            other_str = get_converter('str').to_str(other)
            
            if config.verbose and not isinstance(other, str):
                logger.info(f"Converting {type(other).__name__} to string for concatenation: {other!r} -> {other_str!r}")
            
            return FlowStr(super().__add__(other_str))
        except Exception as e:
            if config.raise_errors:
                raise TypeError(f"Cannot concatenate {type(other).__name__} with string: {e}") from e
            
            # Fallback to string representation
            return FlowStr(super().__add__(str(other)))
    
    def __radd__(self, other: Any) -> 'FlowStr':
        """Handle string concatenation with any type (right side)."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        try:
            # Convert other to string
            other_str = get_converter('str').to_str(other)
            
            if config.verbose and not isinstance(other, str):
                logger.info(f"Converting {type(other).__name__} to string for concatenation: {other!r} -> {other_str!r}")
            
            return FlowStr(other_str + self)
        except Exception as e:
            if config.raise_errors:
                raise TypeError(f"Cannot concatenate string with {type(other).__name__}: {e}") from e
            
            # Fallback to string representation
            return FlowStr(str(other) + self)
    
    def __mul__(self, other: Any) -> 'FlowStr':
        """Handle string multiplication with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, int):
            return FlowStr(super().__mul__(other))
        
        try:
            # Convert other to integer
            other_int = get_converter('int').to_int(other)
            
            if config.verbose and not isinstance(other, int):
                logger.info(f"Converting {type(other).__name__} to integer for string multiplication: {other!r} -> {other_int!r}")
            
            return FlowStr(super().__mul__(other_int))
        except Exception as e:
            if config.raise_errors:
                raise TypeError(f"Cannot multiply string with {type(other).__name__}: {e}") from e
            
            # Fallback to 1
            return FlowStr(self)
    
    def __rmul__(self, other: Any) -> 'FlowStr':
        """Handle string multiplication with any type (right side)."""
        return self.__mul__(other)

class FlowInt(int):
    """Enhanced integer class that handles operations with different types."""
    
    def __add__(self, other: Any) -> Union['FlowInt', FlowStr, 'FlowFloat']:
        """Handle integer addition with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, (int, float)):
            return super().__add__(other)
        elif isinstance(other, str):
            # When adding int to str, convert int to str
            int_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {int_str!r}")
            
            return FlowStr(int_str + other)
        
        try:
            # Try to convert other to int
            other_int = get_converter('int').to_int(other)
            
            if config.verbose and not isinstance(other, (int, float, str)):
                logger.info(f"Converting {type(other).__name__} to integer for addition: {other!r} -> {other_int!r}")
            
            return FlowInt(super().__add__(other_int))
        except Exception as e:
            # If conversion to int fails, try converting self to the other's type
            if isinstance(other, float):
                return FlowFloat(float(self) + other)
            
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to integer, using string concatenation")
            
            int_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot add integer with {type(other).__name__}: {e}") from e
            
            return FlowStr(int_str + other_str)
    
    def __radd__(self, other: Any) -> Union['FlowInt', FlowStr, 'FlowFloat']:
        """Handle integer addition with any type (right side)."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, (int, float)):
            return FlowInt(other + self)
        elif isinstance(other, str):
            # When adding str to int, convert int to str
            int_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {int_str!r}")
            
            return FlowStr(other + int_str)
        
        try:
            # Try to convert other to int
            other_int = get_converter('int').to_int(other)
            
            if config.verbose and not isinstance(other, (int, float, str)):
                logger.info(f"Converting {type(other).__name__} to integer for addition: {other!r} -> {other_int!r}")
            
            return FlowInt(other_int + self)
        except Exception as e:
            # If conversion to int fails, try converting self to the other's type
            if isinstance(other, float):
                return FlowFloat(other + float(self))
            
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to integer, using string concatenation")
            
            int_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot add {type(other).__name__} with integer: {e}") from e
            
            return FlowStr(other_str + int_str)
    
    def __mul__(self, other: Any) -> Union['FlowInt', FlowStr, 'FlowFloat', List[Any]]:
        """Handle integer multiplication with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, (int, float)):
            return super().__mul__(other)
        elif isinstance(other, str):
            # When multiplying int with str, use string repetition
            return FlowStr(other * self)
        elif isinstance(other, list):
            # When multiplying int with list, repeat the list
            return other * self
        
        try:
            # Try to convert other to int
            other_int = get_converter('int').to_int(other)
            
            if config.verbose and not isinstance(other, (int, float, str, list)):
                logger.info(f"Converting {type(other).__name__} to integer for multiplication: {other!r} -> {other_int!r}")
            
            return FlowInt(super().__mul__(other_int))
        except Exception as e:
            # If conversion to int fails, try converting self to the other's type
            if isinstance(other, float):
                return FlowFloat(float(self) * other)
            
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to integer for multiplication")
            
            if config.raise_errors:
                raise TypeError(f"Cannot multiply integer with {type(other).__name__}: {e}") from e
            
            # Default behavior: convert other to int or return self
            return FlowInt(self)

class FlowFloat(float):
    """Enhanced float class that handles operations with different types."""
    
    def __add__(self, other: Any) -> Union['FlowFloat', FlowStr]:
        """Handle float addition with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, (int, float)):
            return super().__add__(other)
        elif isinstance(other, str):
            # When adding float to str, convert float to str
            float_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {float_str!r}")
            
            return FlowStr(float_str + other)
        
        try:
            # Try to convert other to float
            other_float = get_converter('float').to_float(other)
            
            if config.verbose and not isinstance(other, (int, float, str)):
                logger.info(f"Converting {type(other).__name__} to float for addition: {other!r} -> {other_float!r}")
            
            return FlowFloat(super().__add__(other_float))
        except Exception as e:
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to float, using string concatenation")
            
            float_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot add float with {type(other).__name__}: {e}") from e
            
            return FlowStr(float_str + other_str)
    
    def __radd__(self, other: Any) -> Union['FlowFloat', FlowStr]:
        """Handle float addition with any type (right side)."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, (int, float)):
            return FlowFloat(other + self)
        elif isinstance(other, str):
            # When adding str to float, convert float to str
            float_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {float_str!r}")
            
            return FlowStr(other + float_str)
        
        try:
            # Try to convert other to float
            other_float = get_converter('float').to_float(other)
            
            if config.verbose and not isinstance(other, (int, float, str)):
                logger.info(f"Converting {type(other).__name__} to float for addition: {other!r} -> {other_float!r}")
            
            return FlowFloat(other_float + self)
        except Exception as e:
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to float, using string concatenation")
            
            float_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot add {type(other).__name__} with float: {e}") from e
            
            return FlowStr(other_str + float_str)

class FlowList(list):
    """Enhanced list class that handles operations with different types."""
    
    def __add__(self, other: Any) -> Union['FlowList', FlowStr]:
        """Handle list concatenation with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, list):
            return FlowList(super().__add__(other))
        elif isinstance(other, str):
            # When adding list to str, convert list to str
            list_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {list_str!r}")
            
            return FlowStr(list_str + other)
        
        try:
            # Try to convert other to list
            other_list = get_converter('list').to_list(other)
            
            if config.verbose and not isinstance(other, (list, str)):
                logger.info(f"Converting {type(other).__name__} to list for concatenation: {other!r} -> {other_list!r}")
            
            return FlowList(super().__add__(other_list))
        except Exception as e:
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to list, using string concatenation")
            
            list_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot concatenate list with {type(other).__name__}: {e}") from e
            
            return FlowStr(list_str + other_str)
    
    def __radd__(self, other: Any) -> Union['FlowList', FlowStr]:
        """Handle list concatenation with any type (right side)."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, list):
            return FlowList(other + self)
        elif isinstance(other, str):
            # When adding str to list, convert list to str
            list_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {list_str!r}")
            
            return FlowStr(other + list_str)
        
        try:
            # Try to convert other to list
            other_list = get_converter('list').to_list(other)
            
            if config.verbose and not isinstance(other, (list, str)):
                logger.info(f"Converting {type(other).__name__} to list for concatenation: {other!r} -> {other_list!r}")
            
            return FlowList(other_list + self)
        except Exception as e:
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to list, using string concatenation")
            
            list_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot concatenate {type(other).__name__} with list: {e}") from e
            
            return FlowStr(other_str + list_str)
    
    def __mul__(self, other: Any) -> 'FlowList':
        """Handle list multiplication with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, int):
            return FlowList(super().__mul__(other))
        
        try:
            # Try to convert other to int
            other_int = get_converter('int').to_int(other)
            
            if config.verbose and not isinstance(other, int):
                logger.info(f"Converting {type(other).__name__} to integer for list multiplication: {other!r} -> {other_int!r}")
            
            return FlowList(super().__mul__(other_int))
        except Exception as e:
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to integer for list multiplication")
            
            if config.raise_errors:
                raise TypeError(f"Cannot multiply list with {type(other).__name__}: {e}") from e
            
            # Default behavior: return empty list
            return FlowList([])

class FlowDict(dict):
    """Enhanced dictionary class that handles operations with different types."""
    
    def __add__(self, other: Any) -> Union['FlowDict', FlowStr]:
        """Handle dictionary addition with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, dict):
            # When adding dict to dict, merge them
            result = FlowDict(self)
            result.update(other)
            return result
        elif isinstance(other, str):
            # When adding dict to str, convert dict to str
            dict_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {dict_str!r}")
            
            return FlowStr(dict_str + other)
        
        try:
            # Try to convert other to dict
            other_dict = get_converter('dict').to_dict(other)
            
            if config.verbose and not isinstance(other, (dict, str)):
                logger.info(f"Converting {type(other).__name__} to dict for merging: {other!r} -> {other_dict!r}")
            
            result = FlowDict(self)
            result.update(other_dict)
            return result
        except Exception as e:
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to dict, using string concatenation")
            
            dict_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot add dictionary with {type(other).__name__}: {e}") from e
            
            return FlowStr(dict_str + other_str)
    
    def __radd__(self, other: Any) -> Union['FlowDict', FlowStr]:
        """Handle dictionary addition with any type (right side)."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, dict):
            # When adding dict to dict, merge them (other takes precedence)
            result = FlowDict(other)
            result.update(self)
            return result
        elif isinstance(other, str):
            # When adding str to dict, convert dict to str
            dict_str = get_converter('str').to_str(self)
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {dict_str!r}")
            
            return FlowStr(other + dict_str)
        
        try:
            # Try to convert other to dict
            other_dict = get_converter('dict').to_dict(other)
            
            if config.verbose and not isinstance(other, (dict, str)):
                logger.info(f"Converting {type(other).__name__} to dict for merging: {other!r} -> {other_dict!r}")
            
            result = FlowDict(other_dict)
            result.update(self)
            return result
        except Exception as e:
            # As a last resort, convert to string
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} to dict, using string concatenation")
            
            dict_str = get_converter('str').to_str(self)
            other_str = get_converter('str').to_str(other)
            
            if config.raise_errors:
                raise TypeError(f"Cannot add {type(other).__name__} with dictionary: {e}") from e
            
            return FlowStr(other_str + dict_str)

class FlowBool(int):
    """Enhanced boolean class that handles operations with different types."""
    
    def __new__(cls, value=False):
        return super().__new__(cls, 1 if value else 0)
    
    def __repr__(self):
        return 'True' if self else 'False'
    
    def __str__(self):
        return 'True' if self else 'False'
    
    def __add__(self, other: Any) -> Union['FlowInt', 'FlowFloat', FlowStr]:
        """Handle boolean addition with any type."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, (int, float)):
            # When adding bool to number, convert bool to int
            return FlowInt(int(self) + other) if isinstance(other, int) else FlowFloat(int(self) + other)
        elif isinstance(other, str):
            # When adding bool to str, convert bool to str
            bool_str = 'True' if self else 'False'
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {bool_str!r}")
            
            return FlowStr(bool_str + other)
        
        try:
            # Try to convert other to appropriate type
            if isinstance(other, bool):
                return FlowInt(int(self) + int(other))
            
            # Try numeric conversion first
            try:
                other_num = get_converter('int').to_int(other)
                
                if config.verbose and not isinstance(other, (int, float, bool, str)):
                    logger.info(f"Converting {type(other).__name__} to integer for addition: {other!r} -> {other_num!r}")
                
                return FlowInt(int(self) + other_num)
            except Exception:
                # If numeric conversion fails, try string
                bool_str = 'True' if self else 'False'
                other_str = get_converter('str').to_str(other)
                
                if config.verbose:
                    logger.info(f"Converting {type(other).__name__} to string for concatenation: {other!r} -> {other_str!r}")
                
                return FlowStr(bool_str + other_str)
        except Exception as e:
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} for addition with boolean")
            
            if config.raise_errors:
                raise TypeError(f"Cannot add boolean with {type(other).__name__}: {e}") from e
            
            # Default: convert both to strings
            bool_str = 'True' if self else 'False'
            other_str = str(other)
            return FlowStr(bool_str + other_str)
    
    def __radd__(self, other: Any) -> Union['FlowInt', 'FlowFloat', FlowStr]:
        """Handle boolean addition with any type (right side)."""
        from .config import get_config
        from .converters import get_converter
        
        config = get_config()
        
        if isinstance(other, (int, float)):
            # When adding number to bool, convert bool to int
            return FlowInt(other + int(self)) if isinstance(other, int) else FlowFloat(other + int(self))
        elif isinstance(other, str):
            # When adding str to bool, convert bool to str
            bool_str = 'True' if self else 'False'
            
            if config.verbose:
                logger.info(f"Converting {type(self).__name__} to string for concatenation with string: {self!r} -> {bool_str!r}")
            
            return FlowStr(other + bool_str)
        
        try:
            # Try to convert other to appropriate type
            if isinstance(other, bool):
                return FlowInt(int(other) + int(self))
            
            # Try numeric conversion first
            try:
                other_num = get_converter('int').to_int(other)
                
                if config.verbose and not isinstance(other, (int, float, bool, str)):
                    logger.info(f"Converting {type(other).__name__} to integer for addition: {other!r} -> {other_num!r}")
                
                return FlowInt(other_num + int(self))
            except Exception:
                # If numeric conversion fails, try string
                bool_str = 'True' if self else 'False'
                other_str = get_converter('str').to_str(other)
                
                if config.verbose:
                    logger.info(f"Converting {type(other).__name__} to string for concatenation: {other!r} -> {other_str!r}")
                
                return FlowStr(other_str + bool_str)
        except Exception as e:
            if config.verbose:
                logger.warning(f"Failed to convert {type(other).__name__} for addition with boolean")
            
            if config.raise_errors:
                raise TypeError(f"Cannot add {type(other).__name__} with boolean: {e}") from e
            
            # Default: convert both to strings
            bool_str = 'True' if self else 'False'
            other_str = str(other)
            return FlowStr(other_str + bool_str)

def flow(value: Any) -> Union[FlowStr, FlowInt, FlowFloat, FlowList, FlowDict, FlowBool]:
    """
    Convert a value to its corresponding TypeFlow type.
    
    Args:
        value: The value to convert
    
    Returns:
        The value wrapped in the appropriate TypeFlow type
    """
    if isinstance(value, str):
        return FlowStr(value)
    elif isinstance(value, int) and not isinstance(value, bool):
        return FlowInt(value)
    elif isinstance(value, float):
        return FlowFloat(value)
    elif isinstance(value, list):
        return FlowList(value)
    elif isinstance(value, dict):
        return FlowDict(value)
    elif isinstance(value, bool):
        return FlowBool(value)
    else:
        # Try to convert to string as a fallback
        return FlowStr(str(value))
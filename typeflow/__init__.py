"""
TypeFlow: Seamlessly handle type conversion during operations in Python.
"""

import logging

# Set up package logging
logger = logging.getLogger("typeflow")
logger.addHandler(logging.NullHandler())

# Import key components for public API
from .config import configure
from .converters import register_converter, get_converter
from .core import TypeFlowContext, with_typeflow, enable, disable, is_enabled
from .types import (
    FlowStr, FlowInt, FlowFloat, FlowList, FlowDict, FlowBool, flow
)

# Version information
__version__ = "0.13.6"
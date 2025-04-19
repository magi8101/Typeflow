"""
TypeFlow: Seamless Type Conversion for Python Operations

A Python package that automatically handles type conversion during operations,
eliminating TypeError exceptions when combining different data types.
"""

from .core import enable, disable, is_enabled, TypeFlowContext, with_typeflow
from .converters import register_converter, get_converter, ConversionRegistry
from .config import configure, get_config, Config
from .types import FlowStr, FlowInt, FlowFloat, FlowList, FlowDict, FlowBool, flow

__version__ = "0.1.0"

__all__ = [
    'enable',
    'disable',
    'is_enabled',
    'TypeFlowContext',
    'with_typeflow',
    'register_converter',
    'get_converter',
    'ConversionRegistry',
    'configure',
    'get_config',
    'Config',
    'FlowStr',
    'FlowInt',
    'FlowFloat',
    'FlowList',
    'FlowDict',
    'FlowBool',
    'flow'
]
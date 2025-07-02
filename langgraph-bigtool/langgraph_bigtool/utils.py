import inspect
from functools import wraps
from typing import Callable

from langchain_core._api import beta
from langchain_core.tools import tool


@beta()
def convert_positional_only_function_to_tool(func: Callable):
    """Handle tool creation for functions with positional-only args."""
    try:
        original_signature = inspect.signature(func)
    except ValueError:  # no signature
        return None
    new_params = []

    # Convert any POSITIONAL_ONLY parameters into POSITIONAL_OR_KEYWORD
    for param in original_signature.parameters.values():
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            return None
        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            new_params.append(
                param.replace(kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)
            )
        else:
            new_params.append(param)

    updated_signature = inspect.Signature(new_params)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = updated_signature.bind(*args, **kwargs)
        bound.apply_defaults()
        return func(*bound.args, **bound.kwargs)

    wrapper.__signature__ = updated_signature

    return tool(wrapper)

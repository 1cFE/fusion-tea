"""Module introspection utilities for automatic registry building."""
from typing import Any, Dict, Type, get_args, get_origin

from pydantic import BaseModel, RootModel

from .base import ModuleBase


class ModuleIntrospectionError(Exception):
    """Raised when module introspection fails validation."""

    pass


def is_rootmodel(model_cls: Type[BaseModel]) -> bool:
    """Check if a Pydantic model is a RootModel.

    Args:
        model_cls: Pydantic model class to check

    Returns:
        True if model_cls is a RootModel subclass, False otherwise

    Example:
        >>> from pydantic import RootModel
        >>> is_rootmodel(RootModel[float])
        True
        >>> is_rootmodel(BaseModel)
        False
    """
    try:
        # Check if it's a subclass of RootModel
        # RootModel[float] creates a class that inherits from RootModel
        return issubclass(model_cls, RootModel)
    except TypeError:
        # issubclass raises TypeError if model_cls is not a class
        return False


def extract_io_models(module_cls: Type[ModuleBase]) -> tuple[Type[BaseModel], Type[BaseModel]]:
    """Extract InputModel and OutputModel from ModuleBase generic type hints.

    Args:
        module_cls: Module class that inherits from ModuleBase[InputModel, OutputModel]

    Returns:
        Tuple of (InputModel, OutputModel) types

    Raises:
        ModuleIntrospectionError: If module does not properly inherit ModuleBase with type params
    """
    # Get original base classes with generic type parameters
    if not hasattr(module_cls, "__orig_bases__"):
        raise ModuleIntrospectionError(
            f"Module class {module_cls.__name__} does not have __orig_bases__. "
            "It must directly inherit from ModuleBase[InputModel, OutputModel]."
        )

    # Find ModuleBase in the inheritance chain
    module_base = None
    for base in module_cls.__orig_bases__:
        origin = get_origin(base)
        if origin is not None and issubclass(origin, ModuleBase):
            module_base = base
            break

    if module_base is None:
        raise ModuleIntrospectionError(
            f"Module class {module_cls.__name__} does not inherit from ModuleBase with type parameters. "
            "Expected: class MyModule(ModuleBase[InputModel, OutputModel])"
        )

    # Extract type arguments
    type_args = get_args(module_base)
    if len(type_args) != 2:
        raise ModuleIntrospectionError(
            f"Module class {module_cls.__name__} must have exactly 2 type parameters. "
            f"Found {len(type_args)}. Expected: ModuleBase[InputModel, OutputModel]"
        )

    input_model, output_model = type_args

    # Validate both are BaseModel subclasses
    if not (isinstance(input_model, type) and issubclass(input_model, BaseModel)):
        raise ModuleIntrospectionError(
            f"Input type parameter must be a Pydantic BaseModel subclass. "
            f"Got: {input_model}"
        )

    if not (isinstance(output_model, type) and issubclass(output_model, BaseModel)):
        raise ModuleIntrospectionError(
            f"Output type parameter must be a Pydantic BaseModel subclass. "
            f"Got: {output_model}"
        )

    return input_model, output_model


def extract_field_types(
    model_cls: Type[BaseModel],
) -> tuple[Dict[str, type], Dict[str, type]]:
    """Extract required and optional field types from Pydantic model.

    Args:
        model_cls: Pydantic BaseModel class

    Returns:
        Tuple of (required_fields, optional_fields) where each is dict[field_name -> type]
    """
    required_fields: Dict[str, type] = {}
    optional_fields: Dict[str, type] = {}

    for field_name, field_info in model_cls.model_fields.items():
        field_type = field_info.annotation

        if field_info.is_required():
            required_fields[field_name] = field_type
        else:
            optional_fields[field_name] = field_type

    return required_fields, optional_fields


def introspect_module(module_cls: Type[ModuleBase]) -> Dict[str, Any]:
    """Introspect module to extract all metadata needed for ModuleDescriptor.

    Args:
        module_cls: Module class inheriting from ModuleBase[InputModel, OutputModel]

    Returns:
        Dictionary with keys: module_type, input_model, output_model,
        required_inputs, optional_inputs, outputs, version, name

    Raises:
        ModuleIntrospectionError: If module structure is invalid
    """
    # Validate required attributes
    if not hasattr(module_cls, "name"):
        raise ModuleIntrospectionError(
            f"Module class {module_cls.__name__} must define 'name' class attribute"
        )

    if not hasattr(module_cls, "version"):
        raise ModuleIntrospectionError(
            f"Module class {module_cls.__name__} must define 'version' class attribute"
        )

    # Extract I/O models
    input_model, output_model = extract_io_models(module_cls)

    # Extract field types from input model
    required_inputs, optional_inputs = extract_field_types(input_model)

    # Extract field types from output model (all outputs are "required")
    outputs_raw, _ = extract_field_types(output_model)

    # SPECIAL CASE: RootModel single-output modules
    # For single-output modules, the executor stores the WHOLE OutputModel object
    # in the channel (see pipeline_executor.py:217-220), not extracted fields.
    # So the descriptor must declare the OutputModel type, not the field type.
    # This enables field extraction validation to work correctly (e.g., channel.root).
    if is_rootmodel(output_model) and len(outputs_raw) == 1:
        # Replace field type with OutputModel type
        # For RootModel[float], field is 'root' with type float
        # We need to register 'root' with type RootModel[float] instead
        field_name = next(iter(outputs_raw.keys()))  # Should be 'root'
        outputs = {field_name: output_model}  # Use RootModel[T], not T
    else:
        # Normal case: use extracted field types
        # This handles multi-output and non-RootModel modules
        outputs = outputs_raw

    # Build metadata dictionary
    metadata = {
        "module_type": module_cls.__name__,
        "input_model": input_model,
        "output_model": output_model,
        "required_inputs": required_inputs,
        "optional_inputs": optional_inputs,
        "outputs": outputs,
        "version": module_cls.version,
        "name": module_cls.name,
    }

    return metadata

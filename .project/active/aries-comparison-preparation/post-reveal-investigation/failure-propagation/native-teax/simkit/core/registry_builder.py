"""Registry builder for automatic module registration."""
from typing import Dict, List, Type

from .base import ModuleBase
from .module_introspector import ModuleIntrospectionError, introspect_module
from .pipeline_registry import ModuleDescriptor, PipelineModuleRegistry


def create_registry(
    modules: List[Type[ModuleBase]],
    module_type_override: Dict[Type[ModuleBase], str] | None = None,
) -> PipelineModuleRegistry:
    """Create PipelineModuleRegistry from list of module classes.

    This function automatically introspects each module class to extract metadata
    and creates ModuleDescriptor instances without manual specification.

    Args:
        modules: List of ModuleBase subclasses to register
        module_type_override: Optional dict mapping module classes to custom module_type names
                             (defaults to class.__name__ if not provided)

    Returns:
        PipelineModuleRegistry ready for pipeline execution

    Raises:
        ModuleIntrospectionError: If any module fails validation
        ValueError: If duplicate module_type names detected

    Example:
        >>> from pydantic import BaseModel
        >>> from simkit.core.base import ModuleBase, ModuleResult
        >>>
        >>> class MyInput(BaseModel):
        ...     value: float
        >>>
        >>> class MyOutput(BaseModel):
        ...     result: float
        >>>
        >>> class MyModule(ModuleBase[MyInput, MyOutput]):
        ...     name = "my_module"
        ...     version = "v1.0"
        ...
        ...     def validate_and_fill_default(self, inputs):
        ...         return MyInput(**inputs)
        ...
        ...     def run(self, inputs):
        ...         return ModuleResult(data=MyOutput(result=inputs.value * 2))
        >>>
        >>> # Create registry with custom module
        >>> registry = create_registry([MyModule])
        >>> assert registry.has('MyModule')
        >>>
        >>> # Override module_type name
        >>> registry = create_registry(
        ...     [MyModule],
        ...     module_type_override={MyModule: "CustomName"}
        ... )
        >>> assert registry.has('CustomName')
    """
    # Helper function to create factory closures
    def _make_factory(cls: Type[ModuleBase]):
        def factory():
            return cls()

        return factory

    # Start with empty registry
    registry = PipelineModuleRegistry()

    # Track seen module_types to detect duplicates
    seen_module_types: set[str] = set()

    # Override dict defaults to empty
    override_dict = module_type_override or {}

    # Process each module
    for module_cls in modules:
        try:
            # Introspect module to extract metadata
            metadata = introspect_module(module_cls)

            # Determine module_type (use override if provided, else class name)
            module_type = override_dict.get(module_cls, metadata["module_type"])

            # Check for duplicates
            if module_type in seen_module_types:
                raise ValueError(
                    f"Duplicate module_type '{module_type}' detected. "
                    f"Module class {module_cls.__name__} conflicts with existing registration. "
                    f"Use module_type_override to provide a unique name."
                )

            seen_module_types.add(module_type)

            # Create factory
            factory = _make_factory(module_cls)

            # Create descriptor
            descriptor = ModuleDescriptor(
                module_type=module_type,
                factory=factory,
                required_inputs=metadata["required_inputs"],
                optional_inputs=metadata["optional_inputs"],
                outputs=metadata["outputs"],
                version=metadata["version"],
            )

            # Register in registry
            registry.register(module_type, descriptor)

        except ModuleIntrospectionError as e:
            # Re-raise with additional context
            raise ModuleIntrospectionError(
                f"Failed to register module {module_cls.__name__}: {e}"
            ) from e

    return registry


def create_fusion_registry_example() -> PipelineModuleRegistry:
    """Example function showing how external packages would create registries.

    This pattern would be implemented in fusion_simkit.__init__.py or similar.
    External users would import this function rather than building registries manually.

    Returns:
        Registry with all fusion physics modules

    Example:
        >>> # In fusion_simkit package
        >>> from fusion_simkit import create_fusion_registry
        >>> from simkit.core.pipeline import execute_pipeline
        >>>
        >>> # Create registry with fusion modules
        >>> registry = create_fusion_registry()
        >>>
        >>> # Execute pipeline with custom modules
        >>> result = execute_pipeline(
        ...     "fusion_pipeline.yaml",
        ...     "outputs/",
        ...     registry=registry
        ... )

    Note:
        This is a placeholder example. Real implementation would import actual
        fusion module classes from tests.teax_simkit.modules or similar location.
        For now, returns empty registry as fusion modules are not yet available.
    """
    # TODO: Replace with actual fusion module imports when available
    # from tests.teax_simkit.modules.alphaneutronsplit import AlphaNeutronSplitModule
    # from tests.teax_simkit.modules.otherfusionmodule import OtherFusionModule
    #
    # fusion_modules = [
    #     AlphaNeutronSplitModule,
    #     OtherFusionModule,
    # ]
    #
    # return create_registry(fusion_modules)

    # For now, return empty registry
    return create_registry([])

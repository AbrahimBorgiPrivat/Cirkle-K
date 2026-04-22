import logging
import importlib

logger = logging.getLogger(__name__)


def main(runtime_vars: dict) -> None:
    modules = runtime_vars.get("modules", [])
    if not modules:
        logger.warning("No modules configured.")
        return

    for module_config in modules:
        module_path = module_config["module"]
        callable_name = module_config.get("callable", "main")
        kwargs = module_config.get("kwargs", {})
        step_name = module_config.get("name", module_path)

        logger.info("Running: %s", step_name)
        module = importlib.import_module(module_path)
        callable_obj = getattr(module, callable_name)
        callable_obj(**kwargs)
        logger.info("Completed: %s", step_name)

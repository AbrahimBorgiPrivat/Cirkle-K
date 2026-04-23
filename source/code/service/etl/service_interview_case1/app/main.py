import importlib
import logging
import os
from pathlib import Path

from libraries.utils import runtime

logger = logging.getLogger(__name__)


def get_runtime_base(current_dir: Path, runtime_namespace: str) -> Path:
    container_path = current_dir.parent / "runtime_definitions" / runtime_namespace / "runtime"
    if container_path.exists():
        return container_path

    repo_path = current_dir.parents[3] / "runtime_definitions" / runtime_namespace / "runtime"
    if repo_path.exists():
        return repo_path

    raise FileNotFoundError(f"Could not locate runtime directory for '{runtime_namespace}'.")


def run_runner(module_path: str, runtime_json_path: Path) -> None:
    logger.info("Running %s using %s", module_path, runtime_json_path)
    module = importlib.import_module(module_path)
    if not hasattr(module, "main"):
        raise AttributeError(f"Module {module_path} has no 'main' function")
    runtime_vars = runtime.load_runtime_vars(JSON_PATH=runtime_json_path)
    module.main(runtime_vars)
    logger.info("Completed runtime file %s", runtime_json_path.name)


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    runtime_namespace = os.getenv("RUNTIME_NAMESPACE", "service_interview_case1")
    runtime_base = get_runtime_base(current_dir, runtime_namespace)
    runner_module = os.getenv("RUNNER_MODULE", "libraries.runners.module_sequence")
    runtime_files_env = os.getenv("RUNTIME_FILES", "all.json")
    runtime_files = [file_name.strip() for file_name in runtime_files_env.split(",") if file_name.strip()]

    for file_name in runtime_files:
        runtime_json = runtime_base / file_name
        if not runtime_json.exists():
            logger.warning("Runtime file not found, skipping: %s", runtime_json)
            continue
        run_runner(runner_module, runtime_json)

    logger.info("All runtime files processed successfully.")

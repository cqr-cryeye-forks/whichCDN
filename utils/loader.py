import importlib.util
import pathlib

from utils.paths import PLUGIN_FOLDER


def get_plugins() -> list[str]:
    return [d.name for d in PLUGIN_FOLDER.iterdir() if (d / "behaviors.py").exists()]


def load_plugin(name: str):
    path = PLUGIN_FOLDER / name / "behaviors.py"
    spec = importlib.util.spec_from_file_location(f"plugins.{name}.behaviors", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

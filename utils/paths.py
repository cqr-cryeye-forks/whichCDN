import pathlib
from typing import Final

MAIN_DIR: Final[pathlib.Path] = pathlib.Path(__file__).resolve().parents[1]
PLUGIN_FOLDER: Final[pathlib.Path] = MAIN_DIR / "plugins"

import pathlib
from os.path import abspath, dirname, join
import tomllib

from dynaconf import Dynaconf


PR_AGENT_TOML_KEY = "pr-agent"

current_dir = dirname(abspath(__file__))
setting_dir = current_dir


toml_files = list(pathlib.Path(join(setting_dir)).glob('*.toml')) # includes hidden files
global_settings = Dynaconf(
    envvar_prefix=False,
    merge_enabled=True,
    settings_files=toml_files,
)


def get_settings():
    return global_settings


if __name__ == "__main__":
    for path in toml_files:
        print(path)
        with open(path, "rb") as f:
            print(tomllib.load(f))

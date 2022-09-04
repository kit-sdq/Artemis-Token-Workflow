import json
from pathlib import Path
from typing import Any, List, Optional


class ConfigLoader:
    def __init__(self, paths: List[Path]):
        """
        Supply a list of configuration files.
        List items at the front take precedence over later list items.
        """
        print(f"Using config files {paths}")

        self._configs = []
        for path in paths:
            with open(path, "r") as file:
                self._configs.append(json.load(file))

    def _get_from_config(self, config: dict, key: str) -> Optional[Any]:
        current = config
        for part in key.split("."):
            if not isinstance(current, dict):
                return None
            if part not in current:
                return None
            current = current[part]
        if isinstance(current, dict):
            return None
        return current

    def get(self, key: str) -> str:
        """
        Returns the setting for a given key.
        Nested settings can be accessed by separating the objects by a dot.
        Raises KeyError if setting is missing.
        """

        for config in self._configs:
            single = self._get_from_config(config, key)
            if single is not None:
                return single

        raise KeyError(f"Key {key} was not found in settings.")

    def __getitem__(self, key) -> str:
        return self.get(key)

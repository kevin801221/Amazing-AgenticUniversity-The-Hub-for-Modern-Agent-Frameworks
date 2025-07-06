import json

class ConfigLoader:
    """
    A class to load configuration from a JSON file.
    """
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self):
        """
        Load and parse the JSON configuration file.
        """
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing {self.config_file}: {e}")

    def get(self, key, default=None):
        """
        Get a configuration value by key.
        """
        return self.config_data.get(key, default)

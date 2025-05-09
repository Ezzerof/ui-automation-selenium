import os
import yaml

def load_config():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_path, "config", "config.yaml")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

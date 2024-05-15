import yaml
import os

def load_config(file_path="config/config.yml"):
    """Load YAML configuration file."""
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        print("Configuration file not found.")
    except yaml.YAMLError as exc:
        print("Error in configuration file:", exc)

# 例如使用
if __name__ == "__main__":
    config = load_config()
    print(config)
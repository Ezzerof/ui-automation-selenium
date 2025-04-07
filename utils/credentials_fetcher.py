from utils.config_loader import load_config

config = load_config()

def get_credentials(credential: str) -> str:
    try:
        return config["credentials"][credential]
    except KeyError:
        raise ValueError(f"Credential '{credential}' not found in config.")

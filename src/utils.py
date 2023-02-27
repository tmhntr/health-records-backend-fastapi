from configparser import ConfigParser
from dotenv import load_dotenv
import os

dotenv_files = [
    ".env.local",
    ".env",
]

for dotenv_file in dotenv_files:
    load_dotenv(dotenv_file)

env = os.environ

def set_up():
    """Sets up configuration for the app"""

    env = os.getenv("ENV", ".config")

    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["AUTH0"]
    else:
        config = {
            "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
            "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
            "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
        }
    return config

def env_get(key, default=None):
    """Gets a value from the environment"""
    return env.get(key, default)
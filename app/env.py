from dotenv import load_dotenv
import os

dotenv_files = [
    ".env.local",
    ".env",
]

for dotenv_file in dotenv_files:
    load_dotenv(dotenv_file)

env = os.environ
import os

DATABASE_URL: str = os.getenv('DATA_BASE_URL')
if not DATABASE_URL:
    from .config import CONFIG_DATABASE_URL
    DATABASE_URL = CONFIG_DATABASE_URL
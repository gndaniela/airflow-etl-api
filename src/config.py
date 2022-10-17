from decouple import AutoConfig
import pkgutil
from pathlib import Path

ROOT_DIR = Path(pkgutil.get_loader("src").get_filename()).parent

dconfig = AutoConfig()

DB_USER = dconfig("DB_USER", default=False)
DB_PASS = dconfig("DB_PASS", default=False)
DB_IP = dconfig("DB_IP", default=False)
DB_PORT = dconfig("DB_PORT", default=False)
DB_DATABASE_NAME = dconfig("DB_DATABASE_NAME", default=False)
NEW_TABLE_NAME = dconfig("NEW_TABLE_NAME", default=False)

# postgresql+psycopg2
CONN_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_DATABASE_NAME}"
)

API_KEY = dconfig("API_KEY", default=False)
SYMBOLS = ["BTC", "ETH", "ADA"]

# MARKET = dconfig("MARKET", default=False)

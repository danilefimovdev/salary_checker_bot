from decouple import config

TOKEN = config("BOT_TOKEN")
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_COLLECTION = config("DB_COLLECTION")

mongodb_uri = f"mongodb://{DB_HOST}:{DB_PORT}"

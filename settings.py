from os import environ, path
from dotenv import load_dotenv

dotenv_path = path.join(path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

TOKEN = environ.get('TOKEN')

if not TOKEN:
    raise Exception("Specify the token in .env!")
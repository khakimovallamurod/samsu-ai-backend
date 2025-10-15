from dotenv import load_dotenv
import os

load_dotenv()
def get_url():
    url = os.getenv('URL')
    if url is None:
        raise "URL not found"
    return url

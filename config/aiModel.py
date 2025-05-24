import os
from openai import OpenAI
from constants.index import constants

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get DB URL from .env
MODEL_API_KEY = os.getenv("MODEL_API_KEY")

# Configure your API key
client = OpenAI(
    api_key=MODEL_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

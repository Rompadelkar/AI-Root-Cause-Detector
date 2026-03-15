from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("AIzaSyB7QZu2bk7ka-nRrWdQv8QgjJ244uM4Rg0"))

models = client.models.list()

for model in models:
    print(model.name)
import openai
from game import Game
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)
client.files.create(
    file=open("FineTuneData50.jsonl", "rb"),
    purpose="fine-tune",
)
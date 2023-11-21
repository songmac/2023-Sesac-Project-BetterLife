import openai
import os
from dotenv import load_dotenv


openai_embeddgin_model = "text-embedding-ada-002"

def get_embedding(text: str, model: str) -> List[float]:
    result = openai.Embedding.create(
        model = model,
        input = text
    )
    return result["data"][0]["embedding"]


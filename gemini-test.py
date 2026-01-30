import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?",
    config=types.EmbedContentConfig(output_dimensionality=3072)
)

[embedding_obj] = result.embeddings
embedding_length = len(embedding_obj.values)

print(result)
print(f"Length of embedding: {embedding_length}")

import os

from google import genai
from groq import Groq
from llama_index.core.async_utils import chunks
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import  load_dotenv

load_dotenv()

client = Groq(api_key=os.environ['GROQ_API_KEY'])
# client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])


EMBED_MODEL = "text-embedding-3-large"
EMBED_DIM = 3072

splitter = SentenceSplitter(chunk_size=1000,chunk_overlap=200)


def load_and_chunk_pdf(path:str):
    docs = PDFReader().load_data(path)
    texts = [d.text for d in docs if getattr(d,"text",None)]
    chunks = []

    for t in texts:
        chunks.extend(splitter.split_texts(texts))
    return  chunks

def embed_texts(texts:list[str])->list[list[float]]:
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts
    )
    return  [item.embedding for item in response.data]




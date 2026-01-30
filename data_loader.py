import os

from google import genai
from google.genai import types

from groq import Groq
from llama_index.core.async_utils import chunks
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import  load_dotenv
import  constants as const

load_dotenv()

# client = Groq(api_key=os.environ['GROQ_API_KEY'])
gemini_client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

splitter = SentenceSplitter(chunk_size=const.CHUNK_SIZE,chunk_overlap=const.OVERLAP)


def load_and_chunk_pdf(path:str):
    docs = PDFReader().load_data(path)
    texts = [d.text for d in docs if getattr(d,"text",None)]
    chunks = []

    for t in texts:
        chunks.extend(splitter.split_texts(texts))
    return  chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    # Use 'contents' (plural) for the newer SDK
    result = gemini_client.models.embed_content(
        model=const.EMBED_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(output_dimensionality=const.EMBEDDING_DIM)


    )
    # Access the 'embeddings' list from the result
    return [item.values for item in result.embeddings]




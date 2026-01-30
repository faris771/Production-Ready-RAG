import os
from groq import Groq
import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import datetime

from openai import embeddings
from workflows import step
from custom_types import *

from data_loader import load_and_chunk_pdf
from data_loader import embed_texts
from vector_db import QdrantStorage

# Load environment variables from .env file (if you created one)
load_dotenv()

inngest_client = inngest.Inngest(
    app_id='rag_app',
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer()
)


@inngest_client.create_function(

    fn_id='RAG: Ingest PDF',
    trigger=inngest.TriggerEvent(event='rag/innggest_pdf')
)
async def rag_inngest_pdf(ctx: inngest.Context):
    def _load(ctx: inngest.Context) -> RAGChunkAndSrc:
        pdf_path = ctx.event.data["pdf_path"]
        source_id = ctx.event.data.get("source", pdf_path)
        chunks = load_and_chunk_pdf(pdf_path)

        return RAGChunkAndSrc(chunks=chunks, source_id=source_id)

    def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertResult:
        chunks = chunks_and_src.chunks
        source_id = chunks_and_src.source_id

        vectors = embed_texts(chunks)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_URL,f"{source_id}:{i}")) for i in range(len(chunks))]
        payloads = [{"source":source_id,"text":chunks[i]} for i in range(len(chunks))]
        QdrantStorage().upsert(ids,vectors,payloads)
        return RAGUpsertResult(ingested=len(chunks))




    chunks_and_src = await ctx.step.run("load-and-chunk", lambda: _load(ctx), output_type=RAGChunkAndSrc)
    ingested = await ctx.step.run("embed-and-upsert", lambda: _upsert(chunks_and_src), output_type=RAGUpsertResult)
    return ingested.model_dump()


# if __name__ == '__main__':

app = FastAPI()
inngest.fast_api.serve(app, inngest_client, [rag_inngest_pdf])  # inngest server

# # The client automatically picks up the GROQ_API_KEY environment variable
# # If not using a .env file, ensure the key is set in your OS environment
# # You can also pass it directly as a keyword argument (less secure):
# # client = Groq(api_key="your-groq-api-key")
#
# client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
#
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "what is the capital of Dubai",
#         },
#
#     ],
#     stream=True,
#     model="openai/gpt-oss-20b", # Specify the desired model
# )
#
# # print(chat_completion.choices[0].message.content)
# for chunk in chat_completion:
#     print(chunk.choices[0].delta.content or "", end="")

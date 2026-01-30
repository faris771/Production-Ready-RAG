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

from workflows import step

# Load environment variables from .env file (if you created one)
load_dotenv()

inngest_client = inngest.Inngest(
    app_id='rag_app',
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer
)


@inngest_client.create_function(

    fn_id='RAG: Ingest PDF',
    trigger=inngest.TriggerEvent(event='rag/innggest_pdf')
)
async def rag_inngest_pdf(context: inngest.Context):
    return {'hello': 'world'}


app = FastAPI()

inngest.fast_api.serve(app, inngest_client, [rag_inngest_pdf])  # inngest server

#
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

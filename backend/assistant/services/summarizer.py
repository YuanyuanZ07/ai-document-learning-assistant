from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI

from django.conf import settings


def summarize_text(text):
    """Summarize a block of text using LlamaIndex + OpenAI."""
    if not text.strip():
        return ""

    llm = OpenAI(
        model="gpt-3.5-turbo",
        api_key=settings.OPENAI_API_KEY,
    )
    Settings.llm = llm

    doc = Document(text=text)
    index = VectorStoreIndex.from_documents([doc])
    query_engine = index.as_query_engine()

    response = query_engine.query(
        "Please provide a comprehensive summary of this document. "
        "Cover the main topics, key points, and important details."
    )
    return str(response)

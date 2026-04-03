from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI

from django.conf import settings


def answer_question(question, context):
    """Answer a question based on the provided document text using LlamaIndex."""
    if not context.strip():
        return "No document content available to answer the question."

    llm = OpenAI(
        model="gpt-3.5-turbo",
        api_key=settings.OPENAI_API_KEY,
    )
    Settings.llm = llm

    doc = Document(text=context)
    index = VectorStoreIndex.from_documents([doc])
    query_engine = index.as_query_engine()

    response = query_engine.query(question)
    return str(response)

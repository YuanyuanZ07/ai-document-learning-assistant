from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from django.conf import settings
from .hf_llm import HFInferenceLLM


def summarize_text(text):
    """Summarize a block of text using LlamaIndex RAG with Hugging Face models."""
    if not text.strip():
        return ""

    api_token = settings.HUGGINGFACE_API_TOKEN
    if not api_token:
        raise ValueError("HUGGINGFACE_API_TOKEN is not set. Please set it as an environment variable.")

    llm = HFInferenceLLM(token=api_token)
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
    )
    Settings.llm = llm
    Settings.embed_model = embed_model

    doc = Document(text=text)
    index = VectorStoreIndex.from_documents([doc])
    query_engine = index.as_query_engine()

    response = query_engine.query(
        "Please provide a comprehensive summary of this document. "
        "Cover the main topics, key points, and important details."
    )
    return str(response)

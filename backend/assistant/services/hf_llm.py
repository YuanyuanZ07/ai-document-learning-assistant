from huggingface_hub import InferenceClient
from llama_index.core.llms import CustomLLM, CompletionResponse, LLMMetadata
from pydantic import PrivateAttr


class HFInferenceLLM(CustomLLM):
    """Custom LLM using HuggingFace Inference Client."""
    model_name: str = "Qwen/Qwen2.5-72B-Instruct"
    _client: InferenceClient = PrivateAttr()

    def __init__(self, model_name: str = "Qwen/Qwen2.5-72B-Instruct", token: str = ""):
        super().__init__(model_name=model_name)
        self._client = InferenceClient(token=token)

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(model_name=self.model_name)

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        response = self._client.chat_completion(
            model=self.model_name,
            messages=[{"role": "user", "content": str(prompt)}],
            max_tokens=512,
        )
        text = response.choices[0].message.content
        return CompletionResponse(text=text)

    def stream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Streaming not supported")

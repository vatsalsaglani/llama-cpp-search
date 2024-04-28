from llama_cpp import Llama
from ctx import ContextManagement
from typing import List, Dict, Union


class LLM:

    def __init__(self, model_path: str, **kwargs):
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=kwargs.get("n_gpu_layers",
                                    -1),  # Uncomment to use GPU acceleration
            seed=kwargs.get("seed", 1337),  # Uncomment to set a specific seed
            n_ctx=kwargs.get("n_ctx",
                             4096),  # Uncomment to increase the context window
            n_threads=kwargs.get("n_threads", 8))
        self.ctx = ContextManagement(2560)

    def __stream__(self, messages: List[Dict], **kwargs):
        input_message = self.ctx(messages)
        output = self.llm(input_message, stream=True, echo=False, **kwargs)
        for op in output:
            yield op.get("choices")[0].get("text") or ""

    def __complete__(self, messages: List[Dict], **kwargs):
        input_message = self.ctx(messages)
        output = self.llm(input_message, echo=False, **kwargs)
        return output.get("choices")[0].get("text")

import os
from dotenv import load_dotenv

load_dotenv()

BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY")

MODELS = {
    "Meta-Llama-3-8B-Instruct-IQ3_M.gguf": "meta-llama/Meta-Llama-3-8B",
    "Phi-3-mini-4k-instruct-q4.gguf": "microsoft/Phi-3-mini-4k-instruct"
}

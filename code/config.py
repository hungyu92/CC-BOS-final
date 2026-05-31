# API configuration - fill in according to your needs
API_SECRET_KEY = ""   # OpenAI API key
BASE_URL = ""  # Base URL for the API

# Local model configuration
LOCAL_MODEL_PATH = ""  # Local path for the HuggingFace model
DEVICE = "cuda"  # Device to run the model on

# Ollama configuration
BASE_URL_ollama = "http://localhost:11434/v1"  # OpenAI-compatible Ollama API
OLLAMA_MODEL = "qwen3:14b"  # Default local/free model; use qwen3:8b if memory is tight

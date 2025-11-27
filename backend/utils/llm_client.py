import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
from backend.config import settings

# Ensure environment variables from backend/.env are available
project_root = Path(__file__).parent.parent.parent
dotenv_path = project_root / "backend" / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Prefer configuration from settings, with environment fallbacks
AZURE_OPENAI_API_KEY = settings.AZURE_OPENAI_API_KEY or os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = settings.AZURE_OPENAI_ENDPOINT or os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = settings.AZURE_OPENAI_API_VERSION or os.getenv(
    "AZURE_OPENAI_API_VERSION", "2024-08-01-preview"
)
# Support both variable names for deployment
AZURE_OPENAI_DEPLOYMENT = (
    settings.AZURE_OPENAI_DEPLOYMENT_NAME
    or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
)

# Lazily create client; avoid import-time crashes when envs are missing
_client: AzureOpenAI | None = None

def _get_client() -> AzureOpenAI:
    global _client
    if _client is not None:
        return _client
    if not (AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT):
        raise RuntimeError(
            "Azure OpenAI configuration missing. Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in your .env or environment."
        )
    _client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
    )
    return _client

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Call Azure OpenAI Chat Completions and return the response text.
    Used by TriageAgent and PlannerAgent.
    """
    if not AZURE_OPENAI_DEPLOYMENT:
        raise RuntimeError(
            "Azure OpenAI deployment name not set. Set AZURE_OPENAI_DEPLOYMENT_NAME (preferred) or AZURE_OPENAI_DEPLOYMENT in your .env or environment."
        )
    client = _get_client()
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,  # this is the deployment name
        temperature=0.0,                # deterministic for planning / classification
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content
    if content is None:
        raise ValueError("LLM returned empty content")
    return content

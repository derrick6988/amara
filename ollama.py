#!/usr/bin/env python3
import os
import logging
import requests

try:
    import openai
except Exception:
    openai = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _openai_chat(model, messages, temperature=0.7, max_tokens=800):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required for OpenAI provider")
    if openai is None:
        raise RuntimeError("openai package not installed")

    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    text = resp["choices"][0]["message"]["content"]
    return text


def _ollama_chat(model, messages):
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    url = f"{ollama_url}/chat?model={model}"
    payload = {"messages": messages}
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    # Ollama responses vary by version. Try common fields.
    if isinstance(data, dict):
        if "response" in data:
            return data["response"]
        if "message" in data and isinstance(data["message"], dict):
            return data["message"].get("content")
    return str(data)


def chat(model: str, messages: list, stream: bool = False, temperature: float = 0.7, max_tokens: int = 800):
    """A small compatibility wrapper named `chat` so main_enhanced.py (which calls
    `ollama.chat(...)`) works while defaulting to OpenAI when configured.

    Returns: dict with structure {'message': {'content': '<text>'}}
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    try:
        if provider == "openai":
            text = _openai_chat(model, messages, temperature=temperature, max_tokens=max_tokens)
        else:
            text = _ollama_chat(model, messages)

        if text is None:
            text = ""
        return {"message": {"content": text}}

    except Exception as e:
        logger.error("LLM chat error (%s): %s", provider, e)
        # Keep the error surface minimal for callers
        return {"message": {"content": f"[LLM error] {e}"}}
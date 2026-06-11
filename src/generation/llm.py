"""LLM abstraction — supports Ollama (local) and HuggingFace Inference API."""

import requests
import json
from src.config import LLM_BACKEND, LLM_MODEL, OLLAMA_URL, HF_MODEL, HF_API_TOKEN


def call_llm(prompt: str, max_tokens: int = 2048, temperature: float = 0.3) -> str:
    if LLM_BACKEND == "ollama":
        return _call_ollama(prompt, max_tokens, temperature)
    elif LLM_BACKEND == "hf":
        return _call_hf(prompt, max_tokens, temperature)
    else:
        raise ValueError(f"Unknown LLM_BACKEND: {LLM_BACKEND}")


def _call_ollama(prompt: str, max_tokens: int, temperature: float) -> str:
    resp = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def _call_hf(prompt: str, max_tokens: int, temperature: float) -> str:
    headers = {"Content-Type": "application/json"}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"

    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": max(temperature, 0.01),
                "return_full_text": False,
            },
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list) and data:
        return data[0].get("generated_text", "").strip()
    return str(data).strip()

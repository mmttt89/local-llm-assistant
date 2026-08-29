import requests
import time

from app.config import (
    LM_STUDIO_URL,
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)
from app.models.llm_response import LLMResponse


class LLMClient:
    def chat(self, messages: list[dict]) -> LLMResponse:
        payload_messages = [message.to_dict() for message in messages]
        start = time.perf_counter()
        
        response = requests.post(
            LM_STUDIO_URL,
            json={
                "model": MODEL,
                "messages": payload_messages,
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
            },
        )
        
        elapsed = time.perf_counter() - start
        response.raise_for_status()
        data = response.json()
        return LLMResponse(
                content=data["choices"][0]["message"]["content"],
                prompt_tokens=data["usage"]["prompt_tokens"],
                completion_tokens=data["usage"]["completion_tokens"],
                total_tokens=data["usage"]["total_tokens"],
                response_time=elapsed,
                )
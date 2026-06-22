from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request

from asep.config import load_settings

logger = logging.getLogger("asep.llm")


class LLMClient:
    def __init__(
        self,
        provider: str | None = None,
        model: str | None = None,
        api_base: str | None = None,
    ) -> None:
        settings = load_settings()
        self.provider = provider or settings.llm.provider
        self.model = model or settings.llm.model
        self.api_base = api_base or settings.llm.api_base

    def generate(self, prompt: str, system_instruction: str | None = None) -> str:
        """Generate text completions using the configured model and provider."""
        prov = self.provider.lower()

        if prov == "openai":
            return self._call_openai(prompt, system_instruction)
        elif prov == "anthropic":
            return self._call_anthropic(prompt, system_instruction)
        elif prov == "gemini":
            return self._call_gemini(prompt, system_instruction)
        elif prov in ("ollama", "openai_compatible"):
            return self._call_ollama_or_compatible(prompt, system_instruction)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def _call_openai(self, prompt: str, system_instruction: str | None) -> str:
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        client = OpenAI(api_key=api_key)
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _call_ollama_or_compatible(self, prompt: str, system_instruction: str | None) -> str:
        from openai import OpenAI

        base_url = self.api_base or "http://localhost:11434/v1"
        api_key = os.environ.get("OPENAI_API_KEY") or "ollama"

        client = OpenAI(api_key=api_key, base_url=base_url)
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.1
        )
        return response.choices[0].message.content.strip()

    def _call_anthropic(self, prompt: str, system_instruction: str | None) -> str:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_instruction:
            payload["system"] = system_instruction

        return self._make_http_post(
            url, headers, payload, lambda res: res["content"][0]["text"]
        )

    def _call_gemini(self, prompt: str, system_instruction: str | None) -> str:
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "Neither GEMINI_API_KEY nor OPENAI_API_KEY environment variable is set."
            )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
        headers = {"content-type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        return self._make_http_post(
            url,
            headers,
            payload,
            lambda res: res["candidates"][0]["content"]["parts"][0]["text"],
        )

    def _make_http_post(
        self, url: str, headers: dict[str, str], payload: dict, extractor_func
    ) -> str:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        for k, v in headers.items():
            req.add_header(k, v)

        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                return extractor_func(res_json).strip()
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            logger.error(
                f"HTTP error calling LLM API {url}: status={e.code}, body={err_body}"
            )
            raise RuntimeError(f"LLM API call failed: status={e.code}, body={err_body}") from e
        except Exception as e:
            logger.error(f"Error calling LLM API {url}: {e}")
            raise

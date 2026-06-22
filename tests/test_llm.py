from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from asep.llm import LLMClient


def test_llm_client_initialization():
    client = LLMClient(provider="openai", model="gpt-4o-mini")
    assert client.provider == "openai"
    assert client.model == "gpt-4o-mini"
    assert client.api_base is None


@patch("openai.OpenAI")
def test_llm_client_openai_routing(mock_openai_class):
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[
        0
    ].message.content = "openai response"

    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        client = LLMClient(provider="openai", model="gpt-4")
        res = client.generate("hello", "system instruct")

        assert res == "openai response"
        mock_openai_class.assert_called_once_with(api_key="test-key")
        mock_client.chat.completions.create.assert_called_once()
        args, kwargs = mock_client.chat.completions.create.call_args
        assert kwargs["model"] == "gpt-4"
        assert kwargs["messages"] == [
            {"role": "system", "content": "system instruct"},
            {"role": "user", "content": "hello"},
        ]


@patch("openai.OpenAI")
def test_llm_client_ollama_routing(mock_openai_class):
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    mock_client.chat.completions.create.return_value.choices[
        0
    ].message.content = "ollama response"

    client = LLMClient(
        provider="ollama", model="qwen2.5-coder:7b", api_base="http://localhost:11434/v1"
    )
    res = client.generate("hello local", "system local")

    assert res == "ollama response"
    mock_openai_class.assert_called_once_with(
        api_key="ollama", base_url="http://localhost:11434/v1"
    )
    mock_client.chat.completions.create.assert_called_once()


@patch("urllib.request.urlopen")
def test_llm_client_anthropic_routing(mock_urlopen):
    mock_response = MagicMock()
    mock_urlopen.return_value.__enter__.return_value = mock_response
    mock_response.read.return_value = json.dumps(
        {"content": [{"type": "text", "text": "claude response"}]}
    ).encode("utf-8")

    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "claude-key"}):
        client = LLMClient(provider="anthropic", model="claude-3-5-sonnet")
        res = client.generate("hello claude", "system claude")

        assert res == "claude response"
        mock_urlopen.assert_called_once()
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert req.full_url == "https://api.anthropic.com/v1/messages"
        assert req.get_header("X-api-key") == "claude-key"
        assert req.get_header("Anthropic-version") == "2023-06-01"


@patch("urllib.request.urlopen")
def test_llm_client_gemini_routing(mock_urlopen):
    mock_response = MagicMock()
    mock_urlopen.return_value.__enter__.return_value = mock_response
    mock_response.read.return_value = json.dumps(
        {"candidates": [{"content": {"parts": [{"text": "gemini response"}]}}]}
    ).encode("utf-8")

    with patch.dict("os.environ", {"GEMINI_API_KEY": "gemini-key"}):
        client = LLMClient(provider="gemini", model="gemini-2.5-flash")
        res = client.generate("hello gemini", "system gemini")

        assert res == "gemini response"
        mock_urlopen.assert_called_once()
        req = mock_urlopen.call_args[0][0]
        assert req.get_method() == "POST"
        assert "generativelanguage.googleapis.com" in req.full_url
        assert "key=gemini-key" in req.full_url

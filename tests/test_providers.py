import os
import sys
from pathlib import Path
from types import SimpleNamespace

import anthropic
import pytest

try:
    import httpx
except ImportError:  # newer SDKs ship httpx2
    import httpx2 as httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from newsletter import providers  # noqa: E402

ALL_VARS = ["LLM_PROVIDER", "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY",
            "OPENROUTER_API_KEY", "LLM_BASE_URL", "LLM_API_KEY", "LLM_MODEL", "LLM_TIMEOUT", "CLAUDE_BIN"]
CONFIG = {"llm": {"default_models": {"anthropic": "claude-opus-5-5", "openai": "gpt-5", "gemini": "gemini-2.5-flash",
                                     "openrouter": "openai/gpt-5", "claude_cli": "sonnet"}}}


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for v in ALL_VARS:
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setattr(providers, "find_claude", lambda: None)
    providers.configure(CONFIG)
    yield
    providers.reset()


def provider_name():
    providers.reset()
    b = providers.detect_backend()
    return b["provider"] if b else None


# ---------- detection ----------

@pytest.mark.parametrize("var,expected", [
    ("ANTHROPIC_API_KEY", "anthropic"), ("OPENAI_API_KEY", "openai"), ("GEMINI_API_KEY", "gemini"),
    ("GOOGLE_API_KEY", "gemini"), ("OPENROUTER_API_KEY", "openrouter")])
def test_each_key_alone(monkeypatch, var, expected):
    monkeypatch.setenv(var, "k")
    assert provider_name() == expected


def test_base_url_is_openai_compatible(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("LLM_MODEL", "qwen3:8b")
    assert provider_name() == "openai_compatible"
    assert providers.worker_count(4) == 1


def test_openai_compatible_needs_model(monkeypatch):
    monkeypatch.setenv("LLM_BASE_URL", "http://x/v1")
    with pytest.raises(SystemExit):
        providers.detect_backend()


def test_anthropic_wins_over_others(monkeypatch):
    for v in ["OPENAI_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"]:
        monkeypatch.setenv(v, "k")
    monkeypatch.setattr(providers, "find_claude", lambda: "claude.exe")
    assert provider_name() == "anthropic"


def test_provider_override(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    assert provider_name() == "openai"


def test_provider_override_missing_key_exits(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    with pytest.raises(SystemExit):
        providers.detect_backend()


def test_cli_used_only_without_keys(monkeypatch):
    monkeypatch.setattr(providers, "find_claude", lambda: "claude.exe")
    assert provider_name() == "claude_cli"
    assert providers.detect_backend()["model"] == "sonnet"


def test_nothing_configured():
    assert provider_name() is None
    assert providers.complete_json("p", {"type": "object"}, 5, "medium") is None


def test_model_env_override(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    monkeypatch.setenv("LLM_MODEL", "gpt-x")
    providers.reset()
    assert providers.detect_backend()["model"] == "gpt-x"


# ---------- .env loader ----------

def test_env_loader(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text("# comment\nA_KEY=\"quoted value\"\nB_KEY='single'\nEXISTING=new\nC_KEY=plain # tail\nEMPTY=\n",
                   encoding="utf-8")
    monkeypatch.setenv("EXISTING", "old")
    for k in ["A_KEY", "B_KEY", "C_KEY", "EMPTY"]:
        monkeypatch.delenv(k, raising=False)
    providers.load_env(env)
    try:
        assert os.environ["A_KEY"] == "quoted value" and os.environ["B_KEY"] == "single"
        assert os.environ["EXISTING"] == "old" and os.environ["C_KEY"] == "plain"
        assert "EMPTY" not in os.environ
    finally:
        for k in ["A_KEY", "B_KEY", "C_KEY"]:
            os.environ.pop(k, None)


# ---------- schema ----------

SCHEMA = {"type": "object", "required": ["items"], "properties": {"items": {"type": "array", "items": {
    "type": "object", "required": ["id", "scores", "text"], "properties": {
        "id": {"type": "integer"},
        "scores": {"type": "object", "required": ["a", "b"], "properties": {
            "a": {"type": "integer", "minimum": 0, "maximum": 5}, "b": {"type": "integer", "minimum": 0, "maximum": 5}}},
        "text": {"type": "string", "maxLength": 5}}}}}}


def test_sanitize_schema():
    clean = providers.sanitize_schema(SCHEMA)
    text = str(clean)
    for word in ["maxLength", "minimum", "maximum", "minLength", "multipleOf"]:
        assert word not in text
    item = clean["properties"]["items"]["items"]
    assert item["additionalProperties"] is False and clean["additionalProperties"] is False
    assert item["properties"]["scores"]["properties"]["a"]["enum"] == [0, 1, 2, 3, 4, 5]
    assert "maxLength" in str(SCHEMA)  # original untouched


def test_clean_output_clamps_and_truncates():
    data = {"items": [{"id": 1, "scores": {"a": 9, "b": None}, "text": "abcdefghij"}, {"scores": {}, "text": "x"}]}
    out = providers.clean_output(data, SCHEMA)
    assert out["items"] == [{"id": 1, "scores": {"a": 5, "b": 0}, "text": "abcde"}]
    assert providers.clean_output({"nope": 1}, SCHEMA) is None


# ---------- JSON parsing ----------

def test_parse_json_text():
    assert providers.parse_json_text('```json\n{"a": 1}\n```') == {"a": 1}
    assert providers.parse_json_text('<think>hmm {"x":0}</think>\n{"a": 2}') == {"a": 2}
    assert providers.parse_json_text('Here you go: {"a": {"b": 3}} hope that helps') == {"a": {"b": 3}}
    assert providers.parse_json_text("no json") is None


# ---------- Anthropic backend with a mocked client ----------

class FakeStream:
    def __init__(self, msg=None, error=None):
        self.msg, self.error = msg, error

    def __enter__(self):
        if self.error:
            raise self.error
        return self

    def __exit__(self, *a):
        return False

    def get_final_message(self):
        return self.msg


def message(text='{"items": []}', stop="end_turn"):
    return SimpleNamespace(stop_reason=stop, stop_details=SimpleNamespace(category="cyber"),
                           content=[SimpleNamespace(type="text", text=text)])


def fake_client(beta_stream, plain_stream, calls):
    def beta(**kw):
        calls.append(("beta", kw))
        return beta_stream

    def plain(**kw):
        calls.append(("plain", kw))
        return plain_stream
    return SimpleNamespace(beta=SimpleNamespace(messages=SimpleNamespace(stream=beta)),
                           messages=SimpleNamespace(stream=plain))


def use_anthropic(monkeypatch, client):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    created = {}

    def factory(**kw):
        created.update(kw)
        return client
    monkeypatch.setattr(anthropic, "Anthropic", factory)
    providers.reset()
    return created


def test_anthropic_request(monkeypatch):
    calls = []
    created = use_anthropic(monkeypatch, fake_client(FakeStream(message('{"items": []}')), None, calls))
    out = providers.complete_json("hello", SCHEMA, 99, "high")
    assert out == {"items": []}
    kind, kw = calls[0]
    assert kind == "beta" and kw["model"] == "claude-opus-5-5" and kw["fallbacks"] == "default"
    assert kw["betas"] == ["server-side-fallback-2026-07-01"]
    assert kw["output_config"]["effort"] == "high"
    assert kw["output_config"]["format"]["type"] == "json_schema"
    assert "maxLength" not in str(kw["output_config"])
    assert "temperature" not in kw and "thinking" not in kw and "tool_choice" not in kw
    assert created["timeout"] == 99 and created["max_retries"] == 3


def test_anthropic_refusal_returns_none(monkeypatch):
    calls = []
    use_anthropic(monkeypatch, fake_client(FakeStream(message(stop="refusal")), None, calls))
    assert providers.complete_json("p", SCHEMA, 5, "medium") is None
    assert len(calls) == 1  # a refusal is not retried


def test_anthropic_fallback_without_betas_on_400(monkeypatch):
    calls = []
    resp = httpx.Response(400, request=httpx.Request("POST", "http://x"))
    err = anthropic.BadRequestError("unknown parameter: fallbacks", response=resp, body=None)
    use_anthropic(monkeypatch, fake_client(FakeStream(error=err), FakeStream(message('{"items": []}')), calls))
    assert providers.complete_json("p", SCHEMA, 5, "medium") == {"items": []}
    assert [c[0] for c in calls] == ["beta", "plain"]
    assert "betas" not in calls[1][1] and "fallbacks" not in calls[1][1]
    assert calls[1][1]["output_config"]["effort"] == "medium"

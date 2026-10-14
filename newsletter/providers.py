"""LLM backends behind one function: complete_json(prompt, schema, timeout, effort) -> dict | None.

If an API key is present it is used INSTEAD of the Claude CLI. The CLI is the last resort.
Key values are never printed or logged."""
import glob
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlparse

log = logging.getLogger("providers")
ROOT = Path(__file__).resolve().parent.parent

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
OPENROUTER_URL = "https://openrouter.ai/api/v1"
ANTHROPIC_BETA = "server-side-fallback-2026-07-01"
PROVIDERS = ["anthropic", "openai", "gemini", "openrouter", "openai_compatible", "claude_cli"]
KEY_VARS = {"anthropic": ["ANTHROPIC_API_KEY"], "openai": ["OPENAI_API_KEY"],
            "gemini": ["GEMINI_API_KEY", "GOOGLE_API_KEY"], "openrouter": ["OPENROUTER_API_KEY"]}
NO_LLM_MESSAGE = "No LLM configured: set an API key in .env (see deliverables/README.md); producing keyword-only newsletter"

_default_models = {}
_backend_cache = []   # [backend or None] once detection has run
_state = {}           # remembered per-run quirks, e.g. which response_format a server accepts


# ---------- .env loader ----------

def load_env(path=None):
    """Read KEY=VALUE lines from <project>/.env. Only sets variables not already in os.environ."""
    path = Path(path) if path else ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        elif value.startswith("#"):
            value = ""
        elif " #" in value:
            value = value.split(" #", 1)[0].strip()
        if key and value and key not in os.environ:
            os.environ[key] = value


# ---------- backend detection ----------

def configure(config):
    """Take the per-provider default models from config.yaml (llm.default_models) and reset the cache."""
    _default_models.clear()
    _default_models.update(config.get("llm", {}).get("default_models") or {})
    reset()


def reset():
    _backend_cache.clear()
    _state.clear()


def find_claude():
    """CLAUDE_BIN env var -> claude on PATH -> newest VS Code extension binary."""
    env = os.environ.get("CLAUDE_BIN")
    if env and Path(env).exists():
        return env
    found = shutil.which("claude")
    if found:
        return found
    pattern = str(Path.home() / ".vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude.exe")
    matches = sorted(glob.glob(pattern), key=os.path.getmtime)
    return matches[-1] if matches else None


def first_env(names):
    for name in names:
        if os.environ.get(name):
            return os.environ[name]
    return None


def make_backend(provider):
    """Build the backend description for a provider; exits with a clear message if its settings are missing."""
    backend = {"provider": provider, "api_key": None, "base_url": None}
    if provider in KEY_VARS:
        backend["api_key"] = first_env(KEY_VARS[provider])
        if not backend["api_key"]:
            raise SystemExit(f"LLM_PROVIDER={provider} but {' or '.join(KEY_VARS[provider])} is not set (see .env.example)")
        backend["base_url"] = {"gemini": GEMINI_URL, "openrouter": OPENROUTER_URL}.get(provider)
    elif provider == "openai_compatible":
        backend["base_url"] = os.environ.get("LLM_BASE_URL")
        if not backend["base_url"]:
            raise SystemExit("LLM_PROVIDER=openai_compatible but LLM_BASE_URL is not set (see .env.example)")
        backend["api_key"] = os.environ.get("LLM_API_KEY") or "none"
    elif provider == "claude_cli":
        backend["binary"] = find_claude()
        if not backend["binary"]:
            raise SystemExit("LLM_PROVIDER=claude_cli but the claude binary was not found (set CLAUDE_BIN)")
    else:
        raise SystemExit(f"Unknown LLM_PROVIDER={provider!r}; use one of: {', '.join(PROVIDERS)}")
    model = os.environ.get("LLM_MODEL") or _default_models.get(provider)
    if not model:
        raise SystemExit(f"{provider} needs a model: set LLM_MODEL in .env (see .env.example)")
    backend["model"] = model
    return backend


def pick_provider():
    """First match wins. Returns a provider name or None."""
    forced = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if forced:
        return forced
    for provider in ["anthropic", "openai", "gemini", "openrouter"]:
        if first_env(KEY_VARS[provider]):
            return provider
    if os.environ.get("LLM_BASE_URL"):
        return "openai_compatible"
    if find_claude():
        return "claude_cli"
    return None


def detect_backend():
    """Cached. Returns a backend dict (provider, model, ...) or None when nothing is configured."""
    if not _backend_cache:
        provider = pick_provider()
        _backend_cache.append(make_backend(provider) if provider else None)
    return _backend_cache[0]


def describe(backend):
    return f"LLM backend: {backend['provider']} ({backend['model']})"


def worker_count(default):
    """Local servers (Ollama, LM Studio) cannot run calls in parallel well."""
    backend = detect_backend()
    if backend and backend["provider"] == "openai_compatible":
        if urlparse(backend["base_url"]).hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            return 1
    return default


# ---------- schema and output helpers ----------

UNSUPPORTED = {"minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf", "minLength", "maxLength",
               "minItems", "maxItems", "uniqueItems", "pattern", "format", "minProperties", "maxProperties"}


def sanitize_schema(schema):
    """Copy of the schema that structured-output APIs accept: no range/length keywords,
    0-5 integers become an enum, every object is closed (additionalProperties false) with all keys required."""
    if isinstance(schema, list):
        return [sanitize_schema(s) for s in schema]
    if not isinstance(schema, dict):
        return schema
    out = {k: sanitize_schema(v) for k, v in schema.items() if k not in UNSUPPORTED}
    if schema.get("type") == "integer" and schema.get("minimum") == 0 and schema.get("maximum") == 5:
        out["enum"] = [0, 1, 2, 3, 4, 5]
    if "properties" in schema:
        out["type"] = "object"
        out["additionalProperties"] = False
        out["required"] = list(schema["properties"])
    return out


def enforce_limits(data, schema):
    """Apply what sanitize_schema removed: truncate strings to maxLength, clamp numbers to minimum/maximum."""
    if isinstance(data, dict) and isinstance(schema.get("properties"), dict):
        for key, sub in schema["properties"].items():
            if key in data:
                data[key] = enforce_limits(data[key], sub)
    elif isinstance(data, list) and isinstance(schema.get("items"), dict):
        return [enforce_limits(x, schema["items"]) for x in data]
    elif isinstance(data, str) and "maxLength" in schema:
        return data[:schema["maxLength"]].rstrip()
    elif isinstance(data, (int, float)) and not isinstance(data, bool):
        if "maximum" in schema:
            data = min(data, schema["maximum"])
        if "minimum" in schema:
            data = max(data, schema["minimum"])
    return data


def clean_output(data, schema):
    """Minimal validation. Returns the (limit-enforced) dict, or None if it is unusable."""
    if not isinstance(data, dict) or any(k not in data for k in schema.get("required", [])):
        return None
    data = enforce_limits(data, schema)
    for key, sub in schema.get("properties", {}).items():
        item_props = (sub.get("items") or {}).get("properties", {}) if sub.get("type") == "array" else {}
        if "scores" not in item_props:
            continue
        score_ids = item_props["scores"].get("required", [])
        rows = data.get(key)
        if not isinstance(rows, list):
            return None
        good = []
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("id"), int):
                continue  # an item without an id cannot be matched, drop it
            scores = row.get("scores") if isinstance(row.get("scores"), dict) else {}
            row["scores"] = {i: clamp_score(scores.get(i)) for i in score_ids}
            good.append(row)
        data[key] = good
    return data


def clamp_score(value):
    try:
        return max(0, min(5, int(value)))
    except (TypeError, ValueError):
        return 0


def parse_json_text(text):
    """Strip <think> blocks and ``` fences, then json.loads the outermost {...}. None if it fails."""
    if not text:
        return None
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"```(?:json)?", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except ValueError:
        return None


# ---------- backend: Claude CLI (unchanged behaviour) ----------

def call_cli(backend, prompt, schema, timeout):
    """Run one headless call with one retry. Returns the structured output or None."""
    cmd = [backend["binary"], "-p", "--output-format", "json", "--json-schema", json.dumps(schema),
           "--model", backend["model"], "--tools", "", "--no-session-persistence"]
    for attempt in range(2):
        try:
            with tempfile.TemporaryDirectory() as tmp:  # temp cwd: project CLAUDE.md/agents are not loaded
                proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                                      encoding="utf-8", timeout=timeout, cwd=tmp)
            envelope = json.loads(proc.stdout) if proc.stdout.strip() else {}
            if envelope.get("is_error") or proc.returncode != 0 or "structured_output" not in envelope:
                reason = envelope.get("result") or proc.stderr.strip()[:300] or f"exit {proc.returncode}"
                raise RuntimeError(str(reason)[:300])
            return envelope["structured_output"]
        except subprocess.TimeoutExpired:
            log.warning("claude call timed out after %ss (attempt %d)", timeout, attempt + 1)
        except (RuntimeError, ValueError, OSError) as exc:
            log.warning("claude call failed (attempt %d): %s", attempt + 1, exc)
    return None


# ---------- backend: Anthropic API ----------

def anthropic_request(backend, prompt, schema, effort, with_fallback):
    return dict(
        model=backend["model"], max_tokens=32000,
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        messages=[{"role": "user", "content": prompt}],
        **({"betas": [ANTHROPIC_BETA], "fallbacks": "default"} if with_fallback else {}))


def anthropic_message(client, request, with_fallback):
    api = client.beta.messages if with_fallback else client.messages
    with api.stream(**request) as stream:
        return stream.get_final_message()


def anthropic_text(msg):
    """The JSON text of a finished message, or None (reason logged) for refusals and cut-off output."""
    if msg.stop_reason == "refusal":
        details = getattr(msg, "stop_details", None)
        log.warning("anthropic refused the request (%s)", getattr(details, "category", None) or details)
        return None
    if msg.stop_reason == "max_tokens":
        log.warning("anthropic output hit max_tokens")
        return None
    return next((b.text for b in msg.content if b.type == "text"), None)


def call_anthropic(backend, prompt, schema, timeout, effort):
    import anthropic
    client = anthropic.Anthropic(api_key=backend["api_key"], timeout=timeout, max_retries=3)  # SDK retries 429/5xx
    clean_schema = sanitize_schema(schema)
    for attempt in range(2):
        with_fallback = _state.get("anthropic_fallback", True)
        try:
            try:
                msg = anthropic_message(client, anthropic_request(backend, prompt, clean_schema, effort, with_fallback), with_fallback)
            except anthropic.BadRequestError as exc:
                text = str(exc).lower()
                if not with_fallback or not ("fallbacks" in text or "beta" in text):
                    raise
                log.info("model rejected the fallback beta, retrying without it")
                _state["anthropic_fallback"] = False
                msg = anthropic_message(client, anthropic_request(backend, prompt, clean_schema, effort, False), False)
            if msg.stop_reason == "refusal" or msg.stop_reason == "max_tokens":
                anthropic_text(msg)  # logs why
                return None
            data = clean_output(parse_json_text(anthropic_text(msg)), schema)
            if data is not None:
                return data
            log.warning("anthropic returned unusable JSON (attempt %d)", attempt + 1)
        except Exception as exc:  # fail soft: any API error is logged and skipped
            log.warning("anthropic call failed (attempt %d): %s", attempt + 1, str(exc)[:300])
    return None


# ---------- backend: OpenAI-compatible (openai, gemini, openrouter, openai_compatible) ----------

RESPONSE_MODES = ["json_schema", "json_object", "none"]


def schema_instruction(schema):
    return "\n\nRespond with ONLY a JSON object matching this JSON schema:\n" + json.dumps(schema)


def openai_create(client, backend, prompt, schema, mode):
    kwargs = {"model": backend["model"], "messages": [{"role": "user", "content": prompt}]}
    if mode == "json_schema":
        kwargs["response_format"] = {"type": "json_schema",
                                     "json_schema": {"name": "output", "strict": True, "schema": schema}}
    else:
        kwargs["messages"] = [{"role": "user", "content": prompt + schema_instruction(schema)}]
        if mode == "json_object":
            kwargs["response_format"] = {"type": "json_object"}
    return client.chat.completions.create(**kwargs).choices[0].message.content


def openai_text(client, backend, prompt, schema):
    """Try the response formats from strict to none; a 400/422 means 'this format is not supported'."""
    start = _state.get("openai_mode", 0)
    for index in range(start, len(RESPONSE_MODES)):
        try:
            text = openai_create(client, backend, prompt, schema, RESPONSE_MODES[index])
            _state["openai_mode"] = index
            return text
        except Exception as exc:
            if getattr(exc, "status_code", None) in (400, 422) and index < len(RESPONSE_MODES) - 1:
                log.info("response_format %s not accepted, trying %s", RESPONSE_MODES[index], RESPONSE_MODES[index + 1])
                continue
            raise
    return None


def call_openai_compatible(backend, prompt, schema, timeout):
    from openai import OpenAI
    client = OpenAI(api_key=backend["api_key"], base_url=backend["base_url"], timeout=timeout, max_retries=3)
    clean_schema = sanitize_schema(schema)
    for attempt in range(2):
        try:
            text = openai_text(client, backend, prompt, clean_schema)
            data = clean_output(parse_json_text(text), schema)
            if data is not None:
                return data
            log.warning("%s returned invalid JSON (attempt %d)", backend["provider"], attempt + 1)
        except Exception as exc:
            log.warning("%s call failed (attempt %d): %s", backend["provider"], attempt + 1, str(exc)[:300])
    return None


# ---------- the one function the rest of the code calls ----------

def complete_json(prompt, schema, timeout, effort):
    """Returns parsed JSON (dict) or None after one retry. Never raises for call failures."""
    backend = detect_backend()
    if backend is None:
        return None
    if os.environ.get("LLM_TIMEOUT"):
        timeout = int(os.environ["LLM_TIMEOUT"])  # slow local models: raise all timeouts
    provider = backend["provider"]
    if provider == "claude_cli":
        return call_cli(backend, prompt, schema, timeout)
    if provider == "anthropic":
        return call_anthropic(backend, prompt, schema, timeout, effort)
    return call_openai_compatible(backend, prompt, schema, timeout)

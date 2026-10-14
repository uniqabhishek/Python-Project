"""
Intent-based command processor — JSON knowledge base.

- Loads intents from data/knowledge.json
- Matches user input with weighted, token-aware scoring
- Returns a structured Response the web layer can render and speak
"""

from __future__ import annotations

import datetime
import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote_plus


# ---------- response shape ----------

@dataclass
class Response:
    text: str
    open_url: str | None = None
    exit: bool = False
    intent_id: str = ""
    confidence: float = 0.0
    meta: dict = field(default_factory=dict)


# ---------- knowledge base ----------

_KB_PATH = Path(__file__).parent / "data" / "knowledge.json"
_intents: list[dict] = []


def _load_kb() -> list[dict]:
    """Load and validate the knowledge base once at import time."""
    if not _KB_PATH.exists():
        print(f"[kb] WARNING: {_KB_PATH} not found. Only time/date/search will work.")
        return []

    try:
        with _KB_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[kb] JSON parse error in {_KB_PATH.name}: {e}")
        print(f"[kb] line {e.lineno}, column {e.colno}: {e.msg}")
        return []

    intents = data.get("intents", [])
    cleaned = []
    for it in intents:
        if not isinstance(it, dict):
            continue
        if "patterns" not in it or "response" not in it:
            print(f"[kb] skipping malformed intent: {it.get('id', '?')}")
            continue
        it.setdefault("kind", "info")
        it.setdefault("priority", 50)
        it.setdefault("id", f"intent_{len(cleaned)}")
        it["patterns"] = [str(p).lower().strip() for p in it["patterns"]]
        cleaned.append(it)

    print(f"[kb] loaded {len(cleaned)} intents from {_KB_PATH.name}")
    return cleaned


def reload_kb() -> int:
    """Reload the knowledge base at runtime. Returns the new intent count."""
    global _intents
    _intents = _load_kb()
    return len(_intents)


_intents = _load_kb()


# ---------- matching ----------

_TOKEN_RE = re.compile(r"[a-z0-9']+")


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def _score(intent: dict, user_tokens: list[str], raw: str) -> float:
    """Score how well an intent matches the user's input. Higher = better."""
    user_set = set(user_tokens)
    best = 0.0

    for pattern in intent["patterns"]:
        p_tokens = _tokens(pattern)
        if not p_tokens:
            continue

        if pattern in raw:
            best = max(best, 1.0)
            continue

        if set(p_tokens).issubset(user_set):
            weight = min(1.0, 0.6 + 0.1 * len(p_tokens))
            best = max(best, weight)
            continue

        overlap = len(set(p_tokens) & user_set) / len(p_tokens)
        if overlap >= 0.66:
            best = max(best, 0.4 + 0.2 * overlap)

    return best


def _pick_response(intent: dict) -> str:
    resp = intent["response"]
    if isinstance(resp, list):
        return random.choice(resp)
    return str(resp)


# ---------- built-in dynamic responses ----------

def _dynamic_time() -> str:
    now = datetime.datetime.now()
    h = now.strftime("%I").lstrip("0") or "12"
    m = now.strftime("%M")
    ap = now.strftime("%p")
    return f"It's currently {h}:{m} {ap}."


def _dynamic_date() -> str:
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today}."


# ---------- special handlers ----------

def _handle_search(cmd: str) -> Response | None:
    m = re.search(
        r"(?:search(?:\s+for)?|google|look\s+up|find)\s+(.+)",
        cmd,
        flags=re.IGNORECASE,
    )
    if not m:
        return None
    query = m.group(1).strip(" ?.!")
    if not query:
        return Response("What would you like me to search for?")
    return Response(
        f"Searching for {query}.",
        open_url=f"https://www.google.com/search?q={quote_plus(query)}",
        intent_id="search_web",
        confidence=0.9,
    )


# ---------- main entry point ----------

def process(cmd: str) -> Response:
    if not cmd or not cmd.strip():
        return Response("I didn't catch that. Could you repeat it?", confidence=0.0)

    raw = cmd.lower().strip()
    raw = re.sub(r"[?!.]+$", "", raw).strip()
    tokens = _tokens(raw)

    search_resp = _handle_search(raw)
    if search_resp:
        return search_resp

    scored: list[tuple[float, dict]] = []
    for intent in _intents:
        s = _score(intent, tokens, raw)
        if s > 0:
            scored.append((s + intent["priority"] / 1000.0, intent))

    if not scored:
        return _fallback(raw)

    scored.sort(key=lambda x: x[0], reverse=True)
    score, best = scored[0]

    resp_text = _pick_response(best)
    if resp_text == "__DYNAMIC_TIME__":
        resp_text = _dynamic_time()
    elif resp_text == "__DYNAMIC_DATE__":
        resp_text = _dynamic_date()

    r = Response(
        text=resp_text,
        intent_id=best["id"],
        confidence=round(min(score, 1.0), 2),
    )

    kind = best.get("kind", "info")

    if kind == "site" and best.get("url"):
        r.open_url = best["url"]

    if best["id"] == "exit":
        r.exit = True

    return r


def _fallback(raw: str) -> Response:
    return Response(
        text=(
            "I'm not sure how to help with that yet. "
            "I can tell you the time or date, open sites like Google and YouTube, "
            "run a web search, or answer questions from my knowledge base. "
            "You can also say 'what can you do' for a full list."
        ),
        intent_id="fallback",
        confidence=0.0,
    )
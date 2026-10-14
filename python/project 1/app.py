from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from commands import process, reload_kb

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    raw = (data.get("command") or "").strip()

    if not raw:
        return jsonify({"text": "I didn't catch that.", "open_url": None, "exit": False})

    if len(raw) > 500:
        return jsonify({"text": "That command is too long.", "open_url": None, "exit": False})

    resp = process(raw)
    return jsonify({
        "text": resp.text,
        "open_url": resp.open_url,
        "exit": resp.exit,
        "intent": resp.intent_id,
        "confidence": resp.confidence,
    })


@app.route("/api/reload", methods=["POST"])
def reload():
    """Hot-reload knowledge.yaml without restarting Flask."""
    count = reload_kb()
    return jsonify({"ok": True, "intents": count})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
# server1.py

from flask import Flask, request
from main1 import handle_signal
import json
import os

app = Flask(__name__)


@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_json(silent=True)

        # fallback if JSON not parsed
        if not data:
            raw = request.data.decode("utf-8").strip()
            print("📥 RAW DATA:", raw)

            try:
                data = json.loads(raw)
            except:
                data = {"signal": raw}

        print("📩 Parsed Data:", data)

        signal = str(data.get("signal", "")).lower()

        # support both numeric + text signals
        if signal in ["1", "buy"]:
            handle_signal("buy")

        elif signal in ["-1", "sell"]:
            handle_signal("sell")

        else:
            print("⚠️ Invalid signal:", signal)

        return "OK", 200

    except Exception as e:
        print("❌ SERVER ERROR:", str(e))
        return "Error", 400


if __name__ == "__main__":
    print("🚀 Server running on port...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# main1.py

import os
from delta_rest_client import DeltaRestClient, OrderType

# ================= CONFIG ==================
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://cdn-ind.testnet.deltaex.org")
PRODUCT_ID = int(os.getenv("PRODUCT_ID", 84))

# =============== CLIENT ===================
delta_client = DeltaRestClient(
    base_url=BASE_URL,
    api_key=API_KEY,
    api_secret=API_SECRET
)

# ============== STATE =====================
current_position = None  # "buy", "sell", or None


# ============== FUNCTIONS =================

def place_buy():
    global current_position
    print("➡️ Placing BUY order")

    try:
        response = delta_client.place_order(
            product_id=PRODUCT_ID,
            size=1,
            side="buy",
            order_type=OrderType.MARKET,
        )
        print("✅ BUY SUCCESS:", response)
        current_position = "buy"
    except Exception as e:
        print("❌ BUY FAILED:", str(e))


def place_sell():
    global current_position
    print("➡️ Placing SELL order")

    try:
        response = delta_client.place_order(
            product_id=PRODUCT_ID,
            size=1,
            side="sell",
            order_type=OrderType.MARKET,
        )
        print("✅ SELL SUCCESS:", response)
        current_position = "sell"
    except Exception as e:
        print("❌ SELL FAILED:", str(e))


def close_position():
    global current_position

    print("🔄 Closing position:", current_position)

    try:
        if current_position == "buy":
            delta_client.place_order(
                product_id=PRODUCT_ID,
                size=1,
                side="sell",
                order_type=OrderType.MARKET,
            )

        elif current_position == "sell":
            delta_client.place_order(
                product_id=PRODUCT_ID,
                size=1,
                side="buy",
                order_type=OrderType.MARKET,
            )

        print("✅ Position closed")
        current_position = None

    except Exception as e:
        print("❌ CLOSE FAILED:", str(e))


def handle_signal(signal: str):
    global current_position

    print(f"📊 Signal received: {signal}")

    if signal == "buy":
        if current_position == "sell":
            close_position()

        if current_position != "buy":
            place_buy()

    elif signal == "sell":
        if current_position == "buy":
            close_position()

        if current_position != "sell":
            place_sell()

    else:
        print("⚠️ Unknown signal:", signal)
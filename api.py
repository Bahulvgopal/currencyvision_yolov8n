from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------- BASIC TEST ROUTE ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "CurrencyVision API running",
        "message": "Backend is working correctly"
    })


# ---------------- START DETECTION ----------------
@app.route("/start", methods=["POST"])
def start_detection():
    return jsonify({
        "status": "started",
        "message": "Detection started"
    })


# ---------------- STOP DETECTION ----------------
@app.route("/stop", methods=["POST"])
def stop_detection():
    return jsonify({
        "status": "stopped",
        "message": "Detection stopped"
    })


# ---------------- RESET TOTAL ----------------
@app.route("/reset", methods=["POST"])
def reset_total():
    return jsonify({
        "status": "reset",
        "message": "Total amount reset to zero"
    })


# ---------------- GET TOTAL ----------------
@app.route("/total", methods=["GET"])
def get_total():
    # temporary static value for testing
    return jsonify({
        "total": 0
    })


if __name__ == "__main__":
    print("🚀 Starting CurrencyVision API...")
    app.run(host="0.0.0.0", port=5000, debug=False)

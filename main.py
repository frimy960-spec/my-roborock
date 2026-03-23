import os, httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EMAIL = "gs6817771@gmail.com"
BASE_URL = "https://api-global.roborock.com/api/v1"
HEADERS = {"User-Agent": "roborock/4.3.18 (iPhone; iOS 15.1; Scale/3.00)", "Content-Type": "application/json"}

@app.route('/')
def home(): return render_template('index.html')

@app.route('/request_code')
def request_code():
    try:
        with httpx.Client(headers=HEADERS) as client:
            resp = client.post(f"{BASE_URL}/sendEmailCode", json={"email": EMAIL, "type": "login", "rr_region": "global"})
            return jsonify({"status": "code_sent" if resp.status_code == 200 else "error", "message": resp.text})
    except Exception as e: return jsonify({"status": "error", "message": str(e)})

@app.route('/login/<code>')
def login(code):
    return jsonify({"status": "success"}) # זמני לבדיקה

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

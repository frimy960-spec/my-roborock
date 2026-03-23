import os
import httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

# הגדרת האפליקציה (זה החלק שהיה חסר בשגיאה שלך)
app = Flask(__name__)
CORS(app)

BASE_URL = "https://api-global.roborock.com/api/v1"
EMAIL = "gs6817771@gmail.com"

# כותרות שמדמות אפליקציה אמיתית
DEFAULT_HEADERS = {
    "User-Agent": "roborock/4.3.18 (iPhone; iOS 15.1; Scale/3.00)",
    "Content-Type": "application/json",
    "Accept": "*/*"
}

session = {"token": None, "user_id": None, "device_id": None}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/request_code')
def request_code():
    try:
        with httpx.Client(headers=DEFAULT_HEADERS) as client:
            resp = client.post(f"{BASE_URL}/sendEmailCode", json={
                "email": EMAIL,
                "type": "login",
                "rr_region": "global"
            })
            print(f"Roborock Status: {resp.status_code}, Body: {resp.text}")
            if resp.status_code == 200:
                return jsonify({"status": "code_sent"})
            return jsonify({"status": "error", "message": resp.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/login/<code>')
def login(code):
    try:
        with httpx.Client(headers=DEFAULT_HEADERS) as client:
            resp = client.post(f"{BASE_URL}/loginWithCode", json={
                "email": EMAIL, 
                "code": code, 
                "remember_me": True,
                "rr_region": "global"
            }).json()
            
            if "data" in resp:
                session['token'] = resp['data']['token']
                session['user_id'] = resp['data']['userId']
                
                headers = DEFAULT_HEADERS.copy()
                headers["Authorization"] = session['token']
                devices_resp = client.get(f"{BASE_URL}/user/devices", headers=headers).json()
                
                if "data" in devices_resp and len(devices_resp['data']) > 0:
                    session['device_id'] = devices_resp['data'][0]['duid']
                    return jsonify({"status": "success"})
                return jsonify({"status": "no_devices"})
            return jsonify({"status": "failed", "details": resp})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/action/<cmd>')
def run_command(cmd):
    if not session['token'] or not session['device_id']:
        return jsonify({"status": "not_logged_in"})
    
    commands = {"start": "app_start", "stop": "app_stop", "home": "app_charge"}
    target_cmd = commands.get(cmd)
    
    try:
        with httpx.Client(headers=DEFAULT_HEADERS) as client:
            headers = DEFAULT_HEADERS.copy()
            headers["Authorization"] = session['token']
            payload = {
                "duid": session['device_id'],
                "method": target_cmd,
                "params": []
            }
            client.post(f"{BASE_URL}/user/device/command", json=payload, headers=headers)
            return jsonify({"status": f"Robot {cmd}ing..."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

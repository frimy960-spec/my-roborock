import os, httpx
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home(): 
    return render_template('index.html')

# שינינו את השם מ-request_code ל-send_auth
@app.route('/send_auth')
def send_auth():
    print("!!! NEW VERSION EXECUTING !!!")
    email = "gs6817771@gmail.com"
    # כתובת API חלופית של רובורוק
    url = "https://api-global.roborock.com/api/v1/sendEmailCode"
    
    headers = {
        "User-Agent": "roborock/4.3.18 (iPhone; iOS 15.1; Scale/3.00)",
        "Content-Type": "application/json"
    }
    
    try:
        with httpx.Client(headers=headers, timeout=20.0) as client:
            resp = client.post(url, json={
                "email": email, 
                "type": "login", 
                "rr_region": "global"
            })
            print(f"ROBOROCK ANSWER: {resp.status_code} | {resp.text}")
            return jsonify({"status": "ok", "server_msg": resp.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

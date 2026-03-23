import os
import asyncio
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from roborock import RoborockApiClient

app = Flask(__name__)
CORS(app)

client = None
EMAIL = "gs6817771@gmail.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/request_code')
def request_code():
    async def _req():
        global client
        client = RoborockApiClient(EMAIL)
        await client.request_code()
        return True
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_req())
    return jsonify({"status": "code_sent"})

@app.route('/login/<code>')
def login(code):
    async def _login():
        global client
        if not client:
            client = RoborockApiClient(EMAIL)
        await client.code_login(code)
        return True

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(_login())
    return jsonify({"status": "success" if res else "failed"})

@app.route('/action/<cmd>')
def run_command(cmd):
    async def _do():
        global client
        if not client: return False
        
        home_data = await client.get_home_data()
        if not home_data or not home_data.devices: return False
        
        device_id = home_data.devices[0].duid
        
        if cmd == "start": await client.send_command(device_id, "app_start", [])
        elif cmd == "stop": await client.send_command(device_id, "app_stop", [])
        elif cmd == "home": await client.send_command(device_id, "app_charge", [])
        return True

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(_do())
    return jsonify({"status": "done", "result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

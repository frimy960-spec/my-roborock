import os
from flask import Flask, jsonify
from flask_cors import CORS
from roborock import RoborockClient
import asyncio

app = Flask(__name__)
CORS(app)

EMAIL = "gs6817771@gmail.com"

@app.route('/')
def home():
    return "The Robot Server is Running!"

@app.route('/action/<cmd>')
def run_command(cmd):
    async def _do():
        client = RoborockClient(EMAIL)
        devices = await client.get_devices()
        if devices:
            device = devices[0]
            if cmd == "start": await client.start_clean(device)
            elif cmd == "stop": await client.stop_clean(device)
            elif cmd == "home": await client.return_to_dock(device)
            return True
        return False

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_do())
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

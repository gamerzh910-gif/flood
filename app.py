from flask import Flask
import os
import threading
import time

app = Flask(__name__)

# Global variable to track bot status
bot_status = {
    "status": "initializing",
    "uptime": 0,
    "start_time": time.time()
}

def run_bot():
    """Run the bot in a separate thread"""
    try:
        bot_status["status"] = "running"
        # Import and run main bot
        import main
    except Exception as e:
        bot_status["status"] = f"error: {str(e)}"

@app.route('/')
def hello_world():
    uptime = int(time.time() - bot_status["start_time"])
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SudoR2spr Repository</title>
    <link rel="icon" type="image/x-icon" href="https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png">
    <style>
        body {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            font-family: 'Courier New', monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .container {{
            text-align: center;
            background: rgba(0,0,0,0.3);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        .ascii-art {{
            font-size: 14px;
            line-height: 1.2;
            margin: 20px 0;
            color: #00ff88;
        }}
        .status {{
            margin-top: 20px;
            padding: 10px;
            background: rgba(0,255,136,0.1);
            border-radius: 10px;
            border: 1px solid #00ff88;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="ascii-art">
            />▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄<br>
            />██░▄▄▄░█░▄▄▀█▄░▄██░▀██░█▄░▄██<br>
            />██▄▄▄▀▀█░▀▀░██░███░█░█░██░███<br>
            />██░▀▀▀░█░██░█▀░▀██░██▄░█▀░▀██<br>
            />▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀<br>
        </div>
        <h2>⚡ Bot Status: {bot_status["status"]} ⚡</h2>
        <div class="status">
            <p>🟢 Uptime: {uptime} seconds</p>
            <p>🚀 Speed Optimized Version</p>
            <p>📦 Concurrent Fragments: 16</p>
            <p>⚡ External Downloader: aria2c (16 connections)</p>
        </div>
        <footer style="margin-top: 30px; font-size: 12px;">
            <p>Powered By SAINI | v2.0.0 MAX SPEED</p>
        </footer>
    </div>
</body>
</html>
"""

@app.route('/health')
def health_check():
    return {"status": "ok", "bot_status": bot_status["status"], "uptime": int(time.time() - bot_status["start_time"])}

if __name__ == "__main__":
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Get port from environment variable (Heroku)
    port = int(os.environ.get("PORT", 8000))

    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)

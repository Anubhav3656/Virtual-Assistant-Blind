from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import os

app = Flask(__name__)

assistant_process = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_assistant():
    global assistant_process
    if assistant_process is None:
        assistant_process = subprocess.Popen(["python3", "main.py"])
        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})

@app.route("/stop", methods=["POST"])
def stop_assistant():
    global assistant_process
    if assistant_process is not None:
        assistant_process.terminate()
        assistant_process = None
        return jsonify({"status": "stopped"})
    return jsonify({"status": "not running"})

if __name__ == "__main__":
    app.run(debug=True)

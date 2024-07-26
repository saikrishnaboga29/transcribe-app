from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message="Hello from Flask on Netlify Functions!")

if __name__ == "__main__":
    app.run(debug=True)

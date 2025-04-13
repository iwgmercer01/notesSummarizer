from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from openai import OpenAI  # New import style

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # New client initialization

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    notes = request.json.get("notes", "")
    try:
        response = client.chat.completions.create(  # New syntax
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize these notes into bullet points."},
                {"role": "user", "content": notes},
            ],
        )
        summary = response.choices[0].message.content
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
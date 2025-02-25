import json
import os
import traceback
from google import generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory, Response


API_KEY = 'AIzaSyBQIj8EOOn0e5TCOWwTtrywrXdSz-dChvY'

genai.configure(api_key=API_KEY)

app = Flask(__name__)


@app.route("/")
def index():
    return send_file('web/index.html')


@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        if API_KEY == 'AIzaSyBQIj8EOOn0e5TCOWwTtrywrXdSz-dChvY ':
            return jsonify({ "error": '''
                To get started, get an API key at
                https://g.co/ai/idxGetGeminiKey and enter it in
                main.py
                '''.replace('\n', '') })
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = genai.GenerativeModel(model_name=req_body.get("model"))
            response = model.generate_content(content, stream=True)
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.text })

            return Response(stream(), content_type='text/event-stream')

        except Exception as e:
            traceback.print_exc()
            return jsonify({ "error": str(e) })


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))

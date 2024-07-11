from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from gradio_client import Client, handle_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = f"./{filename}"
        file.save(file_path)

        client = Client("Ayomilala/foodSpace")
        result = client.predict(
            image=handle_file(file_path),
            api_name="/predict"
        )
        return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


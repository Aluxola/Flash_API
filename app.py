import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Flash API is running"

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image/jpeg' not in request.headers.get('Content-Type', ''):
        return jsonify({"error": "Content-Type must be image/jpeg"}), 400

    image_data = request.data
    if not image_data:
        return jsonify({"error": "No image data received"}), 400

    print(f"Received image of size: {len(image_data)} bytes")

    # Save the image to file for verification
    with open("received_image.jpg", "wb") as f:
        f.write(image_data)

    return jsonify({"message": "Image received successfully"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port) 
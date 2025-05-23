from flask import Flask, request, jsonify
import requests
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Your local server URL (you'll need to expose this using ngrok)
LOCAL_SERVER_URL = "http://your-ngrok-url:8000/detect"

@app.route('/')
def index():
    """Root endpoint that returns API status."""
    return jsonify({
        "status": "online",
        "message": "ESP32-CAM Image Forwarding API",
        "endpoints": {
            "POST /upload": "Upload and forward images from ESP32-CAM",
            "GET /health": "Health check endpoint"
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Check if image file is present in request
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({'error': 'No image file provided'}), 400
            
        image_file = request.files['image']
        
        # Log the received request
        logger.info(f"Received image from ESP32-CAM: {image_file.filename}")
        
        try:
            # Forward the image to your local server
            files = {'file': (image_file.filename, image_file.read())}
            response = requests.post(LOCAL_SERVER_URL, files=files)
            
            # Log the forwarding result
            logger.info(f"Forwarded image to local server. Response: {response.status_code}")
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to local server: {str(e)}")
            return jsonify({
                'error': 'Local server unreachable',
                'timestamp': datetime.now().isoformat()
            }), 503
            
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
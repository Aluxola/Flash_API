# ESP32-CAM Image Forwarding API

A Flask-based API deployed on Render that receives images from ESP32-CAM and forwards them to a local server for processing.

## Project Structure
```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run locally:
```bash
python app.py
```

## Deployment to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.9 or higher

## API Endpoints

### Health Check
- URL: `/health`
- Method: `GET`
- Response: `{"status": "healthy"}`

### Upload Image
- URL: `/upload`
- Method: `POST`
- Body: Form-data with key 'image' and file value
- Response: JSON response from local server or error message

## ESP32-CAM Configuration

Update your ESP32-CAM code with the Render deployment URL:
```cpp
const char* serverUrl = "https://your-app-name.onrender.com/upload";
```

## Local Server Setup

1. Install ngrok
2. Start your local server
3. Run ngrok: `ngrok http 8000`
4. Update `LOCAL_SERVER_URL` in `app.py` with your ngrok URL 
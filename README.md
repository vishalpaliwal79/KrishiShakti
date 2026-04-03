# 🌾 KrishiShakti - Smart Agriculture & IoT Monitoring System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**KrishiShakti** (कृषि शक्ति - Agricultural Power) is a comprehensive IoT-based smart agriculture monitoring system that provides real-time sensor data, AI-powered crop analysis, and intelligent farming recommendations.

## 🌟 Features

### 📊 Real-Time Sensor Monitoring
- **MQ-135 Gas Sensor**: Air quality monitoring
- **DHT22 Sensor**: Temperature and humidity monitoring
- **FC-28 Sensor**: Soil moisture tracking
- **Ultrasonic Sensor**: Water tank level

### 🤖 AI-Powered Features
- **Crop Disease Detection**: Upload crop images for AI analysis via OpenRouter vision model
- **Smart Advisory System**: AI-driven irrigation, fertilizer, and pest control recommendations
- **Multi-Language Chatbot**: Get farming advice in English, Hindi (हिंदी), and Punjabi (ਪੰਜਾਬੀ)

### 🌐 Web Dashboard
- Responsive UI with real-time updates via WebSocket
- Historical data visualization
- Automated alerts and warnings
- Mobile-responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open dashboard**
```
http://localhost:5001/dashboard.html
```

## 🏗️ Project Structure

```
krishishakti/
├── app.py                  # Flask server (main application)
├── ai_chat.py              # AI chatbot (OpenRouter)
├── ai_disease_model.py     # Crop disease detection (OpenRouter vision)
├── ai_engine.py            # AI decision engine
├── arduino_bridge.py       # Arduino hardware interface
├── device_controller.py    # Device control logic
├── database.py             # SQLite database
├── requirements.txt        # Python dependencies
├── public/                 # Frontend files
│   ├── dashboard.html
│   ├── agriculture.html
│   ├── chatbot.html
│   ├── control.html
│   ├── alerts.html
│   └── ...
├── data/                   # Local data storage
└── arduino/                # Arduino sketch
    └── sensor_reader.ino
```

## 🌐 API Endpoints

- `GET  /api/sensors` — Current sensor readings
- `POST /api/sensors` — Update sensor data
- `GET  /api/history` — Historical data
- `POST /api/chatbot/message` — AI chatbot
- `POST /api/predict-disease` — Crop disease detection
- `GET  /api/alerts` — System alerts

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask & Socket.IO for backend and real-time communication
- OpenRouter for AI capabilities
- Arduino for hardware integration

---

**Made with ❤️ for farmers and agriculture**

**कृषि शक्ति - Agricultural Power** 🌾
# KrishiShakti

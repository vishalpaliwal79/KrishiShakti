# 🌾 KrishiShakti - Smart Agriculture & IoT Monitoring System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**KrishiShakti** (कृषि शक्ति - Agricultural Power) is a comprehensive IoT-based smart agriculture monitoring system that provides real-time sensor data, AI-powered crop analysis, and intelligent farming recommendations.

![Dashboard Preview](https://via.placeholder.com/800x400?text=KrishiShakti+Dashboard)

## 🌟 Features

### 📊 Real-Time Sensor Monitoring
- **MQ-135 Gas Sensor**: Air quality monitoring (18-20 ppm)
- **PMS5003 Sensor**: Particulate matter detection (PM2.5, PM10: 10-12 µg/m³)
- **DHT22 Sensor**: Temperature (28-30°C) and humidity monitoring
- **FC-28 Sensor**: Soil moisture/water level tracking (10-12%)
- **TDS Sensor**: Water quality measurement (100-150 ppm)

### 🤖 AI-Powered Features
- **Crop Disease Detection**: Upload crop images for AI analysis
- **Smart Advisory System**: AI-driven irrigation, fertilizer, and pest control recommendations
- **Multi-Language Chatbot**: Get farming advice in English, Hindi (हिंदी), and Punjabi (ਪੰਜਾਬੀ)
- **Predictive Analytics**: Weather-based farming suggestions

### 🌐 Web Dashboard
- Beautiful, responsive UI with real-time updates
- WebSocket support for live data streaming
- Historical data visualization
- Export data to CSV/Excel
- Google Sheets integration (optional)

### 📱 Additional Features
- Location-based recommendations
- Automated alerts and warnings
- Data logging and history
- Mobile-responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/krishishakti.git
cd krishishakti
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
# Terminal 1: Start Flask server
python app.py

# Terminal 2: Start simulator (for testing without hardware)
python simulator.py
```

5. **Open dashboard**
```
http://localhost:5001/dashboard.html
```

## 📖 Documentation

- **[Quick Start Guide](QUICK-START-GUIDE.md)** - Get started in 5 minutes
- **[Data Flow Explained](DATA-FLOW-EXPLAINED.md)** - Understand the system architecture
- **[Sensor Ranges](SENSOR-RANGES-UPDATED.md)** - Current sensor configurations
- **[Google Sheets Setup](GOOGLE-SHEETS-SETUP.md)** - Cloud data storage setup
- **[API Documentation](API-DOCS.md)** - REST API endpoints

## 🏗️ Project Structure

```
krishishakti/
├── app.py                      # Flask server (main application)
├── simulator.py                # Sensor data simulator
├── arduino_bridge.py           # Arduino hardware interface
├── google_sheets_setup.py      # Google Sheets integration
├── view_data.py               # Data viewer utility
├── requirements.txt           # Python dependencies
├── public/                    # Frontend files
│   ├── dashboard.html         # Main dashboard
│   ├── dashboard.css          # Dashboard styles
│   ├── dashboard.js           # Dashboard logic
│   ├── chatbot.html          # AI chatbot interface
│   ├── agriculture.html      # Agriculture AI module
│   └── ...
├── data/                      # Data storage
│   ├── history.json          # Sensor data history
│   └── sensor_data_export.csv # Exported data
├── arduino/                   # Arduino code
│   └── sensor_reader.ino     # Arduino sensor code
└── docs/                      # Documentation
```

## 🔧 Configuration

### Sensor Ranges (Customizable)
Edit `simulator.py` to change sensor ranges:

```python
data = {
    'mq135': round(18 + random.random() * 2, 2),      # 18-20 ppm
    'temperature': round(28 + random.random() * 2, 2), # 28-30°C
    'pm25': round(10 + random.random() * 2, 2),       # 10-12 µg/m³
    'fc28': round(10 + random.random() * 2, 2),       # 10-12%
    'tds': round(100 + random.random() * 50, 0)       # 100-150 ppm
}
```

### Update Frequency
Data updates every 7-8 seconds (configurable in `simulator.py`)

## 🌐 API Endpoints

### Sensor Data
- `GET /api/sensors` - Get current sensor readings
- `POST /api/sensors` - Update sensor data
- `GET /api/history` - Get historical data

### Chatbot
- `POST /api/chatbot/message` - Send message to AI chatbot

### Agriculture AI
- `POST /api/agriculture/analyze` - Analyze crop image
- `POST /api/agriculture/irrigation-advice` - Get irrigation recommendations
- `POST /api/agriculture/fertilizer-advice` - Get fertilizer suggestions
- `POST /api/agriculture/pest-advice` - Get pest control guidance

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/600x400?text=Dashboard)

### AI Chatbot
![Chatbot](https://via.placeholder.com/600x400?text=Chatbot)

### Agriculture AI
![Agriculture](https://via.placeholder.com/600x400?text=Agriculture+AI)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/YOUR_USERNAME)

## 🙏 Acknowledgments

- Flask framework for the backend
- Socket.IO for real-time communication
- OpenStreetMap for location services
- All contributors and supporters

## 📞 Support

For support, email your-email@example.com or open an issue on GitHub.

## 🔗 Links

- [Documentation](https://github.com/YOUR_USERNAME/krishishakti/wiki)
- [Issue Tracker](https://github.com/YOUR_USERNAME/krishishakti/issues)
- [Changelog](CHANGELOG.md)

---

**Made with ❤️ for farmers and agriculture**

**कृषि शक्ति - Agricultural Power** 🌾
# krishishakti
# KrishiShakti
# KrishiShakti
# KrishiShakti_local

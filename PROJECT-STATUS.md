# 🎯 AirWater Pro - Project Status

## ✅ Current Stack

**Backend**: Flask (Python 3)
**Frontend**: HTML, CSS, JavaScript
**Real-time**: Flask-SocketIO (WebSocket)
**Data Storage**: Local JSON file (`data/history.json`)
**Hardware**: Arduino Uno + 5 sensors

## 🚀 Quick Start Commands

```bash
# Setup (first time only)
./setup.sh

# Run Flask server
./run.sh

# Run simulator (in another terminal)
./run_simulator.sh
```

## 📂 Project Structure

```
├── app.py                    # Flask server (port 5001)
├── simulator.py              # Python data simulator
├── arduino_bridge.py         # Arduino serial bridge
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script
├── run.sh                    # Run server
├── run_simulator.sh          # Run simulator
├── public/                   # Frontend files
│   ├── index.html           # Landing page
│   ├── dashboard.html       # Main dashboard
│   ├── login.html           # Login page
│   ├── signup.html          # Signup page
│   └── *.css, *.js          # Styles and scripts
├── arduino/
│   └── sensor_reader.ino    # Arduino code
└── data/
    └── history.json         # Sensor data storage
```

## 🌐 URLs

- Landing Page: http://localhost:5001
- Dashboard: http://localhost:5001/dashboard.html
- Login: http://localhost:5001/login.html
- Signup: http://localhost:5001/signup.html

## 📊 Sensors

1. **MQ-135** - Air quality (ppm)
2. **PMS5003** - Particulate matter (PM2.5, PM10)
3. **DHT22** - Temperature & humidity
4. **FC-28** - Water tank level (%)
5. **TDS Sensor** - Water quality (ppm)

## 🔧 How It Works

1. Simulator/Arduino generates sensor data
2. Data sent to Flask server via POST `/api/sensors`
3. Server stores in `data/history.json`
4. WebSocket broadcasts to connected clients
5. Dashboard updates in real-time

## 📝 Recent Changes

- ✅ Converted from Node.js to Flask
- ✅ Removed Google Sheets integration (now local storage)
- ✅ Updated all documentation
- ✅ Cleaned up unused files
- ✅ Working simulator and Arduino bridge

## 🎓 For IIT Hackathon

This project demonstrates:
- Full-stack IoT development
- Real-time data visualization
- Environmental monitoring
- Air purification + water generation
- Modern web technologies

## 🐛 Troubleshooting

**Server won't start?**
- Run `./setup.sh` first
- Make sure port 5001 is free

**No data showing?**
- Start the simulator: `./run_simulator.sh`
- Check server terminal for errors

**Arduino not working?**
- Update port in `arduino_bridge.py`
- Check Arduino is connected: `ls /dev/cu.*`

---

**Status**: ✅ Fully functional Flask application
**Last Updated**: February 2026

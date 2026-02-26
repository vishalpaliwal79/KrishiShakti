# 🚀 KrishiShakti Quick Start Guide

## Where Does The Data Come From? (Simple Answer)

Your KrishiShakti system gets data from **2 possible sources**:

---

## 📱 Option 1: Simulator (For Testing) ✅ RECOMMENDED

**What is it?**
A Python script that generates fake but realistic sensor data for testing.

**How to start:**
```bash
python simulator.py
```

**What it does:**
- Generates random sensor values every 6-8 seconds
- Temperature: 25-28°C (optimal range)
- Humidity: 40-80%
- Air Quality: 50-200 ppm
- Soil Moisture: 20-30% (low - needs watering)
- Water Quality: 100-500 ppm
- Detects your location automatically

**You'll see:**
```
╔════════════════════════════════════════════════════════╗
║  Air Purification + Water Generation System           ║
║  Sensor Data Simulator (Python)                       ║
╚════════════════════════════════════════════════════════╝

📊 Generating random sensor data...
☁️  Data will be sent to Flask server
🔄 Sending data every 2 seconds

🌍 Detecting location...
✓ Location detected: Mumbai, India

Sending simulated data: {
  "mq135": 125.43,
  "temperature": 27.8,
  "humidity": 65.2,
  ...
}
✓ Data sent successfully
```

---

## 🔌 Option 2: Arduino Hardware (For Real Sensors)

**What is it?**
A Python script that reads data from actual Arduino sensors connected via USB.

**How to start:**
```bash
python arduino_bridge.py
```

**What you need:**
- Arduino board with sensors connected
- USB cable
- Sensors: MQ-135, PMS5003, DHT22, FC-28, TDS

**What it does:**
- Reads real sensor values from Arduino
- Sends to Flask server
- Adds location information

---

## 🌐 The Complete Flow

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Data Generation                                │
│  ┌──────────────┐         ┌──────────────┐             │
│  │  Simulator   │   OR    │   Arduino    │             │
│  │ (Fake Data)  │         │ (Real Data)  │             │
│  │ Every 6-8s   │         │ Every 5s     │             │
│  └──────┬───────┘         └──────┬───────┘             │
│         │                        │                      │
│         └────────────┬───────────┘                      │
│                      │                                  │
│                      ▼                                  │
│         ┌────────────────────────┐                     │
│         │  HTTP POST Request     │                     │
│         │  to /api/sensors       │                     │
│         └────────────┬───────────┘                     │
└──────────────────────┼──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 2: Flask Server (app.py)                          │
│  ┌──────────────────────────────────────────────┐      │
│  │  1. Receives sensor data                     │      │
│  │  2. Stores in memory (sensor_data variable)  │      │
│  │  3. Saves to file (data/history.json)        │      │
│  │  4. Broadcasts via WebSocket                 │      │
│  └──────────────────┬───────────────────────────┘      │
└────────────────────┼────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 3: Frontend Display                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Dashboard   │  │   Chatbot    │  │ Agriculture  │ │
│  │              │  │              │  │     AI       │ │
│  │ Shows live   │  │ Uses sensor  │  │ Analyzes     │ │
│  │ sensor data  │  │ data in      │  │ crop health  │ │
│  │              │  │ responses    │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Simple 3-Step Setup

### Step 1: Start Flask Server
```bash
python app.py
```
**You'll see:**
```
 * Running on http://127.0.0.1:5001
```

### Step 2: Start Simulator (in new terminal)
```bash
python simulator.py
```
**You'll see:**
```
✓ Data sent successfully
```

### Step 3: Open Dashboard
Open browser: `http://localhost:5001/dashboard.html`

**You'll see:**
- Live sensor readings updating every 2 seconds
- Your location (city, country)
- Historical data table
- All values changing in real-time

---

## 🔍 How Each Page Gets Data

### 📊 Dashboard (dashboard.html)
**Gets data from:**
- `/api/sensors` - Current readings
- `/api/history` - Historical data
- WebSocket - Real-time updates

**Shows:**
- Temperature, humidity, air quality
- Soil moisture, water quality
- Location, timestamp
- Historical table

### 💬 Chatbot (chatbot.html)
**Gets data from:**
- `/api/chatbot/message` - Send message
- Uses live sensor data in responses

**Example:**
```
You: What is the temperature?

Bot: 📊 Current Sensor Readings:
🌡️ Temperature: 27.8°C - Optimal
✓ Perfect for most crops
✓ Good photosynthesis rate
...
```

**The 27.8°C comes from the simulator!**

### 🌾 Agriculture AI (agriculture.html)
**Gets data from:**
- `/api/agriculture/analyze` - Image analysis
- `/api/agriculture/irrigation-advice` - Water tips
- `/api/agriculture/fertilizer-advice` - Fertilizer tips

**Uses:**
- Live sensor data for recommendations
- Temperature, humidity, soil moisture
- Location for weather-based advice

---

## 🎓 Key Concepts

### 1. Simulator = Fake Data Generator
- Runs continuously
- Sends data every 2 seconds
- Perfect for testing without hardware

### 2. Flask Server = Central Hub
- Receives data from simulator/Arduino
- Stores in memory and file
- Serves to all web pages

### 3. Frontend = Display Layer
- Dashboard shows live data
- Chatbot uses data in responses
- Agriculture AI uses data for advice

### 4. Everything is Connected!
- Same data flows everywhere
- Update in one place = updates everywhere
- Real-time synchronization

---

## 🐛 Common Issues

### "All values showing 0"
**Problem:** Simulator not running
**Fix:** Run `python simulator.py`

### "Cannot connect to server"
**Problem:** Flask not running
**Fix:** Run `python app.py`

### "No location showing"
**Problem:** Internet connection or API blocked
**Fix:** Check internet, or location will show after first data

### "Data not updating"
**Problem:** WebSocket connection failed
**Fix:** Refresh page, check Flask console for errors

---

## 📊 Data Update Timing

| What | How Often | Source |
|------|-----------|--------|
| Simulator sends data | Every 6-8 seconds | simulator.py |
| Dashboard updates | Real-time | WebSocket |
| History table refreshes | Every 10 seconds | HTTP request |
| Chatbot gets data | When you ask | On demand |
| Location detected | Once at startup | IP geolocation |

---

## 🎉 Success Checklist

✅ Flask server running (port 5001)
✅ Simulator running (sending data every 2 seconds)
✅ Dashboard showing live values (not all zeros)
✅ Location showing (city, country)
✅ Historical table has data
✅ Chatbot responds with sensor data
✅ Agriculture AI works

---

## 💡 Pro Tips

1. **Keep simulator running** - It continuously sends data
2. **Check Flask console** - Shows all incoming data
3. **Refresh dashboard** - If data stops updating
4. **Use simulator for testing** - No hardware needed
5. **Check browser console** - For frontend errors (F12)

---

## 📝 File Locations

```
krishishakti/
├── app.py                    ← Flask server (receives data)
├── simulator.py              ← Data generator (sends data)
├── arduino_bridge.py         ← Arduino reader (alternative)
├── data/
│   └── history.json          ← Stored sensor history
└── public/
    ├── dashboard.html        ← Shows live data
    ├── dashboard.js          ← Fetches and displays data
    ├── chatbot.html          ← Chat interface
    ├── chatbot.js            ← Uses sensor data
    ├── agriculture.html      ← AI analysis
    └── agriculture.js        ← Smart advisory
```

---

## 🎯 Summary

**Where does data come from?**
→ Simulator (simulator.py) generates it

**Where does it go?**
→ Flask server (app.py) receives and stores it

**How do I see it?**
→ Dashboard (dashboard.html) displays it

**How does chatbot use it?**
→ Chatbot reads same data and includes in responses

**How often does it update?**
→ Every 6-8 seconds from simulator

**Do I need Arduino?**
→ No! Simulator works perfectly for testing

---

**That's it!** Your data flows from simulator → Flask → dashboard/chatbot/AI. Simple! 🚀

---

**Created:** February 19, 2026
**Project:** KrishiShakti (कृषि शक्ति)

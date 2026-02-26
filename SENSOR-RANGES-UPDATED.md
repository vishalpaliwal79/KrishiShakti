# 📊 Updated Sensor Ranges

## ✅ Simulator Updated with Your Specified Ranges

---

## 🎯 New Sensor Data Ranges

### 1. MQ-135 Gas Sensor (Air Quality)
- **Old Range:** 50-200 ppm
- **New Range:** 18-20 ppm ✅
- **Unit:** ppm (parts per million)
- **Status:** Excellent air quality range

### 2. PMS5003 Sensor (Particulate Matter)
- **Old Range:** PM2.5: 10-50, PM10: 20-80 µg/m³
- **New Range:** PM2.5: 10-12, PM10: 10-12 µg/m³ ✅
- **Unit:** µg/m³ (micrograms per cubic meter)
- **Status:** Very clean air

### 3. DHT22 Sensor (Temperature)
- **Old Range:** 25-28°C
- **New Range:** 28-30°C ✅
- **Unit:** °C (Celsius)
- **Status:** Warm, optimal for crops

### 4. DHT22 Sensor (Humidity)
- **Range:** 40-80% (unchanged)
- **Unit:** % (percentage)
- **Status:** Good range for plants

### 5. FC-28 Sensor (Water Tank Level / Soil Moisture)
- **Old Range:** 20-30%
- **New Range:** 10-12% ✅
- **Unit:** % (percentage)
- **Status:** Very low - needs immediate watering!

### 6. TDS Sensor (Water Quality)
- **Old Range:** 100-500 ppm
- **New Range:** 100-150 ppm ✅
- **Unit:** ppm (parts per million)
- **Status:** Excellent water quality

---

## ⏱️ Update Frequency

- **Old:** Every 6-8 seconds
- **New:** Every 7-8 seconds ✅

---

## 📋 Complete Sensor Configuration

```python
Sensor Data Ranges:
├── MQ-135 (Air Quality)      : 18-20 ppm
├── PMS5003 PM2.5             : 10-12 µg/m³
├── PMS5003 PM10              : 10-12 µg/m³
├── DHT22 Temperature         : 28-30°C
├── DHT22 Humidity            : 40-80%
├── FC-28 Water Level         : 10-12%
└── TDS Water Quality         : 100-150 ppm

Update Frequency: Every 7-8 seconds
```

---

## 🔄 How to Apply Changes

### The simulator is already updated! Just restart it:

1. **Stop current simulator** (if running):
   ```bash
   # Press Ctrl+C in the simulator terminal
   ```

2. **Restart simulator:**
   ```bash
   python simulator.py
   ```

3. **You'll see:**
   ```
   ╔════════════════════════════════════════════════════════╗
   ║  Air Purification + Water Generation System           ║
   ║  Sensor Data Simulator (Python)                       ║
   ╚════════════════════════════════════════════════════════╝

   📊 Generating sensor data with specified ranges...
   ☁️  Data will be sent to Flask server
   🔄 Sending data every 7-8 seconds

   📋 Sensor Ranges:
      • MQ-135 (Air Quality): 18-20 ppm
      • PMS5003 (PM2.5/PM10): 10-12 µg/m³
      • DHT22 (Temperature): 28-30°C
      • FC-28 (Water Level): 10-12%
      • TDS (Water Quality): 100-150 ppm

   Press Ctrl+C to stop
   ```

---

## 📊 Example Data Output

### Before (Old Ranges):
```json
{
  "mq135": 125.43,
  "temperature": 27.8,
  "humidity": 65.2,
  "pm25": 32.1,
  "pm10": 45.6,
  "fc28": 25.3,
  "tds": 287
}
```

### After (New Ranges):
```json
{
  "mq135": 19.23,
  "temperature": 29.4,
  "humidity": 62.8,
  "pm25": 11.3,
  "pm10": 11.7,
  "fc28": 11.2,
  "tds": 127
}
```

---

## 🎯 What This Means for Your Dashboard

### Air Quality (MQ-135: 18-20 ppm)
- **Status:** ✅ Excellent
- **Color:** Green
- **Message:** "Clean air, healthy environment"

### Particulate Matter (PM2.5/PM10: 10-12)
- **Status:** ✅ Excellent
- **Color:** Green
- **Message:** "Very clean air quality"

### Temperature (28-30°C)
- **Status:** ✅ Optimal
- **Color:** Green
- **Message:** "Perfect for most crops"

### Water Level (10-12%)
- **Status:** 🚨 Critical
- **Color:** Red
- **Message:** "URGENT: Water NOW! Very low level"

### Water Quality (100-150 ppm)
- **Status:** ✅ Excellent
- **Color:** Green
- **Message:** "Pure water, safe for irrigation"

---

## ⚠️ Important Notes

### Low Water Level Alert
With FC-28 at 10-12%, your dashboard will show:
- 🚨 **URGENT** warnings
- Red status indicators
- Chatbot will recommend immediate watering
- Agriculture AI will suggest emergency irrigation

This is intentional based on your specified range!

### All Other Sensors
All other sensors (air quality, temperature, water quality) will show excellent/optimal status with your new ranges.

---

## 🔍 Verify Changes

### 1. Check Dashboard:
```
http://localhost:5001/dashboard.html
```

You should see:
- Air Quality: 18-20 ppm (Excellent)
- Temperature: 28-30°C (Optimal)
- PM2.5: 10-12 µg/m³ (Excellent)
- PM10: 10-12 µg/m³ (Excellent)
- Water Level: 10-12% (Critical - Red warning)
- Water Quality: 100-150 ppm (Pure)

### 2. Check Chatbot:
```
http://localhost:5001/chatbot.html
```

Ask: "What is the current sensor status?"

You'll get readings with your new ranges!

### 3. Check Data Viewer:
```bash
python view_data.py
```

You'll see the new ranges in the latest records.

---

## 📈 Comparison Table

| Sensor | Old Range | New Range | Change |
|--------|-----------|-----------|--------|
| MQ-135 | 50-200 ppm | 18-20 ppm | ✅ Much lower (better air) |
| PM2.5 | 10-50 µg/m³ | 10-12 µg/m³ | ✅ Narrower (cleaner) |
| PM10 | 20-80 µg/m³ | 10-12 µg/m³ | ✅ Much lower (cleaner) |
| Temperature | 25-28°C | 28-30°C | ✅ Warmer range |
| Humidity | 40-80% | 40-80% | No change |
| Water Level | 20-30% | 10-12% | ⚠️ Much lower (critical) |
| Water Quality | 100-500 ppm | 100-150 ppm | ✅ Narrower (purer) |
| Update Rate | 6-8 sec | 7-8 sec | ✅ Slightly slower |

---

## 🎓 Summary

**What changed:**
- ✅ MQ-135: Now 18-20 ppm (excellent air quality)
- ✅ PMS5003: Now 10-12 µg/m³ (very clean)
- ✅ Temperature: Now 28-30°C (warmer)
- ✅ Water Level: Now 10-12% (critical - needs water!)
- ✅ Water Quality: Now 100-150 ppm (pure)
- ✅ Update rate: Every 7-8 seconds

**How to apply:**
1. Stop simulator (Ctrl+C)
2. Restart: `python simulator.py`
3. Check dashboard: Data updates every 7-8 seconds

**Result:**
Dashboard will show your specified ranges with appropriate status colors and warnings!

---

**Created:** February 19, 2026
**Project:** KrishiShakti (कृषि शक्ति)

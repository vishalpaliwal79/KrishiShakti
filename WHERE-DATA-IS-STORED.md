# 📊 Where Your Data is Stored

## ✅ Your Data is Being Saved!

**You have 670+ sensor readings stored!**

---

## 📁 Data Storage Locations

### 1. Local File Storage (Primary)

**File:** `data/history.json`
**Location:** `/Users/amankaushik/Documents/All kiro/AIR CONVERTER PROJECT /data/history.json`
**Size:** 464 KB
**Records:** 670+ readings

**What's stored:**
- All sensor readings (temperature, humidity, air quality, etc.)
- Timestamps
- Location data (Bhiwadi, India)
- Complete history since you started

---

## 🔍 How to View Your Data

### Option 1: Command Line Viewer (Detailed)

```bash
python view_data.py
```

**Shows:**
- Latest 10 records with full details
- Statistics (averages, min/max)
- Total record count
- Warnings if any issues detected

### Option 2: Export to CSV (For Excel)

```bash
python view_data.py export
```

**Creates:** `data/sensor_data_export.csv`
**You can open this in:**
- Microsoft Excel
- Google Sheets
- Any spreadsheet software

### Option 3: Web Browser Viewer (Beautiful UI)

**Open in browser:**
```
http://localhost:5001/data-viewer.html
```

**Features:**
- Beautiful table view
- Statistics cards
- Auto-refresh every 10 seconds
- Export to CSV button
- Shows last 100 records
- Color-coded status (Good/Warning/Critical)

---

## 📊 Your Current Data Summary

**From the latest view:**

```
📊 Total Records: 670
📅 First Record: 2026-02-19 22:38:26
📅 Last Record: 2026-02-19 22:49:57

📈 STATISTICS:

🌡️  Temperature:
   Average: 27.5°C
   Range: 20.0°C - 35.0°C

💧 Humidity:
   Average: 60.6%

🌿 Air Quality:
   Average: 125.4 ppm

💦 Soil Moisture:
   Average: 55.2%
   Range: 30.1% - 80.0%
```

---

## 📋 Latest 3 Records (Example)

**Record #670:**
- Time: 2026-02-19 22:49:57
- Location: Bhiwadi, India
- Temperature: 32.1°C
- Humidity: 75.3%
- Air Quality: 63.9 ppm
- Soil Moisture: 74.0%
- Water Quality: 344 ppm

**Record #669:**
- Time: 2026-02-19 22:49:57
- Temperature: 20.1°C
- Humidity: 75.3%
- Air Quality: 180.0 ppm
- Soil Moisture: 75.9%
- Water Quality: 211 ppm

**Record #668:**
- Time: 2026-02-19 22:49:55
- Temperature: 34.6°C
- Humidity: 78.3%
- Air Quality: 175.0 ppm
- Soil Moisture: 48.6%
- Water Quality: 197 ppm

---

## 🔄 Data Flow

```
Simulator (every 6-8 seconds)
    ↓
Flask Server (app.py)
    ↓
Saves to: data/history.json
    ↓
You can view with:
    - python view_data.py
    - http://localhost:5001/data-viewer.html
    - Open data/sensor_data_export.csv in Excel
```

---

## 📁 Files Created for You

### 1. `view_data.py`
**Purpose:** Command-line data viewer
**Usage:**
```bash
python view_data.py          # View data
python view_data.py export   # Export to CSV
```

### 2. `data/history.json`
**Purpose:** Main data storage file
**Format:** JSON
**Size:** 464 KB (670+ records)

### 3. `data/sensor_data_export.csv`
**Purpose:** Exported CSV file
**Format:** CSV (Excel-compatible)
**Size:** 69.5 KB
**Can open in:** Excel, Google Sheets, Numbers

### 4. `public/data-viewer.html`
**Purpose:** Web-based data viewer
**Access:** http://localhost:5001/data-viewer.html
**Features:** Beautiful UI, auto-refresh, export button

---

## 💡 Quick Commands

### View data in terminal:
```bash
python view_data.py
```

### Export to Excel:
```bash
python view_data.py export
```

### View in browser:
1. Make sure Flask is running: `python app.py`
2. Open: http://localhost:5001/data-viewer.html

### Check file directly:
```bash
cat data/history.json | python -m json.tool | head -50
```

---

## 📊 Data Viewer Features

### Command Line Viewer (`view_data.py`):
✅ Shows latest 10 records
✅ Displays full details for each record
✅ Calculates statistics (averages, min/max)
✅ Shows warnings for critical values
✅ Export to CSV functionality

### Web Viewer (`data-viewer.html`):
✅ Beautiful, modern UI
✅ Shows last 100 records in table
✅ Statistics cards (total, averages)
✅ Auto-refresh every 10 seconds
✅ Export to CSV button
✅ Color-coded status indicators
✅ Responsive design (works on mobile)

---

## 🎯 What You Can Do Now

### 1. View Your Data:
```bash
python view_data.py
```

### 2. Open in Browser:
```
http://localhost:5001/data-viewer.html
```

### 3. Export to Excel:
```bash
python view_data.py export
# Then open: data/sensor_data_export.csv
```

### 4. Check Raw File:
```bash
ls -lh data/
# You'll see history.json and sensor_data_export.csv
```

---

## 📈 Data Growth

**Current:** 670 records in ~11 minutes
**Rate:** ~1 record per second (old rate was every 2 seconds)
**New rate:** 1 record every 6-8 seconds

**Estimated storage:**
- 1 hour: ~500 records (~350 KB)
- 1 day: ~12,000 records (~8 MB)
- 1 week: ~84,000 records (~56 MB)
- 1 month: ~360,000 records (~240 MB)

---

## 🔐 Data Backup

Your data is automatically saved to:
1. **Local file:** `data/history.json` (always)
2. **Google Sheets:** (when you set it up)

**Backup recommendations:**
- Copy `data/history.json` regularly
- Export to CSV weekly
- Set up Google Sheets for cloud backup

---

## 🎓 Summary

**Where is data stored?**
→ `data/history.json` file (464 KB, 670+ records)

**How to view it?**
→ `python view_data.py` OR `http://localhost:5001/data-viewer.html`

**How to export?**
→ `python view_data.py export` (creates CSV file)

**Is it working?**
→ YES! You have 670+ records already saved!

**How often is it saved?**
→ Every 6-8 seconds (new rate)

---

**Your data is safe and accessible! Use any of the 3 methods above to view it.** 🎉

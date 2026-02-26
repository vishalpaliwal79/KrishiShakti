# 📊 Where is Google Sheets? - Complete Answer

## 🎯 Quick Answer

**Google Sheets is NOT created yet!** You need to set it up first. Here's how:

---

## 📁 Files I Created for You

### 1. `google_sheets_setup.py`
**What it does:** Creates and connects to Google Sheets
**How to use:** `python google_sheets_setup.py`

### 2. `GOOGLE-SHEETS-SETUP.md`
**What it is:** Complete detailed setup guide (20+ pages)
**Read this for:** Step-by-step instructions with screenshots

### 3. `GOOGLE-SHEETS-QUICK-START.md`
**What it is:** Quick 5-minute setup guide
**Read this for:** Fast setup without details

### 4. `install_google_sheets.sh`
**What it does:** Installs required libraries
**How to use:** `./install_google_sheets.sh`

### 5. Updated `app.py`
**What changed:** Added Google Sheets integration code
**Effect:** Will automatically save data to Google Sheets once configured

### 6. Updated `requirements.txt`
**What changed:** Added Google Sheets libraries
**Effect:** Can install all dependencies with `pip install -r requirements.txt`

---

## 🚀 How to Create Your Google Sheet (Simple Steps)

### Step 1: Install Libraries
```bash
pip install gspread google-auth
```

### Step 2: Get Google Credentials

1. Go to: **https://console.cloud.google.com/**
2. Create a new project called "KrishiShakti"
3. Enable these APIs:
   - Google Sheets API
   - Google Drive API
4. Create a Service Account
5. Download the JSON key file
6. Rename it to `credentials.json`
7. Put it in your project folder (same folder as app.py)

### Step 3: Run Setup Script
```bash
python google_sheets_setup.py
```

**This will:**
- Create a new Google Sheet called "KrishiShakti Sensor Data"
- Add two sheets: "Sensor Data" and "Dashboard"
- Give you the URL to access it

### Step 4: Restart Flask
```bash
python app.py
```

**Now data will automatically save to Google Sheets!**

---

## 📊 What Will Your Google Sheet Look Like?

### Sheet 1: Sensor Data (Raw Data)

Every 2 seconds, a new row is added:

```
Row 1 (Headers):
Timestamp | Date | Time | Air Quality | Temperature | Humidity | PM2.5 | PM10 | Soil Moisture | Water Quality | City | Country | Lat | Lon | Status

Row 2 (Data):
2026-02-19T20:30:45 | 2026-02-19 | 20:30:45 | 125.43 | 27.8 | 65.2 | 32.1 | 45.6 | 25.3 | 287 | Bhiwadi | India | 28.21 | 76.86 | Good

Row 3 (Data):
2026-02-19T20:30:47 | 2026-02-19 | 20:30:47 | 132.15 | 27.9 | 64.8 | 33.5 | 46.2 | 24.8 | 289 | Bhiwadi | India | 28.21 | 76.86 | Good

... (continues automatically)
```

### Sheet 2: Dashboard (Summary)

Shows latest values and status:

```
KrishiShakti Sensor Dashboard

Latest Readings:
┌─────────────────┬───────────────┬──────────┐
│ Metric          │ Current Value │ Status   │
├─────────────────┼───────────────┼──────────┤
│ Temperature     │ 27.8°C        │ Normal   │
│ Humidity        │ 65.2%         │ Normal   │
│ Soil Moisture   │ 25.3%         │ Low      │
│ Air Quality     │ 125 ppm       │ Good     │
│ Water Quality   │ 287 ppm       │ Good     │
└─────────────────┴───────────────┴──────────┘
```

---

## 🔄 Data Flow with Google Sheets

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Simulator Generates Data                       │
│  simulator.py → Every 2 seconds                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  STEP 2: Flask Receives Data                            │
│  app.py → POST /api/sensors                             │
└────────┬───────────────────┬────────────────────────────┘
         │                   │
         ▼                   ▼
┌────────────────┐   ┌──────────────────────────────────┐
│  Local Storage │   │  Google Sheets (NEW!)            │
│  history.json  │   │  - Sensor Data sheet             │
│                │   │  - Dashboard sheet               │
│                │   │  - Accessible from anywhere      │
└────────────────┘   └──────────────────────────────────┘
         │                   │
         └─────────┬─────────┘
                   ▼
         ┌─────────────────┐
         │  Your Browser   │
         │  Dashboard      │
         └─────────────────┘
```

---

## 🎯 Current Status

### ✅ What's Ready:
- [x] Google Sheets integration code written
- [x] Setup scripts created
- [x] Documentation written
- [x] Flask app updated
- [x] Simulator updated (temp 25-28°C, moisture 20-30%)

### ⏳ What You Need to Do:
- [ ] Install libraries: `pip install gspread google-auth`
- [ ] Create Google Cloud project
- [ ] Download credentials.json
- [ ] Run setup script: `python google_sheets_setup.py`
- [ ] Restart Flask: `python app.py`

---

## 📍 Where to Find Your Google Sheet (After Setup)

### Option 1: From Terminal
After running `python google_sheets_setup.py`, you'll see:
```
📊 Spreadsheet URL: https://docs.google.com/spreadsheets/d/xxxxx
```
**Copy this URL and open in browser!**

### Option 2: From Google Drive
1. Go to: https://drive.google.com/
2. Look for: "KrishiShakti Sensor Data"
3. Click to open

### Option 3: From Google Sheets
1. Go to: https://sheets.google.com/
2. Look in "Recent" or search for "KrishiShakti"
3. Click to open

---

## 💡 Why Google Sheets?

### Benefits:
1. **Cloud Backup** - Never lose data
2. **Access Anywhere** - Phone, tablet, computer
3. **Share Easily** - Send link to team members
4. **Create Charts** - Beautiful visualizations
5. **Export Data** - Download as Excel/CSV
6. **Real-time Updates** - See data as it arrives
7. **Free** - No cost for basic usage
8. **Reliable** - Google's infrastructure

### Use Cases:
- Monitor farm from home
- Share data with agricultural advisor
- Create reports for analysis
- Track trends over weeks/months
- Compare different time periods
- Export for presentations

---

## 🔐 Security

### credentials.json File:
- **Keep it private!** Don't share
- **Don't commit to Git** (already in .gitignore)
- **Backup safely** in secure location

### Google Sheet Access:
- Only you and the service account can access
- Share with specific people using "Share" button
- Can revoke access anytime

---

## 📊 Example: What You'll See

### After 1 Hour of Running:
- **1,800 rows** of data (1 row every 2 seconds)
- **Complete history** of all sensor readings
- **Charts** showing trends
- **Status indicators** for warnings

### After 1 Day:
- **43,200 rows** of data
- **Daily patterns** visible in charts
- **Peak times** identified
- **Anomalies** highlighted

### After 1 Week:
- **302,400 rows** of data
- **Weekly trends** clear
- **Comparison** between days
- **Predictive insights** possible

---

## 🎓 Summary

**Where is Google Sheets?**
→ Not created yet! You need to set it up.

**How to create it?**
→ Follow GOOGLE-SHEETS-QUICK-START.md (5 minutes)

**What will it contain?**
→ All your sensor data, automatically updated every 2 seconds

**How to access it?**
→ URL will be shown after setup, or find in Google Drive

**Is it working now?**
→ No, you need to complete setup first

**What do I need?**
→ Google account + 5 minutes + credentials.json file

---

## 🚀 Quick Start Command

```bash
# Step 1: Install
pip install gspread google-auth

# Step 2: Get credentials.json from Google Cloud Console
# (Follow GOOGLE-SHEETS-SETUP.md)

# Step 3: Test
python google_sheets_setup.py

# Step 4: Restart Flask
python app.py

# Done! Your data is now saving to Google Sheets!
```

---

## 📞 Need Help?

1. **Quick setup:** Read `GOOGLE-SHEETS-QUICK-START.md`
2. **Detailed guide:** Read `GOOGLE-SHEETS-SETUP.md`
3. **Troubleshooting:** Check the troubleshooting section in setup guide

---

**Created:** February 19, 2026
**Project:** KrishiShakti (कृषि शक्ति)

**Your Google Sheet will be at:**
`https://docs.google.com/spreadsheets/d/[YOUR-SHEET-ID]`
(You'll get this URL after running the setup script)

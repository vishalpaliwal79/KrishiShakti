# 🚀 Google Sheets Quick Start (5 Minutes)

## What is Google Sheets Integration?

Your sensor data will automatically save to Google Sheets in the cloud, so you can:
- ✅ View data from anywhere (phone, tablet, computer)
- ✅ Create beautiful charts and graphs
- ✅ Share with team members
- ✅ Never lose data (cloud backup)
- ✅ Export to Excel anytime

---

## 🎯 Quick Setup (5 Steps)

### Step 1: Install Libraries (1 minute)

```bash
./install_google_sheets.sh
```

OR manually:

```bash
pip install gspread google-auth
```

---

### Step 2: Get Google Credentials (2 minutes)

1. **Go to:** https://console.cloud.google.com/
2. **Create project:** Click "New Project" → Name it "KrishiShakti"
3. **Enable APIs:**
   - Search "Google Sheets API" → Enable
   - Search "Google Drive API" → Enable
4. **Create Service Account:**
   - Go to "IAM & Admin" → "Service Accounts"
   - Click "Create Service Account"
   - Name: `krishishakti-bot`
   - Role: Editor
   - Click "Done"
5. **Download Key:**
   - Click on the service account
   - Go to "Keys" tab
   - "Add Key" → "Create new key" → JSON
   - Save as `credentials.json` in your project folder

---

### Step 3: Test Connection (30 seconds)

```bash
python google_sheets_setup.py
```

**You'll see:**
```
✅ Successfully connected to Google Sheets!
📊 Spreadsheet URL: https://docs.google.com/spreadsheets/d/xxxxx
```

**Copy this URL!** This is your Google Sheet.

---

### Step 4: Restart Flask (10 seconds)

Stop Flask (Ctrl+C) and restart:

```bash
python app.py
```

**You should see:**
```
✅ Google Sheets connected!
📊 Spreadsheet: https://docs.google.com/spreadsheets/d/xxxxx
```

---

### Step 5: View Your Data (30 seconds)

1. Open the spreadsheet URL from Step 3
2. You'll see two sheets:
   - **Sensor Data** - All readings
   - **Dashboard** - Summary

**Data updates automatically every 2 seconds!**

---

## 📊 What Your Google Sheet Looks Like

### Sensor Data Sheet:

```
┌──────────────────────┬────────────┬──────────┬─────────────┬──────┬──────────┬─────────┐
│ Timestamp            │ Date       │ Time     │ Air Quality │ Temp │ Humidity │ Status  │
├──────────────────────┼────────────┼──────────┼─────────────┼──────┼──────────┼─────────┤
│ 2026-02-19T20:30:45  │ 2026-02-19 │ 20:30:45 │ 125.43      │ 27.8 │ 65.2     │ Good    │
│ 2026-02-19T20:30:47  │ 2026-02-19 │ 20:30:47 │ 132.15      │ 27.9 │ 64.8     │ Good    │
│ 2026-02-19T20:30:49  │ 2026-02-19 │ 20:30:49 │ 128.67      │ 25.3 │ 65.5     │ Warning │
└──────────────────────┴────────────┴──────────┴─────────────┴──────┴──────────┴─────────┘
```

**15 columns total:**
- Timestamp, Date, Time
- Air Quality, Temperature, Humidity
- PM2.5, PM10, Soil Moisture, Water Quality
- City, Country, Latitude, Longitude
- Status (Good/Warning/Critical)

---

## 🎨 Create Charts (Optional)

### Temperature Over Time:

1. Select columns B (Date) and E (Temperature)
2. Insert → Chart
3. Choose "Line chart"
4. Done!

### All Sensors Dashboard:

1. Select columns B, E, F, I (Date, Temp, Humidity, Moisture)
2. Insert → Chart
3. Choose "Combo chart"
4. Customize colors

---

## 🔍 Troubleshooting

### "credentials.json not found"
→ Make sure the file is in the same folder as app.py

### "Permission denied"
→ Share the Google Sheet with the service account email (found in credentials.json)

### "Module not found"
→ Run: `pip install gspread google-auth`

### Data not appearing
→ Make sure simulator is running: `python simulator.py`

---

## 📱 Access from Phone

1. Install Google Sheets app on your phone
2. Open the spreadsheet URL
3. View real-time data anywhere!

---

## 🎯 Summary

**What you did:**
1. Installed libraries
2. Created Google Cloud project
3. Downloaded credentials
4. Tested connection
5. Restarted Flask

**What you get:**
- ✅ Automatic cloud backup
- ✅ Real-time data logging
- ✅ Beautiful charts
- ✅ Access from anywhere
- ✅ Share with team

**Your Google Sheet URL:**
(Copy from terminal after running `python google_sheets_setup.py`)

---

## 📞 Need Help?

Read the detailed guide: `GOOGLE-SHEETS-SETUP.md`

---

**Created:** February 19, 2026
**Project:** KrishiShakti (कृषि शक्ति)

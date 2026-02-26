# 🚀 Setup Google Sheets NOW - Simple Steps

## Why You Can't See Google Sheets

**2 things are missing:**
1. ❌ Libraries not installed (`gspread`)
2. ❌ No `credentials.json` file

---

## ✅ Fix It Now (10 Minutes)

### STEP 1: Install Libraries (1 minute)

Copy and paste this command:

```bash
pip install gspread google-auth google-auth-oauthlib google-auth-httplib2
```

Wait for it to finish. You'll see:
```
Successfully installed gspread-5.12.0 google-auth-2.23.4 ...
```

---

### STEP 2: Get credentials.json (5 minutes)

#### A. Open Google Cloud Console

**Click this link:** https://console.cloud.google.com/

Sign in with your Google account.

#### B. Create Project

1. Click project dropdown (top left)
2. Click "NEW PROJECT"
3. Name: `KrishiShakti`
4. Click "CREATE"

#### C. Enable APIs

**First API:**
1. Click this link: https://console.cloud.google.com/apis/library/sheets.googleapis.com
2. Select "KrishiShakti" project
3. Click "ENABLE"

**Second API:**
1. Click this link: https://console.cloud.google.com/apis/library/drive.googleapis.com
2. Click "ENABLE"

#### D. Create Service Account

1. Click this link: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "CREATE SERVICE ACCOUNT"
3. Name: `krishishakti-bot`
4. Click "CREATE AND CONTINUE"
5. Role: Choose "Editor"
6. Click "CONTINUE"
7. Click "DONE"

#### E. Download Key

1. Click on the service account you just created
2. Click "KEYS" tab
3. Click "ADD KEY" → "Create new key"
4. Choose "JSON"
5. Click "CREATE"
6. File downloads automatically

#### F. Move File

1. Find the downloaded file (in Downloads folder)
2. Rename it to: `credentials.json`
3. Move it to your project folder (same folder as app.py)

---

### STEP 3: Test Connection (1 minute)

Run this command:

```bash
python google_sheets_setup.py
```

**You should see:**
```
╔════════════════════════════════════════════════════════╗
║  KrishiShakti Google Sheets Integration Test         ║
╚════════════════════════════════════════════════════════╝

✓ Connected to existing spreadsheet: KrishiShakti Sensor Data
✓ Created 'Sensor Data' worksheet with headers

📝 Adding sample data...
✓ Added data to Google Sheets (Row 2)
✓ Sample data added successfully!

============================================================
✅ Setup Complete!
============================================================

📊 Open your spreadsheet: https://docs.google.com/spreadsheets/d/xxxxx
```

**COPY THAT URL!** That's your Google Sheet!

---

### STEP 4: Restart Flask (30 seconds)

Stop Flask (press Ctrl+C) and restart:

```bash
python app.py
```

**You should see:**
```
✅ Google Sheets connected!
📊 Spreadsheet: https://docs.google.com/spreadsheets/d/xxxxx
 * Running on http://127.0.0.1:5001
```

---

### STEP 5: Open Your Google Sheet (10 seconds)

1. Copy the URL from Step 3 or Step 4
2. Paste it in your browser
3. Press Enter

**You'll see:**
- Sheet 1: "Sensor Data" with all your readings
- Sheet 2: "Dashboard" with summary

**Data updates automatically every 2 seconds!**

---

## 📊 What You'll See

### Sensor Data Sheet:

```
Row 1: Headers
Timestamp | Date | Time | Air Quality | Temperature | Humidity | ...

Row 2: Data (updates every 2 seconds)
2026-02-19T20:30:45 | 2026-02-19 | 20:30:45 | 125.43 | 27.8 | 65.2 | ...

Row 3: Data
2026-02-19T20:30:47 | 2026-02-19 | 20:30:47 | 132.15 | 27.9 | 64.8 | ...
```

### Dashboard Sheet:

```
KrishiShakti Sensor Dashboard

Latest Readings:
Temperature: 27.8°C - Normal
Humidity: 65.2% - Normal
Soil Moisture: 25.3% - Low
Air Quality: 125 ppm - Good
Water Quality: 287 ppm - Good
```

---

## 🎯 Summary

**Why you can't see it:**
- Libraries not installed
- No credentials.json file
- Google Sheet not created yet

**How to fix:**
1. Install libraries: `pip install gspread google-auth`
2. Get credentials.json from Google Cloud Console
3. Run: `python google_sheets_setup.py`
4. Open the URL shown

**Time needed:** 10 minutes

**Result:** Real-time sensor data in Google Sheets, accessible from anywhere!

---

## 🆘 Still Having Issues?

### Error: "credentials.json not found"
→ Make sure file is in same folder as app.py
→ Check filename is exactly `credentials.json`

### Error: "Permission denied"
→ Open credentials.json
→ Copy the `client_email` value
→ Go to Google Sheet → Share → Add that email

### Error: "Module not found"
→ Run: `pip install gspread google-auth`

### Can't find downloaded file
→ Check Downloads folder
→ Look for file like `krishishakti-xxxxx.json`

---

## 📱 After Setup

**Access from anywhere:**
- Computer: Open the URL
- Phone: Install Google Sheets app → Open URL
- Tablet: Same as phone

**Share with others:**
- Click "Share" button in Google Sheets
- Add their email
- They can view/edit

**Create charts:**
- Select data columns
- Insert → Chart
- Choose chart type

---

**Start now! Follow Step 1 above.** 🚀

# ❌ Why You Can't See Google Sheets

## The Problem

**You're missing the `credentials.json` file!**

Without this file, the system cannot connect to Google Sheets.

---

## ✅ Solution: Get credentials.json (3 Minutes)

### Step 1: Go to Google Cloud Console

**Open this link:** https://console.cloud.google.com/

### Step 2: Create a Project

1. Click the project dropdown (top left, next to "Google Cloud")
2. Click "NEW PROJECT"
3. Project name: `KrishiShakti`
4. Click "CREATE"
5. Wait 30 seconds for it to be created

### Step 3: Enable APIs

**Enable Google Sheets API:**
1. Go to: https://console.cloud.google.com/apis/library/sheets.googleapis.com
2. Make sure "KrishiShakti" project is selected (top left)
3. Click "ENABLE"
4. Wait for it to enable

**Enable Google Drive API:**
1. Go to: https://console.cloud.google.com/apis/library/drive.googleapis.com
2. Click "ENABLE"
3. Wait for it to enable

### Step 4: Create Service Account

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Make sure "KrishiShakti" project is selected
3. Click "CREATE SERVICE ACCOUNT"
4. Service account name: `krishishakti-bot`
5. Click "CREATE AND CONTINUE"
6. Role: Select "Editor" from the dropdown
7. Click "CONTINUE"
8. Click "DONE"

### Step 5: Download credentials.json

1. You'll see your service account in the list
2. Click on it (the email address)
3. Go to the "KEYS" tab
4. Click "ADD KEY" → "Create new key"
5. Choose "JSON"
6. Click "CREATE"
7. A file will download (like `krishishakti-xxxxx.json`)

### Step 6: Rename and Move File

1. Find the downloaded file (probably in Downloads folder)
2. Rename it to exactly: `credentials.json`
3. Move it to your project folder (where app.py is)

---

## 🧪 Test the Setup

Run this command:

```bash
python google_sheets_setup.py
```

**If successful, you'll see:**
```
✅ Successfully connected to Google Sheets!
📊 Spreadsheet URL: https://docs.google.com/spreadsheets/d/xxxxx
```

**Copy that URL and open it in your browser!**

---

## 🔍 Troubleshooting

### "credentials.json not found"
→ Make sure the file is in the same folder as app.py
→ Check the filename is exactly `credentials.json` (not `credentials (1).json`)

### "Permission denied"
→ After creating the sheet, you need to share it with the service account
→ Open credentials.json and copy the `client_email`
→ Go to your Google Sheet → Share → Add that email with Editor access

### "API not enabled"
→ Go back to Step 3 and enable both APIs
→ Wait 1-2 minutes for changes to take effect

### "Module not found: gspread"
→ Run: `pip install gspread google-auth`

---

## 📊 What Happens After Setup?

1. **Google Sheet is created** automatically
2. **Data starts flowing** from simulator → Flask → Google Sheets
3. **New row added every 2 seconds** with sensor data
4. **You can access it** from the URL or Google Drive

---

## 🎯 Quick Checklist

- [ ] Go to https://console.cloud.google.com/
- [ ] Create project "KrishiShakti"
- [ ] Enable Google Sheets API
- [ ] Enable Google Drive API
- [ ] Create service account "krishishakti-bot"
- [ ] Download JSON key
- [ ] Rename to `credentials.json`
- [ ] Move to project folder
- [ ] Run `python google_sheets_setup.py`
- [ ] Copy the spreadsheet URL
- [ ] Open URL in browser
- [ ] See your data!

---

## 💡 Alternative: Use Local Storage Only

If you don't want to set up Google Sheets right now, your data is already being saved locally:

**File:** `data/history.json`

You can:
- Open this file to see all data
- Import it into Excel
- Use it for analysis

**But Google Sheets is better because:**
- ✅ Cloud backup
- ✅ Access from anywhere
- ✅ Beautiful charts
- ✅ Share with others
- ✅ Real-time updates

---

## 🚀 After You Get credentials.json

1. **Test connection:**
   ```bash
   python google_sheets_setup.py
   ```

2. **Restart Flask:**
   ```bash
   python app.py
   ```

3. **Check Flask output:**
   ```
   ✅ Google Sheets connected!
   📊 Spreadsheet: https://docs.google.com/spreadsheets/d/xxxxx
   ```

4. **Open that URL** - You'll see your data!

---

**The reason you can't see Google Sheets is because you haven't created the credentials.json file yet. Follow the steps above to get it!**

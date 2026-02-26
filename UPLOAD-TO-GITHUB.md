# 📤 Upload KrishiShakti to GitHub - Step by Step

## 🎯 Prerequisites

1. **GitHub Account**: Create one at https://github.com/signup if you don't have one
2. **Git Installed**: Check by running `git --version` in terminal

If Git is not installed:
- **Mac**: `brew install git` or download from https://git-scm.com/
- **Windows**: Download from https://git-scm.com/

---

## 📋 Step-by-Step Instructions

### Step 1: Create GitHub Repository

1. Go to https://github.com/
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in details:
   - **Repository name**: `krishishakti`
   - **Description**: `Smart Agriculture & IoT Monitoring System`
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** check "Initialize with README" (we already have one)
4. Click **"Create repository"**

### Step 2: Prepare Your Project

Open terminal in your project folder and run:

```bash
# Check if you're in the right folder
pwd
# Should show: /Users/amankaushik/Documents/All kiro/AIR CONVERTER PROJECT

# Initialize Git (if not already done)
git init

# Check Git status
git status
```

### Step 3: Configure Git (First Time Only)

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your-email@example.com"

# Verify
git config --global --list
```

### Step 4: Add Files to Git

```bash
# Add all files
git add .

# Check what will be committed
git status

# You should see files in green (ready to commit)
```

### Step 5: Create First Commit

```bash
# Commit with a message
git commit -m "Initial commit: KrishiShakti Smart Agriculture System"
```

### Step 6: Connect to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/krishishakti.git

# Verify remote
git remote -v
```

### Step 7: Push to GitHub

```bash
# Push to GitHub (first time)
git push -u origin main

# If it asks for branch name, try:
git branch -M main
git push -u origin main
```

**If it asks for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your password)

---

## 🔑 Creating Personal Access Token (If Needed)

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `KrishiShakti Upload`
4. Select scopes: Check **"repo"** (full control)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as password when pushing

---

## ✅ Verify Upload

1. Go to your GitHub repository: `https://github.com/YOUR_USERNAME/krishishakti`
2. You should see all your files!
3. The README will be displayed automatically

---

## 🔄 Future Updates

When you make changes and want to update GitHub:

```bash
# Check what changed
git status

# Add changed files
git add .

# Commit changes
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

---

## 📝 Quick Commands Reference

```bash
# Check status
git status

# Add all files
git add .

# Add specific file
git add filename.py

# Commit
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log

# Create new branch
git checkout -b feature-name

# Switch branch
git checkout main
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "fatal: not a git repository"
**Solution:**
```bash
git init
```

### Issue 2: "remote origin already exists"
**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/krishishakti.git
```

### Issue 3: "failed to push some refs"
**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

### Issue 4: "Permission denied"
**Solution:** Use Personal Access Token instead of password

### Issue 5: Large files error
**Solution:** Add to .gitignore:
```bash
echo "large-file.zip" >> .gitignore
git add .gitignore
git commit -m "Update gitignore"
```

---

## 🔒 Important: Protect Sensitive Files

**Already protected in .gitignore:**
- ✅ `credentials.json` (Google Sheets credentials)
- ✅ `*.log` files
- ✅ `venv/` folder
- ✅ `__pycache__/`

**Never commit:**
- API keys
- Passwords
- Personal credentials
- Large data files (>100MB)

---

## 📊 What Gets Uploaded

**Included:**
- ✅ All Python files (`.py`)
- ✅ HTML/CSS/JS files
- ✅ Documentation (`.md` files)
- ✅ Requirements file
- ✅ Arduino code
- ✅ Shell scripts

**Excluded (by .gitignore):**
- ❌ Virtual environment (`venv/`)
- ❌ Log files (`*.log`)
- ❌ Credentials (`credentials.json`)
- ❌ Cache files (`__pycache__/`)
- ❌ IDE settings (`.vscode/`)

---

## 🎉 After Upload

### Update README
1. Edit `README-GITHUB.md`
2. Replace `YOUR_USERNAME` with your actual GitHub username
3. Add screenshots (optional)
4. Rename to `README.md`:
```bash
mv README-GITHUB.md README.md
git add README.md
git commit -m "Update README"
git push
```

### Add Topics/Tags
On GitHub repository page:
1. Click ⚙️ (Settings icon) next to "About"
2. Add topics: `iot`, `agriculture`, `python`, `flask`, `sensors`, `smart-farming`
3. Save

### Add License
1. On GitHub, click "Add file" → "Create new file"
2. Name it `LICENSE`
3. Click "Choose a license template"
4. Select "MIT License"
5. Commit

---

## 🌟 Make it Look Professional

### Add Badges
Edit README.md and add at the top:
```markdown
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Stars](https://img.shields.io/github/stars/YOUR_USERNAME/krishishakti)](https://github.com/YOUR_USERNAME/krishishakti/stargazers)
```

### Add Screenshots
1. Take screenshots of your dashboard
2. Upload to GitHub: Create `screenshots/` folder
3. Reference in README:
```markdown
![Dashboard](screenshots/dashboard.png)
```

---

## 📞 Need Help?

If you encounter issues:
1. Check the error message carefully
2. Google the error message
3. Ask on GitHub Discussions
4. Check Git documentation: https://git-scm.com/doc

---

## ✅ Checklist

Before uploading, make sure:
- [ ] `.gitignore` file exists
- [ ] No sensitive data (credentials, API keys)
- [ ] README.md is complete
- [ ] requirements.txt is up to date
- [ ] Code is tested and working
- [ ] Documentation is clear
- [ ] License file added (optional)

---

## 🎯 Quick Upload Script

Save this as `upload.sh`:

```bash
#!/bin/bash

echo "🚀 Uploading KrishiShakti to GitHub..."

# Add all files
git add .

# Commit
echo "📝 Enter commit message:"
read message
git commit -m "$message"

# Push
git push

echo "✅ Upload complete!"
echo "🌐 View at: https://github.com/YOUR_USERNAME/krishishakti"
```

Make it executable:
```bash
chmod +x upload.sh
```

Use it:
```bash
./upload.sh
```

---

**Good luck with your upload! 🎉**

**Your project will be at:**
`https://github.com/YOUR_USERNAME/krishishakti`

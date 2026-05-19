# QUICK DEPLOYMENT GUIDE
## Deploy Questionnaire Website to Pantheon

---

## 🚀 **3-STEP DEPLOYMENT**

### **Step 1: Prepare Files** (5 minutes)

1. **Locate your files:**
   ```
   c:/Users/sidra/.gemini/antigravity/playground/fusion-feynman/questionnaire-website/
   ```

2. **Files you have:**
   - ✅ `index.html` - Main questionnaire
   - ✅ `styles.css` - Styling
   - ✅ `script.js` - Functionality
   - ✅ `submit.php` - Data collection
   - ✅ `README.md` - Documentation

3. **Update contact info in `index.html`:**
   - Replace `[Your Name]` with your actual name
   - Replace `[Your Email]` with your email
   - Replace `[Supervisor Name]` with supervisor's name
   - Replace `[Supervisor Email]` with supervisor's email

4. **Update email in `submit.php`:**
   - Line 134: Replace `[your-email@example.com]` with your email

---

### **Step 2: Upload to Pantheon** (10 minutes)

#### **Option A: SFTP Upload (Easiest)**

1. **Get SFTP credentials from Pantheon:**
   - Log in to Pantheon dashboard
   - Select your site
   - Go to "Connection Info"
   - Copy SFTP command

2. **Connect via SFTP:**
   ```bash
   # Use the SFTP command from Pantheon
   sftp -P 2222 dev.{site-id}@appserver.dev.{site-id}.drush.in
   ```

3. **Upload files:**
   ```bash
   # Navigate to web directory
   cd code

   # Upload all files
   put index.html
   put styles.css
   put script.js
   put submit.php
   put README.md

   # Create data directory
   mkdir data
   chmod 755 data
   ```

4. **Done!** Your site is live at: `https://dev-{site-name}.pantheonsite.io`

#### **Option B: Git Deployment**

1. **Initialize Git:**
   ```bash
   cd questionnaire-website
   git init
   ```

2. **Add Pantheon remote:**
   ```bash
   git remote add pantheon ssh://codeserver.dev.{site-id}@codeserver.dev.{site-id}.drush.in:2222/~/repository.git
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Deploy questionnaire website"
   git push pantheon master
   ```

#### **Option C: File Manager (If available)**

1. Log in to Pantheon
2. Go to "Files" or "File Manager"
3. Upload all files from `questionnaire-website` folder
4. Done!

---

### **Step 3: Test & Launch** (5 minutes)

1. **Visit your site:**
   ```
   https://dev-{site-name}.pantheonsite.io
   ```

2. **Test checklist:**
   - [ ] Page loads correctly
   - [ ] Timer starts when you click "I Agree"
   - [ ] Progress bar updates
   - [ ] All questions display
   - [ ] Images load (or placeholders show)
   - [ ] Can complete full survey
   - [ ] Thank you page shows completion time
   - [ ] Data saves (check `data/` folder)

3. **Check data collection:**
   ```bash
   # Via SFTP
   sftp -P 2222 dev.{site-id}@appserver.dev.{site-id}.drush.in
   cd code/data
   ls -la
   # You should see response_*.json files
   ```

4. **Enable HTTPS:**
   - In Pantheon dashboard
   - Go to "Domains/HTTPS"
   - Enable "HTTPS" for your domain

5. **Launch!**
   - Share the URL with participants
   - Monitor responses in `data/` folder

---

## 📊 **ACCESSING YOUR DATA**

### **Method 1: Download via SFTP**

```bash
# Connect
sftp -P 2222 dev.{site-id}@appserver.dev.{site-id}.drush.in

# Download all responses
cd code/data
get response_*.json
get responses.csv

# Exit
exit
```

### **Method 2: Download via Pantheon Dashboard**

1. Log in to Pantheon
2. Go to "Files" or "Backups"
3. Download the `data/` folder
4. Extract and analyze

### **Method 3: View in Browser**

Create `view-data.php`:

```php
<?php
// Simple data viewer (password protect this!)
$password = 'your-secure-password';

if (!isset($_GET['pass']) || $_GET['pass'] !== $password) {
    die('Access denied');
}

$data_dir = __DIR__ . '/data';
$files = glob($data_dir . '/response_*.json');

echo "<h1>Questionnaire Responses (" . count($files) . ")</h1>";
echo "<a href='data/responses.csv'>Download CSV</a><br><br>";

foreach ($files as $file) {
    $data = json_decode(file_get_contents($file), true);
    echo "<h3>" . basename($file) . "</h3>";
    echo "<pre>" . json_encode($data, JSON_PRETTY_PRINT) . "</pre>";
    echo "<hr>";
}
?>
```

Access: `https://your-site.com/view-data.php?pass=your-secure-password`

---

## 🔧 **TROUBLESHOOTING**

### **Problem: Data not saving**

**Solution:**
```bash
# Check data directory permissions
cd code
mkdir data
chmod 755 data
```

### **Problem: 404 Error**

**Solution:**
- Verify files are in the correct directory
- Check Pantheon dashboard for deployment status
- Clear Pantheon cache

### **Problem: Images not loading**

**Solution:**
- Images auto-generate as placeholders (already implemented)
- Or upload real images to `images/` folder

### **Problem: PHP errors**

**Solution:**
```bash
# Check PHP error log
tail -f /srv/bindings/.../logs/php-error.log
```

---

## 📧 **EMAIL NOTIFICATIONS**

To receive email when someone completes the survey:

1. **Edit `submit.php` line 145:**
   ```php
   mail($to, $subject, $message, $headers);
   ```
   Uncomment this line (remove `//`)

2. **Update email address line 134:**
   ```php
   $to = 'your-email@example.com';
   ```

3. **Test:**
   - Complete a test survey
   - Check your email

---

## 📊 **ANALYZING DATA**

### **CSV Analysis (Excel/Google Sheets)**

1. Download `data/responses.csv`
2. Open in Excel or Google Sheets
3. Each row = one participant
4. Columns = questions + metadata

### **JSON Analysis (Python/R)**

**Python example:**

```python
import json
import pandas as pd
from glob import glob

# Load all responses
responses = []
for file in glob('data/response_*.json'):
    with open(file) as f:
        responses.append(json.load(f))

# Convert to DataFrame
df = pd.json_normalize(responses)

# Analyze
print(f"Total responses: {len(df)}")
print(f"Average completion time: {df['metadata.totalTime'].mean()} seconds")
print(f"\nAge distribution:")
print(df['responses.age'].value_counts())
```

**R example:**

```r
library(jsonlite)
library(dplyr)

# Load all responses
files <- list.files("data", pattern = "response_.*\\.json", full.names = TRUE)
responses <- lapply(files, fromJSON)

# Convert to data frame
df <- bind_rows(responses)

# Analyze
summary(df)
```

---

## 🔒 **SECURITY CHECKLIST**

Before launching:

- [ ] Enable HTTPS
- [ ] Password protect `view-data.php` (if using)
- [ ] Restrict access to `data/` folder
- [ ] Don't expose participant emails
- [ ] Regular backups
- [ ] Monitor for spam submissions

**Add `.htaccess` to protect data folder:**

```apache
# In data/.htaccess
Order deny,allow
Deny from all
```

---

## 📈 **MONITORING RESPONSES**

### **Check response count:**

```bash
# Via SFTP
cd code/data
ls -1 response_*.json | wc -l
```

### **View latest response:**

```bash
cd code/data
tail -1 responses.csv
```

### **Monitor in real-time:**

Create `stats.php`:

```php
<?php
$data_dir = __DIR__ . '/data';
$files = glob($data_dir . '/response_*.json');

echo json_encode([
    'total_responses' => count($files),
    'latest_response' => max(array_map('filemtime', $files)),
    'today' => count(array_filter($files, function($f) {
        return date('Y-m-d', filemtime($f)) === date('Y-m-d');
    }))
]);
?>
```

Access: `https://your-site.com/stats.php`

---

## 🎯 **RECRUITMENT**

Share your questionnaire:

**Direct Link:**
```
https://your-site.pantheonsite.io
```

**QR Code:**
Generate at: https://www.qr-code-generator.com/

**Social Media Post Template:**
```
🎓 Research Participants Needed!

I'm conducting research on AI and online shopping for my 
PGD in Data Science at NED University.

⏱️ Time: 28-30 minutes
🎁 Incentive: Prize draw (₨1,000 × 3 winners)
🔒 Anonymous & confidential

Help advance AI research! 👇
[Your Link]

#Research #AI #NEDUniversity #DataScience
```

**Email Template:**
```
Subject: Research Participation Request - AI & Shopping Study

Dear [Name],

I am conducting research for my Postgraduate Diploma in Data Science 
at NED University. I would greatly appreciate your participation in 
my online questionnaire about AI and shopping decisions.

Time Required: 28-30 minutes
Incentive: Entry into prize draw (₨1,000 × 3 winners)
Privacy: Completely anonymous

Link: [Your Link]

Thank you for supporting my research!

Best regards,
[Your Name]
```

---

## ✅ **FINAL CHECKLIST**

Before sharing with participants:

- [ ] All contact info updated
- [ ] Data collection tested
- [ ] HTTPS enabled
- [ ] Mobile tested
- [ ] Desktop tested
- [ ] Timer working
- [ ] Progress bar working
- [ ] All 66 questions display
- [ ] Thank you page works
- [ ] Data saves correctly
- [ ] CSV exports correctly
- [ ] Email notifications working (optional)
- [ ] Backup system in place
- [ ] IRB approval obtained

---

## 🆘 **NEED HELP?**

### **Pantheon Support:**
- Documentation: https://pantheon.io/docs
- Support: https://pantheon.io/support

### **Technical Issues:**
- Check browser console (F12)
- Check PHP error logs
- Review README.md

### **Research Questions:**
- Contact: [Your Name]
- Email: [Your Email]

---

## 🎉 **YOU'RE READY!**

Your questionnaire website is now:
✅ Deployed to Pantheon
✅ Collecting data
✅ Tracking time
✅ Randomizing conditions
✅ Saving responses
✅ Ready for participants

**Next steps:**
1. Test thoroughly
2. Get IRB approval (if not already)
3. Start recruitment
4. Monitor responses
5. Analyze data

**Good luck with your research!** 🚀

---

**Estimated Timeline:**
- Setup: 20 minutes
- Testing: 30 minutes
- Recruitment: 4-6 weeks
- Data collection: 6-8 weeks
- Analysis: 2-3 weeks

**Target:** 200-300 participants
**Current:** 0 responses

**Start recruiting today!** 📊

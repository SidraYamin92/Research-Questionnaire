# 🚀 DEPLOY YOUR QUESTIONNAIRE - SIMPLE GUIDE
## Netlify + Google Forms (100% Free, Unlimited Responses)

**Time Required:** 15 minutes  
**Cost:** FREE  
**Responses:** Unlimited

---

## ✅ **STEP 1: Deploy to Netlify (5 minutes)**

### **1.1 Create Account**
1. Go to: https://app.netlify.com/signup
2. Sign up with email or GitHub
3. Verify your email

### **1.2 Deploy Your Site**
1. Go to: https://app.netlify.com
2. Click: **"Add new site"** → **"Deploy manually"**
3. **Drag and drop** your `questionnaire-website` folder
4. Wait 30 seconds
5. **Done!** Copy your URL (e.g., `https://random-name.netlify.app`)

### **1.3 Customize URL (Optional)**
1. Click on your site
2. **Site settings** → **Domain management**
3. **Change site name** → Enter: `sidra-ai-research`
4. New URL: `https://sidra-ai-research.netlify.app`

---

## ✅ **STEP 2: Set Up Google Forms (5 minutes)**

### **2.1 Create Form**
1. Go to: https://forms.google.com
2. Click: **+ Blank form**
3. Title: "AI Research Questionnaire Data"

### **2.2 Add Question**
1. Click: **"Untitled Question"**
2. Change to: **"Paragraph"** (long answer)
3. Question text: "Response Data"
4. Toggle: **Required** ON

### **2.3 Get Form URL**
1. Click: **Send** button (top right)
2. Click: **Link icon** (🔗)
3. **Copy the link**
4. Save it somewhere (you'll need it)

### **2.4 Create Response Sheet**
1. Click: **Responses** tab
2. Click: **Green Sheets icon** (📊)
3. Click: **Create**
4. A Google Sheet opens - this will store all responses!

### **2.5 Get Entry ID**
1. Open your form link in a new tab
2. Right-click → **View Page Source**
3. Press `Ctrl+F` and search for: `entry.`
4. Find something like: `entry.1234567890`
5. Copy the number (e.g., `1234567890`)

---

## ✅ **STEP 3: Connect Form to Website (5 minutes)**

### **3.1 Update script.js**

Open `questionnaire-website/script.js` and find the `sendDataToServer` function (around line 208).

Replace it with:

```javascript
function sendDataToServer(data) {
    // Google Form submission
    const FORM_URL = 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse';
    const ENTRY_ID = 'entry.YOUR_ENTRY_ID'; // Replace with your entry ID
    
    const formData = new FormData();
    formData.append(ENTRY_ID, JSON.stringify(data, null, 2));
    
    fetch(FORM_URL, {
        method: 'POST',
        mode: 'no-cors',
        body: formData
    }).then(() => {
        console.log('✅ Data submitted successfully');
    }).catch(error => {
        console.error('❌ Submission error:', error);
        // Backup to localStorage
        localStorage.setItem('questionnaire_backup_' + Date.now(), JSON.stringify(data));
    });
}
```

### **3.2 Replace Placeholders**

In the code above, replace:
- `YOUR_FORM_ID` with your form ID from the URL
- `YOUR_ENTRY_ID` with the entry number you found

**Example:**
If your form URL is:
```
https://docs.google.com/forms/d/e/1FAIpQLSdXXXXXXXXXXXXXXXXXXXXXXXXX/viewform
```

And your entry ID is `entry.987654321`, then:

```javascript
const FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSdXXXXXXXXXXXXXXXXXXXXXXXXX/formResponse';
const ENTRY_ID = 'entry.987654321';
```

---

## ✅ **STEP 4: Redeploy to Netlify**

### **4.1 Update Your Site**
1. Go to: https://app.netlify.com
2. Click on your site
3. Scroll down to: **"Deploys"**
4. **Drag and drop** your updated `questionnaire-website` folder
5. Wait 30 seconds
6. **Done!**

---

## ✅ **STEP 5: Test Everything**

### **5.1 Test the Questionnaire**
1. Open your Netlify URL
2. Complete the questionnaire
3. Submit

### **5.2 Check Google Sheets**
1. Open your Google Sheet
2. You should see a new row with:
   - Timestamp
   - JSON data with all responses

### **5.3 Verify Data**
The data should look like:
```json
{
  "responses": {
    "participant-name": "Test User",
    "participant-email": "test@example.com",
    "age": "25-34",
    ...
  },
  "metadata": {
    "totalTime": 1425,
    "deviceType": "desktop",
    ...
  }
}
```

---

## 📊 **VIEWING YOUR DATA**

### **In Google Sheets:**
1. Each row = 1 participant
2. Column A = Timestamp
3. Column B = All response data (JSON)

### **To Analyze:**
1. Download the sheet as CSV
2. Use Python/R to parse JSON
3. Or use this Python script:

```python
import pandas as pd
import json

# Read CSV
df = pd.read_csv('responses.csv')

# Parse JSON column
data = []
for idx, row in df.iterrows():
    json_data = json.loads(row['Response Data'])
    data.append(json_data)

# Convert to DataFrame
responses_df = pd.json_normalize(data)
print(responses_df.head())
```

---

## 🎯 **YOUR FINAL URLS**

After setup, you'll have:

1. **Questionnaire URL:** `https://sidra-ai-research.netlify.app`
   - Share this with participants

2. **Google Sheet:** `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID`
   - View all responses here

3. **Google Form:** `https://forms.google.com/YOUR_FORM_ID`
   - Don't share this (it's just for data collection)

---

## ✅ **CHECKLIST**

Before sharing with participants:

- [ ] Deployed to Netlify
- [ ] Custom URL set (optional)
- [ ] Google Form created
- [ ] Google Sheet connected
- [ ] Entry ID found
- [ ] script.js updated
- [ ] Redeployed to Netlify
- [ ] Tested with dummy submission
- [ ] Data appears in Google Sheet
- [ ] All 62 questions working
- [ ] Images loading correctly
- [ ] Timer working
- [ ] Progress bar working

---

## 🆘 **TROUBLESHOOTING**

### **Problem: Data not appearing in Google Sheet**

**Solution:**
1. Check if form URL is correct
2. Check if entry ID is correct
3. Open browser console (F12) and look for errors
4. Try submitting the Google Form directly to test

### **Problem: Images not showing**

**Solution:**
1. Make sure images are in `images/` folder
2. Check image names: `product1.jpg`, `product2.jpg`, etc.
3. Redeploy to Netlify

### **Problem: Website not loading**

**Solution:**
1. Check Netlify deploy logs
2. Make sure `index.html` is in root folder
3. Clear browser cache (Ctrl+Shift+R)

---

## 📧 **NEED HELP?**

Contact: sidrashahid535@gmail.com

---

## 🎉 **YOU'RE DONE!**

Your questionnaire is now:
- ✅ Live on the internet
- ✅ Collecting data automatically
- ✅ Storing responses in Google Sheets
- ✅ Ready for 300+ participants
- ✅ 100% FREE

**Share your Netlify URL and start collecting data!**

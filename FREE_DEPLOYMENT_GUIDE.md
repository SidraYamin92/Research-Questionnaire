# 🚀 FREE DEPLOYMENT GUIDE
## Deploy Your Questionnaire Website with Data Collection

This guide shows you how to deploy your questionnaire website **for FREE** using **Netlify** + **Formspree** (or alternatives) to collect up to 300+ responses.

---

## 📋 QUICK OVERVIEW

| Component | Service | Cost | Limit |
|-----------|---------|------|-------|
| **Website Hosting** | Netlify | FREE | Unlimited |
| **Data Collection** | Formspree | FREE | 50/month |
| **Backup Option** | Google Forms | FREE | Unlimited |
| **Alternative** | Netlify Forms | FREE | 100/month |

**Recommended:** Netlify (hosting) + Google Sheets (data storage) = **100% FREE, unlimited responses**

---

## 🎯 OPTION 1: NETLIFY + GOOGLE SHEETS (RECOMMENDED)

This is the **best free option** for 300+ participants.

### Step 1: Prepare Your Files

Your questionnaire-website folder should contain:
```
questionnaire-website/
├── index.html
├── styles.css
├── script.js
├── submit.php (not needed for this option)
└── images/
    └── product1.jpg, product2.jpg, etc.
```

### Step 2: Create a Google Form for Data Collection

1. Go to [Google Forms](https://forms.google.com)
2. Create a new form with ONE question:
   - **Question:** "Survey Data"
   - **Type:** Long answer
3. Click **Send** → Get the form response URL
4. Go to **Responses** tab → Click the **Google Sheets** icon
5. This creates a spreadsheet to store all responses

### Step 3: Update script.js to Submit to Google

Replace the `submitData()` function in `script.js`:

```javascript
function submitData(data) {
    // Google Form submission URL
    const GOOGLE_FORM_URL = 'YOUR_GOOGLE_FORM_URL';
    
    // Store locally as backup
    localStorage.setItem('questionnaire_backup_' + Date.now(), JSON.stringify(data));
    
    // Create a hidden iframe for submission
    const formData = new FormData();
    formData.append('entry.XXXXXXXXX', JSON.stringify(data)); // Replace XXXXXXXXX with your entry ID
    
    fetch(GOOGLE_FORM_URL, {
        method: 'POST',
        mode: 'no-cors',
        body: formData
    }).then(() => {
        console.log('Data submitted successfully');
    }).catch(error => {
        console.error('Submission error:', error);
    });
}
```

### Step 4: Deploy to Netlify

#### Method A: Drag and Drop (Easiest)

1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub or email
3. Click **"Add new site"** → **"Deploy manually"**
4. **Drag your `questionnaire-website` folder** onto the drop zone
5. Wait 30 seconds - your site is LIVE! 🎉
6. Get your free URL: `https://your-site-name.netlify.app`

#### Method B: GitHub Integration

1. Create a GitHub repository
2. Upload your questionnaire-website files
3. Connect Netlify to your GitHub repo
4. Auto-deploys on every push!

### Step 5: Share Your Link

Your questionnaire is now live at:
```
https://your-questionnaire.netlify.app
```

Share this link with participants!

---

## 🎯 OPTION 2: NETLIFY FORMS (Simple, 100/month free)

Netlify has built-in form handling - no backend needed!

### Step 1: Add Netlify Form Attribute

Update your form in `index.html`:

```html
<form name="questionnaire" method="POST" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="bot-field">
    <!-- Your form fields here -->
</form>
```

### Step 2: Deploy to Netlify

1. Go to [app.netlify.com](https://app.netlify.com)
2. Drag and drop your folder
3. Done! Forms work automatically

### Step 3: View Submissions

1. Go to your Netlify dashboard
2. Click **Forms** tab
3. View and download all submissions!

**Limit:** 100 submissions/month (free tier)

---

## 🎯 OPTION 3: VERCEL + SUPABASE (Advanced, Unlimited)

For unlimited free data storage with a real database.

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create free account
3. Create new project
4. Create table: `questionnaire_responses`
5. Get your API URL and anon key

### Step 2: Update script.js

```javascript
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_KEY = 'your-anon-key';

async function submitData(data) {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/questionnaire_responses`, {
        method: 'POST',
        headers: {
            'apikey': SUPABASE_KEY,
            'Authorization': `Bearer ${SUPABASE_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.ok;
}
```

### Step 3: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Connect GitHub/upload files
3. Deploy automatically

---

## 📊 DATA COLLECTION COMPARISON

| Method | Free Limit | Difficulty | Best For |
|--------|-----------|------------|----------|
| **Google Sheets** | Unlimited | Easy | 300+ responses |
| **Netlify Forms** | 100/month | Easy | Small studies |
| **Formspree** | 50/month | Easy | Quick testing |
| **Supabase** | Unlimited | Medium | Real database |
| **Firebase** | Unlimited | Medium | Real-time data |

---

## 🖼️ ADDING PRODUCT IMAGES

### Option A: Use Free Stock Images

1. Go to [unsplash.com](https://unsplash.com) or [pexels.com](https://pexels.com)
2. Search for: "laptop backpack", "wireless earbuds", etc.
3. Download images
4. Rename to: `product1.jpg`, `product2.jpg`, etc.
5. Put in `images/` folder

### Option B: Use Placeholder Images

The website already has fallback placeholders if images are missing!

### Recommended Product Images:

| Scenario | Product | Search Term |
|----------|---------|-------------|
| 1 | Laptop Backpack | "laptop backpack product" |
| 2 | Wireless Earbuds | "wireless earbuds" |
| 3 | Phone Case | "phone case" |
| 4 | Smartwatch | "smartwatch fitness" |
| 5 | Running Shoes | "running shoes" |
| 6 | Power Bank | "power bank charger" |
| 7 | Android Tablet | "tablet android" |

---

## 🔧 STEP-BY-STEP: NETLIFY + GOOGLE SHEETS

This is the **COMPLETE RECOMMENDED SETUP**:

### 1. Create Google Form

1. Go to https://forms.google.com
2. Create form with title "Questionnaire Data Collection"
3. Add ONE question:
   - Question: "Response Data"
   - Type: Long answer text
4. Click Settings (gear icon) → Collect email addresses: OFF
5. Click Send → Copy the form link

### 2. Get Form Entry ID

1. Click on the form link you copied
2. Right-click → View Page Source
3. Search for "entry." (Ctrl+F)
4. Copy the number after "entry." (e.g., `entry.1234567890`)

### 3. Create Google Sheet

1. In Google Forms, click Responses tab
2. Click the green Sheets icon
3. A spreadsheet is created automatically
4. Rename it "Questionnaire Responses"

### 4. Update Your Website

In `script.js`, update the `completeSurvey` function:

```javascript
function completeSurvey() {
    // Collect all form data
    const formData = new FormData(document.querySelector('form') || document.body);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    // Add metadata
    data.timestamp = new Date().toISOString();
    data.completionTime = document.getElementById('timerText').textContent;
    
    // Submit to Google Form
    const GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse';
    const ENTRY_ID = 'entry.XXXXXXXXX'; // Your entry ID
    
    const submitData = new FormData();
    submitData.append(ENTRY_ID, JSON.stringify(data, null, 2));
    
    fetch(GOOGLE_FORM_URL, {
        method: 'POST',
        mode: 'no-cors',
        body: submitData
    });
    
    // Show thank you page
    showSection('section-thankyou');
    updateProgress(100);
}
```

### 5. Deploy to Netlify

1. Go to https://app.netlify.com
2. Sign up/Login
3. Click "Add new site" → "Deploy manually"
4. Drag your questionnaire-website folder
5. Wait for deployment (30 seconds)
6. Copy your new URL!

### 6. Test Your Setup

1. Visit your Netlify URL
2. Complete the questionnaire
3. Check your Google Sheet - data should appear!

---

## 📝 FINAL CHECKLIST

Before sharing with participants:

- [ ] Website deployed to Netlify
- [ ] Google Form/Sheet connected
- [ ] Test submission works
- [ ] Product images added (or fallbacks work)
- [ ] Contact email updated (sidrashahid535@gmail.com)
- [ ] Prize info correct (₨1,000 × 3 winners)
- [ ] All 62 questions working
- [ ] Timer and progress bar working
- [ ] Mobile view tested

---

## 🔗 YOUR SHAREABLE LINK

After deployment, share this with participants:

```
https://your-questionnaire.netlify.app
```

You can also use a custom domain or URL shortener like:
- [bit.ly](https://bit.ly)
- [tinyurl.com](https://tinyurl.com)

---

## 📧 CONTACT

Questions about this guide?
Contact: sidrashahid535@gmail.com

---

## 💡 TIPS FOR 300 RESPONSES

1. **Share on WhatsApp groups** - Higher response rate
2. **Share on LinkedIn** - Professional network
3. **Share in university groups** - Easy access
4. **Use QR code** - For in-person recruitment
5. **Follow up** - Remind after 3-5 days

---

## 🎉 YOU'RE DONE!

Your questionnaire website is now:
- ✅ Hosted for FREE on Netlify
- ✅ Collecting data via Google Sheets
- ✅ Accessible via a simple link
- ✅ Ready for 300+ participants
- ✅ Mobile-friendly
- ✅ No monthly costs!

**Good luck with your research!** 🎓

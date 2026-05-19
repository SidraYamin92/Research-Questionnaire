# Cognitive AI Research Questionnaire Website

Professional web-based questionnaire for collecting research data on cognitive AI and online shopping decisions.

## 🎯 Features

### ✅ Core Functionality
- **66 Questions** across 8 sections
- **Timer Tracking** - Monitors total time and time per section
- **Progress Bar** - Visual progress indicator
- **Randomization** - Scenario conditions randomized per participant
- **Validation** - Required field checking before proceeding
- **Data Collection** - Comprehensive response and metadata tracking
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Accessibility** - WCAG 2.1 compliant

### ✅ Research Features
- **7 Shopping Scenarios** with product images
- **Validated Scales**: Trust in Automation, REI-10, TAM, CRT
- **Cognitive Bias Testing**: Anchoring, Loss Aversion, Social Proof, Scarcity, Time Pressure, Information Overload, Confirmation Bias
- **Metadata Collection**: User agent, screen resolution, timestamps
- **Section Timing**: Track time spent on each section

### ✅ User Experience
- Beautiful gradient design
- Smooth animations and transitions
- Clear progress indication
- Mobile-friendly interface
- Print-friendly completion certificate

## 📁 File Structure

```
questionnaire-website/
├── index.html          # Main HTML file with all questions
├── styles.css          # Complete stylesheet
├── script.js           # JavaScript for functionality
├── README.md           # This file
├── images/             # Product images (auto-generated placeholders)
└── data/               # Data collection endpoint (to be implemented)
```

## 🚀 Deployment to Pantheon

### Option 1: Direct Upload (Easiest)

1. **Prepare Files**
   - Ensure all files are in the `questionnaire-website` folder
   - Zip the folder contents (not the folder itself)

2. **Upload to Pantheon**
   - Log in to your Pantheon dashboard
   - Create a new site or select existing site
   - Go to the "Code" tab
   - Upload the files via SFTP or Git

3. **Configure**
   - Set the document root to the questionnaire folder
   - Enable HTTPS (recommended for data security)

### Option 2: Git Deployment (Recommended)

```bash
# Initialize Git repository
cd questionnaire-website
git init

# Add Pantheon remote
git remote add pantheon ssh://codeserver.dev.{site-id}@codeserver.dev.{site-id}.drush.in:2222/~/repository.git

# Commit and push
git add .
git commit -m "Initial questionnaire deployment"
git push pantheon master
```

### Option 3: SFTP Upload

```bash
# Connect via SFTP
sftp -P 2222 dev.{site-id}@appserver.dev.{site-id}.drush.in

# Upload files
put -r questionnaire-website/* /code/
```

## 🔧 Configuration

### 1. Update Contact Information

Edit `index.html` and replace placeholders:
- `[Your Name]` → Your actual name
- `[Your Email]` → Your email address
- `[Supervisor Name]` → Supervisor's name
- `[Supervisor Email]` → Supervisor's email

### 2. Set Up Data Collection

You need to implement a backend endpoint to receive data. Options:

#### Option A: PHP Backend (Simple)

Create `submit.php`:

```php
<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Get JSON data
$data = json_decode(file_get_contents('php://input'), true);

// Add timestamp
$data['server_timestamp'] = date('Y-m-d H:i:s');

// Save to file (or database)
$filename = 'data/response_' . time() . '_' . uniqid() . '.json';
file_put_contents($filename, json_encode($data, JSON_PRETTY_PRINT));

// Send email notification (optional)
mail('[your-email]', 'New Questionnaire Response', 
     'New response received at ' . date('Y-m-d H:i:s'));

echo json_encode(['success' => true, 'message' => 'Data saved']);
?>
```

Then update `script.js` line 160:

```javascript
fetch('/submit.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
})
```

#### Option B: Google Sheets (No Backend Required)

1. Create a Google Apps Script web app
2. Use the script URL in `script.js`
3. Data automatically saves to Google Sheets

See: https://github.com/jamiewilson/form-to-google-sheets

#### Option C: Database (MySQL/PostgreSQL)

Create database table:

```sql
CREATE TABLE questionnaire_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    participant_id VARCHAR(50) UNIQUE,
    responses JSON,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Add Real Product Images

Replace placeholder images in `images/` folder:
- `backpack.jpg` (400x300px)
- `earbuds.jpg` (400x300px)
- `phonecase.jpg` (400x300px)
- `smartwatch.jpg` (400x300px)
- `shoes.jpg` (400x300px)
- `powerbank.jpg` (400x300px)
- `tablet.jpg` (400x300px)

Or use the auto-generated placeholders (already implemented).

## 📊 Data Collection

### Data Structure

```javascript
{
    "responses": {
        "age": "25-34",
        "gender": "female",
        "s1-q1": "5",
        "s1-q2": "6",
        // ... all 66 questions
    },
    "metadata": {
        "totalTime": 1847,  // seconds
        "completionDate": "2026-02-04T17:30:00.000Z",
        "sectionTimes": {
            "section-demographics": 45000,  // milliseconds
            "section-scenario1": 32000,
            // ... all sections
        },
        "scenarioConditions": {
            "scenario1": "A",  // With original price
            "scenario2": "B",  // Loss framing
            // ... all scenarios
        },
        "userAgent": "Mozilla/5.0...",
        "screenResolution": "1920x1080"
    }
}
```

### Accessing Data

Data is saved in three places:

1. **LocalStorage** (backup): `questionnaire_data`
2. **Server** (via AJAX): Your endpoint
3. **Console** (debugging): Check browser console

To retrieve localStorage data:

```javascript
const data = JSON.parse(localStorage.getItem('questionnaire_data'));
console.log(data);
```

## 🎨 Customization

### Change Colors

Edit `styles.css` CSS variables:

```css
:root {
    --primary-color: #2563eb;  /* Change to your color */
    --secondary-color: #10b981;
    --accent-color: #f59e0b;
}
```

### Modify Questions

Edit `index.html` sections. Each question follows this structure:

```html
<div class="question">
    <label>Question text <span class="required">*</span></label>
    <div class="likert-scale">
        <span class="likert-label">Low</span>
        <div class="likert-options">
            <label><input type="radio" name="q1" value="1" required> 1</label>
            <!-- ... more options -->
        </div>
        <span class="likert-label">High</span>
    </div>
</div>
```

### Add/Remove Sections

1. Update `state.totalSections` in `script.js`
2. Add section HTML in `index.html`
3. Update navigation buttons

## 🧪 Testing

### Local Testing

1. Open `index.html` in a browser
2. Complete the questionnaire
3. Check browser console for data
4. Check localStorage for saved data

### Test Checklist

- [ ] Timer starts when survey begins
- [ ] Progress bar updates correctly
- [ ] All required fields validate
- [ ] Scenario conditions randomize
- [ ] Data saves to localStorage
- [ ] Thank you page displays completion time
- [ ] Mobile responsive (test on phone)
- [ ] All images load correctly

## 📱 Mobile Optimization

The website is fully responsive:
- Stacks vertically on mobile
- Touch-friendly buttons
- Readable text sizes
- Optimized for small screens

Test on:
- iPhone (Safari)
- Android (Chrome)
- Tablet (iPad)

## 🔒 Privacy & Security

### Data Protection
- No personally identifiable information collected
- Anonymous responses
- Secure HTTPS connection (when deployed)
- LocalStorage backup

### GDPR Compliance
- Clear informed consent
- Right to withdraw
- Data purpose explained
- Contact information provided

## 📈 Analytics (Optional)

Add Google Analytics:

```html
<!-- Add before </head> in index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

Track events:

```javascript
// In script.js
gtag('event', 'section_complete', {
    'section_name': sectionId,
    'time_spent': timeSpent
});
```

## 🐛 Troubleshooting

### Images Not Loading
- Check `images/` folder exists
- Verify image paths in HTML
- Use placeholder generator (already implemented)

### Data Not Saving
- Check browser console for errors
- Verify server endpoint is correct
- Check localStorage in DevTools

### Timer Not Starting
- Check JavaScript console for errors
- Verify `startTimer()` is called
- Check browser compatibility

### Validation Not Working
- Ensure all required fields have `required` attribute
- Check `validateSection()` function
- Verify input names are unique

## 📞 Support

For technical issues:
- Check browser console (F12)
- Review this README
- Contact: [Your Email]

For research questions:
- Contact: [Your Name]
- Supervisor: [Supervisor Name]

## 📄 License

This questionnaire is for research purposes only.
© 2026 NED University of Engineering and Technology

## 🎓 Citation

If you use this questionnaire, please cite:

```
[Your Name] (2026). Cognitive Agentic AI for Human-AI Collaboration:
Understanding Online Shopping Decisions. NED University of Engineering
and Technology, Postgraduate Diploma in Data Science.
```

## ✅ Deployment Checklist

Before going live:

- [ ] Update all contact information
- [ ] Set up data collection endpoint
- [ ] Add real product images (or use placeholders)
- [ ] Test on multiple devices
- [ ] Test data submission
- [ ] Enable HTTPS
- [ ] Add privacy policy link (if required)
- [ ] Test completion flow
- [ ] Verify timer accuracy
- [ ] Check all 66 questions display correctly
- [ ] Test randomization
- [ ] Backup data collection method working

## 🚀 Quick Start

```bash
# 1. Navigate to folder
cd questionnaire-website

# 2. Test locally
# Open index.html in browser

# 3. Deploy to Pantheon
# Follow deployment instructions above

# 4. Test live site
# Complete full questionnaire

# 5. Verify data collection
# Check your endpoint/database
```

## 📊 Expected Metrics

- **Completion Time**: 28-30 minutes average
- **Completion Rate**: 70-80% (industry standard)
- **Mobile Users**: 40-50%
- **Drop-off Points**: Monitor section transitions

---

**Ready to deploy!** 🎉

For questions or issues, contact [Your Name] at [Your Email]

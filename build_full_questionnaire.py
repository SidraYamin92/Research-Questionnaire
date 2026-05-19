"""
COMPLETE CLEAN BUILD of index.html — generates every section from scratch.
This guarantees perfect div balance and no bleeding between sections.
All 55 questions included with correct HTML structure.
"""

# ─── Helpers ──────────────────────────────────────────────────────────────────

def likert7(qnum, qtext, name, low, high, required=True):
    req = ' <span class="required">*</span>' if required else ''
    req_attr = ' required' if required else ''
    options = '\n'.join(
        f'                        <label><input type="radio" name="{name}" value="{v}"{req_attr if v==1 else ""}> {v}</label>'
        for v in range(1, 8)
    )
    return f'''
            <div class="question">
                <label>{qnum}. {qtext}{req}</label>
                <div class="likert-scale">
                    <div class="likert-scale-header" style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:0.2rem;">
                        <span style="color:#ef4444;font-weight:700;">1 = {low}</span>
                        <span style="color:#10b981;font-weight:700;">7 = {high}</span>
                    </div>
                    <div class="likert-row">
                        <div class="likert-options">
{options}
                        </div>
                    </div>
                </div>
            </div>'''

def likert5(qnum, qtext, name, low, high, required=True):
    req = ' <span class="required">*</span>' if required else ''
    req_attr = ' required' if required else ''
    options = '\n'.join(
        f'                        <label><input type="radio" name="{name}" value="{v}"{req_attr if v==1 else ""}> {v}</label>'
        for v in range(1, 6)
    )
    return f'''
            <div class="question">
                <label>{qnum}. {qtext}{req}</label>
                <div class="likert-scale">
                    <div class="likert-scale-header" style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:0.2rem;">
                        <span style="color:#ef4444;font-weight:700;">1 = {low}</span>
                        <span style="color:#5b21b6;font-weight:700;">5 = {high}</span>
                    </div>
                    <div class="likert-row">
                        <div class="likert-options">
{options}
                        </div>
                    </div>
                </div>
            </div>'''

def nav(back_id, next_id=None, validate=True):
    back = f'<button class="btn btn-secondary" onclick="showSection(\'{back_id}\')">← Back</button>'
    if next_id:
        fn = f'validateAndNext' if validate else f'showSection'
        fwd_args = f"'{back_id if validate else next_id}'{', ' + repr(next_id) if validate else ''}"
        fwd = f'<button class="btn btn-primary" onclick="{fn}({fwd_args})">Continue →</button>'
    else:
        fwd = f'<button class="btn btn-primary btn-large" onclick="completeSurvey()">🎉 Submit Survey</button>'
    return f'''
            <div class="button-group">
                {back}
                {fwd}
            </div>'''

def section(sid, active, content):
    cls = 'section active' if active else 'section'
    return f'        <div class="{cls}" id="{sid}">\n{content}\n        </div>\n'

# ─── Question counter ──────────────────────────────────────────────────────────
q = [0]
def nq():
    q[0] += 1
    return q[0]

# ─── Scenario card helper ──────────────────────────────────────────────────────
def product_card(title, img, price_id, features, rating='⭐⭐⭐⭐⭐ 4.5+ stars'):
    feat_li = '\n'.join(f'                        <li>✓ {f}</li>' for f in features)
    return f'''            <div class="product-card">
                <div class="product-image"><img src="images/{img}" alt="{title}" onerror="this.style.display='none'; this.parentElement.innerHTML='<div class=placeholder-img>🛍️ {title}</div>';"></div>
                <div class="product-details">
                    <h3>{title}</h3>
                    <div class="product-rating">{rating}</div>
                    <ul class="product-features">
{feat_li}
                    </ul>
                    <div class="product-price" id="{price_id}"></div>
                </div>
            </div>
'''

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD EACH SECTION
# ═══════════════════════════════════════════════════════════════════════════════

# ── Welcome ────────────────────────────────────────────────────────────────────
s_welcome = '''            <div class="welcome-header">
                <h1>🎓 Research Study</h1>
                <h2>Cognitive Agentic AI for Human-AI Collaboration</h2>
                <p class="subtitle">Understanding Online Shopping Decisions and Trust in AI</p>
            </div>
            <div class="university-info">
                <p><strong>NED University of Engineering and Technology</strong></p>
                <p>Postgraduate Diploma in Data Science</p>
            </div>
            <div class="info-box">
                <h3>📋 Study Information</h3>
                <ul>
                    <li>⏱️ <strong>Time Required:</strong> 15-18 minutes</li>
                    <li>📝 <strong>Questions:</strong> 55 questions</li>
                    <li>🎯 <strong>Topic:</strong> Online shopping decisions and AI trust</li>
                    <li>🔒 <strong>Privacy:</strong> Your data is confidential</li>
                </ul>
            </div>
            <button class="btn btn-primary btn-large" onclick="showSection('section-consent')">Begin Study →</button>
'''

# ── Consent ────────────────────────────────────────────────────────────────────
s_consent = '''            <h2>Informed Consent for Research Participation</h2>
            <div class="consent-box">
                <h3>Research Title</h3>
                <p>Cognitive Agentic AI for Human-AI Collaboration: Understanding Online Shopping Decisions</p>
                <h3>Research Team</h3>
                <p><strong>Principal Investigator:</strong> Sidra Yamin<br><strong>Supervisor:</strong> Imran Bashir<br>NED University of Engineering and Technology<br>Programme: Postgraduate Diploma in Data Science</p>
                <h3>Purpose of the Study</h3>
                <p>This research investigates how people make online shopping decisions and how they trust AI recommendations.</p>
                <h3>What You Will Do</h3>
                <p>You will complete shopping scenarios and answer questions about your decisions, thinking style, and trust in AI. This will take approximately 15-18 minutes.</p>
                <h3>Confidentiality</h3>
                <p>Your responses are completely anonymous. No personally identifiable information will be collected.</p>
                <h3>Voluntary Participation</h3>
                <p>Your participation is entirely voluntary. You may withdraw at any time without penalty.</p>
            </div>
            <div class="consent-checkbox">
                <label>
                    <input type="checkbox" id="consentCheck" onchange="toggleConsentButton()">
                    <strong>I confirm that I am 18+ years old, have read this information, and voluntarily agree to participate.</strong>
                </label>
            </div>
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-welcome')">← Back</button>
                <button class="btn btn-primary" id="consentButton" disabled onclick="startSurvey()">I Agree - Start Survey →</button>
            </div>
'''

# ── Demographics ───────────────────────────────────────────────────────────────
q1=nq(); q2=nq(); q3=nq(); q4=nq(); q5=nq(); q6=nq()
s_demo = f'''            <h2>Part A: Your Information</h2>
            <p class="section-intro">Please provide the following information (6 questions):</p>

            <div class="question">
                <label>{q1}. What is your age group? <span class="required">*</span></label>
                <select name="age" required>
                    <option value="">Select...</option>
                    <option value="18-24">18–24 years</option>
                    <option value="25-34">25–34 years</option>
                    <option value="35-44">35–44 years</option>
                    <option value="45-54">45–54 years</option>
                    <option value="55-64">55–64 years</option>
                    <option value="65+">65+ years</option>
                </select>
            </div>

            <div class="question">
                <label>{q2}. What is your gender? <span class="required">*</span></label>
                <div class="radio-group">
                    <label><input type="radio" name="gender" value="male" required> Male</label>
                    <label><input type="radio" name="gender" value="female"> Female</label>
                    <label><input type="radio" name="gender" value="other"> Other / Non-binary</label>
                    <label><input type="radio" name="gender" value="prefer-not"> Prefer not to say</label>
                </div>
            </div>

            <div class="question">
                <label>{q3}. What is your highest level of education? <span class="required">*</span></label>
                <select name="education" required>
                    <option value="">Select...</option>
                    <option value="highschool">High school</option>
                    <option value="bachelors">Bachelor's degree</option>
                    <option value="masters">Master's degree</option>
                    <option value="phd">Doctoral degree</option>
                    <option value="other">Other</option>
                </select>
            </div>

            <div class="question">
                <label>{q4}. How often do you shop online? <span class="required">*</span></label>
                <select name="shopping-frequency" required>
                    <option value="">Select...</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                    <option value="rarely">Rarely</option>
                </select>
            </div>
{likert7(q5, "How comfortable are you with technology?", "tech-comfort", "Not comfortable", "Very comfortable")}
            <div class="question">
                <label>{q6}. Have you used AI shopping recommendations (e.g., Amazon, Daraz)? <span class="required">*</span></label>
                <div class="radio-group">
                    <label><input type="radio" name="ai-experience" value="frequently" required> Yes, frequently</label>
                    <label><input type="radio" name="ai-experience" value="occasionally"> Yes, occasionally</label>
                    <label><input type="radio" name="ai-experience" value="rarely"> Yes, rarely</label>
                    <label><input type="radio" name="ai-experience" value="never"> No, never</label>
                </div>
            </div>

            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-consent')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-demographics', 'section-scenarios-intro')">Continue →</button>
            </div>
'''

# ── Scenarios Intro ─────────────────────────────────────────────────────────
s_intro = '''            <h2>Part B: Shopping Scenarios</h2>
            <div class="info-box">
                <h3>📝 Instructions</h3>
                <p>You will see <strong>7 different online shopping scenarios</strong>. For each:</p>
                <ul>
                    <li>Imagine you are actually shopping online</li>
                    <li>Consider whether to purchase the product shown</li>
                    <li>Answer honestly — there are no right or wrong answers</li>
                </ul>
            </div>
            <button class="btn btn-primary btn-large" onclick="showSection('section-scenario1')">Start Scenarios →</button>
'''

# ── Scenario helpers ───────────────────────────────────────────────────────────
def scenario_section(prev_id, next_id, title, card_html, questions_html):
    return f'''            <h2>{title}</h2>
{card_html}{questions_html}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('{prev_id}')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('{next_id.replace("section-", "section-").replace("next_id", next_id)}', '{next_id}')">Next →</button>
            </div>
'''

# Scenario 1 — Backpack (Anchoring Bias)
qa = nq(); qb = nq()
s_s1 = f'''            <h2>Scenario 1 of 7: Laptop Backpack</h2>
            <div class="scenario-badge">🧠 Anchoring & Price Perception</div>
{product_card("Premium Laptop Backpack", "product1.jpg", "price-scenario1",
    ["Water-resistant", "USB charging port", "Fits 15.6\" laptops", "Multiple compartments"])}
            <div class="ai-recommendation">
                <div class="ai-badge">🤖 AI Recommendation</div>
                <p>"Based on your browsing history and 2,847 similar shoppers, this backpack scores <strong>9.2/10</strong> for value. Users who bought this also rated durability 4.8/5."</p>
            </div>
{likert7(qa, "How likely are you to purchase this backpack?", "s1-purchase", "Very unlikely", "Very likely")}
{likert7(qb, "How would you rate the value for money?", "s1-value", "Very poor value", "Excellent value")}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenarios-intro')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-scenario1', 'section-scenario2')">Next →</button>
            </div>
'''

# Scenario 2 — Earbuds (Scarcity Bias)
qa = nq(); qb = nq()
s_s2 = f'''            <h2>Scenario 2 of 7: Wireless Earbuds</h2>
            <div class="scenario-badge">⚡ Scarcity & Urgency</div>
{product_card("Premium Wireless Earbuds", "product2.jpg", "price-scenario2",
    ["Active Noise Cancellation", "30-hour battery", "Premium sound quality", "Only 3 left in stock!"])}
            <div class="ai-recommendation">
                <div class="ai-badge">🤖 AI Recommendation</div>
                <p>"⚠️ High demand alert! This product sells out every week. <strong>87% of users</strong> who viewed this item purchased within 24 hours."</p>
            </div>
{likert7(qa, "How motivated are you to purchase these earbuds?", "s2-motivation", "Not at all motivated", "Extremely motivated")}
{likert7(qb, "How urgent does this purchase feel?", "s2-urgency", "Not urgent at all", "Extremely urgent")}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenario1')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-scenario2', 'section-scenario3')">Next →</button>
            </div>
'''

# Scenario 3 — Phone Case (Social Proof)
qa = nq(); qb = nq()
s_s3 = f'''            <h2>Scenario 3 of 7: Phone Case</h2>
            <div class="scenario-badge">👥 Social Proof</div>
{product_card("Premium Phone Case", "product3.jpg", "price-scenario3",
    ["Military-grade protection", "Wireless charging compatible", "4,523 five-star reviews", "\"Bestseller\" badge"])}
            <div class="ai-recommendation">
                <div class="ai-badge">🤖 AI Recommendation</div>
                <p>"This is the <strong>#1 rated</strong> phone case this month. 4,523 verified buyers gave it 5 stars. Recommended by 96% of users."</p>
            </div>
{likert7(qa, "How much do customer reviews and ratings influence your decision?", "s3-social", "Not at all", "Extremely")}
{likert7(qb, "How likely are you to purchase this case?", "s3-purchase", "Very unlikely", "Very likely")}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenario2')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-scenario3', 'section-scenario4')">Next →</button>
            </div>
'''

# Scenario 4 — Smartwatch (Loss Aversion)
qa = nq(); qb = nq()
s_s4 = f'''            <h2>Scenario 4 of 7: Smart Watch</h2>
            <div class="scenario-badge">😰 Loss Aversion</div>
{product_card("Smart Watch Pro", "product4.jpg", "price-scenario4",
    ["Health & fitness tracking", "GPS", "7-day battery", "Limited time: 40% OFF — ends tonight!"])}
            <div class="ai-recommendation">
                <div class="ai-badge">🤖 AI Recommendation</div>
                <p>"⏳ Flash sale! Regular price Rs12,000. Today only: Rs7,200. You'll <strong>save Rs4,800</strong>. This deal expires in 2 hours."</p>
            </div>
{likert7(qa, "How urgent does this purchase feel?", "s4-urgency", "Not urgent", "Very urgent")}
{likert7(qb, "How likely are you to purchase this smartwatch?", "s4-purchase", "Very unlikely", "Very likely")}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenario3')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-scenario4', 'section-scenario5')">Next →</button>
            </div>
'''

# Scenario 5 — Running Shoes (Choice Overload)
qa = nq(); qb = nq()
s_s5 = f'''            <h2>Scenario 5 of 7: Running Shoes</h2>
            <div class="scenario-badge">🤯 Choice Overload</div>
{product_card("Running Shoes Pro", "product5.jpg", "price-scenario5",
    ["237 similar options available", "Filters: brand, material, size, price, rating...", "Multiple AI recommendations", "Conflicting user reviews"])}
            <div class="ai-recommendation">
                <div class="ai-badge">🤖 AI Recommendation</div>
                <p>"We found <strong>237 running shoes</strong> matching your preferences. Here are the top 5 based on 12 different criteria..."</p>
            </div>
{likert7(qa, "How pressured do you feel to decide quickly?", "s5-pressure", "No pressure", "Extremely pressured")}
{likert7(qb, "How likely are you to purchase these shoes?", "s5-purchase", "Very unlikely", "Very likely")}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenario4')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-scenario5', 'section-scenario6')">Next →</button>
            </div>
'''

# Scenario 6 — Power Bank (Information Overload)
qa = nq(); qb = nq(); qc = nq()
s_s6 = f'''            <h2>Scenario 6 of 7: Power Bank</h2>
            <div class="scenario-badge">📊 Information Overload</div>
{product_card("Power Bank Ultra", "product6.jpg", "price-scenario6",
    ["20,000 mAh capacity", "Fast charging 65W", "8 pages of technical specs", "43 expert reviews with conflicting ratings"])}
            <div class="ai-recommendation">
                <div class="ai-badge">🤖 AI Recommendation</div>
                <p>"Based on 43 technical parameters and 1,247 user reviews, this power bank scores 8.7/10. Key specs: charging efficiency 94.3%, voltage regulation ±0.2V..."</p>
            </div>
{likert7(qa, "How overwhelmed do you feel by the product information?", "s6-overwhelm", "Not overwhelmed", "Extremely overwhelmed")}
{likert7(qb, "How likely are you to purchase this power bank?", "s6-purchase", "Very unlikely", "Very likely")}
{likert7(qc, "Would AI help simplify this decision?", "s6-ai-help", "Not at all", "Definitely yes")}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenario5')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-scenario6', 'section-scenario7')">Next →</button>
            </div>
'''

# Scenario 7 — Tablet (Confirmation Bias)
qa = nq(); qb = nq()
s_s7 = f'''            <h2>Scenario 7 of 7: Tablet</h2>
            <div class="scenario-badge">💭 Confirmation Bias</div>
{product_card("Digital Tablet", "product7.jpg", "price-scenario7",
    ["10.1\" display", "8GB RAM, 256GB storage", "Mixed reviews: some love it, some don't", "AI highlights only positive reviews by default"])}
            <div class="ai-recommendation">
                <div class="ai-badge">🤖 AI Recommendation</div>
                <p>"Showing reviews that match your preferences... <strong>Top positive reviews:</strong> 'Best tablet I've owned!' 'Amazing value for the price!'"</p>
            </div>
{likert7(qa, "How much do you look for information that supports your initial opinion?", "s7-confirmation", "Not at all", "A great deal")}
{likert7(qb, "How likely are you to purchase this tablet?", "s7-purchase", "Very unlikely", "Very likely")}
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenario6')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-scenario7', 'section-trust')">Next →</button>
            </div>
'''

# ── Trust in Automation (TiA) — 12 items ────────────────────────────────────
tia = [
    ("The AI system is reliable.", "trust-1"),
    ("I can trust the AI system.", "trust-2"),
    ("The AI system is dependable.", "trust-3"),
    ("I have confidence in the AI's advice.", "trust-4"),
    ("The AI provides accurate recommendations.", "trust-5"),
    ("I feel comfortable relying on the AI.", "trust-6"),
    ("The AI has my best interests in mind.", "trust-7"),
    ("Overall, I trust the AI system.", "trust-8"),
    ("The AI understands my preferences.", "trust-9"),
    ("The AI's behavior is predictable.", "trust-10"),
    ("The AI acts consistently.", "trust-11"),
    ("I would follow the AI's recommendations.", "trust-12"),
]
s_trust = '            <h2>Part C: Trust in AI</h2>\n'
s_trust += '            <p class="section-intro">Rate your agreement with each statement about the AI system (12 questions):</p>\n'
for txt, name in tia:
    s_trust += likert7(nq(), txt, name, "Strongly disagree", "Strongly agree")
s_trust += '''
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-scenario7')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-trust', 'section-cognitive')">Continue →</button>
            </div>
'''

# ── REI-10 Cognitive Style — 10 items ────────────────────────────────────────
rei = [
    ("I trust my initial feelings about people.", "rei-1"),
    ("I believe in trusting my hunches.", "rei-2"),
    ("My initial impressions are usually right.", "rei-3"),
    ("I can usually feel when something is right or wrong.", "rei-4"),
    ("I trust my gut feelings.", "rei-5"),
    ("I prefer complex to simple problems.", "rei-6"),
    ("I enjoy intellectual challenges.", "rei-7"),
    ("I like to think through problems carefully.", "rei-8"),
    ("I prefer tasks that require thinking.", "rei-9"),
    ("I enjoy analyzing problems systematically.", "rei-10"),
]
s_cog = '            <h2>Part D: Thinking Style</h2>\n'
s_cog += '            <p class="section-intro">Rate how well each statement describes you (10 questions):</p>\n'
for txt, name in rei:
    s_cog += likert7(nq(), txt, name, "Does not describe me at all", "Describes me very well")
s_cog += '''
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-trust')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-cognitive', 'section-tam')">Continue →</button>
            </div>
'''

# ── TAM — 6 items ────────────────────────────────────────────────────────────
tam = [
    ("AI recommendations help me shop more effectively.", "tam-1"),
    ("AI recommendations improve my shopping decisions.", "tam-2"),
    ("AI recommendations are useful for finding products.", "tam-3"),
    ("Learning to use AI shopping tools is easy.", "tam-4"),
    ("AI shopping interfaces are clear and understandable.", "tam-5"),
    ("It is easy to get AI to do what I want.", "tam-6"),
]
s_tam = '            <h2>Part E: AI Acceptance</h2>\n'
s_tam += '            <p class="section-intro">Rate your agreement about AI shopping assistants (6 questions):</p>\n'
for txt, name in tam:
    s_tam += likert7(nq(), txt, name, "Strongly disagree", "Strongly agree")
s_tam += '''
            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-cognitive')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-tam', 'section-crt')">Continue →</button>
            </div>
'''

# ── CRT — 3 items ────────────────────────────────────────────────────────────
qa=nq(); qb=nq(); qc=nq()
s_crt = f'''            <h2>Part F: Analytical Thinking</h2>
            <p class="section-intro">Please answer these 3 questions (type your numerical answer):</p>

            <div class="question">
                <label>{qa}. A bat and a ball cost ₨1,100 in total. The bat costs ₨1,000 more than the ball. How much does the ball cost? <span class="required">*</span></label>
                <input type="number" name="crt-1" placeholder="Enter amount in ₨" required>
            </div>

            <div class="question">
                <label>{qb}. If it takes 5 machines 5 minutes to make 5 widgets, how many minutes would it take 100 machines to make 100 widgets? <span class="required">*</span></label>
                <input type="number" name="crt-2" placeholder="Enter minutes" required>
            </div>

            <div class="question">
                <label>{qc}. In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 48 days for the patch to cover the entire lake, how many days would it take to cover half the lake? <span class="required">*</span></label>
                <input type="number" name="crt-3" placeholder="Enter days" required>
            </div>

            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-tam')">← Back</button>
                <button class="btn btn-primary" onclick="validateAndNext('section-crt', 'section-explainability')">Continue →</button>
            </div>
'''

# ── Explainability — 3 items ──────────────────────────────────────────────────
qa=nq(); qb=nq(); qc=nq()
s_exp = f'''            <h2>Part G: AI Explanation Preferences</h2>
            <p class="section-intro">Tell us about your preferences for AI explanations (3 questions):</p>

            <div class="question">
                <label>{qa}. What type of AI explanation do you prefer? <span class="required">*</span></label>
                <div class="radio-group">
                    <label><input type="radio" name="explain-type" value="simple" required> Simple summary ("Similar to products you liked")</label>
                    <label><input type="radio" name="explain-type" value="detailed"> Detailed reasoning ("Based on your history, reviews, and price range...")</label>
                    <label><input type="radio" name="explain-type" value="visual"> Visual explanation (charts, highlights)</label>
                    <label><input type="radio" name="explain-type" value="none"> No explanation needed</label>
                </div>
            </div>
{likert7(qb, "How important is it for AI to explain its recommendations?", "explain-importance", "Not important", "Very important")}
{likert7(qc, "How transparent should AI be about its limitations?", "explain-transparency", "Not transparent", "Fully transparent")}

            <div class="button-group">
                <button class="btn btn-secondary" onclick="showSection('section-crt')">← Back</button>
                <button class="btn btn-primary btn-large" onclick="completeSurvey()">🎉 Submit Survey</button>
            </div>
'''

total_q = q[0]

# ── Thank You ─────────────────────────────────────────────────────────────────
s_thanks = f'''            <div class="thankyou-container">
                <h1>🎉 Thank You!</h1>
                <p class="thankyou-message">Your responses have been recorded successfully.</p>
                <div class="completion-stats">
                    <div class="stat-box">
                        <div class="stat-number" id="finalTime">--:--</div>
                        <div class="stat-label">Completion Time</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{total_q}</div>
                        <div class="stat-label">Questions Answered</div>
                    </div>
                </div>
                <div class="info-box">
                    <h3>What Happens Next?</h3>
                    <ul>
                        <li>✅ Your responses have been saved securely</li>
                        <li>📊 Your data will contribute to important AI research</li>
                        <li>🎓 Results will be used for academic purposes only</li>
                    </ul>
                </div>
                <p>Questions? Contact: <a href="mailto:sidrashahid535@gmail.com">sidrashahid535@gmail.com</a></p>
            </div>
'''

# ═══════════════════════════════════════════════════════════════════════════════
# ASSEMBLE FULL HTML
# ═══════════════════════════════════════════════════════════════════════════════

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Research study on AI trust and online shopping decisions — NED University">
    <title>Cognitive AI Research Study - NED University</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        html, body {{ overscroll-behavior: none; }}
        .scenario-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 0.3rem 0.9rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
            letter-spacing: 0.03em;
        }}
    </style>
</head>
<body>

    <!-- Timer -->
    <div class="timer-bar" id="timerBar">
        <div class="timer-display" id="timerDisplay">⏱ 00:00</div>
        <div class="progress-text" id="progressText">0% Complete</div>
    </div>

    <!-- Main Container -->
    <div class="container">

{section("section-welcome", True, s_welcome)}
{section("section-consent", False, s_consent)}
{section("section-demographics", False, s_demo)}
{section("section-scenarios-intro", False, s_intro)}
{section("section-scenario1", False, s_s1)}
{section("section-scenario2", False, s_s2)}
{section("section-scenario3", False, s_s3)}
{section("section-scenario4", False, s_s4)}
{section("section-scenario5", False, s_s5)}
{section("section-scenario6", False, s_s6)}
{section("section-scenario7", False, s_s7)}
{section("section-trust", False, s_trust)}
{section("section-cognitive", False, s_cog)}
{section("section-tam", False, s_tam)}
{section("section-crt", False, s_crt)}
{section("section-explainability", False, s_exp)}
{section("section-thankyou", False, s_thanks)}

    </div><!-- /container -->

    <footer>
        <p>© 2026 NED University | Research Study | Your privacy is protected</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''

# ─── Verify balance ────────────────────────────────────────────────────────────
import re
opens  = len(re.findall(r'<div', html))
closes = len(re.findall(r'</div>', html))
print(f"<div> opens : {opens}")
print(f"</div> closes: {closes}")
print(f"Balance      : {opens - closes}  ({'✅ OK' if opens == closes else '❌ BROKEN'})")

# Per-section check
parts = re.split(r'(?=<div class="section)', html)
for part in parts[1:]:
    m = re.match(r'<div class="section[^"]*" id="(section-[^"]+)"', part)
    if m:
        sid = m.group(1)
        qs = part.count('<div class="question">')
        print(f"  {sid}: {qs} questions")

print(f"\nTotal questions: {total_q}")

# ─── Write output ──────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ index.html written successfully")

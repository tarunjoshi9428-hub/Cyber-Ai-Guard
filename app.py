import streamlit as st
import string
import secrets
from zxcvbn import zxcvbn
import requests
import base64
import urllib.parse
import google.generativeai as genai 
from bs4 import BeautifulSoup  # REQUIRED FOR LINK SCANNER
from PIL import Image
import numpy as np
import cv2
from fpdf import FPDF
import time
import re
import pandas as pd

# --- CONFIGURATION ---

# Then your page config
st.set_page_config(page_title="Cyber Guard AI", layout="wide")

# Mobile-Friendly Precision CSS
mobile_fix_css = """
<style>
/* 1. Hide the Deploy/Pencil Button completely */
.stAppDeployButton {display:none !important;}

/* 2. Hide the GitHub link specifically */
[data-testid="stToolbar"] a {display:none !important;}

/* 3. Hide the Streamlit footer */
footer {visibility: hidden;}

/* 4. FORCE the mobile header, 3-dots, and sidebar arrow to stay on top and visible */
header[data-testid="stHeader"] {
    visibility: visible !important;
    z-index: 9999 !important;
}
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
}
</style>
"""
st.markdown(mobile_fix_css, unsafe_allow_html=True)


NAV_DASHBOARD = "🧭 Command Center"
NAV_LINK = "🌐 URL Threat Scanner"
NAV_QR = "▦ QR Threat Scanner"
NAV_PDF = "▤ PDF Malware Analyzer"
NAV_EMAIL = "✉ Email Analyzer"
NAV_BREACH = "🚨 Dark Web Breach Checker"
NAV_SMS = "💭 SMS Fraud Detector"
NAV_PASSWORD = "🔒 Password Audit"
NAV_KEY = "⚿ Secure Key Generator"
NAV_SIEM = "▥ SIEM Log Analyzer"
NAV_NETWORK = "📡 Network Exposure Scanner"
NAV_AI = "◇ AI Security Assistant"
NAV_QUIZ = "🧠 AI Security Quiz"

st.markdown(
    """
    <style>
        :root {
            --cg-bg: #f6f7fb;
            --cg-panel: #ffffff;
            --cg-ink: #152033;
            --cg-muted: #687386;
            --cg-line: #dfe4ec;
            --cg-green: #0f9f6e;
            --cg-red: #d94a4a;
            --cg-amber: #d9922f;
            --cg-blue: #2f6fed;
            --cg-violet: #7257d8;
        }

        .stApp {
            background: var(--cg-bg);
            color: var(--cg-ink);
        }

        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1420px;
        }

        section[data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid rgba(255,255,255,.08);
        }

        section[data-testid="stSidebar"] * {
            color: #e7edf8;
        }

        section[data-testid="stSidebar"] [data-testid="stRadio"] label {
            color: #9ba7bb;
            font-size: .78rem;
            text-transform: uppercase;
            letter-spacing: .08em;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] label {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
            padding: .48rem .6rem;
            margin: .15rem 0;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255,255,255,.07);
            border-color: rgba(255,255,255,.08);
        }

        .sidebar-brand {
            border-bottom: 1px solid rgba(255,255,255,.10);
            margin-bottom: 1rem;
            padding-bottom: 1rem;
        }

        .brand-mark {
            align-items: center;
            display: flex;
            gap: .7rem;
            font-size: 1.22rem;
            font-weight: 760;
            line-height: 1.1;
        }

        .brand-icon {
            align-items: center;
            background: #17b889;
            border-radius: 8px;
            color: #08111f;
            display: inline-flex;
            font-size: 1.05rem;
            height: 2.2rem;
            justify-content: center;
            width: 2.2rem;
        }

        .brand-subtitle, .sidebar-status {
            color: #9ba7bb;
            font-size: .82rem;
            margin-top: .45rem;
        }

        .sidebar-status {
            background: rgba(255,255,255,.06);
            border: 1px solid rgba(255,255,255,.08);
            border-radius: 8px;
            padding: .75rem;
        }

        .dashboard-hero {
            background: #ffffff;
            border: 1px solid var(--cg-line);
            border-radius: 8px;
            padding: 1.3rem 1.45rem;
        }

        .eyebrow {
            color: var(--cg-blue);
            font-size: .76rem;
            font-weight: 760;
            letter-spacing: .08em;
            margin-bottom: .35rem;
            text-transform: uppercase;
        }

        .dashboard-title {
            color: var(--cg-ink);
            font-size: 2rem;
            font-weight: 790;
            line-height: 1.15;
            margin: 0;
        }

        .dashboard-copy {
            color: var(--cg-muted);
            font-size: .98rem;
            margin: .55rem 0 0;
            max-width: 780px;
        }

        .status-pill {
            background: #ecfdf6;
            border: 1px solid #bbe9d7;
            border-radius: 999px;
            color: #087a54;
            display: inline-block;
            font-size: .82rem;
            font-weight: 700;
            padding: .35rem .65rem;
        }

        .metric-card, .panel-card, .alert-row {
            background: var(--cg-panel);
            border: 1px solid var(--cg-line);
            border-radius: 8px;
        }

        .metric-card {
            min-height: 130px;
            padding: 1rem;
        }

        .metric-label {
            color: var(--cg-muted);
            font-size: .78rem;
            font-weight: 720;
            letter-spacing: .06em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--cg-ink);
            font-size: 2.05rem;
            font-weight: 780;
            line-height: 1.05;
            margin-top: .55rem;
        }

        .metric-delta {
            font-size: .86rem;
            font-weight: 700;
            margin-top: .48rem;
        }

        .tone-green .metric-delta { color: var(--cg-green); }
        .tone-red .metric-delta { color: var(--cg-red); }
        .tone-amber .metric-delta { color: var(--cg-amber); }
        .tone-blue .metric-delta { color: var(--cg-blue); }

        .panel-card {
            padding: 1rem 1.05rem;
        }

        .panel-title {
            color: var(--cg-ink);
            font-size: 1.02rem;
            font-weight: 760;
            margin-bottom: .2rem;
        }

        .panel-subtitle {
            color: var(--cg-muted);
            font-size: .86rem;
            margin-bottom: .75rem;
        }

        .alert-row {
            align-items: center;
            display: grid;
            gap: .65rem;
            grid-template-columns: 84px 1fr 110px;
            margin-bottom: .55rem;
            padding: .72rem .8rem;
        }

        .alert-severity {
            border-radius: 999px;
            color: white;
            font-size: .72rem;
            font-weight: 760;
            padding: .25rem .45rem;
            text-align: center;
        }

        .sev-critical { background: var(--cg-red); }
        .sev-high { background: var(--cg-amber); }
        .sev-medium { background: var(--cg-blue); }
        .sev-low { background: var(--cg-green); }

        .alert-name {
            color: var(--cg-ink);
            font-size: .92rem;
            font-weight: 740;
        }

        .alert-meta {
            color: var(--cg-muted);
            font-size: .78rem;
            margin-top: .12rem;
        }

        .alert-owner {
            color: var(--cg-muted);
            font-size: .8rem;
            text-align: right;
        }

        .tool-tile {
            background: #ffffff;
            border: 1px solid var(--cg-line);
            border-radius: 8px;
            min-height: 116px;
            padding: .95rem;
        }

        .tool-icon {
            color: var(--cg-blue);
            font-size: 1.1rem;
            font-weight: 800;
        }

        .tool-title {
            color: var(--cg-ink);
            font-size: .98rem;
            font-weight: 760;
            margin-top: .5rem;
        }

        .tool-text {
            color: var(--cg-muted);
            font-size: .82rem;
            margin-top: .25rem;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--cg-line);
            border-radius: 8px;
            padding: .9rem 1rem;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


def render_metric_card(label, value, delta, tone):
    st.markdown(
        f"""
        <div class="metric-card tone-{tone}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_alert_row(severity, title, detail, owner):
    severity_class = severity.lower()
    st.markdown(
        f"""
        <div class="alert-row">
            <div class="alert-severity sev-{severity_class}">{severity}</div>
            <div>
                <div class="alert-name">{title}</div>
                <div class="alert-meta">{detail}</div>
            </div>
            <div class="alert-owner">{owner}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tool_tile(icon, title, text):
    st.markdown(
        f"""
        <div class="tool-tile">
            <div class="tool-icon">{icon}</div>
            <div class="tool-title">{title}</div>
            <div class="tool-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tool_intro(title, description, image_url, checks, safety_note):
    st.title(title)
    visual_col, content_col = st.columns([1, 2])
    with visual_col:
        st.image(image_url, width="stretch")
    with content_col:
        st.markdown(description)
        st.markdown("#### What this tool helps with")
        for check in checks:
            st.markdown(f"- {check}")
        st.info(safety_note)
    st.divider()# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-mark"><span class="brand-icon">CG</span><span>Cyber Guard AI</span></div>
            <div class="brand-subtitle">Security operations and fraud defense console</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    menu_selection = st.radio("Navigation", [
        NAV_DASHBOARD,
        NAV_LINK,
        NAV_QR,
        NAV_PDF,
        NAV_EMAIL,
        NAV_BREACH,
        NAV_SMS,
        NAV_PASSWORD,
        NAV_KEY,
        NAV_SIEM,
        NAV_NETWORK,
        NAV_AI,
        NAV_QUIZ,
    ])
    st.markdown(
        """
        <div class="sidebar-status">
            <strong>System Status</strong><br>
            AI checks online<br>
            Local analysis ready
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- MAIN LOGIC (ONE SINGLE STRUCTURE) ---
if menu_selection == NAV_DASHBOARD:
    st.markdown(
        """
        <div class="dashboard-hero">
            <div class="eyebrow">Security Operations Dashboard</div>
            <h1 class="dashboard-title">Cyber Guard Command Center</h1>
            <p class="dashboard-copy">
                Monitor suspicious links, phishing messages, QR threats, weak credentials, and log anomalies from one clean workspace.
            </p>
            <div style="margin-top: .9rem;"><span class="status-pill">Protected mode active</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        render_metric_card("Threats Screened", "1,284", "+18% this week", "blue")
    with metric_col2:
        render_metric_card("High Risk Blocks", "73", "12 require review", "red")
    with metric_col3:
        render_metric_card("Clean Verdicts", "91.6%", "+4.2% accuracy trend", "green")
    with metric_col4:
        render_metric_card("Mean Response", "01:42", "34s faster", "amber")

    st.write("")
    trend_data = pd.DataFrame(
        {
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Phishing": [42, 51, 47, 66, 58, 39, 45],
            "Malware": [16, 21, 19, 26, 24, 15, 18],
            "Fraud": [28, 31, 36, 33, 41, 27, 30],
        }
    )
    threat_mix = pd.DataFrame(
        {
            "Threat Vector": ["Phishing", "Malware", "Credential Risk", "QR Abuse", "Suspicious Logs"],
            "Detections": [342, 126, 214, 98, 176],
        }
    )

    chart_col1, chart_col2 = st.columns([1.45, 1])
    with chart_col1:
        st.markdown(
            """
            <div class="panel-card">
                <div class="panel-title">Threat Activity Trend</div>
                <div class="panel-subtitle">Detected events across the last 7 days</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.area_chart(trend_data.set_index("Day"), height=275)
    with chart_col2:
        st.markdown(
            """
            <div class="panel-card">
                <div class="panel-title">Threat Statistics</div>
                <div class="panel-subtitle">Volume by attack category</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.bar_chart(threat_mix.set_index("Threat Vector"), height=275)

    st.write("")
    queue_col, tools_col = st.columns([1.2, 1])
    with queue_col:
        st.markdown(
            """
            <div class="panel-card">
                <div class="panel-title">Priority Alert Queue</div>
                <div class="panel-subtitle">Items that need analyst attention first</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_alert_row("Critical", "Credential phishing domain", "Fake banking login detected from URL scanner", "Triage")
        render_alert_row("High", "Suspicious PDF attachment", "Macro language and impersonation markers found", "Review")
        render_alert_row("Medium", "QR redirect chain", "Shortened URL redirects to newly registered host", "Watch")
        render_alert_row("Low", "Weak password pattern", "Password reuse risk and predictable keyboard sequence", "Resolve")
    with tools_col:
        st.markdown(
            """
            <div class="panel-card">
                <div class="panel-title">Defense Coverage</div>
                <div class="panel-subtitle">Core modules available in this console</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        tile_col1, tile_col2 = st.columns(2)
        with tile_col1:
            render_tool_tile("URL", "Link Defense", "Phishing, redirects, unsafe HTTP")
            render_tool_tile("PDF", "File Review", "Attachment and malware indicators")
        with tile_col2:
            render_tool_tile("OTP", "Fraud Signals", "Email, SMS, identity tricks")
            render_tool_tile("SOC", "Log Hunt", "Brute force and anomaly checks")

    st.write("")
    posture_col1, posture_col2, posture_col3 = st.columns(3)
    posture_col1.metric("Security Posture", "A-", "Improving")
    posture_col2.metric("Open Incidents", "12", "-5 since yesterday")
    posture_col3.metric("Protected Workflows", "9", "All modules ready")

# --- TOOL 0: DASHBOARD HOME ---
if menu_selection == NAV_DASHBOARD:
    pass


elif menu_selection == NAV_LINK:
    render_tool_intro(
        "🌐 URL Threat Scanner",
        "Check suspicious URLs before opening them. This scanner reviews the link format, flags insecure HTTP pages, and asks AI to inspect the destination for phishing or impersonation risk.",
        "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=900&q=80",
        [
            "Fake login pages and brand impersonation",
            "Insecure HTTP links and suspicious domains",
            "Risky redirects, parked pages, and phishing patterns"
        ],
        "Tip: copy the link address instead of clicking it, then paste it here for a safer check."
    )
    
    url_input = st.text_input("Paste the URL to scan:", key="unique_url_scanner")
    
    if st.button("🔍 Run Deep Scan", key="unique_scan_button"):
        if not url_input.startswith("http"):
            st.error("Please enter a valid URL starting with http:// or https://")
        else:
            with st.spinner("Analyzing site security..."):
                try:
                    # 1. Detect if it is insecure HTTP
                    is_insecure = url_input.startswith("http://")
                    
                    # 2. Configure AI
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # 3. Enhanced Prompt (Strict on HTTP)
                    prompt = f"""
                    Analyze this URL: {url_input}. 
                    Security Warning: This link is using insecure HTTP (not HTTPS).
                    Task: Act as a cybersecurity expert. Determine if this site is a threat, parked domain, or phishing site.
                    Instructions: 
                    - If it is HTTP, treat it with higher suspicion.
                    - Check if the domain name looks like a brand impersonation.
                    - Output a Verdict (SAFE/SUSPICIOUS/DANGEROUS) and explain specifically why.
                    """
                    
                    ai_verdict = model.generate_content(prompt).text
                    
                    st.markdown("### 🛡️ Final Security Analysis")
                    st.info(ai_verdict)
                    
                    if "DANGEROUS" in ai_verdict.upper():
                        st.error("🚨 Blocked: Do not interact with this link.")
                    elif "SUSPICIOUS" in ai_verdict.upper() or is_insecure:
                        st.warning("⚠️ Caution: Site is unencrypted (HTTP) or shows suspicious signs. Exercise extreme care.")
                    else:
                        st.success("✅ Verdict: Appears safe.")
                        
                except Exception as e:
                    st.error(f"Scan error: {e}")

# --- TOOL: QR CODE SCANNER (QUISHING DETECTOR) ---
elif menu_selection == NAV_QR:
    render_tool_intro(
        "▦ QR Threat Scanner",
        "QR codes can hide dangerous links behind a simple scan. Upload a QR image here to reveal the destination and inspect it before using your phone.",
        "https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=900&q=80",
        [
            "Hidden phishing links inside QR codes",
            "Fake payment portals and login pages",
            "VirusTotal reputation plus AI risk review"
        ],
        "Tip: be extra careful with QR codes on posters, parcels, restaurant tables, and payment stickers."
    )

    # 1. File Uploader for Images
    uploaded_file = st.file_uploader("Upload a QR Code image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        with st.spinner("Decoding QR Code..."):
            try:
                # 2. Convert the uploaded image so OpenCV can read it
                image = Image.open(uploaded_file)
                img_array = np.array(image)
                
                # Convert RGB to BGR (OpenCV format)
                if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                # 3. Decode the QR Code
                detector = cv2.QRCodeDetector()
                decoded_url, bbox, _ = detector.detectAndDecode(img_array)

                if not decoded_url:
                    st.error("❌ Could not find or read a QR code in this image. Try a clearer picture.")
                else:
                    st.success(f"✅ **QR Code Decoded:** `{decoded_url}`")
                    
                    # Ensure it's actually a web link before scanning
                    if not decoded_url.startswith("http"):
                        st.warning("This QR code contains text, but it is not a web link. No security scan needed.")
                    else:
                        st.markdown("### 🔍 Initiating Threat Scan...")
                        
                        # --- INITIATE LAYERED SECURITY SCAN ---
                        domain = urllib.parse.urlparse(decoded_url).netloc
                        
                        # LAYER 1: VirusTotal
                       # LAYER 1: VirusTotal
                        url_id = base64.urlsafe_b64encode(decoded_url.encode()).decode().replace("=", "")
                        vt_res = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers={"x-apikey": st.secrets["VIRUSTOTAL_API_KEY"]})
                        
                        vt_report = "No database record found."
                        is_dangerous = False
                        
                        if vt_res.status_code == 200:
                            data = vt_res.json()['data']['attributes']
                            stats = data['last_analysis_stats']
                            if stats['malicious'] > 0:
                                is_dangerous = True
                                vt_report = f"Detected as malicious by {stats['malicious']} vendors."
                        
                        # LAYER 2: Gemini AI Inspection
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        prompt = f"""
                        Analyze this URL extracted from a QR code: {decoded_url}
                        Domain: {domain}
                        VirusTotal report: {vt_report}
                        
                        Task: Determine if this destination is SAFE, SUSPICIOUS, or DANGEROUS.
                        QR codes are often used to hide malicious links. Check if this looks like a phishing site, fake payment portal, or malicious redirect.
                        
                        Output EXACTLY like this:
                        VERDICT: (SAFE/SUSPICIOUS/DANGEROUS)
                        REASON: (Brief explanation why)
                        """
                        
                        ai_verdict = model.generate_content(prompt).text
                        
                        # Display Results
                        st.info(ai_verdict)
                        if "DANGEROUS" in ai_verdict.upper() or is_dangerous:
                            st.error("🚨 **CRITICAL WARNING:** This QR code leads to a dangerous site! DO NOT SCAN WITH YOUR PHONE.")
                        elif "SUSPICIOUS" in ai_verdict.upper():
                            st.warning("⚠️ **Caution:** This destination is highly suspicious.")
                        else:
                            st.success("✅ **Verdict:** Appears safe.")

            except Exception as e:
                st.error(f"Error processing the image: {e}")

# --- TOOL: PDF MALWARE ANALYZER ---
elif menu_selection == NAV_PDF:

    render_tool_intro(
        "▤ PDF Malware & Phishing Analyzer",
        "Upload a PDF to check for suspicious scripts, auto-open actions, hidden attachments, and links that may lead to credential theft or malware.",
        "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80",
        [
            "Embedded JavaScript and launch actions",
            "Hidden files, auto-execute behavior, and unsafe PDF objects",
            "Phishing links and suspicious document text"
        ],
        "Tip: do not open unexpected invoices, resumes, statements, or forms until you verify the sender."
    )

    uploaded_pdf = st.file_uploader(
        "Upload a PDF file to analyze",
        type=["pdf"],
        key="pdf_file_uploader"
    )

    # ---------------- REPORTLAB PDF FUNCTION ----------------
    def generate_reportlab_pdf(tool_name, filename, analysis_text):
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from io import BytesIO

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph(f"<b>{tool_name}</b>", styles["Title"]))
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"<b>File:</b> {filename}", styles["Normal"]))
        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>AI Security Analysis:</b>", styles["Heading2"]))
        content.append(Spacer(1, 8))

        safe_text = analysis_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
        content.append(Paragraph(safe_text, styles["Normal"]))

        doc.build(content)
        buffer.seek(0)
        return buffer.read()

    # ---------------- MAIN LOGIC ----------------
    if uploaded_pdf is not None:
        if st.button("🔍 Run Deep PDF Scan", key="pdf_analyze_btn"):
            with st.spinner("Analyzing PDF structure and extracting indicators..."):
                try:
                    import re
                    import time
                    import io
                    from pypdf import PdfReader

                    pdf_bytes = uploaded_pdf.read()

                    # 1. Check Raw Bytes for Auto-Execute Exploits
                    exploit_signatures = {
                        b"/JavaScript": "Embedded JavaScript script found",
                        b"/JS": "Abbreviated Embedded JS routine found",
                        b"/OpenAction": "Auto-execute on open command detected",
                        b"/AA": "Additional Action trigger discovered",
                        b"/Launch": "External application launch exploit attempt",
                        b"/EmbeddedFiles": "Hidden binary/executable attachment"
                    }

                    detected_risks = [
                        desc for sig, desc in exploit_signatures.items()
                        if sig in pdf_bytes
                    ]

                    # 2. Extract Text and Links Safely
                    pdf_file_stream = io.BytesIO(pdf_bytes)
                    reader = PdfReader(pdf_file_stream)

                    extracted_text = ""
                    for i in range(min(len(reader.pages), 5)):
                        text = reader.pages[i].extract_text()
                        if text:
                            extracted_text += text + "\n"

                    urls_found = re.findall(r'(https?://[^\s\"\'\>]+)', extracted_text)
                    extracted_links = list(set(urls_found))

                    # 3. AI ANALYSIS WITH SMART WAIT LOGIC
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel('gemini-2.5-flash')

                    prompt = f"""
                    Analyze this PDF security data:

                    Detected Exploits: {detected_risks if detected_risks else "None"}
                    URLs found: {extracted_links if extracted_links else "None"}
                    Text snippet: {extracted_text[:1500]}

                    Return:
                    VERDICT: SAFE / SUSPICIOUS / DANGEROUS
                    EXPLANATION: 2 sentences
                    TECHNICAL FLAGS: bullet points
                    """

                    max_retries = 3
                    ai_analysis = None

                    for attempt in range(max_retries):
                        try:
                            ai_analysis = model.generate_content(prompt).text
                            break  # Success, exit the loop
                            
                        except Exception as e:
                            error_msg = str(e)
                            if "429" in error_msg and attempt < max_retries - 1:
                                # Extract the exact required wait time from Google's error
                                match = re.search(r"retry in ([0-9.]+)s", error_msg)
                                if match:
                                    # Add 1 second just to be safe
                                    wait_time = float(match.group(1)) + 1.0 
                                else:
                                    wait_time = 10.0 # Default to 10s if we can't read it
                                
                                # Let the user know the app is waiting, not frozen
                                st.warning(f"⏳ Google API limit reached. Pausing scan for {int(wait_time)} seconds to recover...")
                                time.sleep(wait_time)
                                continue # Try the API request again
                                
                            st.error(f"AI inspection error: {e}")
                            break

                    # 4. RESULTS DISPLAY
                    if ai_analysis:
                        st.markdown("### 📊 Structural & Cognitive Threat Report")

                        if "DANGEROUS" in ai_analysis.upper() or len(detected_risks) > 0:
                            st.error("🚨 **CRITICAL RISK:** Malicious code or phishing patterns detected!")
                        elif "SUSPICIOUS" in ai_analysis.upper():
                            st.warning("⚠️ **ELEVATED WARNING:** Deceptive text or unverified links observed.")
                        else:
                            st.success("✅ **VERDICT:** Document appears safe.")

                        if detected_risks:
                            with st.expander("🛠️ Static Code Flag Details (Raw Binary Match)"):
                                for risk in detected_risks:
                                    st.write(f"- `{risk}`")

                        st.info(ai_analysis)

                        # 5. PDF REPORT DOWNLOAD
                        st.divider()
                        pdf_bytes_report = generate_reportlab_pdf(
                            "PDF Malware Analyzer",
                            uploaded_pdf.name,
                            ai_analysis
                        )

                        st.download_button(
                            label="📄 Download PDF Security Report",
                            data=pdf_bytes_report,
                            file_name=f"Report_{uploaded_pdf.name}.pdf",
                            mime="application/pdf",
                            key="pdf_scanner_report_btn"
                        )

                except Exception as e:
                    st.error(f"Failed to compile PDF Analysis: {e}")

# --- TOOL 2: EMAIL PHISHING ANALYZER (AI-POWERED WITH AUTO-RETRY) ---
elif menu_selection == NAV_EMAIL:

    render_tool_intro(
        "✉ Phishing Email Analyzer",
        "Paste an email message to inspect tone, intent, urgency, brand impersonation, and requests for sensitive information.",
        "https://images.unsplash.com/photo-1596526131083-e8c633c948d2?auto=format&fit=crop&w=900&q=80",
        [
            "Fake invoices, bank notices, and account warnings",
            "Fear, urgency, reward, and pressure tactics",
            "Requests for passwords, OTPs, payments, or downloads"
        ],
        "Tip: always compare the sender address with the official website before trusting an email."
    )
    
    email_content = st.text_area("Paste the email text here:", height=200, key="email_text_input")
    
    if st.button("🔍 Analyze Email Intent", key="analyze_email_btn"):
        if not email_content.strip():
            st.error("Please paste the email content to analyze.")
        else:
            with st.spinner("AI is analyzing psychological triggers and fraud patterns..."):
                import time  # Required for the retry pause
                
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                You are a cybersecurity expert. Analyze the following email for phishing, fraud, or social engineering.
                Email Content: "{email_content}"
                Task: 
                1. Evaluate the intent. Is it trying to create fear/urgency? Is it asking for money/passwords?
                2. Check for brand impersonation.
                3. Output a final verdict.
                Format your response exactly like this:
                VERDICT: (SAFE / SUSPICIOUS / DANGEROUS)
                ANALYSIS: (2 sentences explaining why)
                RED FLAGS: (Bullet points of the specific scam tactics used)
                """
                
                # --- NEW RETRY LOGIC FOR 429 ERRORS ---
                max_retries = 3
                ai_analysis = None
                
                for attempt in range(max_retries):
                    try:
                        ai_analysis = model.generate_content(prompt).text
                        break  # Success! Break out of the loop
                    except Exception as e:
                        if "429" in str(e):
                            if attempt < max_retries - 1:
                                # Wait 2 seconds, then 4 seconds before trying again
                                time.sleep(2 ** (attempt + 1)) 
                                continue
                        # If it fails 3 times or gives a different error, stop and show it
                        st.error(f"Analysis system offline or error occurred: {e}")
                        break
                
                # --- DISPLAY RESULTS (Only if successful) ---
                if ai_analysis:
                    st.markdown("### 📊 Threat Intelligence Report")
                    
                    if "DANGEROUS" in ai_analysis.upper():
                        st.error("🚨 **CRITICAL WARNING:** This is highly likely a phishing attempt or scam.")
                    elif "SUSPICIOUS" in ai_analysis.upper():
                        st.warning("⚠️ **CAUTION:** This email exhibits suspicious behavior. Do not click links or download attachments.")
                    else:
                        st.success("✅ **VERDICT:** No obvious malicious intent detected. (Always verify the sender's actual email address).")
                    
                    st.info(ai_analysis)

# --- TOOL 12: EMAIL DARK WEB BREACH CHECKER (SIMULATION ENGINE) ---
elif menu_selection == NAV_BREACH:
    st.title(f"{NAV_BREACH}")
    st.write("Scans global dark web databases to see if an email address has been compromised in a corporate data leak.")

    # 1. User Inputs
    target_email = st.text_input("Enter Email Address to Audit:", placeholder="user@example.com")
    
    # Simulation Controller for Portfolio/Project Demonstration
    st.markdown("##### 🛠️ Testing Environment Control")
    test_scenario = st.radio(
        "Choose what the database should return (Since this is a project without a paid database key):",
        ["🔴 Simulate a Major Data Breach", "🟢 Simulate a Safe / Clean Email"]
    )

    if st.button("🔎 Scan Dark Web Databases", key="breach_scan_btn"):
        import re
        import time

        # Basic email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", target_email):
            st.error("❌ Please enter a valid email address.")
        else:
            with st.spinner("Querying simulated global data breach records..."):
                try:
                    time.sleep(1.5) # Simulate network loading time
                    breach_data = []
                    
                    # --- SIMULATION LOGIC ---
                    if "Safe" in test_scenario:
                        breach_data = [] # Clean email
                    else:
                        # Simulate finding the email in known major historical breaches
                        breach_data = [
                            {"Name": "LinkedIn", "BreachDate": "2012-05-05", "DataClasses": ["Email addresses", "Passwords"]},
                            {"Name": "Canva", "BreachDate": "2019-05-24", "DataClasses": ["Email addresses", "Geographic locations", "Names", "Passwords"]},
                            {"Name": "Apollo", "BreachDate": "2018-07-23", "DataClasses": ["Email addresses", "Employers", "Job titles", "Names", "Phone numbers"]}
                        ]

                    # --- UI METRICS DASHBOARD ---
                    st.markdown("### 📊 Exposure Intelligence Summary")
                    
                    if len(breach_data) == 0:
                        st.success(f"✅ **CLEAN RECORD:** The email `{target_email}` was not found in any public data breaches.")
                        ai_input_data = "No breaches found. The email is safe."
                    else:
                        st.error(f"🚨 **COMPROMISED:** `{target_email}` was found in {len(breach_data)} major data breaches!")
                        
                        ai_input_data = ""
                        with st.expander("👁️ View Breached Databases (Raw Data)", expanded=True):
                            for b in breach_data:
                                st.markdown(f"**🔴 {b['Name']} ({b['BreachDate']})**")
                                st.write(f"*Leaked Data:* {', '.join(b['DataClasses'])}")
                                ai_input_data += f"Breach: {b['Name']}. Leaked: {', '.join(b['DataClasses'])}\n"

                    # --- AI THREAT ASSESSMENT (USING YOUR GEMINI KEY) ---
                    st.markdown("### 🧠 AI Remediation Plan")
                    with st.spinner("Gemini AI is generating a customized security action plan..."):
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        prompt = f"""
                        You are a Cybersecurity Incident Responder. 
                        Target Email: {target_email}
                        Breach Data Extracted:
                        {ai_input_data}
                        
                        Task:
                        If the email is safe, briefly congratulate the user and remind them to use 2FA.
                        If the email is breached, analyze the "Leaked Data" types. If passwords were leaked, emphasize changing passwords. If Phone numbers/Locations were leaked, warn them about spear-phishing and SIM swapping.
                        
                        Format EXACTLY like this:
                        VERDICT: (SAFE / HIGH RISK)
                        THREAT ANALYSIS: (2 sentences evaluating the specific data leaked)
                        ACTION PLAN: (3 bullet points of exactly what the user must do right now to secure their identity)
                        """

                        max_retries = 3
                        ai_analysis = None
                        for attempt in range(max_retries):
                            try:
                                ai_analysis = model.generate_content(prompt).text
                                break
                            except Exception as e:
                                error_msg = str(e)
                                if "429" in error_msg and attempt < max_retries - 1:
                                    match = re.search(r"retry in ([0-9.]+)s", error_msg)
                                    wait_time = float(match.group(1)) + 1.0 if match else 5.0
                                    st.warning(f"⏳ Pausing to prevent API overload ({int(wait_time)}s)...")
                                    time.sleep(wait_time)
                                    continue
                                st.error(f"AI Analysis Error: {e}")
                                break
                        
                        if ai_analysis:
                            st.info(ai_analysis)

                            # --- GENERATE PDF REPORT ---
                            st.divider()
                            def generate_reportlab_pdf(tool_name, filename, analysis_text):
                                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                                from reportlab.lib.styles import getSampleStyleSheet
                                from io import BytesIO

                                buffer = BytesIO()
                                doc = SimpleDocTemplate(buffer)
                                styles = getSampleStyleSheet()
                                content = []

                                content.append(Paragraph(f"<b>{tool_name}</b>", styles["Title"]))
                                content.append(Spacer(1, 12))
                                content.append(Paragraph(f"<b>Identity Target:</b> {filename}", styles["Normal"]))
                                content.append(Spacer(1, 12))
                                content.append(Paragraph("<b>AI Security Analysis:</b>", styles["Heading2"]))
                                content.append(Spacer(1, 8))

                                safe_text = analysis_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
                                content.append(Paragraph(safe_text, styles["Normal"]))

                                doc.build(content)
                                buffer.seek(0)
                                return buffer.read()

                            pdf_bytes_report = generate_reportlab_pdf(
                                "Dark Web Identity & Breach Audit",
                                target_email,
                                ai_analysis
                            )
                            st.download_button(
                                label="📄 Download Official Identity Audit (PDF)", 
                                data=pdf_bytes_report, 
                                file_name=f"Identity_Audit_{target_email}.pdf", 
                                mime="application/pdf", 
                                key="breach_pdf_btn"
                            )

                except Exception as e:
                    st.error(f"Failed to process identity audit: {e}")

# --- TOOL 3: SMS DETECTOR ---
elif menu_selection == NAV_SMS:
  
    render_tool_intro(
        "● SMS Fraud Detector",
        "Paste a suspicious text message to check for common fraud patterns such as delivery scams, fake bank alerts, lottery messages, and unsafe links.",
        "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?auto=format&fit=crop&w=900&q=80",
        [
            "Urgent account-lock or payment messages",
            "Package delivery and prize scam keywords",
            "Shortened URLs and suspicious link prompts"
        ],
        "Tip: banks, delivery companies, and support teams should never ask for OTPs or passwords by SMS."
    )
    
    sms_text = st.text_area("Paste the text message here:", height=150)
    
    if st.button("Evaluate Threat Level"):
        if sms_text:
            # 1. Convert text to lowercase for easier searching
            text_lower = sms_text.lower()
            
            # 2. Define our scam keywords (The Heuristic Engine)
            urgency_words = ["urgent", "immediately", "suspended", "locked", "action required"]
            scam_topics = ["package", "delivery", "usps", "fedex", "ups", "bank", "lottery", "winner"]
            link_indicators = ["http", "bit.ly", "click here", "tap here", ".com", ".info"]
            
            # 3. Calculate the Threat Score
            score = 0
            found_flags = []
            
            # Check for urgency
            for word in urgency_words:
                if word in text_lower:
                    score += 2
                    found_flags.append(f"Urgency keyword: '{word}'")
            
            # Check for common scam topics
            for word in scam_topics:
                if word in text_lower:
                    score += 1
                    found_flags.append(f"Suspicious topic: '{word}'")
                    
            # Check for links (Scams almost ALWAYS have links)
            for word in link_indicators:
                if word in text_lower:
                    score += 3
                    found_flags.append("Contains a link/URL")
                    break # Only count the link threat once
                    
            # 4. Display the Results based on the Score
            st.markdown("### 🔍 Analysis Results")
            
            if score == 0:
                st.success("✅ **Low Risk:** No obvious scam patterns detected. Still, always verify the sender!")
            elif score <= 3:
                st.warning("⚠️ **Medium Risk:** Some suspicious keywords found. Proceed with caution.")
            else:
                st.error("🚨 **CRITICAL RISK:** This message highly matches common fraud patterns! Do NOT click any links.")
                
            # Show the user exactly WHY it was flagged
            if found_flags:
                st.info("**Red Flags Detected:**\n" + "\n".join([f"- {flag}" for flag in found_flags]))
        else:
            st.error("Please paste a message first.")

# --- TOOL 4: PASSWORD EVALUATOR ---
elif menu_selection == NAV_PASSWORD:
   
    render_tool_intro(
        "🔒 Password Audit",
        "Test how resistant a password is against guessing and cracking. The result estimates strength and gives improvement suggestions.",
        "https://images.unsplash.com/photo-1633265486064-086b219458ec?auto=format&fit=crop&w=900&q=80",
        [
            "Weak, common, or predictable passwords",
            "Estimated offline cracking time",
            "Personal details, repeated words, and simple patterns"
        ],
        "Tip: a strong password is long, unique, and stored in a password manager."
    )
    
    # 1. Password input (hidden characters)
    password_input = st.text_input("Enter your password:", type="password")
    
    # 2. Added a Check Button so it doesn't trigger until you are ready
    if st.button("Check Strength"):
        if password_input:
            # Use zxcvbn to analyze
            results = zxcvbn(password_input)
            
            # Use a more reliable key for crack time
            # The structure changed, so we grab the 'offline_slow_hashing_1e4_per_second'
            crack_time = results['crack_times_display']['offline_slow_hashing_1e4_per_second']
            score = results['score'] 
            
            st.markdown("### 📊 Strength Analysis")
            
            # Display results with colors
            if score <= 1:
                st.error(f"❌ Weak Password. Estimated time to crack: {crack_time}")
            elif score == 2:
                st.warning(f"⚠️ Moderate Password. Estimated time to crack: {crack_time}")
            else:
                st.success(f"✅ Strong Password! Estimated time to crack: {crack_time}")
                
            # Show feedback if available
            if results['feedback']['suggestions']:
                st.info("**Suggestions to improve:** " + " ".join(results['feedback']['suggestions']))
        else:
            st.error("Please enter a password first!")

# --- TOOL 5: SECURE PASSWORD GENERATOR ---
elif menu_selection == NAV_KEY:

    render_tool_intro(
        "⚿ Secure Key Generator",
        "Create strong random passwords or personalized keys with secure randomness, adjustable length, and optional symbols or numbers.",
        "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
        [
            "Random passwords for new accounts",
            "Custom length and character options",
            "Personalized passwords with shuffled secure characters"
        ],
        "Tip: generate a different password for every important account and enable two-factor authentication."
    )

    mode = st.radio(
        "Choose Password Generation Mode:",
        [
            "Random Secure Password",
            "Personalized Password"
        ]
    )

    length = st.slider(
        "Select Password Length:",
        min_value=8,
        max_value=32,
        value=16
    )

    include_upper = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
    include_numbers = st.checkbox("Include Numbers (0-9)", value=True)
    include_symbols = st.checkbox("Include Special Symbols (!@#$%^&*)", value=True)

    user_name = ""

    if mode == "Personalized Password":
        user_name = st.text_input(
            "Enter a Name, Nickname, or Keyword:"
        )

    if st.button("Generate Password"):

        chars = string.ascii_lowercase

        if include_upper:
            chars += string.ascii_uppercase

        if include_numbers:
            chars += string.digits

        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # RANDOM PASSWORD MODE
        if mode == "Random Secure Password":

            password = ''.join(
                secrets.choice(chars)
                for _ in range(length)
            )

        # PERSONALIZED PASSWORD MODE
        else:

            if not user_name:
                st.error("Please enter a name or keyword.")
                st.stop()

            remaining_length = max(
                4,
                length - len(user_name)
            )

            random_part = ''.join(
                secrets.choice(chars)
                for _ in range(remaining_length)
            )

            combined = user_name + random_part

            password_list = list(combined)
            secrets.SystemRandom().shuffle(password_list)

            password = ''.join(password_list)

        st.success("✅ Password Generated")
        st.code(password)

        st.info(f"""
        Password Length: {len(password)}

        Security Tips:
        • Never share your password.
        • Use a different password for every account.
        • Enable Two-Factor Authentication (2FA).
        """)


# --- TOOL 5: SIEM LOG ANALYZER ---
elif menu_selection == NAV_SIEM:
    st.title("📊 SIEM Log Analyzer (SOC Engine)")
    st.write("Upload raw server, firewall, or authentication logs to detect brute-force attacks, unauthorized access, and anomalies.")

    # 1. File Uploader for Logs
    uploaded_log = st.file_uploader(
        "Upload a Log File (.txt, .log, .csv)", 
        type=["txt", "log", "csv"], 
        key="siem_log_uploader"
    )

    if uploaded_log is not None:
        if st.button("🚨 Initiate Threat Hunt", key="siem_analyze_btn"):
            with st.spinner("Parsing logs and applying heuristic detection rules..."):
                try:
                    import re
                    import time
                    from collections import Counter

                    # 1. Read and decode the log file
                    log_bytes = uploaded_log.read()
                    try:
                        log_content = log_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        log_content = log_bytes.decode('latin-1') # Fallback for weird log encodings

                    lines = log_content.split('\n')
                    total_events = len(lines)

                    # 2. Heuristic Rule Engine (Keyword & IP Extraction)
                    suspicious_keywords = ["failed", "error", "denied", "unauthorized", "invalid", "timeout", "blocked", "attack"]
                    
                    suspicious_logs = []
                    extracted_ips = []
                    
                    # Regex pattern to find IPv4 addresses
                    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

                    for line in lines:
                        lower_line = line.lower()
                        # Check if line contains any suspicious keywords
                        if any(keyword in lower_line for keyword in suspicious_keywords):
                            suspicious_logs.append(line)
                            
                        # Extract IPs from the suspicious lines
                        ips = ip_pattern.findall(line)
                        extracted_ips.extend(ips)

                    # Get the top 5 most common IPs to find potential brute-force sources
                    top_ips = Counter(extracted_ips).most_common(5)
                    top_ips_str = ", ".join([f"{ip} ({count}x)" for ip, count in top_ips])

                    # 3. Build the Visual SOC Dashboard
                    st.markdown("### 🖥️ Security Operations Center (SOC) Metrics")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Log Events", f"{total_events:,}")
                    col2.metric("Suspicious Events Flagged", f"{len(suspicious_logs):,}")
                    col3.metric("Unique IPs Detected", f"{len(set(extracted_ips)):,}")

                    # 4. AI SOC ANALYST ENGINE
                    # We only feed the first 100 suspicious logs to stay within token limits
                    logs_to_analyze = "\n".join(suspicious_logs[:100])
                    
                    if not logs_to_analyze.strip():
                        st.success("✅ **CLEAN LOG:** No standard suspicious keywords or attack patterns detected in this file.")
                    else:
                        st.markdown("### 🧠 AI Threat Intelligence Correlation")
                        with st.spinner("AI is correlating events and identifying attack vectors..."):
                            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                            model = genai.GenerativeModel('gemini-2.5-flash')

                            prompt = f"""
                            You are a Senior SOC Analyst. Analyze this extracted batch of suspicious server/firewall logs.
                            
                            Top Detected IP Addresses: {top_ips_str}
                            
                            Suspicious Log Snippet:
                            {logs_to_analyze[:3000]}

                            Task:
                            1. Identify if this represents a specific type of attack (e.g., SSH Brute Force, DDoS, SQL Injection, Port Scan).
                            2. Provide a verdict on the severity of the log data.
                            
                            Output EXACTLY in this format:
                            VERDICT: (SAFE / SUSPICIOUS / DANGEROUS)
                            EXPLANATION: (2-3 sentences explaining the attack pattern or anomaly found)
                            TECHNICAL FLAGS: (Bullet points of specific targeted ports, repeated IPs, or compromised accounts)
                            """

                            max_retries = 3
                            ai_analysis = None

                            for attempt in range(max_retries):
                                try:
                                    ai_analysis = model.generate_content(prompt).text
                                    break
                                except Exception as e:
                                    error_msg = str(e)
                                    if "429" in error_msg and attempt < max_retries - 1:
                                        match = re.search(r"retry in ([0-9.]+)s", error_msg)
                                        wait_time = float(match.group(1)) + 1.0 if match else 10.0
                                        st.warning(f"⏳ SOC Engine syncing. Pausing analysis for {int(wait_time)} seconds...")
                                        time.sleep(wait_time)
                                        continue
                                    st.error(f"SOC AI error: {e}")
                                    break

                            # 5. Display AI Results
                            if ai_analysis:
                                if "DANGEROUS" in ai_analysis.upper():
                                    st.error("🚨 **ACTIVE THREAT DETECTED:** High severity attack patterns found in logs!")
                                elif "SUSPICIOUS" in ai_analysis.upper():
                                    st.warning("⚠️ **ANOMALY DETECTED:** Unusual behavior observed. Investigation recommended.")
                                else:
                                    st.success("✅ **VERDICT:** Logs indicate normal operational errors. No malicious intent correlated.")

                                st.info(ai_analysis)
                                
                                # View Raw Data Expander
                                with st.expander("👁️ View Raw Suspicious Log Extracts"):
                                    st.code(logs_to_analyze[:1500] + "\n\n... [TRUNCATED FOR DISPLAY]", language="bash")

                                # 6. Generate PDF Incident Report
                                st.divider()
                                pdf_bytes_report = generate_reportlab_pdf(
                                    "SIEM Log Analyzer & Threat Hunt",
                                    uploaded_log.name,
                                    ai_analysis
                                )

                                st.download_button(
                                    label="📄 Download Official Incident Report (PDF)",
                                    data=pdf_bytes_report,
                                    file_name=f"Incident_Report_{uploaded_log.name}.pdf",
                                    mime="application/pdf",
                                    key="siem_report_btn"
                                )

                except Exception as e:
                    st.error(f"Failed to process log file: {e}")

# --- TOOL: NETWORK EXPOSURE SCANNER ---
elif menu_selection == NAV_NETWORK:
    st.title(f"{NAV_NETWORK}")
    st.write("Performs a safe perimeter audit on an IP address or domain to map open ports and evaluate external attack surfaces.")

    # 1. Target Input Layout
    target_input = st.text_input("Enter Target Domain or IP Address (e.g., scanme.nmap.org or 8.8.8.8)", placeholder="scanme.nmap.org")
    
    # 2. Main Logic Execution
    if target_input:
        # Clean target string (remove http/https prefixes if user pastes a URL)
        target_clean = target_input.replace("https://", "").replace("http://", "").split("/")[0].strip()

        if st.button("🚀 Launch Perimeter Audit", key="network_scan_btn"):
            with st.spinner(f"Resolving host and auditing network ports for {target_clean}..."):
                try:
                    import socket
                    import time
                    import re

                    # Resolve Domain to IP address
                    try:
                        target_ip = socket.gethostbyname(target_clean)
                        st.caption(f"📍 Target resolved to IP: `{target_ip}`")
                    except socket.gaierror:
                        st.error("❌ **DNS Resolution Error:** Unable to resolve host domain name. Verify the address.")
                        st.stop()

                    # Define common high-risk or administrative ports to audit
                    target_ports = {
                        21: "FTP (File Transfer)",
                        22: "SSH (Secure Shell)",
                        23: "Telnet (Unencrypted Management)",
                        25: "SMTP (Email System)",
                        53: "DNS (Domain Name System)",
                        80: "HTTP (Web Server)",
                        110: "POP3 (Email Retrieval)",
                        443: "HTTPS (Secure Web Server)",
                        445: "SMB (File Sharing / High Risk)",
                        1433: "MSSQL (Database Engine)",
                        3306: "MySQL (Database Engine)",
                        3389: "RDP (Remote Desktop Protocol)",
                        8080: "HTTP-Proxy / Alternate Web"
                    }

                    open_ports = []
                    closed_count = 0

                    # Run structural socket port test connection loops
                    start_time = time.time()
                    for port, service in target_ports.items():
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.6) 
                        
                        result = s.connect_ex((target_ip, port))
                        if result == 0:
                            open_ports.append(f"Port {port} ({service})")
                        else:
                            closed_count += 1
                        s.close()
                    
                    scan_duration = time.time() - start_time

                    # 3. Render Dashboard Metrics
                    st.markdown("### 🖥️ Network Reconnaissance Summary")
                    m_col1, m_col2, m_col3 = st.columns(3)
                    m_col1.metric("Audited Ports", len(target_ports))
                    m_col2.metric("Exposed Ports Found", len(open_ports), delta=len(open_ports), delta_color="inverse")
                    m_col3.metric("Scan Speed Time", f"{scan_duration:.2f}s")

                    # Display open port flags to user interface immediately
                    if open_ports:
                        st.warning("⚠️ **Exposed Entryways Identified:**")
                        for p in open_ports:
                            st.write(f"▪️ `{p}` is responding to connection attempts.")
                    else:
                        st.success("🔒 No critical administrative entry ports responded during this lightweight scan.")

                    # 4. AI THREAT SURFACE ASSESSMENT ENGINE
                    st.markdown("### 🧠 AI Attack Surface Intelligence Correlation")
                    with st.spinner("Analyzing open port signatures against active exploitation vectors..."):
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                        model = genai.GenerativeModel('gemini-2.5-flash')

                        prompt = f"""
                        You are an expert Network Penetration Tester. Analyze this basic perimeter scan profile:
                        
                        Target: {target_clean} ({target_ip})
                        Exposed Open Ports Found: {open_ports if open_ports else "None Detected"}
                        Total Closed Core Ports: {closed_count}

                        Task:
                        Evaluate what risk profile this exposure creates. If high risk protocols like FTP, Telnet, RDP (3389), or SMB (445) are open, highlight potential exploitation strategies (brute force, sniffing, ransomware deployment). If only 80/443 are open, confirm standard web behavior.

                        Output EXACTLY in this formatting layout:
                        VERDICT: (SAFE / SUSPICIOUS / DANGEROUS)
                        EXPLANATION: (2 clear sentences breaking down network service exposure risks)
                        TECHNICAL FLAGS: (Bullet points detailing vulnerabilities, outdated protocols, or defensive perimeter improvements)
                        """

                        max_retries = 3
                        ai_analysis = None

                        for attempt in range(max_retries):
                            try:
                                ai_analysis = model.generate_content(prompt).text
                                break
                            except Exception as e:
                                error_msg = str(e)
                                if "429" in error_msg and attempt < max_retries - 1:
                                    match = re.search(r"retry in ([0-9.]+)s", error_msg)
                                    wait_time = float(match.group(1)) + 1.0 if match else 10.0
                                    st.warning(f"⏳ Syncing threat database. Pausing scanner for {int(wait_time)} seconds...")
                                    time.sleep(wait_time)
                                    continue
                                st.error(f"Network Intelligence AI Error: {e}")
                                break

                        # 5. Display AI Perimeter Threat Evaluation Results
                        if ai_analysis:
                            if "DANGEROUS" in ai_analysis.upper() or len(open_ports) > 3:
                                st.error("🚨 **CRITICAL PERIMETER EXPOSURE:** High-risk protocols or overly loose server access controls identified!")
                            elif "SUSPICIOUS" in ai_analysis.upper():
                                st.warning("⚠️ **ATTACK SURFACE WARNING:** Exposed entry paths found that require patch management or firewall filtering.")
                            else:
                                st.success("✅ **VERDICT:** Minimal network exposure footprint. Perimeter matches baseline security hardening practices.")

                            st.info(ai_analysis)

                            # 6. Generate Structural Download PDF Security Report
                            st.divider()
                            
                            def generate_reportlab_pdf(tool_name, filename, analysis_text):
                                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                                from reportlab.lib.styles import getSampleStyleSheet
                                from io import BytesIO

                                buffer = BytesIO()
                                doc = SimpleDocTemplate(buffer)
                                styles = getSampleStyleSheet()
                                content = []

                                content.append(Paragraph(f"<b>{tool_name}</b>", styles["Title"]))
                                content.append(Spacer(1, 12))
                                content.append(Paragraph(f"<b>Target Evaluated:</b> {filename}", styles["Normal"]))
                                content.append(Spacer(1, 12))
                                content.append(Paragraph("<b>AI Security Analysis:</b>", styles["Heading2"]))
                                content.append(Spacer(1, 8))

                                safe_text = analysis_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
                                content.append(Paragraph(safe_text, styles["Normal"]))

                                doc.build(content)
                                buffer.seek(0)
                                return buffer.read()

                            pdf_bytes_report = generate_reportlab_pdf(
                                "Network Exposure & Attack Surface Assessment",
                                target_clean,
                                ai_analysis
                            )

                            st.download_button(
                                label="📄 Download Network Audit Report (PDF)",
                                data=pdf_bytes_report,
                                file_name=f"Network_Report_{target_clean}.pdf",
                                mime="application/pdf",
                                key="network_scanner_report_btn"
                            )

                except Exception as e:
                    st.error(f"Failed to compile structural network scan: {e}")


# --- TOOL: AI SECURITY ASSISTANT ---
elif menu_selection == NAV_AI:
  
    render_tool_intro(
        "◇ AI Security Assistant",
        "Ask cyber-safety questions in plain language. The assistant can explain scams, account protection steps, phishing signs, and safer online habits.",
        "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
        [
            "Understanding suspicious messages or links",
            "Learning how to secure email, banking, and social accounts",
            "Getting simple explanations of cyber-security terms"
        ],
        "Tip: never paste real passwords, OTPs, API keys, or private bank details into any chat."
    )

    # Configure Gemini
    # Replace with your actual API key or use st.secrets
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your security assistant. How can I help you stay safe today?"}
        ]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a security question..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Optional: Add system instructions to keep the bot focused on security
                    response = model.generate_content(
                        f"You are a helpful security expert. Answer this question: {prompt}"
                    )
                    full_response = response.text
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Error: {e}")


# --- TOOL 13: AI SECURITY QUESTIONS QUIZ ---
elif menu_selection == NAV_QUIZ:
    st.title(f"{NAV_QUIZ}")
    st.write("Test your cybersecurity knowledge with real-time, dynamic multiple-choice questions generated completely by Gemini AI.")

    import json
    import re
    import time

    # Initialize Session States so the quiz state stays stable across clicks
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = None
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_topic" not in st.session_state:
        st.session_state.quiz_topic = "General Cybersecurity"

    # 1. Topic Selector
    selected_topic = st.selectbox(
        "Select Quiz Topic:",
        ["General Cybersecurity", "Phishing & Social Engineering", "Network Security", "Password & Identity Safety", "Malware & Ransomware"]
    )

    # If user changes the topic, reset the quiz state
    if selected_topic != st.session_state.quiz_topic:
        st.session_state.quiz_topic = selected_topic
        st.session_state.quiz_questions = None
        st.session_state.quiz_submitted = False

    # Button to generate the quiz
    if st.button("🔄 Generate Fresh AI Quiz", key="gen_quiz_btn") or st.session_state.quiz_questions is None:
        with st.spinner(f"Gemini AI is crafting unique questions about {selected_topic}..."):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # We force Gemini to output raw JSON so our Python code can parse the MCQs cleanly
                prompt = f"""
                You are a Cybersecurity Professor. Create exactly 3 multiple-choice questions (MCQs) regarding: "{selected_topic}".
                Each question must have exactly 4 options.
                
                You must return your output ONLY as a valid JSON array. Do not include any introductory or concluding text.
                Format structure:
                [
                  {{
                    "question": "The question text here?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_index": 0,
                    "explanation": "Why this option is correct."
                  }}
                ]
                Note: correct_index must be an integer from 0 to 3 matching the correct option index.
                """

                response_text = model.generate_content(prompt).text
                
                # Clean up any potential markdown wrappers (like ```json ... ```) that AI sometimes adds
                clean_json_text = re.sub(r"```json\s*|\s*```", "", response_text).strip()
                
                # Parse JSON and save it to the app's session memory
                st.session_state.quiz_questions = json.loads(clean_json_text)
                st.session_state.quiz_submitted = False
                st.rerun() # Refresh to draw the quiz elements cleanly
                
            except Exception as e:
                st.error(f"Failed to generate quiz. Please try again. Error: {e}")

elif current_nav == NAV_QUIZ:
    render_tool_intro(
        "🧠 AI Security Quiz",
        "Test your cybersecurity knowledge. Enter any topic, and our AI will generate a custom 3-question evaluation.",
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
        ["Customized threat scenarios", "Immediate feedback and explanations", "Downloadable certification scorecard"],
        "Powered by Gemini AI. Context is automatically mapped to cybersecurity domains."
    )

    # Initialize Session States for Quiz
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = None
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_topic" not in st.session_state:
        st.session_state.quiz_topic = ""

    # 1. Topic Input and AI Generation
    topic_input = st.text_input("Enter a topic (e.g., 'Phishing', 'Passwords', 'SMS', 'Cloud'):", placeholder="Type a topic here...")
    
    if st.button("Generate Quiz", type="primary"):
        if not topic_input:
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("🧠 AI is building your custom security assessment..."):
                try:
                    # THE UPGRADED AI LOGIC: Forcing the Cybersecurity Context
                    prompt = f"""
                    You are a strict Cybersecurity Training Instructor. The user wants a 3-question multiple-choice quiz about: '{topic_input}'.
                    
                    CRITICAL INSTRUCTION: You MUST map this topic to a cybersecurity threat, defense, or privacy context. 
                    - If they type "SMS", make the quiz about "SMS Phishing (Smishing)".
                    - If they type "Coffee", make it about "Public Wi-Fi risks at coffee shops".
                    - NEVER reject a topic. Always find the security angle.

                    Return EXACTLY this JSON format and nothing else. No markdown blocks, just raw JSON:
                    [
                        {{
                            "question": "The question text?",
                            "options": ["A", "B", "C", "D"],
                            "correct_index": 0,
                            "explanation": "Why this is correct."
                        }}
                    ]
                    Ensure there are exactly 3 questions.
                    """
                    
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    
                    # Clean the JSON response
                    raw_text = response.text.strip()
                    if raw_text.startswith("```json"):
                        raw_text = raw_text[7:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]
                        
                    import json
                    questions = json.loads(raw_text)
                    
                    # Save to session state
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_topic = topic_input
                    st.session_state.quiz_submitted = False
                    st.rerun()
                    except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "Quota" in error_msg:
                        st.warning("⏳ The AI engine is currently cooling down to prevent spam. Please wait 30 seconds and click Generate again.")
                    else:
                        st.error(f"⚠️ Failed to generate quiz. Try a slightly different word. Error details: {e}")

    # 2. Render the Quiz if questions are loaded
    if st.session_state.quiz_questions:
        st.markdown(f"### 📝 Topic: {st.session_state.quiz_topic}")
        st.write("Answer the questions below and click 'Submit Answers' to see your score.")
        
        user_selections = []
        
        # Display each question using Streamlit radio buttons
        for idx, q_data in enumerate(st.session_state.quiz_questions):
            st.markdown(f"**Q{idx+1}: {q_data['question']}**")
            
            # Disable changing answers after they click submit
            is_disabled = st.session_state.quiz_submitted
            
            user_choice = st.radio(
                f"Select option for Q{idx+1}:",
                options=q_data['options'],
                key=f"q_{idx}_input",
                disabled=is_disabled,
                label_visibility="collapsed"
            )
            # Track index of what option text the user picked
            chosen_index = q_data['options'].index(user_choice)
            user_selections.append(chosen_index)
            st.divider()

        # 3. Grade the Quiz
        if not st.session_state.quiz_submitted:
            if st.button("🎯 Submit Answers", key="submit_answers_btn"):
                st.session_state.quiz_submitted = True
                st.rerun()
                
        else:
            # Calculate Final Score
            correct_count = 0
            report_summary = f"Quiz Results - Topic: {st.session_state.quiz_topic}\n\n"
            
            st.markdown("### 📊 Quiz Evaluation & Feedback")
            
            for idx, q_data in enumerate(st.session_state.quiz_questions):
                user_ans_idx = user_selections[idx]
                correct_ans_idx = q_data['correct_index']
                
                report_summary += f"Question {idx+1}: {q_data['question']}\n"
                
                if user_ans_idx == correct_ans_idx:
                    correct_count += 1
                    st.success(f"✅ **Question {idx+1}: Correct!**")
                    report_summary += "Result: Correct\n"
                else:
                    st.error(f"❌ **Question {idx+1}: Incorrect**")
                    st.write(f"*Your Answer:* {q_data['options'][user_ans_idx]}")
                    st.write(f"*Correct Answer:* {q_data['options'][correct_ans_idx]}")
                    report_summary += f"Result: Incorrect (User picked: {q_data['options'][user_ans_idx]} | Correct: {q_data['options'][correct_ans_idx]})\n"
                    
                st.info(f"💡 *Explanation:* {q_data['explanation']}\n")
                report_summary += f"Explanation: {q_data['explanation']}\n\n"

            # Display final score metrics
            percentage = int((correct_count / len(st.session_state.quiz_questions)) * 100)
            st.metric("Your Total Score", f"{correct_count} / {len(st.session_state.quiz_questions)}", f"{percentage}% Accuracy")
            
            report_summary += f"Final Score: {correct_count}/{len(st.session_state.quiz_questions)} ({percentage}%)"

            # --- GENERATE PDF SCORECARD ---
            def generate_reportlab_pdf(tool_name, filename, analysis_text):
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                from io import BytesIO

                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer)
                styles = getSampleStyleSheet()
                content = []

                content.append(Paragraph(f"<b>{tool_name}</b>", styles["Title"]))
                content.append(Spacer(1, 12))
                content.append(Paragraph(f"<b>Category Tested:</b> {filename}", styles["Normal"]))
                content.append(Spacer(1, 12))
                content.append(Paragraph("<b>Detailed Scoring Breakdown:</b>", styles["Heading2"]))
                content.append(Spacer(1, 8))

                # Safe formatting for any generated characters
                safe_text = analysis_text.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
                content.append(Paragraph(safe_text, styles["Normal"]))

                doc.build(content)
                buffer.seek(0)
                return buffer.read()

            pdf_bytes_report = generate_reportlab_pdf(
                "CyberGuard Academy Knowledge Audit",
                st.session_state.quiz_topic,
                report_summary
            )
            
            st.download_button(
                label="📄 Download Quiz Score Certificate (PDF)", 
                data=pdf_bytes_report, 
                file_name=f"Quiz_Certificate_{st.session_state.quiz_topic.replace(' ', '_')}.pdf", 
                mime="application/pdf", 
                key="quiz_pdf_btn"
            )

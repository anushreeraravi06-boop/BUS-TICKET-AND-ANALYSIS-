# ============================================================
# BUS ANALYTICS - CRACKER HEADS
# COMPLETE APP - PART 1 OF 2
# ============================================================

from pathlib import Path
import base64
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="BUS ANALYTICS | CRACKER HEADS",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tickets.csv"

# ============================================================
# COLOUR PALETTE
# ============================================================

BURGUNDY = "#64243D"
PLUM = "#351324"
ROSE = "#C77B8C"
GOLD = "#D7A66B"
BACKGROUND = "#FFF8F5"
PINK = "#F8E6E5"
TEXT = "#30202A"
MUTED = "#604B55"

# ============================================================
# WEBSITE DESIGN
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

html, body, .stApp,
[data-testid="stAppViewContainer"] {
    background: #FFF8F5 !important;
    color: #30202A !important;
    font-family: 'DM Sans', Arial, sans-serif !important;
}

[data-testid="stAppViewContainer"] * {
    color: #30202A;
}

[data-testid="stHeader"] {
    background: #FFF8F5 !important;
}

.block-container {
    max-width: 1550px;
    padding-top: 1.3rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #F8E6E5 !important;
    border-right: 1px solid #E7C9D0;
}

[data-testid="stSidebar"] * {
    color: #351324 !important;
}

[data-testid="stSidebar"] button {
    border-radius: 12px !important;
    min-height: 42px;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] button[kind="primary"] {
    background: #64243D !important;
}

[data-testid="stSidebar"] button[kind="primary"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] button[kind="secondary"] {
    background: #FFF8F5 !important;
    border: 1px solid #E7C9D0 !important;
}

[data-testid="stSidebar"] button[kind="secondary"] * {
    color: #64243D !important;
}

h1, h2, h3, h4 {
    color: #64243D !important;
}

p, label, li {
    color: #30202A;
}

[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #E7D5D9;
    border-radius: 17px;
    padding: 16px;
}

[data-testid="stMetricLabel"] * {
    color: #604B55 !important;
}

[data-testid="stMetricValue"] * {
    color: #351324 !important;
    font-weight: 800 !important;
}

.stButton button[kind="primary"] {
    background: #64243D !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
}

.stButton button[kind="primary"] * {
    color: white !important;
}

.stDownloadButton button {
    background: #F3DDE1 !important;
    color: #64243D !important;
    border: 1px solid #E4C2CA !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
}

.stDownloadButton button * {
    color: #64243D !important;
}

[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid #E7C9D0 !important;
    border-radius: 13px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #64243D !important;
    background: white !important;
    font-weight: 700 !important;
}

[data-testid="stExpander"] [data-testid="stMarkdownContainer"] * {
    color: #30202A !important;
}

[data-testid="stAlert"] {
    background: #FFF0EF !important;
    border: 1px solid #E9C7CD !important;
}

[data-testid="stAlert"] * {
    color: #351324 !important;
}

[data-testid="stCaptionContainer"] * {
    color: #604B55 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E7D5D9;
    border-radius: 12px;
}

.hero {
    background: linear-gradient(110deg, #351324, #64243D);
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 22px;
}

.hero h1 {
    color: #FFF7F2 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 38px;
}

.hero p {
    color: #FCE9E8 !important;
}

.hero .eyebrow {
    color: #F2C9CE !important;
    font-weight: 700;
    letter-spacing: 2px;
    font-size: 12px;
}

.info-card {
    background: #FFFFFF;
    border: 1px solid #E7D5D9;
    border-radius: 17px;
    padding: 20px;
    margin-bottom: 12px;
}

.info-card h3 {
    color: #64243D !important;
}

.info-card p {
    color: #604B55 !important;
}

.section-heading {
    color: #64243D;
    font-weight: 800;
    font-size: 21px;
    margin-top: 20px;
    margin-bottom: 12px;
}

hr {
    border-color: #E7D5D9 !important;
}

@media(max-width: 768px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .hero {
        padding: 20px;
    }

    .hero h1 {
        font-size: 27px;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LANGUAGE DICTIONARY
# ============================================================

LANGUAGES = {
    "English": {
        "Home": "Home",
        "Ticket Records": "Ticket Records",
        "Dashboard": "Dashboard",
        "Route Analysis": "Route Analysis",
        "Revenue Analysis": "Revenue Analysis",
        "Passenger Insights": "Passenger Insights",
        "Demand Prediction": "Demand Prediction",
        "Smart Insights": "Smart Insights",
        "AI Website Assistant": "AI Website Assistant",
        "Reports": "Reports",
        "Upload Dataset": "Upload Dataset",
        "Navigation": "NAVIGATION",
        "Language": "Select Language",
        "Welcome": "Welcome to Bus Analytics",
        "Tagline": "Intelligent Bus Ticket Data Platform",
        "Tickets": "Total Tickets",
        "Passengers": "Total Passengers",
        "Revenue": "Total Revenue",
        "Routes": "Active Routes",
        "Trend": "Ticket Bookings Trend",
        "TopRoutes": "Top Routes by Tickets",
        "Explore": "Explore Your Analytics",
        "Search": "Search ticket, waybill or stop",
        "RouteFilter": "Filter by Route",
        "DateFilter": "Filter by Travel Date",
        "AllRoutes": "All Routes",
        "AllDates": "All Dates",
        "StartDate": "Start Date",
        "EndDate": "End Date",
        "Records": "Matching Records",
        "Download": "Download Filtered Records",
        "NoData": "Please upload a valid ticket dataset.",
        "ChooseFile": "Choose CSV File",
        "UseFile": "Use This Dataset",
        "Preview": "Dataset Preview",
        "Ask": "Ask Assistant",
        "Question": "Type your question here",
        "Footer": "Created by CRACKER HEADS",
        "Collected": "Collected Revenue",
        "Uncollected": "Uncollected Amount",
        "CollectionRate": "Collection Rate",
        "Busiest": "Busiest Recorded Hour",
        "NoTime": "No valid time information is available.",
        "NoRecords": "No records match your filters."
    },

    "ಕನ್ನಡ": {
        "Home": "ಮುಖಪುಟ",
        "Ticket Records": "ಟಿಕೆಟ್ ದಾಖಲೆಗಳು",
        "Dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "Route Analysis": "ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆ",
        "Revenue Analysis": "ಆದಾಯ ವಿಶ್ಲೇಷಣೆ",
        "Passenger Insights": "ಪ್ರಯಾಣಿಕರ ಮಾಹಿತಿ",
        "Demand Prediction": "ಬೇಡಿಕೆ ವಿಶ್ಲೇಷಣೆ",
        "Smart Insights": "ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳು",
        "AI Website Assistant": "AI ವೆಬ್‌ಸೈಟ್ ಸಹಾಯಕ",
        "Reports": "ವರದಿಗಳು",
        "Upload Dataset": "ಡೇಟಾಸೆಟ್ ಅಪ್‌ಲೋಡ್",
        "Navigation": "ನ್ಯಾವಿಗೇಶನ್",
        "Language": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
        "Welcome": "ಬಸ್ ಅನಾಲಿಟಿಕ್ಸ್‌ಗೆ ಸ್ವಾಗತ",
        "Tagline": "ಬುದ್ಧಿವಂತ ಬಸ್ ಟಿಕೆಟ್ ಡೇಟಾ ವೇದಿಕೆ",
        "Tickets": "ಒಟ್ಟು ಟಿಕೆಟ್‌ಗಳು",
        "Passengers": "ಒಟ್ಟು ಪ್ರಯಾಣಿಕರು",
        "Revenue": "ಒಟ್ಟು ಆದಾಯ",
        "Routes": "ಸಕ್ರಿಯ ಮಾರ್ಗಗಳು",
        "Trend": "ಟಿಕೆಟ್ ಬುಕ್ಕಿಂಗ್ ಪ್ರವೃತ್ತಿ",
        "TopRoutes": "ಹೆಚ್ಚಿನ ಟಿಕೆಟ್‌ಗಳ ಮಾರ್ಗಗಳು",
        "Explore": "ನಿಮ್ಮ ವಿಶ್ಲೇಷಣೆಯನ್ನು ಅನ್ವೇಷಿಸಿ",
        "Search": "ಟಿಕೆಟ್ ಅಥವಾ ಮಾರ್ಗ ಹುಡುಕಿ",
        "RouteFilter": "ಮಾರ್ಗದ ಪ್ರಕಾರ ಫಿಲ್ಟರ್",
        "DateFilter": "ಪ್ರಯಾಣದ ದಿನಾಂಕದ ಪ್ರಕಾರ ಫಿಲ್ಟರ್",
        "AllRoutes": "ಎಲ್ಲಾ ಮಾರ್ಗಗಳು",
        "AllDates": "ಎಲ್ಲಾ ದಿನಾಂಕಗಳು",
        "StartDate": "ಪ್ರಾರಂಭ ದಿನಾಂಕ",
        "EndDate": "ಅಂತಿಮ ದಿನಾಂಕ",
        "Records": "ಹೊಂದಾಣಿಕೆಯ ದಾಖಲೆಗಳು",
        "Download": "ದಾಖಲೆಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
        "NoData": "ದಯವಿಟ್ಟು ಮಾನ್ಯವಾದ ಟಿಕೆಟ್ ಡೇಟಾಸೆಟ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "ChooseFile": "CSV ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ",
        "UseFile": "ಈ ಡೇಟಾಸೆಟ್ ಬಳಸಿ",
        "Preview": "ಡೇಟಾಸೆಟ್ ಪೂರ್ವವೀಕ್ಷಣೆ",
        "Ask": "ಸಹಾಯಕರನ್ನು ಕೇಳಿ",
        "Question": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಟೈಪ್ ಮಾಡಿ",
        "Footer": "CRACKER HEADS ರಚನೆ",
        "Collected": "ಸಂಗ್ರಹಿಸಿದ ಆದಾಯ",
        "Uncollected": "ಸಂಗ್ರಹಿಸದ ಮೊತ್ತ",
        "CollectionRate": "ಸಂಗ್ರಹ ದರ",
        "Busiest": "ಅತ್ಯಂತ ಕಾರ್ಯನಿರತ ಸಮಯ",
        "NoTime": "ಮಾನ್ಯವಾದ ಸಮಯದ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.",
        "NoRecords": "ಯಾವುದೇ ದಾಖಲೆಗಳು ಹೊಂದಿಕೆಯಾಗಿಲ್ಲ."
    },

    "हिन्दी": {
        "Home": "होम",
        "Ticket Records": "टिकट रिकॉर्ड",
        "Dashboard": "डैशबोर्ड",
        "Route Analysis": "रूट विश्लेषण",
        "Revenue Analysis": "राजस्व विश्लेषण",
        "Passenger Insights": "यात्री जानकारी",
        "Demand Prediction": "मांग विश्लेषण",
        "Smart Insights": "स्मार्ट इनसाइट्स",
        "AI Website Assistant": "AI वेबसाइट सहायक",
        "Reports": "रिपोर्ट",
        "Upload Dataset": "डेटासेट अपलोड",
        "Navigation": "नेविगेशन",
        "Language": "भाषा चुनें",
        "Welcome": "बस एनालिटिक्स में आपका स्वागत है",
        "Tagline": "इंटेलिजेंट बस टिकट डेटा प्लेटफॉर्म",
        "Tickets": "कुल टिकट",
        "Passengers": "कुल यात्री",
        "Revenue": "कुल राजस्व",
        "Routes": "सक्रिय रूट",
        "Trend": "टिकट बुकिंग का रुझान",
        "TopRoutes": "सबसे अधिक टिकट वाले रूट",
        "Explore": "अपने एनालिटिक्स को देखें",
        "Search": "टिकट या रूट खोजें",
        "RouteFilter": "रूट के अनुसार फ़िल्टर",
        "DateFilter": "यात्रा की तारीख के अनुसार फ़िल्टर",
        "AllRoutes": "सभी रूट",
        "AllDates": "सभी तारीखें",
        "StartDate": "शुरुआती तारीख",
        "EndDate": "अंतिम तारीख",
        "Records": "मिलते हुए रिकॉर्ड",
        "Download": "रिकॉर्ड डाउनलोड करें",
        "NoData": "कृपया एक मान्य टिकट डेटासेट अपलोड करें।",
        "ChooseFile": "CSV फ़ाइल चुनें",
        "UseFile": "इस डेटासेट का उपयोग करें",
        "Preview": "डेटासेट पूर्वावलोकन",
        "Ask": "सहायक से पूछें",
        "Question": "अपना प्रश्न यहाँ लिखें",
        "Footer": "CRACKER HEADS द्वारा निर्मित",
        "Collected": "एकत्रित राजस्व",
        "Uncollected": "अवैतनिक राशि",
        "CollectionRate": "संग्रह दर",
        "Busiest": "सबसे व्यस्त दर्ज समय",
        "NoTime": "समय की मान्य जानकारी उपलब्ध नहीं है।",
        "NoRecords": "कोई रिकॉर्ड नहीं मिला।"
    }
}

# ============================================================
# LANGUAGE HELPER
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "page" not in st.session_state:
    st.session_state.page = "Home"

def T(key):
    return LANGUAGES[st.session_state.language].get(
        key,
        LANGUAGES["English"].get(key, key)
    )

# ============================================================
# LOGO SPLASH SCREEN
# ============================================================

if "splash_seen" not in st.session_state:
    st.session_state.splash_seen = False

if not st.session_state.splash_seen:

    splash = st.empty()

    logo_path = ROOT / "logo.png.jpeg"

    if not logo_path.exists():
        logo_path = ROOT / "brand_panel.png.jpeg"

    if logo_path.exists():
        try:
            encoded = base64.b64encode(
                logo_path.read_bytes()
            ).decode("utf-8")

            logo_html = (
                '<img src="data:image/jpeg;base64,'
                + encoded
                + '" style="width:220px;max-height:190px;'
                + 'object-fit:contain;">'
            )
        except Exception:
            logo_html = "<div style='font-size:75px'>🚌</div>"
    else:
        logo_html = "<div style='font-size:75px'>🚌</div>"

    splash.markdown(
        "<div style='position:fixed;inset:0;z-index:999999;"
        "background:#F8E6E5;display:flex;flex-direction:column;"
        "align-items:center;justify-content:center;text-align:center;'>"
        + logo_html
        + "<h1 style='color:#64243D !important;'>BUS ANALYTICS</h1>"
        + "<p style='color:#351324 !important;'>"
        + "Intelligent Bus Ticket Data Platform</p>"
        + "<p style='color:#64243D !important;font-weight:bold;'>"
        + "BOOK • ANALYZE • PREDICT</p>"
        + "<p style='color:#64243D !important;'>"
        + "Created by CRACKER HEADS</p></div>",
        unsafe_allow_html=True
    )

    time.sleep(2)
    splash.empty()
    st.session_state.splash_seen = True

# ============================================================
# DATA PREPARATION
# ============================================================

def find_column(df, names):
    columns = {
        str(c).strip().lower(): c
        for c in df.columns
    }

    for name in names:
        if name.lower() in columns:
            return columns[name.lower()]

    for name in names:
        for key, original in columns.items():
            if name.lower() in key:
                return original

    return None


def prepare_data(raw):
    df = raw.copy()

    aliases = {
        "waybill": ["Waybill Number", "Waybill"],
        "ticket": ["Ticket Number", "Ticket No"],
        "from_stop": ["From Stop", "From", "Origin"],
        "to_stop": ["To Stop", "To", "Destination"],
        "date": ["Date", "Journey Date", "Travel Date"],
        "time": ["Time", "Journey Time"],
        "passengers": [
            "Total Psgr", "Total Passenger",
            "Passengers", "Passenger Count"
        ],
        "collected": [
            "Coll Amt", "Collected Amount",
            "Fare", "Amount Collected"
        ],
        "uncollected": [
            "Uncoll Amt", "Uncollected Amount",
            "Pending Amount"
        ]
    }

    selected = {
        key: find_column(df, values)
        for key, values in aliases.items()
    }

    required = [
        "from_stop", "to_stop", "date",
        "passengers", "collected"
    ]

    missing = [
        key for key in required
        if selected[key] is None
    ]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    result = pd.DataFrame()

    for key, source in selected.items():
        if source is not None:
            result[key] = df[source]
        elif key in ["waybill", "ticket", "time"]:
            result[key] = ""
        else:
            result[key] = 0

    result["from_stop"] = (
        result["from_stop"].fillna("Unknown").astype(str).str.strip()
    )

    result["to_stop"] = (
        result["to_stop"].fillna("Unknown").astype(str).str.strip()
    )

    result["route"] = (
        result["from_stop"] + " – " + result["to_stop"]
    )

    result["date"] = pd.to_datetime(
        result["date"],
        errors="coerce",
        dayfirst=True
    )

    for column in ["passengers", "collected", "uncollected"]:
        result[column] = pd.to_numeric(
            result[column],
            errors="coerce"
        ).fillna(0).clip(lower=0)

    for column in ["waybill", "ticket", "time"]:
        result[column] = (
            result[column].fillna("").astype(str)
        )

    result = result.dropna(subset=["date"])

    return result


# ============================================================
# LOAD DATASET
# ============================================================

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

raw_data = st.session_state.uploaded_data

if raw_data is None and DATA_FILE.exists():
    try:
        raw_data = pd.read_csv(DATA_FILE)
    except Exception as error:
        st.error("Dataset loading error: " + str(error))

if raw_data is not None:
    try:
        data = prepare_data(raw_data)
        data_error = None
    except Exception as error:
        data = pd.DataFrame()
        data_error = str(error)
else:
    data = pd.DataFrame()
    data_error = "No dataset found. Please upload a CSV file."


# ============================================================
# COMMON HELPERS
# ============================================================

def money(value):
    return "₹{:,.2f}".format(float(value))


def chart_style(fig, height=370):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            color="#351324",
            size=13
        ),
        margin=dict(l=15, r=20, t=55, b=25),
        title_font=dict(color="#64243D", size=18)
    )

    fig.update_xaxes(
        tickfont=dict(color="#351324"),
        title_font=dict(color="#64243D"),
        gridcolor="#EADDE0"
    )

    fig.update_yaxes(
        tickfont=dict(color="#351324"),
        title_font=dict(color="#64243D"),
        gridcolor="#EADDE0"
    )

    return fig


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    logo = ROOT / "brand_panel.png.jpeg"

    if not logo.exists():
        logo = ROOT / "logo.png.jpeg"

    if logo.exists():
        st.image(str(logo), use_container_width=True)
    else:
        st.markdown("## 🚌 BUS ANALYTICS")

    st.divider()

    languages = ["English", "ಕನ್ನಡ", "हिन्दी"]

    selected_language = st.selectbox(
        T("Language"),
        languages,
        index=languages.index(st.session_state.language)
    )

    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

    st.markdown("### " + T("Navigation"))

    pages = [
        "Home",
        "Ticket Records",
        "Dashboard",
        "Route Analysis",
        "Revenue Analysis",
        "Passenger Insights",
        "Demand Prediction",
        "Smart Insights",
        "AI Website Assistant",
        "Reports",
        "Upload Dataset"
    ]

    icons = {
        "Home": "⌂",
        "Ticket Records": "▤",
        "Dashboard": "▦",
        "Route Analysis": "⌁",
        "Revenue Analysis": "₹",
        "Passenger Insights": "♙",
        "Demand Prediction": "↗",
        "Smart Insights": "✧",
        "AI Website Assistant": "✦",
        "Reports": "▧",
        "Upload Dataset": "⇧"
    }

    for item in pages:

        if st.button(
            icons[item] + "  " + T(item),
            key="nav_" + item,
            type=(
                "primary"
                if st.session_state.page == item
                else "secondary"
            ),
            use_container_width=True
        ):
            st.session_state.page = item
            st.rerun()

    st.divider()

    st.markdown("**BOOK • ANALYZE • PREDICT**")
    st.caption(T("Footer"))


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.page

st.markdown(
    "<p style='color:#64243D;font-weight:800;"
    "letter-spacing:1px;'>🚌 BUS ANALYTICS</p>",
    unsafe_allow_html=True
)

if data_error and page != "Upload Dataset":
    st.warning(data_error)


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.markdown(
        "<div class='hero'>"
        "<div class='eyebrow'>" + T("Tagline") + "</div>"
        "<h1>" + T("Welcome") + "</h1>"
        "<p>BOOK • ANALYZE • PREDICT</p>"
        "</div>",
        unsafe_allow_html=True
    )

    if data.empty:
        st.info(T("NoData"))

    else:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(T("Tickets"), f"{len(data):,}")

        c2.metric(
            T("Passengers"),
            f"{int(data['passengers'].sum()):,}"
        )

        c3.metric(
            T("Revenue"),
            money(data["collected"].sum())
        )

        c4.metric(
            T("Routes"),
            f"{data['route'].nunique():,}"
        )

        st.markdown(
            "<div class='section-heading'>"
            + T("Explore")
            + "</div>",
            unsafe_allow_html=True
        )

        left, right = st.columns([1.2, 1])

        with left:

            trend = (
                data.groupby(data["date"].dt.date)
                .size()
                .reset_index(name="Tickets")
            )

            trend.columns = ["Date", "Tickets"]

            fig = px.area(
                trend,
                x="Date",
                y="Tickets",
                title=T("Trend")
            )

            fig.update_traces(
                line_color=BURGUNDY,
                fillcolor="rgba(199,123,140,0.25)"
            )

            st.plotly_chart(
                chart_style(fig),
                use_container_width=True
            )

        with right:

            top = (
                data.groupby("route")
                .size()
                .reset_index(name="Tickets")
                .nlargest(8, "Tickets")
                .sort_values("Tickets")
            )

            fig = px.bar(
                top,
                x="Tickets",
                y="route",
                orientation="h",
                title=T("TopRoutes"),
                color_discrete_sequence=[ROSE]
            )

            st.plotly_chart(
                chart_style(fig),
                use_container_width=True
            )


# ============================================================
# TICKET RECORDS
# ============================================================

elif page == "Ticket Records":

    st.title(T("Ticket Records"))

    if data.empty:
        st.warning(T("NoData"))

    else:

        search = st.text_input(T("Search"))

        routes = [T("AllRoutes")] + sorted(
            data["route"].dropna().unique().tolist()
        )

        selected_route = st.selectbox(
            T("RouteFilter"),
            routes
        )

        st.markdown("#### " + T("DateFilter"))

        min_date = data["date"].min().date()
        max_date = data["date"].max().date()

        date_mode = st.radio(
            T("DateFilter"),
            [T("AllDates"), "Select Date Range"],
            horizontal=True,
            label_visibility="collapsed"
        )

        selected_dates = None

        if date_mode != T("AllDates"):

            selected_dates = st.date_input(
                T("DateFilter"),
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                format="DD/MM/YYYY"
            )

        filtered = data.copy()

        if selected_route != T("AllRoutes"):
            filtered = filtered[
                filtered["route"] == selected_route
            ]

        if selected_dates:

            if isinstance(selected_dates, (tuple, list)):

                if len(selected_dates) == 2:

                    start_date, end_date = selected_dates

                    filtered = filtered[
                        (filtered["date"].dt.date >= start_date)
                        & (filtered["date"].dt.date <= end_date)
                    ]

                elif len(selected_dates) == 1:

                    filtered = filtered[
                        filtered["date"].dt.date == selected_dates[0]
                    ]

            else:

                filtered = filtered[
                    filtered["date"].dt.date == selected_dates
                ]

        if search.strip():

            mask = filtered.astype(str).apply(
                lambda column: column.str.contains(
                    search.strip(),
                    case=False,
                    na=False
                )
            ).any(axis=1)

            filtered = filtered[mask]

        st.metric(T("Records"), f"{len(filtered):,}")

        display = filtered.rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from_stop": "From Stop",
            "to_stop": "To Stop",
            "route": "Route",
            "date": "Date",
            "time": "Time",
            "passengers": "Total Passengers",
            "collected": "Collected Amount",
            "uncollected": "Uncollected Amount"
        })

        if filtered.empty:
            st.info(T("NoRecords"))

        else:

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                T("Download"),
                display.to_csv(index=False).encode("utf-8"),
                "filtered_ticket_records.csv",
                "text/csv"
            )


# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.title(T("Dashboard"))

    if data.empty:
        st.warning(T("NoData"))

    else:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(T("Tickets"), f"{len(data):,}")

        c2.metric(
            T("Passengers"),
            f"{int(data['passengers'].sum()):,}"
        )

        c3.metric(
            T("Collected"),
            money(data["collected"].sum())
        )

        c4.metric(
            T("Uncollected"),
            money(data["uncollected"].sum())
        )

        summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum")
            )
            .reset_index()
            .sort_values("Tickets", ascending=False)
        )

        fig = px.bar(
            summary.head(12),
            x="route",
            y="Tickets",
            title="Route-wise Ticket Performance",
            color_discrete_sequence=[BURGUNDY]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )


# ============================================================
# ROUTE ANALYSIS
# ============================================================

elif page == "Route Analysis":

    st.title(T("Route Analysis"))

    if data.empty:
        st.warning(T("NoData"))

    else:

        summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        total_tickets = max(summary["Tickets"].sum(), 1)
        total_passengers = max(summary["Passengers"].sum(), 1)
        total_revenue = max(summary["Revenue"].sum(), 1)

        summary["Performance Score"] = (
            35 * summary["Tickets"] / total_tickets
            + 35 * summary["Passengers"] / total_passengers
            + 30 * summary["Revenue"] / total_revenue
        ) * 100

        top = summary.sort_values(
            "Performance Score",
            ascending=False
        )

        fig = px.bar(
            top.head(12).sort_values("Performance Score"),
            x="Performance Score",
            y="route",
            orientation="h",
            title="Route Performance Score",
            color_discrete_sequence=[ROSE]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

        st.dataframe(
            top.round(2),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# REVENUE ANALYSIS
# ============================================================

elif page == "Revenue Analysis":

    st.title(T("Revenue Analysis"))

    if data.empty:
        st.warning(T("NoData"))

    else:

        collected = data["collected"].sum()
        pending = data["uncollected"].sum()

        total = collected + pending

        rate = collected / total * 100 if total else 0

        a, b, c = st.columns(3)

        a.metric(T("Collected"), money(collected))
        b.metric(T("Uncollected"), money(pending))
        c.metric(T("CollectionRate"), f"{rate:.2f}%")

        summary = (
            data.groupby("route")
            .agg(
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        fig = px.bar(
            summary,
            x="route",
            y=["Collected", "Uncollected"],
            barmode="group",
            title="Collected vs Uncollected Revenue",
            color_discrete_sequence=[BURGUNDY, ROSE]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PASSENGER INSIGHTS
# ============================================================

elif page == "Passenger Insights":

    st.title(T("Passenger Insights"))

    if data.empty:
        st.warning(T("NoData"))

    else:

        a, b = st.columns(2)

        a.metric(
            T("Passengers"),
            f"{int(data['passengers'].sum()):,}"
        )

        b.metric(
            "Average Passengers per Ticket",
            f"{data['passengers'].mean():.2f}"
        )

        summary = (
            data.groupby("route")["passengers"]
            .sum()
            .reset_index()
            .sort_values("passengers", ascending=False)
        )

        fig = px.bar(
            summary.head(12),
            x="route",
            y="passengers",
            title="Passengers by Route",
            color_discrete_sequence=[ROSE]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

        fig = px.histogram(
            data,
            x="passengers",
            nbins=15,
            title="Passenger Distribution",
            color_discrete_sequence=[BURGUNDY]
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )


# ============================================================
# DEMAND PREDICTION
# ============================================================

elif page == "Demand Prediction":

    st.title(T("Demand Prediction"))

    st.caption(
        "Historical demand analysis based on recorded ticket times. "
        "This is not a guaranteed future forecast."
    )

    if data.empty:
        st.warning(T("NoData"))

    else:

        time_data = data.copy()

        time_data["hour"] = pd.to_datetime(
            time_data["time"].astype(str),
            errors="coerce"
        ).dt.hour

        time_data = time_data.dropna(subset=["hour"])

        if time_data.empty:

            st.warning(T("NoTime"))

        else:

            time_data["hour"] = time_data["hour"].astype(int)

            hourly = (
                time_data.groupby("hour")
                .agg(
                    Tickets=("ticket", "count"),
                    Passengers=("passengers", "sum"),
                    Revenue=("collected", "sum")
                )
                .reset_index()
            )

            busiest = hourly.loc[hourly["Tickets"].idxmax()]

            st.metric(
                T("Busiest"),
                f"{int(busiest['hour']):02d}:00"
            )

            fig = px.bar(
                hourly,
                x="hour",
                y="Tickets",
                title="Hourly Ticket Demand",
                color_discrete_sequence=[BURGUNDY]
            )

            st.plotly_chart(
                chart_style(fig),
                use_container_width=True
            )

            fig = px.line(
                hourly,
                x="hour",
                y="Passengers",
                markers=True,
                title="Hourly Passenger Movement"
            )

            fig.update_traces(line_color=ROSE)

            st.plotly_chart(
                chart_style(fig),
                use_container_width=True
            )

            st.dataframe(
                hourly,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# SMART INSIGHTS - SIX FEATURES
# ============================================================

elif page == "Smart Insights":

    st.title(T("Smart Insights"))

    st.caption(
        "Statistical analysis and rule-based recommendations "
        "generated from the uploaded ticket data."
    )

    if data.empty:

        st.warning(T("NoData"))

    else:

        summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        # 1. DEMAND RECOMMENDATIONS

        with st.expander(
            "✧ " + (
                "1. Smart Demand Recommendations"
                if st.session_state.language == "English"
                else "1. ಸ್ಮಾರ್ಟ್ ಬೇಡಿಕೆ ಶಿಫಾರಸುಗಳು"
                if st.session_state.language == "ಕನ್ನಡ"
                else "1. स्मार्ट मांग सुझाव"
            )
        ):

            top = summary.nlargest(5, "Tickets")

            st.markdown("### High-demand routes")

            st.dataframe(
                top,
                use_container_width=True,
                hide_index=True
            )

            st.success(
                "Review bus frequency and capacity on routes "
                "with higher recorded ticket activity."
            )

        # 2. ROUTE INTELLIGENCE

        with st.expander(
            "⌁ " + (
                "2. Route Intelligence"
                if st.session_state.language == "English"
                else "2. ಮಾರ್ಗ ಬುದ್ಧಿವಂತಿಕೆ"
                if st.session_state.language == "ಕನ್ನಡ"
                else "2. रूट इंटेलिजेंस"
            )
        ):

            st.dataframe(
                summary.sort_values(
                    "Tickets",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

            low = summary.nsmallest(1, "Tickets").iloc[0]

            st.info(
                f"Lowest recorded ticket activity: {low['route']} "
                f"({int(low['Tickets'])} tickets). "
                "Review demand before changing service frequency."
            )

        # 3. REVENUE INTELLIGENCE

        with st.expander(
            "₹ " + (
                "3. Revenue Intelligence"
                if st.session_state.language == "English"
                else "3. ಆದಾಯ ಬುದ್ಧಿವಂತಿಕೆ"
                if st.session_state.language == "ಕನ್ನಡ"
                else "3. राजस्व इंटेलिजेंस"
            )
        ):

            collected = data["collected"].sum()
            pending = data["uncollected"].sum()

            total = collected + pending

            rate = collected / total * 100 if total else 0

            a, b, c = st.columns(3)

            a.metric(T("Collected"), money(collected))
            b.metric(T("Uncollected"), money(pending))
            c.metric(T("CollectionRate"), f"{rate:.2f}%")

            st.dataframe(
                summary.sort_values(
                    "Revenue",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

        # 4. PEAK-HOUR INTELLIGENCE AND HEATMAP

        with st.expander(
            "◷ " + (
                "4. Peak-Hour Intelligence & Heatmap"
                if st.session_state.language == "English"
                else "4. ಗರಿಷ್ಠ ಸಮಯ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಹೀಟ್‌ಮ್ಯಾಪ್"
                if st.session_state.language == "ಕನ್ನಡ"
                else "4. व्यस्त समय विश्लेषण और हीटमैप"
            )
        ):

            time_data = data.copy()

            time_data["hour"] = pd.to_datetime(
                time_data["time"].astype(str),
                errors="coerce"
            ).dt.hour

            time_data = time_data.dropna(subset=["hour"])

            if time_data.empty:

                st.warning(T("NoTime"))

            else:

                time_data["hour"] = time_data["hour"].astype(int)

                hourly = (
                    time_data.groupby("hour")
                    .size()
                    .reset_index(name="Tickets")
                )

                busiest = hourly.loc[hourly["Tickets"].idxmax()]

                st.metric(
                    T("Busiest"),
                    f"{int(busiest['hour']):02d}:00"
                )

                fig = px.bar(
                    hourly,
                    x="hour",
                    y="Tickets",
                    title="Peak-Hour Ticket Activity",
                    color="Tickets",
                    color_continuous_scale=[
                        "#F8E6E5", "#C77B8C", "#64243D"
                    ]
                )

                st.plotly_chart(
                    chart_style(fig),
                    use_container_width=True
                )

                time_data["travel_date"] = (
                    time_data["date"].dt.strftime("%d-%m-%Y")
                )

                heat = (
                    time_data.groupby(
                        ["travel_date", "hour"]
                    )
                    .size()
                    .reset_index(name="Tickets")
                )

                pivot = heat.pivot(
                    index="travel_date",
                    columns="hour",
                    values="Tickets"
                ).fillna(0)

                fig = px.imshow(
                    pivot,
                    aspect="auto",
                    title="Passenger Demand Heatmap",
                    color_continuous_scale=[
                        "#F8E6E5", "#C77B8C", "#64243D"
                    ]
                )

                st.plotly_chart(
                    chart_style(fig, 350),
                    use_container_width=True
                )

        # 5. UNUSUAL ACTIVITY DETECTION

        with st.expander(
            "⚑ " + (
                "5. Unusual Activity Detection"
                if st.session_state.language == "English"
                else "5. ಅಸಾಮಾನ್ಯ ಚಟುವಟಿಕೆ ಪತ್ತೆ"
                if st.session_state.language == "ಕನ್ನಡ"
                else "5. असामान्य गतिविधि पहचान"
            )
        ):

            if len(summary) >= 3:

                mean = summary["Tickets"].mean()
                std = summary["Tickets"].std()

                if std > 0:

                    unusual = summary[
                        (summary["Tickets"] - mean).abs()
                        > 2 * std
                    ]

                else:

                    unusual = summary.iloc[0:0]

                if unusual.empty:

                    st.success(
                        "No unusual ticket-count outliers detected."
                    )

                else:

                    st.warning(
                        "The following routes have unusual "
                        "ticket counts and should be reviewed."
                    )

                    st.dataframe(
                        unusual,
                        use_container_width=True,
                        hide_index=True
                    )

            else:

                st.info(
                    "At least three routes are required "
                    "for this statistical comparison."
                )

            st.caption(
                "An unusual value is only a statistical warning. "
                "It does not prove fraud or misconduct."
            )

        # 6. MANAGEMENT RECOMMENDATIONS

        with st.expander(
            "✦ " + (
                "6. Management Recommendations"
                if st.session_state.language == "English"
                else "6. ನಿರ್ವಹಣಾ ಶಿಫಾರಸುಗಳು"
                if st.session_state.language == "ಕನ್ನಡ"
                else "6. प्रबंधन सुझाव"
            )
        ):

            top_route = summary.nlargest(
                1,
                "Tickets"
            ).iloc[0]

            st.markdown("### Suggested actions")

            st.write(
                f"1. Review service frequency on {top_route['route']}."
            )

            st.write(
                "2. Review passenger demand before allocating buses."
            )

            st.write(
                "3. Reconcile uncollected amounts with ticket records."
            )

            st.write(
                "4. Use hourly ticket data to review scheduling."
            )

            st.write(
                "5. Collect data across more dates for daily "
                "and seasonal demand analysis."
            )


# ============================================================
# AI WEBSITE ASSISTANT
# ============================================================

elif page == "AI Website Assistant":

    st.title(T("AI Website Assistant"))

    st.markdown(
        "<div class='info-card'>"
        "<h3>✦ Website Help Assistant</h3>"
        "<p>" + (
            "Ask questions about the website, its features, "
            "ticket records and analytics."
        ) + "</p></div>",
        unsafe_allow_html=True
    )

    assistant_text = {
        "English": {
            "hello": "Hello! Welcome to Bus Analytics. How can I help?",
            "ticket": "Open Ticket Records. You can search by ticket number, waybill or stop. You can also filter by route and travel date.",
            "dashboard": "The Dashboard displays total tickets, passengers, revenue and route performance.",
            "route": "Route Analysis compares ticket counts, passengers, revenue and route performance scores.",
            "revenue": "Revenue Analysis shows collected revenue, uncollected amounts and the collection rate.",
            "passenger": "Passenger Insights shows passenger distribution across routes.",
            "demand": "Demand Prediction analyses historical hourly ticket and passenger activity. It does not predict guaranteed future demand.",
            "smart": "Smart Insights contains six features: demand recommendations, route intelligence, revenue intelligence, peak-hour heatmap, unusual activity detection and management recommendations.",
            "upload": "Open Upload Dataset, choose a CSV file, preview it and click Use This Dataset.",
            "reports": "Open Reports to download ticket records and route summaries.",
            "language": "Choose English, Kannada or Hindi from the language selector in the sidebar.",
            "help": "I can help with Ticket Records, Dashboard, Route Analysis, Revenue Analysis, Passenger Insights, Demand Prediction, Smart Insights, Reports and Upload Dataset.",
            "ai": "This assistant currently uses built-in question matching. It is not connected to a generative AI model."
        },
        "ಕನ್ನಡ": {
            "hello": "ನಮಸ್ಕಾರ! Bus Analytics ಗೆ ಸ್ವಾಗತ. ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
            "ticket": "Ticket Records ತೆರೆಯಿರಿ. ಟಿಕೆಟ್ ಸಂಖ್ಯೆ, ವೇಬಿಲ್ ಅಥವಾ ನಿಲ್ದಾಣದ ಮೂಲಕ ಹುಡುಕಬಹುದು. ಮಾರ್ಗ ಮತ್ತು ದಿನಾಂಕದ ಮೂಲಕ ಫಿಲ್ಟರ್ ಕೂಡ ಮಾಡಬಹುದು.",
            "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಒಟ್ಟು ಟಿಕೆಟ್‌ಗಳು, ಪ್ರಯಾಣಿಕರು, ಆದಾಯ ಮತ್ತು ಮಾರ್ಗಗಳ ಕಾರ್ಯಕ್ಷಮತೆಯನ್ನು ತೋರಿಸುತ್ತದೆ.",
            "route": "ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ಟಿಕೆಟ್‌ಗಳು, ಪ್ರಯಾಣಿಕರು, ಆದಾಯ ಮತ್ತು ಮಾರ್ಗದ ಕಾರ್ಯಕ್ಷಮತೆಯನ್ನು ಹೋಲಿಸಬಹುದು.",
            "revenue": "ಆದಾಯ ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ಸಂಗ್ರಹಿಸಿದ ಆದಾಯ, ಬಾಕಿ ಮೊತ್ತ ಮತ್ತು ಸಂಗ್ರಹ ದರವನ್ನು ನೋಡಬಹುದು.",
            "passenger": "ಪ್ರಯಾಣಿಕರ ಮಾಹಿತಿಯಲ್ಲಿ ಮಾರ್ಗವಾರು ಪ್ರಯಾಣಿಕರ ವಿತರಣೆಯನ್ನು ನೋಡಬಹುದು.",
            "demand": "ಬೇಡಿಕೆ ವಿಶ್ಲೇಷಣೆಯು ಹಿಂದಿನ ಗಂಟೆವಾರು ಟಿಕೆಟ್ ಮತ್ತು ಪ್ರಯಾಣಿಕರ ಚಟುವಟಿಕೆಯನ್ನು ತೋರಿಸುತ್ತದೆ. ಇದು ಖಚಿತ ಭವಿಷ್ಯದ ಮುನ್ಸೂಚನೆ ಅಲ್ಲ.",
            "smart": "ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳಲ್ಲಿ ಆರು ವೈಶಿಷ್ಟ್ಯಗಳಿವೆ: ಬೇಡಿಕೆ ಶಿಫಾರಸುಗಳು, ಮಾರ್ಗ ಮಾಹಿತಿ, ಆದಾಯ ಮಾಹಿತಿ, ಪೀಕ್ ಅವರ್ ಹೀಟ್‌ಮ್ಯಾಪ್, ಅಸಾಮಾನ್ಯ ಚಟುವಟಿಕೆ ಪತ್ತೆ ಮತ್ತು ನಿರ್ವಹಣಾ ಶಿಫಾರಸುಗಳು.",
            "upload": "Upload Dataset ತೆರೆಯಿರಿ, CSV ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ, ಪೂರ್ವವೀಕ್ಷಣೆ ನೋಡಿ ಮತ್ತು Use This Dataset ಕ್ಲಿಕ್ ಮಾಡಿ.",
            "reports": "Reports ತೆರೆಯಿರಿ ಮತ್ತು ಟಿಕೆಟ್ ದಾಖಲೆಗಳು ಹಾಗೂ ಮಾರ್ಗ ಸಾರಾಂಶಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",
            "language": "ಸೈಡ್‌ಬಾರ್‌ನ ಭಾಷೆ ಆಯ್ಕೆಯಲ್ಲಿ ಕನ್ನಡ, ಇಂಗ್ಲಿಷ್ ಅಥವಾ ಹಿಂದಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
            "help": "ಟಿಕೆಟ್ ದಾಖಲೆಗಳು, ಡ್ಯಾಶ್‌ಬೋರ್ಡ್, ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆ, ಆದಾಯ, ಪ್ರಯಾಣಿಕರು, ಬೇಡಿಕೆ, ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳು ಮತ್ತು ವರದಿಗಳ ಬಗ್ಗೆ ಕೇಳಬಹುದು.",
            "ai": "ಈ ಸಹಾಯಕವು ಪ್ರಸ್ತುತ ಒಳಗೊಂಡಿರುವ ಪ್ರಶ್ನೆ ಹೊಂದಾಣಿಕೆಯನ್ನು ಬಳಸುತ್ತದೆ. ಇದು ಜನರೇಟಿವ್ AI ಮಾದರಿಗೆ ಸಂಪರ್ಕಗೊಂಡಿಲ್ಲ."
        },
        "हिन्दी": {
            "hello": "नमस्ते! Bus Analytics में आपका स्वागत है। मैं आपकी कैसे मदद कर सकता हूँ?",
            "ticket": "Ticket Records खोलें। आप टिकट नंबर, वेबिल या स्टॉप से खोज सकते हैं। रूट और तारीख के अनुसार फ़िल्टर भी कर सकते हैं।",
            "dashboard": "डैशबोर्ड कुल टिकट, यात्री, राजस्व और रूट प्रदर्शन दिखाता है।",
            "route": "रूट विश्लेषण में टिकट, यात्री, राजस्व और रूट प्रदर्शन की तुलना की जाती है।",
            "revenue": "राजस्व विश्लेषण में एकत्रित राजस्व, बकाया राशि और संग्रह दर दिखाई जाती है।",
            "passenger": "यात्री जानकारी में अलग-अलग रूट पर यात्रियों का वितरण दिखाया जाता है।",
            "demand": "मांग विश्लेषण ऐतिहासिक घंटेवार टिकट और यात्री गतिविधि दिखाता है। यह भविष्य की निश्चित भविष्यवाणी नहीं है।",
            "smart": "स्मार्ट इनसाइट्स में छह सुविधाएँ हैं: मांग सुझाव, रूट इंटेलिजेंस, राजस्व इंटेलिजेंस, पीक-आवर हीटमैप, असामान्य गतिविधि पहचान और प्रबंधन सुझाव।",
            "upload": "Upload Dataset खोलें, CSV फ़ाइल चुनें, पूर्वावलोकन देखें और Use This Dataset पर क्लिक करें।",
            "reports": "Reports खोलें और टिकट रिकॉर्ड तथा रूट सारांश डाउनलोड करें।",
            "language": "साइडबार में भाषा विकल्प से हिंदी, अंग्रेज़ी या कन्नड़ चुनें।",
            "help": "मैं टिकट रिकॉर्ड, डैशबोर्ड, रूट विश्लेषण, राजस्व, यात्री, मांग, स्मार्ट इनसाइट्स और रिपोर्ट के बारे में मदद कर सकता हूँ।",
            "ai": "यह सहायक वर्तमान में पहले से तैयार प्रश्न मिलान का उपयोग करता है। यह जनरेटिव AI मॉडल से जुड़ा नहीं है।"
        }
    }

    question = st.text_input(
        T("Question"),
        key="assistant_question"
    )

    if st.button(T("Ask"), type="primary"):

        q = question.lower().strip()

        if not q:

            st.warning("Please enter a question.")

        else:

            answers = assistant_text[st.session_state.language]

            if any(x in q for x in [
                "hello", "hi", "hey", "ನಮಸ್ಕಾರ", "नमस्ते"
            ]):
                answer = answers["hello"]

            elif any(x in q for x in [
                "ticket", "waybill", "ಟಿಕೆಟ್", "टिकट"
            ]):
                answer = answers["ticket"]

            elif any(x in q for x in [
                "dashboard", "ಡ್ಯಾಶ್", "डैशबोर्ड"
            ]):
                answer = answers["dashboard"]

            elif any(x in q for x in [
                "route", "ಮಾರ್ಗ", "रूट"
            ]):
                answer = answers["route"]

            elif any(x in q for x in [
                "revenue", "income", "money", "ಆದಾಯ", "राजस्व"
            ]):
                answer = answers["revenue"]

            elif any(x in q for x in [
                "passenger", "ಪ್ರಯಾಣಿಕ", "यात्री"
            ]):
                answer = answers["passenger"]

            elif any(x in q for x in [
                "demand", "prediction", "ಬೇಡಿಕೆ", "मांग"
            ]):
                answer = answers["demand"]

            elif any(x in q for x in [
                "smart", "insight", "ಸ್ಮಾರ್ಟ್", "स्मार्ट"
            ]):
                answer = answers["smart"]

            elif any(x in q for x in [
                "upload", "dataset", "csv", "ಅಪ್‌ಲೋಡ್", "अपलोड"
            ]):
                answer = answers["upload"]

            elif any(x in q for x in [
                "report", "download", "ವರದಿ", "रिपोर्ट"
            ]):
                answer = answers["reports"]

            elif any(x in q for x in [
                "language", "ಭಾಷೆ", "भाषा"
            ]):
                answer = answers["language"]

            elif "ai" in q or "artificial intelligence" in q:
                answer = answers["ai"]

            else:
                answer = answers["help"]

            st.markdown(
                "<div class='info-card'>"
                "<h3>✦ Assistant Response</h3>"
                "<p>" + answer + "</p>"
                "</div>",
                unsafe_allow_html=True
            )

    st.caption(
        "Note: This is a built-in website help assistant, "
        "not a live generative AI chatbot."
    )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title(T("Reports"))

    if data.empty:

        st.warning(T("NoData"))

    else:

        report = data.rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from_stop": "From Stop",
            "to_stop": "To Stop",
            "route": "Route",
            "date": "Date",
            "time": "Time",
            "passengers": "Passengers",
            "collected": "Collected Amount",
            "uncollected": "Uncollected Amount"
        })

        st.subheader("Complete Ticket Report")

        st.download_button(
            "Download Complete Ticket Report",
            report.to_csv(index=False).encode("utf-8"),
            "complete_ticket_report.csv",
            "text/csv",
            use_container_width=True
        )

        route_report = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        st.subheader("Route Summary")

        st.dataframe(
            route_report,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Route Summary",
            route_report.to_csv(index=False).encode("utf-8"),
            "route_summary.csv",
            "text/csv",
            use_container_width=True
        )


# ============================================================
# UPLOAD DATASET
# ============================================================

elif page == "Upload Dataset":

    st.title(T("Upload Dataset"))

    st.write(
        "Upload a CSV containing your bus ticket records."
    )

    st.markdown(
        "<div class='info-card'>"
        "<h3>Required Dataset Columns</h3>"
        "<p>From Stop, To Stop, Date, Total Psgr and Coll Amt.</p>"
        "<p>Optional columns: Waybill Number, Ticket Number, "
        "Time and Uncoll Amt.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        T("ChooseFile"),
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            preview = pd.read_csv(uploaded_file)

            st.success(
                f"File loaded: {len(preview):,} records."
            )

            st.subheader(T("Preview"))

            st.dataframe(
                preview.head(10),
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                T("UseFile"),
                type="primary"
            ):

                # Validate before activating the new dataset.
                validated = prepare_data(preview)

                st.session_state.uploaded_data = preview

                st.success(
                    T("Upload Dataset") + " successful."
                )

                st.rerun()

        except Exception as error:

            st.error(
                T("Upload Dataset") + ": " + str(error)
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    "<div style='text-align:center;padding:18px;'>"
    "<h3 style='color:#64243D !important;'>"
    "🚌 BUS ANALYTICS</h3>"
    "<p style='color:#604B55 !important;'>"
    + T("Tagline")
    + "</p>"
    "<p style='color:#987984 !important;'>"
    "BOOK • ANALYZE • PREDICT</p>"
    "<p style='color:#64243D !important;font-weight:700;'>"
    + T("Footer")
    + "</p></div>",
    unsafe_allow_html=True
)
# ============================================================
# BUS ANALYTICS - CRACKER HEADS
# PART 2 OF 2
# ============================================================

# ============================================================
# TICKET RECORDS
# ============================================================

elif page == "Ticket Records":

    st.title(T("Ticket Records"))

    if data.empty:
        st.warning(T("NoData"))

    else:
        search = st.text_input(T("Search"))

        routes = [T("AllRoutes")] + sorted(
            data["route"].dropna().unique().tolist()
        )

        selected_route = st.selectbox(
            T("RouteFilter"),
            routes
        )

        st.markdown("#### " + T("DateFilter"))

        min_date = data["date"].min().date()
        max_date = data["date"].max().date()

        date_mode = st.radio(
            T("DateFilter"),
            [T("AllDates"), "Select Date Range"],
            horizontal=True,
            label_visibility="collapsed"
        )

        selected_dates = None

        if date_mode != T("AllDates"):
            selected_dates = st.date_input(
                T("DateFilter"),
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                format="DD/MM/YYYY"
            )

        filtered = data.copy()

        if selected_route != T("AllRoutes"):
            filtered = filtered[
                filtered["route"] == selected_route
            ]

        if selected_dates:

            if isinstance(selected_dates, (tuple, list)):

                if len(selected_dates) == 2:
                    start_date, end_date = selected_dates

                    filtered = filtered[
                        (filtered["date"].dt.date >= start_date)
                        & (filtered["date"].dt.date <= end_date)
                    ]

                elif len(selected_dates) == 1:
                    filtered = filtered[
                        filtered["date"].dt.date == selected_dates[0]
                    ]

            else:
                filtered = filtered[
                    filtered["date"].dt.date == selected_dates
                ]

        if search.strip():
            mask = filtered.astype(str).apply(
                lambda column: column.str.contains(
                    search.strip(),
                    case=False,
                    na=False
                )
            ).any(axis=1)

            filtered = filtered[mask]

        st.metric(T("Records"), f"{len(filtered):,}")

        display = filtered.rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from_stop": "From Stop",
            "to_stop": "To Stop",
            "route": "Route",
            "date": "Date",
            "time": "Time",
            "passengers": "Total Passengers",
            "collected": "Collected Amount",
            "uncollected": "Uncollected Amount"
        })

        if filtered.empty:
            st.info(T("NoRecords"))

        else:
            display["Date"] = display["Date"].dt.strftime("%d/%m/%Y")

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                T("Download"),
                display.to_csv(index=False).encode("utf-8"),
                "filtered_ticket_records.csv",
                "text/csv"
            )


# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.title(T("Dashboard"))

    if data.empty:
        st.warning(T("NoData"))

    else:
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(T("Tickets"), f"{len(data):,}")

        c2.metric(
            T("Passengers"),
            f"{int(data['passengers'].sum()):,}"
        )

        c3.metric(
            T("Collected"),
            money(data["collected"].sum())
        )

        c4.metric(
            T("Uncollected"),
            money(data["uncollected"].sum())
        )

        summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum")
            )
            .reset_index()
            .sort_values("Tickets", ascending=False)
        )

        fig = px.bar(
            summary.head(12),
            x="route",
            y="Tickets",
            title="Route-wise Ticket Performance",
            color_discrete_sequence=[BURGUNDY]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )


# ============================================================
# ROUTE ANALYSIS
# ============================================================

elif page == "Route Analysis":

    st.title(T("Route Analysis"))

    if data.empty:
        st.warning(T("NoData"))

    else:
        summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        total_tickets = max(summary["Tickets"].sum(), 1)
        total_passengers = max(summary["Passengers"].sum(), 1)
        total_revenue = max(summary["Revenue"].sum(), 1)

        summary["Performance Score"] = (
            35 * summary["Tickets"] / total_tickets
            + 35 * summary["Passengers"] / total_passengers
            + 30 * summary["Revenue"] / total_revenue
        ) * 100

        top = summary.sort_values(
            "Performance Score",
            ascending=False
        )

        fig = px.bar(
            top.head(12).sort_values("Performance Score"),
            x="Performance Score",
            y="route",
            orientation="h",
            title="Route Performance Score",
            color_discrete_sequence=[ROSE]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

        st.dataframe(
            top.round(2),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# REVENUE ANALYSIS
# ============================================================

elif page == "Revenue Analysis":

    st.title(T("Revenue Analysis"))

    if data.empty:
        st.warning(T("NoData"))

    else:
        collected = data["collected"].sum()
        pending = data["uncollected"].sum()

        total = collected + pending

        rate = collected / total * 100 if total else 0

        a, b, c = st.columns(3)

        a.metric(T("Collected"), money(collected))
        b.metric(T("Uncollected"), money(pending))
        c.metric(T("CollectionRate"), f"{rate:.2f}%")

        summary = (
            data.groupby("route")
            .agg(
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        fig = px.bar(
            summary,
            x="route",
            y=["Collected", "Uncollected"],
            barmode="group",
            title="Collected vs Uncollected Revenue",
            color_discrete_sequence=[BURGUNDY, ROSE]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PASSENGER INSIGHTS
# ============================================================

elif page == "Passenger Insights":

    st.title(T("Passenger Insights"))

    if data.empty:
        st.warning(T("NoData"))

    else:
        a, b = st.columns(2)

        a.metric(
            T("Passengers"),
            f"{int(data['passengers'].sum()):,}"
        )

        b.metric(
            "Average Passengers per Ticket",
            f"{data['passengers'].mean():.2f}"
        )

        summary = (
            data.groupby("route")["passengers"]
            .sum()
            .reset_index()
            .sort_values("passengers", ascending=False)
        )

        fig = px.bar(
            summary.head(12),
            x="route",
            y="passengers",
            title="Passengers by Route",
            color_discrete_sequence=[ROSE]
        )

        st.plotly_chart(
            chart_style(fig, 420),
            use_container_width=True
        )

        fig = px.histogram(
            data,
            x="passengers",
            nbins=15,
            title="Passenger Distribution",
            color_discrete_sequence=[BURGUNDY]
        )

        st.plotly_chart(
            chart_style(fig),
            use_container_width=True
        )


# ============================================================
# DEMAND PREDICTION
# ============================================================

elif page == "Demand Prediction":

    st.title(T("Demand Prediction"))

    st.caption(
        "Historical demand analysis based on recorded ticket times. "
        "This is not a guaranteed future forecast."
    )

    if data.empty:
        st.warning(T("NoData"))

    else:
        time_data = data.copy()

        time_data["hour"] = pd.to_datetime(
            time_data["time"].astype(str),
            errors="coerce"
        ).dt.hour

        time_data = time_data.dropna(subset=["hour"])

        if time_data.empty:
            st.warning(T("NoTime"))

        else:
            time_data["hour"] = time_data["hour"].astype(int)

            hourly = (
                time_data.groupby("hour")
                .agg(
                    Tickets=("ticket", "count"),
                    Passengers=("passengers", "sum"),
                    Revenue=("collected", "sum")
                )
                .reset_index()
            )

            busiest = hourly.loc[hourly["Tickets"].idxmax()]

            st.metric(
                T("Busiest"),
                f"{int(busiest['hour']):02d}:00"
            )

            fig = px.bar(
                hourly,
                x="hour",
                y="Tickets",
                title="Hourly Ticket Demand",
                color_discrete_sequence=[BURGUNDY]
            )

            st.plotly_chart(
                chart_style(fig),
                use_container_width=True
            )

            fig = px.line(
                hourly,
                x="hour",
                y="Passengers",
                markers=True,
                title="Hourly Passenger Movement"
            )

            fig.update_traces(line_color=ROSE)

            st.plotly_chart(
                chart_style(fig),
                use_container_width=True
            )

            st.dataframe(
                hourly,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# SMART INSIGHTS - SIX FEATURES
# ============================================================

elif page == "Smart Insights":

    st.title(T("Smart Insights"))

    st.caption(
        "Statistical analysis and rule-based recommendations "
        "generated from the uploaded ticket data."
    )

    if data.empty:
        st.warning(T("NoData"))

    else:
        summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        # 1. SMART DEMAND RECOMMENDATIONS

        with st.expander("✧ 1. Smart Demand Recommendations"):

            top = summary.nlargest(5, "Tickets")

            st.markdown("### High-demand routes")

            st.dataframe(
                top,
                use_container_width=True,
                hide_index=True
            )

            st.success(
                "Review bus frequency and capacity on routes "
                "with higher recorded ticket activity."
            )

        # 2. ROUTE INTELLIGENCE

        with st.expander("⌁ 2. Route Intelligence"):

            st.dataframe(
                summary.sort_values(
                    "Tickets",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

            low = summary.nsmallest(1, "Tickets").iloc[0]

            st.info(
                f"Lowest recorded ticket activity: {low['route']} "
                f"({int(low['Tickets'])} tickets). "
                "Review demand before changing service frequency."
            )

        # 3. REVENUE INTELLIGENCE

        with st.expander("₹ 3. Revenue Intelligence"):

            collected = data["collected"].sum()
            pending = data["uncollected"].sum()

            total = collected + pending

            rate = collected / total * 100 if total else 0

            a, b, c = st.columns(3)

            a.metric(T("Collected"), money(collected))
            b.metric(T("Uncollected"), money(pending))
            c.metric(T("CollectionRate"), f"{rate:.2f}%")

            st.dataframe(
                summary.sort_values(
                    "Revenue",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

        # 4. PEAK-HOUR INTELLIGENCE AND HEATMAP

        with st.expander("◷ 4. Peak-Hour Intelligence & Heatmap"):

            time_data = data.copy()

            time_data["hour"] = pd.to_datetime(
                time_data["time"].astype(str),
                errors="coerce"
            ).dt.hour

            time_data = time_data.dropna(subset=["hour"])

            if time_data.empty:
                st.warning(T("NoTime"))

            else:
                time_data["hour"] = time_data["hour"].astype(int)

                hourly = (
                    time_data.groupby("hour")
                    .size()
                    .reset_index(name="Tickets")
                )

                busiest = hourly.loc[hourly["Tickets"].idxmax()]

                st.metric(
                    T("Busiest"),
                    f"{int(busiest['hour']):02d}:00"
                )

                fig = px.bar(
                    hourly,
                    x="hour",
                    y="Tickets",
                    title="Peak-Hour Ticket Activity",
                    color="Tickets",
                    color_continuous_scale=[
                        "#F8E6E5", "#C77B8C", "#64243D"
                    ]
                )

                st.plotly_chart(
                    chart_style(fig),
                    use_container_width=True
                )

                time_data["travel_date"] = (
                    time_data["date"].dt.strftime("%d-%m-%Y")
                )

                heat = (
                    time_data.groupby(
                        ["travel_date", "hour"]
                    )
                    .size()
                    .reset_index(name="Tickets")
                )

                pivot = heat.pivot(
                    index="travel_date",
                    columns="hour",
                    values="Tickets"
                ).fillna(0)

                fig = px.imshow(
                    pivot,
                    aspect="auto",
                    title="Passenger Demand Heatmap",
                    color_continuous_scale=[
                        "#F8E6E5", "#C77B8C", "#64243D"
                    ]
                )

                st.plotly_chart(
                    chart_style(fig, 350),
                    use_container_width=True
                )

        # 5. UNUSUAL ACTIVITY DETECTION

        with st.expander("⚑ 5. Unusual Activity Detection"):

            if len(summary) >= 3:

                mean = summary["Tickets"].mean()
                deviation = summary["Tickets"].std()

                if deviation > 0:
                    unusual = summary[
                        (summary["Tickets"] - mean).abs()
                        > 2 * deviation
                    ]
                else:
                    unusual = summary.iloc[0:0]

                if unusual.empty:
                    st.success(
                        "No unusual ticket-count outliers detected."
                    )
                else:
                    st.warning(
                        "The following routes have unusual "
                        "ticket counts and should be reviewed."
                    )

                    st.dataframe(
                        unusual,
                        use_container_width=True,
                        hide_index=True
                    )

            else:
                st.info(
                    "At least three routes are required "
                    "for this statistical comparison."
                )

            st.caption(
                "An unusual value is only a statistical warning. "
                "It does not prove fraud or misconduct."
            )

        # 6. MANAGEMENT RECOMMENDATIONS

        with st.expander("✦ 6. Management Recommendations"):

            top_route = summary.nlargest(
                1,
                "Tickets"
            ).iloc[0]

            st.markdown("### Suggested actions")

            st.write(
                f"1. Review service frequency on {top_route['route']}."
            )

            st.write(
                "2. Review passenger demand before allocating buses."
            )

            st.write(
                "3. Reconcile uncollected amounts with ticket records."
            )

            st.write(
                "4. Use hourly ticket data to review scheduling."
            )

            st.write(
                "5. Collect data across more dates for daily "
                "and seasonal demand analysis."
            )


# ============================================================
# AI WEBSITE ASSISTANT
# ============================================================

elif page == "AI Website Assistant":

    st.title(T("AI Website Assistant"))

    st.markdown(
        "<div class='info-card'>"
        "<h3>✦ Website Help Assistant</h3>"
        "<p>Ask questions about the website, its features, "
        "ticket records and analytics.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    assistant_text = {
        "English": {
            "hello": "Hello! Welcome to Bus Analytics. How can I help?",
            "ticket": "Open Ticket Records. You can search by ticket number, waybill or stop. You can also filter by route and travel date.",
            "dashboard": "The Dashboard displays total tickets, passengers, revenue and route performance.",
            "route": "Route Analysis compares ticket counts, passengers, revenue and route performance scores.",
            "revenue": "Revenue Analysis shows collected revenue, uncollected amounts and the collection rate.",
            "passenger": "Passenger Insights shows passenger distribution across routes.",
            "demand": "Demand Prediction analyses historical hourly ticket and passenger activity. It does not predict guaranteed future demand.",
            "smart": "Smart Insights contains six features: demand recommendations, route intelligence, revenue intelligence, peak-hour heatmap, unusual activity detection and management recommendations.",
            "upload": "Open Upload Dataset, choose a CSV file, preview it and click Use This Dataset.",
            "reports": "Open Reports to download ticket records and route summaries.",
            "language": "Choose English, Kannada or Hindi from the language selector in the sidebar.",
            "help": "I can help with Ticket Records, Dashboard, Route Analysis, Revenue Analysis, Passenger Insights, Demand Prediction, Smart Insights, Reports and Upload Dataset.",
            "ai": "This assistant currently uses built-in question matching. It is not connected to a generative AI model."
        },

        "ಕನ್ನಡ": {
            "hello": "ನಮಸ್ಕಾರ! Bus Analytics ಗೆ ಸ್ವಾಗತ. ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?",
            "ticket": "Ticket Records ತೆರೆಯಿರಿ. ಟಿಕೆಟ್ ಸಂಖ್ಯೆ, ವೇಬಿಲ್ ಅಥವಾ ನಿಲ್ದಾಣದ ಮೂಲಕ ಹುಡುಕಬಹುದು. ಮಾರ್ಗ ಮತ್ತು ದಿನಾಂಕದ ಮೂಲಕ ಫಿಲ್ಟರ್ ಕೂಡ ಮಾಡಬಹುದು.",
            "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಒಟ್ಟು ಟಿಕೆಟ್‌ಗಳು, ಪ್ರಯಾಣಿಕರು, ಆದಾಯ ಮತ್ತು ಮಾರ್ಗಗಳ ಕಾರ್ಯಕ್ಷಮತೆಯನ್ನು ತೋರಿಸುತ್ತದೆ.",
            "route": "ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ಟಿಕೆಟ್‌ಗಳು, ಪ್ರಯಾಣಿಕರು, ಆದಾಯ ಮತ್ತು ಮಾರ್ಗದ ಕಾರ್ಯಕ್ಷಮತೆಯನ್ನು ಹೋಲಿಸಬಹುದು.",
            "revenue": "ಆದಾಯ ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ಸಂಗ್ರಹಿಸಿದ ಆದಾಯ, ಬಾಕಿ ಮೊತ್ತ ಮತ್ತು ಸಂಗ್ರಹ ದರವನ್ನು ನೋಡಬಹುದು.",
            "passenger": "ಪ್ರಯಾಣಿಕರ ಮಾಹಿತಿಯಲ್ಲಿ ಮಾರ್ಗವಾರು ಪ್ರಯಾಣಿಕರ ವಿತರಣೆಯನ್ನು ನೋಡಬಹುದು.",
            "demand": "ಬೇಡಿಕೆ ವಿಶ್ಲೇಷಣೆಯು ಹಿಂದಿನ ಗಂಟೆವಾರು ಟಿಕೆಟ್ ಮತ್ತು ಪ್ರಯಾಣಿಕರ ಚಟುವಟಿಕೆಯನ್ನು ತೋರಿಸುತ್ತದೆ. ಇದು ಖಚಿತ ಭವಿಷ್ಯದ ಮುನ್ಸೂಚನೆ ಅಲ್ಲ.",
            "smart": "ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳಲ್ಲಿ ಆರು ವೈಶಿಷ್ಟ್ಯಗಳಿವೆ: ಬೇಡಿಕೆ ಶಿಫಾರಸುಗಳು, ಮಾರ್ಗ ಮಾಹಿತಿ, ಆದಾಯ ಮಾಹಿತಿ, ಪೀಕ್ ಅವರ್ ಹೀಟ್‌ಮ್ಯಾಪ್, ಅಸಾಮಾನ್ಯ ಚಟುವಟಿಕೆ ಪತ್ತೆ ಮತ್ತು ನಿರ್ವಹಣಾ ಶಿಫಾರಸುಗಳು.",
            "upload": "Upload Dataset ತೆರೆಯಿರಿ, CSV ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ, ಪೂರ್ವವೀಕ್ಷಣೆ ನೋಡಿ ಮತ್ತು Use This Dataset ಕ್ಲಿಕ್ ಮಾಡಿ.",
            "reports": "Reports ತೆರೆಯಿರಿ ಮತ್ತು ಟಿಕೆಟ್ ದಾಖಲೆಗಳು ಹಾಗೂ ಮಾರ್ಗ ಸಾರಾಂಶಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",
            "language": "ಸೈಡ್‌ಬಾರ್‌ನ ಭಾಷೆ ಆಯ್ಕೆಯಲ್ಲಿ ಕನ್ನಡ, ಇಂಗ್ಲಿಷ್ ಅಥವಾ ಹಿಂದಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
            "help": "ಟಿಕೆಟ್ ದಾಖಲೆಗಳು, ಡ್ಯಾಶ್‌ಬೋರ್ಡ್, ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆ, ಆದಾಯ, ಪ್ರಯಾಣಿಕರು, ಬೇಡಿಕೆ, ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳು ಮತ್ತು ವರದಿಗಳ ಬಗ್ಗೆ ಕೇಳಬಹುದು.",
            "ai": "ಈ ಸಹಾಯಕವು ಪ್ರಸ್ತುತ ಒಳಗೊಂಡಿರುವ ಪ್ರಶ್ನೆ ಹೊಂದಾಣಿಕೆಯನ್ನು ಬಳಸುತ್ತದೆ. ಇದು ಜನರೇಟಿವ್ AI ಮಾದರಿಗೆ ಸಂಪರ್ಕಗೊಂಡಿಲ್ಲ."
        },

        "हिन्दी": {
            "hello": "नमस्ते! Bus Analytics में आपका स्वागत है। मैं आपकी कैसे मदद कर सकता हूँ?",
            "ticket": "Ticket Records खोलें। आप टिकट नंबर, वेबिल या स्टॉप से खोज सकते हैं। रूट और तारीख के अनुसार फ़िल्टर भी कर सकते हैं।",
            "dashboard": "डैशबोर्ड कुल टिकट, यात्री, राजस्व और रूट प्रदर्शन दिखाता है।",
            "route": "रूट विश्लेषण अलग-अलग रूट पर टिकट, यात्री और राजस्व की तुलना करता है।",
            "revenue": "राजस्व विश्लेषण में एकत्रित राजस्व, बकाया राशि और संग्रह दर दिखाई जाती है।",
            "passenger": "यात्री जानकारी में अलग-अलग रूट पर यात्रियों का वितरण दिखाया जाता है।",
            "demand": "मांग विश्लेषण ऐतिहासिक घंटेवार टिकट और यात्री गतिविधि दिखाता है। यह भविष्य की निश्चित भविष्यवाणी नहीं है।",
            "smart": "स्मार्ट इनसाइट्स में छह सुविधाएँ हैं: मांग सुझाव, रूट इंटेलिजेंस, राजस्व इंटेलिजेंस, पीक-आवर हीटमैप, असामान्य गतिविधि पहचान और प्रबंधन सुझाव।",
            "upload": "Upload Dataset खोलें, CSV फ़ाइल चुनें, पूर्वावलोकन देखें और Use This Dataset पर क्लिक करें।",
            "reports": "Reports खोलें और टिकट रिकॉर्ड तथा रूट सारांश डाउनलोड करें।",
            "language": "साइडबार में भाषा विकल्प से हिंदी, अंग्रेज़ी या कन्नड़ चुनें।",
            "help": "मैं टिकट रिकॉर्ड, डैशबोर्ड, रूट विश्लेषण, राजस्व, यात्री, मांग, स्मार्ट इनसाइट्स और रिपोर्ट के बारे में मदद कर सकता हूँ।",
            "ai": "यह सहायक वर्तमान में पहले से तैयार प्रश्न मिलान का उपयोग करता है। यह जनरेटिव AI मॉडल से जुड़ा नहीं है।"
        }
    }

    question = st.text_input(
        T("Question"),
        key="assistant_question"
    )

    if st.button(T("Ask"), type="primary"):

        q = question.lower().strip()

        if not q:
            st.warning(T("Question"))

        else:
            answers = assistant_text[st.session_state.language]

            if any(x in q for x in ["hello", "hi", "hey", "ನಮಸ್ಕಾರ", "नमस्ते"]):
                answer = answers["hello"]

            elif any(x in q for x in ["ticket", "waybill", "ಟಿಕೆಟ್", "टिकट"]):
                answer = answers["ticket"]

            elif any(x in q for x in ["dashboard", "ಡ್ಯಾಶ್", "डैशबोर्ड"]):
                answer = answers["dashboard"]

            elif any(x in q for x in ["route", "ಮಾರ್ಗ", "रूट"]):
                answer = answers["route"]

            elif any(x in q for x in ["revenue", "income", "money", "ಆದಾಯ", "राजस्व"]):
                answer = answers["revenue"]

            elif any(x in q for x in ["passenger", "ಪ್ರಯಾಣಿಕ", "यात्री"]):
                answer = answers["passenger"]

            elif any(x in q for x in ["demand", "prediction", "ಬೇಡಿಕೆ", "मांग"]):
                answer = answers["demand"]

            elif any(x in q for x in ["smart", "insight", "ಸ್ಮಾರ್ಟ್", "स्मार्ट"]):
                answer = answers["smart"]

            elif any(x in q for x in ["upload", "dataset", "csv", "ಅಪ್‌ಲೋಡ್", "अपलोड"]):
                answer = answers["upload"]

            elif any(x in q for x in ["report", "download", "ವರದಿ", "रिपोर्ट"]):
                answer = answers["reports"]

            elif any(x in q for x in ["language", "ಭಾಷೆ", "भाषा"]):
                answer = answers["language"]

            elif "ai" in q or "artificial intelligence" in q:
                answer = answers["ai"]

            else:
                answer = answers["help"]

            st.markdown(
                "<div class='info-card'>"
                "<h3>✦ Assistant Response</h3>"
                "<p>" + answer + "</p>"
                "</div>",
                unsafe_allow_html=True
            )

    st.caption(
        "This is a built-in website help assistant, "
        "not a live generative AI chatbot."
    )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title(T("Reports"))

    if data.empty:
        st.warning(T("NoData"))

    else:
        report = data.rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from_stop": "From Stop",
            "to_stop": "To Stop",
            "route": "Route",
            "date": "Date",
            "time": "Time",
            "passengers": "Passengers",
            "collected": "Collected Amount",
            "uncollected": "Uncollected Amount"
        })

        report["Date"] = report["Date"].dt.strftime("%d/%m/%Y")

        st.subheader("Complete Ticket Report")

        st.download_button(
            "Download Complete Ticket Report",
            report.to_csv(index=False).encode("utf-8"),
            "complete_ticket_report.csv",
            "text/csv",
            use_container_width=True
        )

        route_report = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        st.subheader("Route Summary")

        st.dataframe(
            route_report,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Route Summary",
            route_report.to_csv(index=False).encode("utf-8"),
            "route_summary.csv",
            "text/csv",
            use_container_width=True
        )


# ============================================================
# UPLOAD DATASET
# ============================================================

elif page == "Upload Dataset":

    st.title(T("Upload Dataset"))

    st.write(
        "Upload a CSV containing your bus ticket records."
    )

    st.markdown(
        "<div class='info-card'>"
        "<h3>Required Dataset Columns</h3>"
        "<p>From Stop, To Stop, Date, Total Psgr and Coll Amt.</p>"
        "<p>Optional: Waybill Number, Ticket Number, "
        "Time and Uncoll Amt.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        T("ChooseFile"),
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            preview = pd.read_csv(uploaded_file)

            st.success(
                f"File loaded: {len(preview):,} records."
            )

            st.subheader(T("Preview"))

            st.dataframe(
                preview.head(10),
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                T("UseFile"),
                type="primary"
            ):

                prepare_data(preview)

                st.session_state.uploaded_data = preview

                st.success("Dataset successfully activated.")

                st.rerun()

        except Exception as error:
            st.error("Dataset error: " + str(error))


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    "<div style='text-align:center;padding:18px;'>"
    "<h3 style='color:#64243D !important;'>"
    "🚌 BUS ANALYTICS</h3>"
    "<p style='color:#604B55 !important;'>"
    + T("Tagline")
    + "</p>"
    "<p style='color:#987984 !important;'>"
    "BOOK • ANALYZE • PREDICT</p>"
    "<p style='color:#64243D !important;font-weight:700;'>"
    + T("Footer")
    + "</p></div>",
    unsafe_allow_html=True
)

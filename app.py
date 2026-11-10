from pathlib import Path
from datetime import datetime
import base64
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ------------------------------------------------------------
# BUS ANALYTICS | CRACKER HEADS
# Responsive Streamlit dashboard using the approved prototype
# ------------------------------------------------------------

st.set_page_config(
    page_title="Bus Analytics | CRACKER HEADS",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tickets.csv"

# Approved palette: warm ivory, blush, burgundy and rose-gold.
BG = "#FFF8F5"
PINK = "#F8E6E5"
BURGUNDY = "#64243D"
PLUM = "#351324"
ROSE = "#C77B8C"
GOLD = "#D7A66B"
INK = "#382832"
MUTED = "#8B737D"

# Apply readable chart text to every Plotly chart in the application.
BUS_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="DM Sans, Arial, sans-serif", size=13, color=PLUM),
        title=dict(font=dict(family="DM Sans, Arial, sans-serif", size=18, color=BURGUNDY)),
        xaxis=dict(
            tickfont=dict(color=PLUM, size=12),
            title_font=dict(color=BURGUNDY, size=13),
            color=PLUM,
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
            zerolinecolor="#D8C5CB",
        ),
        yaxis=dict(
            tickfont=dict(color=PLUM, size=12),
            title_font=dict(color=BURGUNDY, size=13),
            color=PLUM,
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
            zerolinecolor="#D8C5CB",
        ),
        legend=dict(font=dict(color=PLUM, size=12)),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=BURGUNDY,
            font=dict(color=PLUM, size=13),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
)
pio.templates["bus_analytics"] = BUS_TEMPLATE
pio.templates.default = "bus_analytics"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root {{ --bg:{BG}; --pink:{PINK}; --burgundy:{BURGUNDY}; --plum:{PLUM}; --rose:{ROSE}; --gold:{GOLD}; --ink:{INK}; --muted:{MUTED}; }}
html, body, [data-testid="stAppViewContainer"] {{ background:var(--bg); color:var(--ink); font-family:'DM Sans',sans-serif; }}
[data-testid="stHeader"] {{ background:rgba(255,248,245,.92); }}
[data-testid="stToolbar"] {{ right:1rem; }}
.block-container {{ padding-top:1.15rem !important; padding-bottom:2rem !important; max-width:1600px; }}
[data-testid="stSidebar"] {{ background:linear-gradient(180deg,#FBEAE7 0%,#F5DFE2 100%); border-right:1px solid #EAD1D5; }}
[data-testid="stSidebar"] > div:first-child {{ padding-top:1rem; }}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color:var(--burgundy); }}
[data-testid="stSidebar"] .stButton button {{ width:100%; text-align:left; border:1px solid transparent; border-radius:13px; background:transparent; color:var(--burgundy); font-weight:600; padding:.65rem .8rem; }}
[data-testid="stSidebar"] .stButton button:hover {{ background:#F4D5D8; border-color:#E8BFC7; color:var(--plum); }}
[data-testid="stSidebar"] [data-testid="stImage"] img {{ border-radius:17px; }}
[data-testid="stMetric"] {{ background:linear-gradient(135deg,#FFF 0%,#FCEDEF 100%); border:1px solid #EBD8DC; border-radius:18px; padding:17px 18px; box-shadow:0 4px 16px rgba(85,35,55,.045); }}
[data-testid="stMetricLabel"] p {{ color:#806B75 !important; font-weight:600; }}
[data-testid="stMetricValue"] {{ color:var(--plum) !important; font-weight:800; }}
[data-testid="stMetricDelta"] {{ font-size:.82rem; }}
.card {{ background:#FFFFFF; border:1px solid #EAD9DD; border-radius:20px; padding:20px 22px; box-shadow:0 5px 18px rgba(73,32,50,.045); height:100%; }}
.card h3 {{ color:var(--burgundy); margin:0 0 8px 0; font-size:1.05rem; }}
.card p {{ color:#755F69; margin:0; line-height:1.55; }}
.hero {{ border-radius:22px; padding:30px 34px; color:white; min-height:190px; background:linear-gradient(105deg,rgba(45,17,36,.96),rgba(91,35,61,.78)), url('') center/cover; border:1px solid #6E3A50; margin-bottom:20px; }}
.hero .eyebrow {{ color:#F5D4C9; letter-spacing:2px; font-size:.75rem; font-weight:700; }}
.hero h1 {{ color:#FFF4ED; font-family:'Playfair Display',serif; font-size:clamp(2rem,4vw,3.1rem); line-height:1.08; margin:8px 0; }}
.hero p {{ color:#F8E7E4; font-size:1rem; max-width:650px; margin:0; }}
.section-title {{ color:var(--burgundy); font-size:1.25rem; font-weight:800; margin:1.2rem 0 .7rem 0; }}
.small-note {{ color:var(--muted); font-size:.84rem; }}
.stButton button[kind="primary"] {{ background:var(--burgundy); color:white; border:0; border-radius:12px; font-weight:700; }}
.stButton button[kind="primary"]:hover {{ background:var(--plum); color:white; }}
.stDownloadButton button {{ background:#F3DDE1; color:var(--burgundy); border:1px solid #E6C4CB; border-radius:12px; font-weight:700; }}
[data-testid="stDataFrame"] {{ border:1px solid #EAD9DD; border-radius:14px; overflow:hidden; }}
hr {{ border-color:#EAD5DA !important; }}
footer {{ visibility:hidden; }}

[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] {{
  color: #382832;
}}
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {{
  color: #64243D;
}}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
  color: #624D57 !important;
}}
[data-testid="stDataFrame] {{
  color: #351324 !important;
}}

:root, html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {{
    color-scheme: light !important;
    background-color: #FFF8F5 !important;
    color: #382832 !important;
}}
[data-testid="stMain"] > div {{
    background-color: #FFF8F5 !important;
}}
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] {{
    color: #382832;
}}
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3 {{
    color: #64243D !important;
}}
[data-testid="stAlert"] {{
    color: #382832 !important;
}}

@media (max-width: 768px) {{
  .block-container {{
    width: 100% !important;
    max-width: 100% !important;
    padding: .65rem .7rem 1.5rem .7rem !important;
  }}
  [data-testid="stHorizontalBlock"] {{
    flex-direction: column !important;
    flex-wrap: nowrap !important;
    gap: .8rem !important;
  }}
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
    width: 100% !important;
    min-width: 100% !important;
    flex: 1 1 100% !important;
  }}
  .hero {{ padding: 21px 17px !important; min-height: unset !important; }}
  .hero h1 {{ font-size: 1.7rem !important; line-height: 1.2 !important; }}
  .hero p {{ font-size: .92rem !important; line-height: 1.55 !important; }}
  [data-testid="stMetric"] {{ padding: 12px !important; min-width: 0 !important; }}
  [data-testid="stMetricValue"] {{ font-size: 1.3rem !important; overflow-wrap: anywhere !important; }}
  .card {{ padding: 16px !important; min-height: unset !important; }}
  [data-testid="stPlotlyChart"] {{ width: 100% !important; max-width: 100% !important; overflow-x: auto !important; padding: 2px !important; }}
  [data-testid="stDataFrame"] {{ max-width: 100% !important; overflow-x: auto !important; }}
  .stButton button, .stDownloadButton button {{ min-height: 44px !important; white-space: normal !important; }}
  [data-testid="stSidebar"] {{ min-width: min(86vw, 310px) !important; }}
}}

@media (max-width: 380px) {{
  .block-container {{ padding-left: .5rem !important; padding-right: .5rem !important; }}
  .hero h1 {{ font-size: 1.48rem !important; }}
  [data-testid="stMetricValue"] {{ font-size: 1.15rem !important; }}
}}
@media (max-width: 900px) {{
  .block-container {{ padding: .7rem .8rem 1.5rem .8rem !important; }}
  .hero {{ padding:23px 20px; min-height:unset; }}
  .hero h1 {{ font-size:2rem; }}
  [data-testid="stMetric"] {{ padding:12px 13px; }}
  [data-testid="stSidebar"] {{ min-width: min(82vw, 310px); }}
}}
@media (max-width: 600px) {{
  .block-container {{ padding-left:.65rem !important; padding-right:.65rem !important; }}
  .hero {{ border-radius:17px; padding:20px 17px; }}
  .hero h1 {{ font-size:1.75rem; }}
  .card {{ padding:16px; }}
  [data-testid="stMetricValue"] {{ font-size:1.35rem !important; }}
  [data-testid="stSidebar"] {{ min-width:min(86vw, 300px); }}
}}

@keyframes busFadeUp {{
  from {{ opacity: 0; transform: translateY(16px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes busGlow {{
  0%, 100% {{ box-shadow: 0 5px 18px rgba(73,32,50,.045); }}
  50% {{ box-shadow: 0 9px 26px rgba(100,36,61,.12); }}
}}
@keyframes busLogoIn {{
  0% {{ opacity: 0; transform: scale(.82) translateY(12px); }}
  70% {{ opacity: 1; transform: scale(1.035) translateY(0); }}
  100% {{ opacity: 1; transform: scale(1); }}
}}
@keyframes busShimmer {{
  0% {{ background-position: -220% 0; }}
  100% {{ background-position: 220% 0; }}
}}
.block-container {{ animation: busFadeUp .45s ease both; }}
.hero {{ animation: busFadeUp .65s ease both; }}
.card {{ animation: busFadeUp .55s ease both; }}
[data-testid="stMetric"] {{ animation: busFadeUp .5s ease both; }}

.st-key-mobile_bottom_nav {{ display: none; }}

.bus-splash {{
  position: fixed;
  inset: 0;
  z-index: 999999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 24px;
  background: radial-gradient(circle at 50% 35%, #FFFDFB 0%, #FBE8E8 48%, #EFCFD6 100%);
  color: #351324;
}}
.bus-splash-logo {{
  width: min(72vw, 310px);
  max-height: 220px;
  object-fit: contain;
  border-radius: 22px;
  animation: busLogoIn .85s ease both;
  filter: drop-shadow(0 12px 20px rgba(53,19,36,.14));
}}
.bus-splash-title {{
  margin-top: 20px;
  color: #64243D;
  font-family: 'Playfair Display', Georgia, serif;
  font-weight: 700;
  font-size: clamp(25px, 5vw, 38px);
  letter-spacing: 1px;
  animation: busFadeUp .8s ease both;
}}
.bus-splash-subtitle {{
  margin-top: 8px;
  color: #755F69;
  font-size: 14px;
  letter-spacing: 1.4px;
  animation: busFadeUp 1s ease both;
}}
.bus-splash-line {{
  width: 150px;
  height: 3px;
  margin-top: 24px;
  border-radius: 99px;
  background: linear-gradient(90deg, #D7A66B, #C77B8C, #64243D, #D7A66B);
  background-size: 220% 100%;
  animation: busShimmer 1.4s linear infinite;
}}

@media (max-width: 768px) {{
  .block-container {{
    padding-bottom: 145px !important;
  }}
  .st-key-mobile_bottom_nav {{
    display: block !important;
    position: fixed !important;
    left: 8px !important;
    right: 8px !important;
    bottom: max(8px, env(safe-area-inset-bottom)) !important;
    z-index: 99990 !important;
    width: auto !important;
    padding: 8px 7px 9px !important;
    border: 1px solid #E5C8CF !important;
    border-radius: 17px !important;
    background: rgba(255,248,245,.97) !important;
    box-shadow: 0 5px 24px rgba(53,19,36,.18) !important;
    backdrop-filter: blur(12px);
  }}
  .st-key-mobile_bottom_nav [data-testid="stHorizontalBlock"] {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 4px !important;
    width: 100% !important;
  }}
  .st-key-mobile_bottom_nav [data-testid="column"] {{
    min-width: 0 !important;
    width: 20% !important;
    flex: 1 1 20% !important;
    padding: 0 !important;
  }}
  .st-key-mobile_bottom_nav .stButton button {{
    min-height: 36px !important;
    height: auto !important;
    padding: 5px 2px !important;
    border-radius: 9px !important;
    font-size: 10px !important;
    line-height: 1.15 !important;
    text-align: center !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    border: 1px solid #EBD8DC !important;
    background: #FFFDFB !important;
    color: #64243D !important;
  }}
  .st-key-mobile_bottom_nav .stButton button[kind="primary"] {{
    background: #64243D !important;
    color: #FFFFFF !important;
    border-color: #64243D !important;
  }}
  [data-testid="stPlotlyChart"] {{
    overflow: hidden !important;
  }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------- Animated welcome splash ----------------------------
if "bus_splash_shown_v2" not in st.session_state:
    st.session_state.bus_splash_shown_v2 = False

if not st.session_state.bus_splash_shown_v2:
    splash_placeholder = st.empty()
    splash_logo_path = ROOT / "logo.png.jpeg"
    if not splash_logo_path.exists():
        splash_logo_path = ROOT / "brand_panel.png.jpeg"

    logo_html = ""
    if splash_logo_path.exists():
        try:
            encoded_logo = base64.b64encode(splash_logo_path.read_bytes()).decode("utf-8")
            suffix = splash_logo_path.suffix.lower()
            mime = "image/jpeg" if suffix in [".jpg", ".jpeg"] else "image/png"
            logo_html = (
                f'<img class="bus-splash-logo" '
                f'src="data:{mime};base64,{encoded_logo}" alt="Bus Analytics logo">'
            )
        except Exception:
            logo_html = '<div style="font-size:76px">🚌</div>'
    else:
        logo_html = '<div style="font-size:76px">🚌</div>'

    splash_placeholder.markdown(
        f"""
        <div class="bus-splash">
            {logo_html}
            <div class="bus-splash-title">BUS ANALYTICS</div>
            <div class="bus-splash-subtitle">INTELLIGENT BUS TICKET DATA PLATFORM</div>
            <div class="bus-splash-line"></div>
            <div style="margin-top:22px;color:#8B737D;font-size:12px;letter-spacing:2px">
                CREATED BY CRACKER HEADS
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(2.2)
    splash_placeholder.empty()
    st.session_state.bus_splash_shown_v2 = True


# ---------------------------- Data helpers ----------------------------

def find_col(frame, candidates):
    lookup = {str(c).strip().lower(): c for c in frame.columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    for candidate in candidates:
        for key, original in lookup.items():
            if candidate.lower() in key:
                return original
    return None


def prepare_data(raw):
    df = raw.copy()
    mapping = {
        "waybill": ["Waybill Number", "Waybill", "waybill_number"],
        "ticket": ["Ticket Number", "Ticket No", "ticket_number"],
        "from": ["From Stop", "From", "Origin"],
        "to": ["To Stop", "To", "Destination"],
        "date": ["Date", "Journey Date", "Travel Date"],
        "time": ["Time", "Journey Time"],
        "passengers": ["Total Psgr", "Total Passenger", "Passengers", "Passenger Count"],
        "collected": ["Coll Amt", "Collected Amount", "Fare", "Amount Collected"],
        "uncollected": ["Uncoll Amt", "Uncollected Amount", "Pending Amount"],
    }
    selected = {name: find_col(df, aliases) for name, aliases in mapping.items()}
    required = ["from", "to", "date", "passengers", "collected"]
    missing = [x for x in required if selected[x] is None]
    if missing:
        raise ValueError("The uploaded CSV is missing required columns: " + ", ".join(missing))

    out = pd.DataFrame()
    for name, source in selected.items():
        if source is not None:
            out[name] = df[source]
        else:
            out[name] = "" if name in ["waybill", "ticket", "time"] else 0
    out["from"] = out["from"].fillna("Unknown").astype(str).str.strip()
    out["to"] = out["to"].fillna("Unknown").astype(str).str.strip()
    out["route"] = out["from"] + " – " + out["to"]
    out["date"] = pd.to_datetime(out["date"], errors="coerce", dayfirst=False)
    bad_dates = out["date"].isna()
    if bad_dates.any():
        out.loc[bad_dates, "date"] = pd.to_datetime(
            df.loc[bad_dates, selected["date"]], errors="coerce", dayfirst=True
        )
    for col in ["passengers", "collected", "uncollected"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)
    out["passengers"] = out["passengers"].clip(lower=0)
    out["collected"] = out["collected"].clip(lower=0)
    out["uncollected"] = out["uncollected"].clip(lower=0)
    out["ticket"] = out["ticket"].astype(str)
    out["waybill"] = out["waybill"].astype(str)
    return out


def load_default_data():
    if not DATA_FILE.exists():
        return None
    return pd.read_csv(DATA_FILE)


def money(value):
    return f"₹{value:,.0f}"


def style_chart(fig, height=360):
    fig.update_layout(
        template="bus_analytics",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, Arial, sans-serif",
            color=PLUM,
            size=13
        ),
        title_font=dict(color=BURGUNDY, size=18),
        margin=dict(l=15, r=25, t=55, b=25),
        autosize=True
    )
    fig.update_xaxes(
        tickfont=dict(color=PLUM, size=12),
        title_font=dict(color=BURGUNDY, size=13),
        color=PLUM
    )
    fig.update_yaxes(
        tickfont=dict(color=PLUM, size=12),
        title_font=dict(color=BURGUNDY, size=13),
        color=PLUM
    )
    return fig


def go_to(page):
    st.session_state.current_page = page


# ---------------------------- Session state ----------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "uploaded_raw" not in st.session_state:
    st.session_state.uploaded_raw = None

raw_data = st.session_state.uploaded_raw
if raw_data is None:
    try:
        raw_data = load_default_data()
    except Exception as exc:
        st.error(f"Could not read data/tickets.csv: {exc}")
        raw_data = None

if raw_data is not None:
    try:
        data = prepare_data(raw_data)
        data_error = None
    except Exception as exc:
        data = pd.DataFrame()
        data_error = str(exc)
else:
    data = pd.DataFrame()
    data_error = "No dataset found. Add your file at data/tickets.csv or upload a CSV from Upload Dataset."

# ---------------------------- Sidebar ----------------------------
with st.sidebar:
    brand_image = ROOT / "brand_panel.png.jpeg"
    logo_image = ROOT / "logo.png.jpeg"
    if brand_image.exists():
        st.image(str(brand_image), use_container_width=True)
    elif logo_image.exists():
        st.image(str(logo_image), use_container_width=True)
    else:
        st.markdown("<div style='text-align:center;padding:20px 8px;color:#64243D'><div style='font-size:3rem'>🚌</div><h2>BUS ANALYTICS</h2><small>Intelligent Bus Ticket Data Platform</small></div>", unsafe_allow_html=True)
    st.markdown("<div style='height:1px;background:#E5C8CF;margin:12px 0 18px'></div><p style='font-weight:800;letter-spacing:1px;font-size:.85rem'>NAVIGATION</p>", unsafe_allow_html=True)
    pages = [
        ("Home", "⌂"), ("Ticket Records", "▤"), ("Dashboard", "▦"),
        ("Route Analysis", "⌁"), ("Revenue Analysis", "₹"),
        ("Passenger Insights", "♙"), ("Demand Prediction", "↗"),
        ("Smart Insights", "✧"), ("Reports", "▧"), ("Upload Dataset", "⇧")
    ]
    for page, symbol in pages:
        label = f"{symbol}   {page}"
        if st.button(label, key=f"nav_{page}", type="primary" if st.session_state.current_page == page else "secondary"):
            go_to(page)
            st.rerun()
    st.markdown("<div style='height:1px;background:#E5C8CF;margin:18px 0'></div><p style='color:#987984;font-size:.8rem;letter-spacing:1px'>BOOK • ANALYZE • PREDICT</p><p style='color:#987984;font-size:.82rem'>Created by <b>CRACKER HEADS ♡</b></p>", unsafe_allow_html=True)

page = st.session_state.current_page

# ---------------------------- Always-accessible mobile navigation ----------------------------
mobile_nav_items = [
    ("Home", "Home"),
    ("Records", "Ticket Records"),
    ("Dashboard", "Dashboard"),
    ("Routes", "Route Analysis"),
    ("Revenue", "Revenue Analysis"),
    ("Passengers", "Passenger Insights"),
    ("Demand", "Demand Prediction"),
    ("Insights", "Smart Insights"),
    ("Reports", "Reports"),
    ("Upload", "Upload Dataset"),
]

with st.container(key="mobile_bottom_nav"):
    first_row = st.columns(5)
    for col, (label, destination) in zip(first_row, mobile_nav_items[:5]):
        with col:
            if st.button(
                label,
                key=f"mobile_nav_{destination}",
                type="primary" if page == destination else "secondary",
                use_container_width=True,
            ):
                go_to(destination)
                st.rerun()

    second_row = st.columns(5)
    for col, (label, destination) in zip(second_row, mobile_nav_items[5:]):
        with col:
            if st.button(
                label,
                key=f"mobile_nav_{destination}",
                type="primary" if page == destination else "secondary",
                use_container_width=True,
            ):
                go_to(destination)
                st.rerun()

# ---------------------------- Header ----------------------------
header_left, header_right = st.columns([5, 1])
with header_left:
    st.markdown(f"<div style='color:{MUTED};font-size:.8rem;font-weight:700;letter-spacing:1.4px'>CRACKER HEADS  /  BUS OPERATIONS</div>", unsafe_allow_html=True)
with header_right:
    st.markdown(f"<div style='text-align:right;color:{BURGUNDY};font-weight:700;padding-top:3px'>🚌 BUS ANALYTICS</div>", unsafe_allow_html=True)

# ---------------------------- Shared validation ----------------------------
if data_error and page != "Upload Dataset":
    st.warning(data_error)

# ---------------------------- Home ----------------------------
if page == "Home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">INTELLIGENT TRANSPORTATION ANALYTICS</div>
      <h1>Welcome to Bus Analytics</h1>
      <p>Monitor ticket activity, understand passenger movement and explore route performance with your bus ticket records.</p>
    </div>
    """, unsafe_allow_html=True)
    if not data.empty:
        total_tickets = len(data)
        total_passengers = int(data["passengers"].sum())
        total_revenue = float(data["collected"].sum())
        total_routes = int(data["route"].nunique())
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Tickets", f"{total_tickets:,}")
        m2.metric("Total Revenue", money(total_revenue))
        m3.metric("Total Passengers", f"{total_passengers:,}")
        m4.metric("Active Routes", f"{total_routes:,}")
        st.markdown("<div class='section-title'>Ticket activity overview</div>", unsafe_allow_html=True)
        chart_left, chart_right = st.columns([1.25, 1])
        with chart_left:
            trend = data.dropna(subset=["date"]).groupby(data["date"].dt.date).size().reset_index(name="Tickets")
            trend.columns = ["Date", "Tickets"]
            if not trend.empty:
                fig = px.area(trend, x="Date", y="Tickets", title="Ticket Bookings Trend")
                fig.update_traces(line_color=BURGUNDY, fillcolor="rgba(199,123,140,.25)")
                fig.update_layout(height=330, margin=dict(l=10,r=10,t=55,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=INK), title_font=dict(color=BURGUNDY, size=17))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No usable date values were found for the trend chart.")
        with chart_right:
            top_routes = data.groupby("route").agg(Tickets=("route", "size"), Passengers=("passengers", "sum")).reset_index().nlargest(7, "Tickets").sort_values("Tickets")
            if not top_routes.empty:
                fig = px.bar(top_routes, x="Tickets", y="route", orientation="h", title="Top Routes by Tickets", text="Tickets")
                fig.update_traces(marker_color=ROSE, textposition="outside", cliponaxis=False)
                fig.update_layout(height=330, margin=dict(l=10,r=25,t=55,b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=INK), title_font=dict(color=BURGUNDY, size=17), yaxis_title="", xaxis_title="Tickets")
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("<div class='section-title'>Explore your analytics</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='card'><h3>↗ Demand Prediction</h3><p>Explore historical ticket demand and simple upcoming demand estimates.</p></div>", unsafe_allow_html=True)
            if st.button("Explore demand", key="home_demand", use_container_width=True): go_to("Demand Prediction"); st.rerun()
        with c2:
            st.markdown("<div class='card'><h3>✧ Smart Insights</h3><p>Find useful observations from routes, passengers and collections.</p></div>", unsafe_allow_html=True)
            if st.button("Explore insights", key="home_insights", use_container_width=True): go_to("Smart Insights"); st.rerun()
        with c3:
            st.markdown("<div class='card'><h3>▧ Generate Reports</h3><p>Export ticket records and summary data for further review.</p></div>", unsafe_allow_html=True)
            if st.button("Explore reports", key="home_reports", use_container_width=True): go_to("Reports"); st.rerun()
    else:
        st.markdown("<div class='card'><h3>Your analytics workspace is ready</h3><p>Upload the ticket dataset to populate ticket totals, revenue, passenger insights, route charts and reports.</p></div>", unsafe_allow_html=True)
        if st.button("Upload ticket dataset", type="primary"):
            go_to("Upload Dataset"); st.rerun()
            # ---------------------------- Ticket Records ----------------------------
elif page == "Ticket Records":
    st.title("Ticket Records")
    st.caption("Search, review and export the ticket records in your dataset.")
    if not data.empty:
        search = st.text_input(
            "Search by ticket, waybill, route or stop",
            placeholder="Type a ticket number, route or stop..."
        )
        view = data.copy()
        if search.strip():
            mask = view.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False)
            ).any(axis=1)
            view = view[mask]

        st.write(f"**{len(view):,}** records found")
        display = view.rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from": "From Stop",
            "to": "To Stop",
            "date": "Date",
            "time": "Time",
            "passengers": "Passengers",
            "collected": "Collected Amount (₹)",
            "uncollected": "Uncollected Amount (₹)"
        })
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )
        st.download_button(
            "Download filtered records (CSV)",
            view.to_csv(index=False).encode("utf-8"),
            "ticket_records.csv",
            "text/csv"
        )
    else:
        st.info("Upload a CSV dataset to view ticket records.")

# ---------------------------- Dashboard ----------------------------
elif page == "Dashboard":
    st.title("Operations Dashboard")
    st.caption("A consolidated view of ticketing and bus operation activity.")
    if not data.empty:
        a, b, c, d = st.columns(4)
        a.metric("Tickets", f"{len(data):,}")
        b.metric("Passengers", f"{int(data.passengers.sum()):,}")
        c.metric("Collected", money(data.collected.sum()))
        d.metric("Uncollected", money(data.uncollected.sum()))

        x, y = st.columns(2)
        with x:
            by_day = (
                data.dropna(subset=["date"])
                .groupby(data.date.dt.day_name())
                .size()
                .reindex([
                    "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"
                ])
                .dropna()
                .reset_index()
            )
            by_day.columns = ["Day", "Tickets"]
            fig = px.bar(
                by_day, x="Day", y="Tickets",
                title="Tickets by Day of Week",
                color_discrete_sequence=[ROSE],
                text="Tickets"
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(height=350, margin=dict(t=55, l=10, r=10, b=10))
            st.plotly_chart(style_chart(fig, 350), use_container_width=True)

        with y:
            origin_counts = (
                data.groupby("from").size().sort_values(ascending=False)
            )
            top_origins = origin_counts.head(10)
            other_count = int(origin_counts.iloc[10:].sum())
            origin_plot = top_origins.reset_index()
            origin_plot.columns = ["Origin", "Tickets"]

            if other_count > 0:
                origin_plot = pd.concat([
                    origin_plot,
                    pd.DataFrame([{
                        "Origin": "Other stops",
                        "Tickets": other_count
                    }])
                ], ignore_index=True)

            fig = px.bar(
                origin_plot.sort_values("Tickets"),
                x="Tickets", y="Origin",
                orientation="h",
                title="Top Ticket Origins",
                text="Tickets",
                color_discrete_sequence=[ROSE]
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(
                height=420,
                margin=dict(t=55, l=10, r=35, b=10),
                yaxis_title="",
                xaxis_title="Number of Tickets",
                showlegend=False
            )
            st.plotly_chart(style_chart(fig, 420), use_container_width=True)
    else:
        st.info("Upload your ticket CSV to see the dashboard.")

# ---------------------------- Route Analysis ----------------------------
elif page == "Route Analysis":
    st.title("Route Analysis")
    st.caption("Compare route activity, passenger volume and collected amounts.")

    if not data.empty:
        routes = (
            data.groupby("route")
            .agg(
                Tickets=("route", "size"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum")
            )
            .reset_index()
            .sort_values("Tickets", ascending=False)
        )

        st.dataframe(routes, use_container_width=True, hide_index=True)

        fig = px.bar(
            routes.head(15).sort_values("Passengers"),
            x="Passengers", y="route",
            orientation="h",
            title="Top 15 Routes by Passenger Count",
            color_discrete_sequence=[BURGUNDY]
        )
        fig.update_layout(
            height=520,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=55, l=10, r=15, b=10),
            yaxis_title="",
            font=dict(color=PLUM),
            title_font=dict(color=BURGUNDY),
            yaxis=dict(tickfont=dict(color=PLUM, size=12)),
            xaxis=dict(tickfont=dict(color=PLUM, size=12))
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            "<div class='section-title'>Route Performance Score</div>",
            unsafe_allow_html=True
        )

        score_df = routes.copy()

        def normalise(series):
            low, high = series.min(), series.max()
            if high == low:
                return pd.Series([50.0] * len(series), index=series.index)
            return (series - low) / (high - low) * 100

        score_df["Ticket Score"] = normalise(score_df["Tickets"])
        score_df["Passenger Score"] = normalise(score_df["Passengers"])
        score_df["Revenue Score"] = normalise(score_df["Revenue"])
        score_df["Performance Score"] = (
            score_df["Ticket Score"] * .35
            + score_df["Passenger Score"] * .35
            + score_df["Revenue Score"] * .30
        ).round(1)

        score_df = score_df.sort_values(
            "Performance Score", ascending=False
        )
        best = score_df.iloc[0]

        st.success(
            f"Top-performing route in this dataset: {best['route']} — "
            f"{best['Performance Score']:.1f}/100"
        )
        st.caption(
            "Score is a relative comparison within this uploaded dataset: "
            "35% ticket volume, 35% passengers and 30% collected revenue. "
            "It is not an official service-quality rating."
        )

        st.dataframe(
            score_df[[
                "route", "Tickets", "Passengers",
                "Revenue", "Performance Score"
            ]].rename(columns={
                "route": "Route",
                "Revenue": "Collected Revenue (₹)"
            }),
            use_container_width=True,
            hide_index=True
        )

        score_chart = px.bar(
            score_df.head(10).sort_values("Performance Score"),
            x="Performance Score",
            y="route",
            orientation="h",
            title="Top 10 Routes by Performance Score",
            text="Performance Score",
            color_discrete_sequence=[ROSE]
        )
        score_chart.update_traces(textposition="outside", cliponaxis=False)
        score_chart.update_layout(
            yaxis_title="",
            xaxis_title="Relative score out of 100",
            xaxis_range=[0, 115],
            margin=dict(l=12, r=45, t=55, b=20)
        )
        st.plotly_chart(
            style_chart(score_chart, 400),
            use_container_width=True
        )
    else:
        st.info("Upload your ticket CSV to analyse routes.")

# ---------------------------- Revenue Analysis ----------------------------
elif page == "Revenue Analysis":
    st.title("Revenue Analysis")
    st.caption("Review collected and uncollected ticket amounts.")

    if not data.empty:
        a, b, c = st.columns(3)
        a.metric("Collected Amount", money(data.collected.sum()))
        b.metric("Uncollected Amount", money(data.uncollected.sum()))
        c.metric(
            "Total Recorded Amount",
            money(data.collected.sum() + data.uncollected.sum())
        )

        rev = (
            data.groupby("route")
            .agg(
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
            .sort_values("Collected", ascending=False)
            .head(12)
        )

        fig = px.bar(
            rev,
            x="route",
            y=["Collected", "Uncollected"],
            barmode="group",
            title="Revenue by Route",
            color_discrete_sequence=[BURGUNDY, GOLD]
        )
        fig.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=55, l=10, r=10, b=100),
            xaxis_title="",
            legend_title_text="Amount"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Upload your ticket CSV to analyse revenue.")

# ---------------------------- Passenger Insights ----------------------------
elif page == "Passenger Insights":
    st.title("Passenger Insights")
    st.caption("Understand passenger volumes and the busiest boarding points.")

    if not data.empty:
        a, b, c = st.columns(3)
        a.metric("Total Passengers", f"{int(data.passengers.sum()):,}")
        b.metric("Average Passengers / Ticket", f"{data.passengers.mean():.2f}")
        c.metric("Boarding Stops", f"{data['from'].nunique():,}")

        board = (
            data.groupby("from")
            .agg(
                Passengers=("passengers", "sum"),
                Tickets=("from", "size")
            )
            .reset_index()
            .nlargest(12, "Passengers")
            .sort_values("Passengers")
        )

        fig = px.bar(
            board,
            x="Passengers", y="from",
            orientation="h",
            title="Busiest Boarding Stops",
            color_discrete_sequence=[ROSE]
        )
        fig.update_layout(
            height=440,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=55, l=10, r=15, b=10),
            yaxis_title="",
            font=dict(color=PLUM),
            title_font=dict(color=BURGUNDY),
            yaxis=dict(tickfont=dict(color=PLUM, size=12)),
            xaxis=dict(tickfont=dict(color=PLUM, size=12))
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Upload your ticket CSV to view passenger insights.")

# ---------------------------- Demand Prediction ----------------------------
elif page == "Demand Prediction":
    st.title("Demand Prediction")
    st.caption(
        "Explore when passengers travel, which routes are busiest, "
        "and how demand changes across the available records."
    )

    if not data.empty:
        time_values = pd.to_datetime(
            data["time"].astype(str).str.strip(),
            errors="coerce"
        )
        hourly_data = data.copy()
        hourly_data["Hour"] = time_values.dt.hour
        valid_hours = hourly_data.dropna(subset=["Hour"]).copy()

        if not valid_hours.empty:
            valid_hours["Hour"] = valid_hours["Hour"].astype(int)

            hourly = (
                valid_hours.groupby("Hour")
                .agg(
                    Tickets=("ticket", "size"),
                    Passengers=("passengers", "sum")
                )
                .reindex(range(24), fill_value=0)
                .reset_index()
            )

            hourly["Time Slot"] = hourly["Hour"].apply(
                lambda h: f"{h:02d}:00"
            )

            peak_row = hourly.loc[hourly["Tickets"].idxmax()]
            peak_hour = int(peak_row["Hour"])
            peak_label = (
                f"{peak_hour:02d}:00–{(peak_hour + 1) % 24:02d}:00"
            )

            busiest_route = (
                data.groupby("route").size().sort_values(ascending=False)
            )
            top_route = busiest_route.index[0]

            k1, k2, k3 = st.columns(3)
            k1.metric("Recorded Tickets", f"{len(data):,}")
            k2.metric("Busiest Hour", peak_label)
            k3.metric("Busiest Route", top_route)

            st.markdown(
                '<div class="section-title">Hourly Travel Demand</div>',
                unsafe_allow_html=True
            )

            fig = px.bar(
                hourly,
                x="Time Slot",
                y="Tickets",
                title="Ticket Activity by Hour",
                color="Tickets",
                color_continuous_scale=["#F3DDE1", BURGUNDY],
            )
            fig.update_traces(
                marker_line_width=0,
                hovertemplate="Time: %{x}<br>Tickets: %{y:,}<extra></extra>"
            )
            fig.update_layout(
                height=390,
                coloraxis_showscale=False,
                xaxis_title="Time of Day",
                yaxis_title="Number of Tickets",
                margin=dict(t=55, l=10, r=20, b=45),
                xaxis=dict(
                    title="Time of Day",
                    tickmode="array",
                    tickvals=[f"{h:02d}:00" for h in range(0, 24, 3)],
                    tickangle=-30,
                    automargin=True
                )
            )
            st.plotly_chart(
                style_chart(fig, 390),
                use_container_width=True,
                config={"responsive": True, "displayModeBar": False}
            )

            left, right = st.columns(2)

            with left:
                st.markdown(
                    '<div class="section-title">Passenger Activity by Hour</div>',
                    unsafe_allow_html=True
                )
                fig2 = px.line(
                    hourly,
                    x="Time Slot",
                    y="Passengers",
                    markers=True,
                    title="Hourly Passenger Volume"
                )
                fig2.update_traces(
                    line=dict(color=BURGUNDY, width=3),
                    marker=dict(color=ROSE, size=7)
                )
                fig2.update_layout(
                    height=340,
                    xaxis_title="Time of Day",
                    yaxis_title="Passengers",
                    margin=dict(t=55, l=10, r=10, b=45),
                    xaxis=dict(
                        title="Time of Day",
                        tickmode="array",
                        tickvals=[f"{h:02d}:00" for h in range(0, 24, 3)],
                        tickangle=-30,
                        automargin=True
                    )
                )
                st.plotly_chart(
                    style_chart(fig2, 340),
                    use_container_width=True,
                    config={"responsive": True, "displayModeBar": False}
                )

            with right:
                st.markdown(
                    '<div class="section-title">Top Routes by Demand</div>',
                    unsafe_allow_html=True
                )
                route_demand = (
                    data.groupby("route")
                    .agg(
                        Tickets=("ticket", "size"),
                        Passengers=("passengers", "sum")
                    )
                    .reset_index()
                    .nlargest(8, "Tickets")
                    .sort_values("Tickets")
                )
                fig3 = px.bar(
                    route_demand,
                    x="Tickets",
                    y="route",
                    orientation="h",
                    title="Most Used Routes",
                    text="Tickets",
                    color_discrete_sequence=[ROSE]
                )
                fig3.update_traces(
                    textposition="outside",
                    cliponaxis=False
                )
                fig3.update_layout(
                    height=340,
                    xaxis_title="Tickets",
                    yaxis_title="",
                    margin=dict(t=55, l=10, r=30, b=10)
                )
                st.plotly_chart(
                    style_chart(fig3, 340),
                    use_container_width=True
                )

            st.info(
                "Data coverage note: your current dataset contains records "
                "for one travel date only. The hourly charts describe that "
                "day's recorded activity. A reliable daily trend or future "
                "forecast needs ticket records from multiple dates."
            )
        else:
            st.warning(
                "The dataset has no readable time values. Check the Time "
                "column to enable hourly demand analysis."
            )
    else:
        st.info("Upload your ticket CSV to explore demand.")

# ---------------------------- Smart Insights ----------------------------
elif page == "Smart Insights":
    st.title("🧠 Intelligent Transport Insights")
    st.caption(
        "An intelligent analysis system that converts ticket records "
        "into operational observations and management recommendations."
    )

    if not data.empty:
        route_stats = (
            data.groupby("route")
            .agg(
                Tickets=("route", "size"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        total_tickets = len(data)
        total_passengers = data["passengers"].sum()
        total_revenue = data["collected"].sum()
        total_uncollected = data["uncollected"].sum()

        busiest_route = route_stats.sort_values(
            "Tickets", ascending=False
        ).iloc[0]
        passenger_route = route_stats.sort_values(
            "Passengers", ascending=False
        ).iloc[0]
        revenue_route = route_stats.sort_values(
            "Revenue", ascending=False
        ).iloc[0]

        average_tickets = route_stats["Tickets"].mean()

        st.markdown("## Intelligence Overview")
        a, b, c, d = st.columns(4)
        a.metric("Routes Analysed", len(route_stats))
        b.metric("Tickets Analysed", f"{total_tickets:,}")
        c.metric("Passengers", f"{total_passengers:,.0f}")
        d.metric("Revenue", money(total_revenue))

        st.markdown("---")

        # 1. Smart Demand Recommendations
        st.markdown("## 1. Smart Demand Recommendations")
        st.markdown(
            f"""
            <div class="card">
                <h3>Highest Ticket Demand</h3>
                <h2>{busiest_route['route']}</h2>
                <p>This route has {int(busiest_route['Tickets']):,}
                ticket records, making it the busiest route in the dataset.</p>
                <p><b>Recommendation:</b> Review passenger demand and
                consider whether additional bus frequency is needed
                during the busiest travel periods.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if busiest_route["Tickets"] > average_tickets * 1.5:
            st.success(
                "High-demand alert: this route has more than "
                "1.5 times the average ticket volume."
            )

        # 2. Route Intelligence
        st.markdown("## 2. Route Intelligence")
        route_stats["Relative Performance"] = (
            route_stats["Tickets"] / max(route_stats["Tickets"].max(), 1) * 35
            + route_stats["Passengers"] / max(route_stats["Passengers"].max(), 1) * 35
            + route_stats["Revenue"] / max(route_stats["Revenue"].max(), 1) * 30
        ).round(1)

        best_routes = route_stats.sort_values(
            "Relative Performance", ascending=False
        )

        st.dataframe(
            best_routes.rename(columns={
                "route": "Route",
                "Revenue": "Collected Revenue (₹)",
                "Uncollected": "Uncollected Amount (₹)",
                "Relative Performance": "Performance Score"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Performance score is a relative comparison using ticket "
            "volume (35%), passenger volume (35%) and collected revenue "
            "(30%). It is not an official route-quality rating."
        )

        lower_activity = route_stats[
            route_stats["Tickets"] < average_tickets * 0.5
        ]

        if not lower_activity.empty:
            st.warning(
                "Some routes have relatively low ticket activity. "
                "Review their demand and schedules before changing service."
            )

        # 3. Revenue Intelligence
        st.markdown("## 3. Revenue Intelligence")
        total_amount = total_revenue + total_uncollected
        collection_rate = (
            total_revenue / total_amount * 100 if total_amount > 0 else 0
        )

        r1, r2, r3 = st.columns(3)
        r1.metric("Collected Revenue", money(total_revenue))
        r2.metric("Uncollected Amount", money(total_uncollected))
        r3.metric("Collection Rate", f"{collection_rate:.1f}%")

        revenue_review = route_stats.sort_values(
            "Uncollected", ascending=False
        ).head(8)

        revenue_fig = px.bar(
            revenue_review.sort_values("Uncollected"),
            x="Uncollected",
            y="route",
            orientation="h",
            title="Routes with Highest Recorded Uncollected Amount",
            color_discrete_sequence=[BURGUNDY],
        )
        revenue_fig.update_layout(
            xaxis_title="Uncollected amount (₹)",
            yaxis_title=""
        )
        st.plotly_chart(
            style_chart(revenue_fig, 360),
            use_container_width=True
        )

        if total_uncollected > 0:
            st.warning(
                f"{money(total_uncollected)} is recorded as uncollected. "
                "Reconcile the related tickets and payment records."
            )
        else:
            st.success("No uncollected amount is recorded in this dataset.")

        # 4. Peak-Hour Intelligence and Heatmap
        st.markdown("## 4. Peak-Hour Intelligence")
        parsed_time = pd.to_datetime(
            data["time"].astype(str).str.strip(),
            errors="coerce"
        )
        timed = data.copy()
        timed["Hour"] = parsed_time.dt.hour
        timed = timed.dropna(subset=["Hour"]).copy()

        if not timed.empty:
            timed["Hour"] = timed["Hour"].astype(int)
            hourly = (
                timed.groupby("Hour")
                .agg(
                    Tickets=("ticket", "size"),
                    Passengers=("passengers", "sum")
                )
                .reindex(range(24), fill_value=0)
                .reset_index()
            )

            peak_row = hourly.loc[hourly["Tickets"].idxmax()]
            peak_hour = int(peak_row["Hour"])
            peak_count = int(peak_row["Tickets"])

            st.metric(
                "Busiest Recorded Hour",
                f"{peak_hour:02d}:00–{(peak_hour + 1) % 24:02d}:00",
                f"{peak_count:,} tickets"
            )

            hourly_fig = px.bar(
                hourly,
                x="Hour",
                y="Tickets",
                title="Ticket Activity by Hour",
                color="Tickets",
                color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
            )
            hourly_fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Hour of day",
                yaxis_title="Tickets"
            )
            st.plotly_chart(
                style_chart(hourly_fig, 350),
                use_container_width=True
            )

            st.info(
                f"Planning suggestion: review staffing and timetable "
                f"coverage around {peak_hour:02d}:00. "
                "This is a historical observation, not a live capacity measurement."
            )

            heat_source = timed.dropna(subset=["date"]).copy()
            if not heat_source.empty:
                heat_source["Travel Date"] = (
                    heat_source["date"].dt.strftime("%d %b %Y")
                )
                heat = (
                    heat_source.groupby(["Travel Date", "Hour"])
                    .size()
                    .reset_index(name="Tickets")
                )
                pivot = heat.pivot(
                    index="Travel Date",
                    columns="Hour",
                    values="Tickets"
                ).fillna(0)
                pivot = pivot.reindex(columns=range(24), fill_value=0)

                heat_fig = go.Figure(data=go.Heatmap(
                    z=pivot.values,
                    x=[f"{hour:02d}:00" for hour in range(24)],
                    y=pivot.index.tolist(),
                    colorscale=[
                        [0, "#FBECEF"],
                        [0.5, "#DFAAB7"],
                        [1, BURGUNDY]
                    ],
                    colorbar=dict(title="Tickets"),
                    hovertemplate=(
                        "Date: %{y}<br>Hour: %{x}<br>"
                        "Tickets: %{z}<extra></extra>"
                    ),
                ))
                heat_fig.update_layout(
                    title="Peak-Hour Heatmap",
                    xaxis_title="Hour of day",
                    yaxis_title="Travel date"
                )
                st.plotly_chart(
                    style_chart(
                        heat_fig,
                        max(300, min(600, 45 * len(pivot) + 120))
                    ),
                    use_container_width=True
                )
        else:
            st.info(
                "Readable time values are needed for peak-hour analysis."
            )

        # 5. Unusual Activity Detection
        st.markdown("## 5. Unusual Activity Detection")
        alerts = []

        if len(route_stats) >= 3:
            ticket_std = route_stats["Tickets"].std(ddof=0)
            if ticket_std > 0:
                ticket_z = (
                    route_stats["Tickets"] - route_stats["Tickets"].mean()
                ) / ticket_std

                for idx in route_stats.index[ticket_z.abs() >= 2]:
                    direction = (
                        "higher" if ticket_z.loc[idx] > 0 else "lower"
                    )
                    alerts.append(
                        f"{route_stats.loc[idx, 'route']}: ticket count is "
                        f"unusually {direction} compared with the route "
                        "average. Review the source records."
                    )

        if len(data) >= 5:
            revenue_mean = data["collected"].mean()
            revenue_std = data["collected"].std(ddof=0)

            if revenue_std > 0:
                revenue_z = (
                    data["collected"] - revenue_mean
                ) / revenue_std
                unusual_revenue = data.loc[revenue_z.abs() >= 3]

                if not unusual_revenue.empty:
                    alerts.append(
                        f"{len(unusual_revenue)} ticket record(s) have "
                        "collected amounts more than three standard "
                        "deviations from the average. Check these records."
                    )

        if alerts:
            for alert in alerts[:8]:
                st.warning(alert)
        else:
            st.success(
                "No major outliers were detected using the current "
                "statistical screening rules."
            )

        st.caption(
            "Outlier flags are review prompts, not proof of fraud "
            "or data-entry errors."
        )

        # 6. Management Recommendations
        st.markdown("## 6. Management Recommendations")

        recommendations = [
            f"Review timetable and service frequency for "
            f"{busiest_route['route']}, the route with the most ticket records.",
            f"Review passenger movement on {passenger_route['route']}, "
            "which has the highest recorded passenger total.",
            f"Monitor collection performance on {revenue_route['route']}, "
            "which has the highest collected revenue.",
        ]

        if total_uncollected > 0:
            recommendations.append(
                "Reconcile uncollected amounts against ticket and payment records."
            )

        if not timed.empty:
            recommendations.append(
                f"Review operating coverage around the recorded peak "
                f"hour of {peak_hour:02d}:00."
            )

        if not lower_activity.empty:
            recommendations.append(
                "Investigate low-activity routes before changing their service allocation."
            )

        for number, recommendation in enumerate(recommendations, start=1):
            st.markdown(
                f"""
                <div class="card">
                    <h3>Recommendation {number}</h3>
                    <p>{recommendation}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.caption(
            "Methodology: these insights are generated using transparent "
            "statistical rules from the uploaded historical ticket data. "
            "They are decision-support suggestions, not a trained AI model, "
            "live bus tracking, or confirmation of current bus capacity. "
            "Reliable daily forecasting requires records from multiple travel dates."
        )

    else:
        st.info(
            "Upload a valid ticket dataset to activate Intelligent Transport Insights."
        )

# ---------------------------- Reports ----------------------------
elif page == "Reports":
    st.title("Reports")
    st.caption("Download the dataset and summary tables for reporting.")

    if not data.empty:
        summary = pd.DataFrame({
            "Metric": [
                "Total Tickets",
                "Total Passengers",
                "Collected Amount",
                "Uncollected Amount",
                "Distinct Routes"
            ],
            "Value": [
                len(data),
                int(data.passengers.sum()),
                data.collected.sum(),
                data.uncollected.sum(),
                data.route.nunique()
            ]
        })

        st.subheader("Dataset summary")
        st.dataframe(summary, use_container_width=True, hide_index=True)

        st.download_button(
            "Download full ticket data (CSV)",
            data.to_csv(index=False).encode("utf-8"),
            "bus_ticket_records.csv",
            "text/csv",
            type="primary"
        )

        st.download_button(
            "Download summary (CSV)",
            summary.to_csv(index=False).encode("utf-8"),
            "bus_analytics_summary.csv",
            "text/csv"
        )

        route_summary = (
            data.groupby("route")
            .agg(
                Tickets=("route", "size"),
                Passengers=("passengers", "sum"),
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        st.download_button(
            "Download route report (CSV)",
            route_summary.to_csv(index=False).encode("utf-8"),
            "route_analysis_report.csv",
            "text/csv"
        )
    else:
        st.info("Upload your ticket CSV to generate reports.")

# ---------------------------- Upload Dataset ----------------------------
elif page == "Upload Dataset":
    st.title("Upload Dataset")
    st.caption(
        "Upload a CSV containing bus ticket records. "
        "Your repository dataset remains the default source after app restarts."
    )

    uploaded = st.file_uploader(
        "Choose ticket data (CSV)",
        type=["csv"]
    )

    if uploaded is not None:
        try:
            candidate = pd.read_csv(uploaded)
            checked = prepare_data(candidate)
            st.session_state.uploaded_raw = candidate

            st.success(
                f"Dataset loaded successfully — "
                f"{len(checked):,} ticket records detected."
            )

            st.dataframe(
                checked.head(10),
                use_container_width=True,
                hide_index=True
            )

            if st.button("Use repository dataset instead"):
                st.session_state.uploaded_raw = None
                st.rerun()

        except Exception as exc:
            st.error(f"This CSV could not be used: {exc}")

    else:
        if DATA_FILE.exists():
            st.success("Repository dataset found: data/tickets.csv")
            st.caption(
                "The app will load this dataset automatically "
                "when no temporary upload is active."
            )
        else:
            st.warning(
                "No repository dataset found yet. Upload a CSV or "
                "add data/tickets.csv to your GitHub repository."
            )

# ---------------------------- Footer ----------------------------
st.markdown(
    "<hr><div style='text-align:center;color:#987984;font-size:.82rem;"
    "padding:8px 0 2px'>BOOK • ANALYZE • PREDICT &nbsp; | &nbsp; "
    "Created by <b>CRACKER HEADS ♡</b></div>",
    unsafe_allow_html=True
)

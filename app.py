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

# Apply readable chart text to every Plotly chart.
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

:root {{
    --bg:{BG};
    --pink:{PINK};
    --burgundy:{BURGUNDY};
    --plum:{PLUM};
    --rose:{ROSE};
    --gold:{GOLD};
    --ink:{INK};
    --muted:{MUTED};
}}

html, body, [data-testid="stAppViewContainer"] {{
    background:var(--bg);
    color:var(--ink);
    font-family:'DM Sans',sans-serif;
}}

[data-testid="stHeader"] {{
    background:rgba(255,248,245,.92);
}}

[data-testid="stToolbar"] {{
    right:1rem;
}}

.block-container {{
    padding-top:1.15rem !important;
    padding-bottom:2rem !important;
    max-width:1600px;
}}

[data-testid="stSidebar"] {{
    background:linear-gradient(180deg,#FBEAE7 0%,#F5DFE2 100%);
    border-right:1px solid #EAD1D5;
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top:1rem;
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color:var(--burgundy);
}}

[data-testid="stSidebar"] .stButton button {{
    width:100%;
    text-align:left;
    border:1px solid transparent;
    border-radius:13px;
    background:transparent;
    color:var(--burgundy);
    font-weight:600;
    padding:.65rem .8rem;
}}

[data-testid="stSidebar"] .stButton button:hover {{
    background:#F4D5D8;
    border-color:#E8BFC7;
    color:var(--plum);
}}

[data-testid="stSidebar"] [data-testid="stImage"] img {{
    border-radius:17px;
}}

[data-testid="stMetric"] {{
    background:linear-gradient(135deg,#FFF 0%,#FCEDEF 100%);
    border:1px solid #EBD8DC;
    border-radius:18px;
    padding:17px 18px;
    box-shadow:0 4px 16px rgba(85,35,55,.045);
}}

[data-testid="stMetricLabel"] p {{
    color:#806B75 !important;
    font-weight:600;
}}

[data-testid="stMetricValue"] {{
    color:var(--plum) !important;
    font-weight:800;
}}

[data-testid="stMetricDelta"] {{
    font-size:.82rem;
}}

.card {{
    background:#FFFFFF;
    border:1px solid #EAD9DD;
    border-radius:20px;
    padding:20px 22px;
    box-shadow:0 5px 18px rgba(73,32,50,.045);
    height:100%;
}}

.card h3 {{
    color:var(--burgundy);
    margin:0 0 8px 0;
    font-size:1.05rem;
}}

.card p {{
    color:#755F69;
    margin:0;
    line-height:1.55;
}}

.hero {{
    border-radius:22px;
    padding:30px 34px;
    color:white;
    min-height:190px;
    background:linear-gradient(
        105deg,
        rgba(45,17,36,.96),
        rgba(91,35,61,.78)
    );
    border:1px solid #6E3A50;
    margin-bottom:20px;
}}

.hero .eyebrow {{
    color:#F5D4C9;
    letter-spacing:2px;
    font-size:.75rem;
    font-weight:700;
}}

.hero h1 {{
    color:#FFF4ED;
    font-family:'Playfair Display',serif;
    font-size:clamp(2rem,4vw,3.1rem);
    line-height:1.08;
    margin:8px 0;
}}

.hero p {{
    color:#F8E7E4;
    font-size:1rem;
    max-width:650px;
    margin:0;
}}

.section-title {{
    color:var(--burgundy);
    font-size:1.25rem;
    font-weight:800;
    margin:1.2rem 0 .7rem 0;
}}

.small-note {{
    color:var(--muted);
    font-size:.84rem;
}}

.stButton button[kind="primary"] {{
    background:var(--burgundy);
    color:white;
    border:0;
    border-radius:12px;
    font-weight:700;
}}

.stButton button[kind="primary"]:hover {{
    background:var(--plum);
    color:white;
}}

.stDownloadButton button {{
    background:#F3DDE1;
    color:var(--burgundy);
    border:1px solid #E6C4CB;
    border-radius:12px;
    font-weight:700;
}}

[data-testid="stDataFrame"] {{
    border:1px solid #EAD9DD;
    border-radius:14px;
    overflow:hidden;
}}

hr {{
    border-color:#EAD5DA !important;
}}

footer {{
    visibility:hidden;
}}

/* High contrast text */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] {{
    color:#382832;
}}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {{
    color:#64243D !important;
}}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
    color:#624D57 !important;
    opacity:1 !important;
}}

/* Force light mode */
:root,
html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {{
    color-scheme:light !important;
    background-color:#FFF8F5 !important;
    color:#382832 !important;
}}

[data-testid="stMain"] > div {{
    background-color:#FFF8F5 !important;
}}

/* Inputs and chat text must remain visible */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input,
[data-testid="stSelectbox"] div,
[data-testid="stDateInput"] input {{
    color:#351324 !important;
    -webkit-text-fill-color:#351324 !important;
    background-color:#FFFFFF !important;
    caret-color:#64243D !important;
}}

[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder {{
    color:#806B75 !important;
    opacity:1 !important;
}}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] span {{
    color:#351324 !important;
    opacity:1 !important;
}}

[data-testid="stDataFrame"] {{
    background:#FFFFFF !important;
}}

[data-testid="stDataFrame"] iframe {{
    color-scheme:light !important;
}}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {{
    color:#64243D !important;
    font-weight:700 !important;
}}

.js-plotly-plot .plotly text,
.js-plotly-plot .plotly .xtick text,
.js-plotly-plot .plotly .ytick text,
.js-plotly-plot .plotly .legend text {{
    fill:#351324 !important;
}}

.js-plotly-plot .plotly .gtitle {{
    fill:#64243D !important;
}}

/* Responsive layout */
@media (max-width:768px) {{
    .block-container {{
        width:100% !important;
        max-width:100% !important;
        padding:.65rem .7rem 1.5rem .7rem !important;
    }}

    [data-testid="stHorizontalBlock"] {{
        flex-direction:column !important;
        flex-wrap:nowrap !important;
        gap:.8rem !important;
    }}

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        width:100% !important;
        min-width:100% !important;
        flex:1 1 100% !important;
    }}

    .hero {{
        padding:21px 17px !important;
        min-height:unset !important;
    }}

    .hero h1 {{
        font-size:1.7rem !important;
        line-height:1.2 !important;
    }}

    .hero p {{
        font-size:.92rem !important;
        line-height:1.55 !important;
    }}

    [data-testid="stMetric"] {{
        padding:12px !important;
        min-width:0 !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size:1.3rem !important;
        overflow-wrap:anywhere !important;
    }}

    .card {{
        padding:16px !important;
        min-height:unset !important;
    }}

    [data-testid="stPlotlyChart"] {{
        width:100% !important;
        max-width:100% !important;
        overflow-x:auto !important;
        padding:2px !important;
    }}

    [data-testid="stDataFrame"] {{
        max-width:100% !important;
        overflow-x:auto !important;
    }}

    .stButton button,
    .stDownloadButton button {{
        min-height:44px !important;
        white-space:normal !important;
    }}

    [data-testid="stSidebar"] {{
        min-width:min(86vw,310px) !important;
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
            encoded_logo = base64.b64encode(
                splash_logo_path.read_bytes()
            ).decode("utf-8")

            suffix = splash_logo_path.suffix.lower()
            mime = (
                "image/jpeg"
                if suffix in [".jpg", ".jpeg"]
                else "image/png"
            )

            logo_html = (
                f'<img class="bus-splash-logo" '
                f'src="data:{mime};base64,{encoded_logo}" '
                f'alt="Bus Analytics logo">'
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
            <div class="bus-splash-subtitle">
                INTELLIGENT BUS TICKET DATA PLATFORM
            </div>
            <div class="bus-splash-line"></div>
            <div style="margin-top:22px;color:#8B737D;
                        font-size:12px;letter-spacing:2px">
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
    lookup = {
        str(column).strip().lower(): column
        for column in frame.columns
    }

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
        "passengers": [
            "Total Psgr",
            "Total Passenger",
            "Passengers",
            "Passenger Count"
        ],
        "collected": [
            "Coll Amt",
            "Collected Amount",
            "Fare",
            "Amount Collected"
        ],
        "uncollected": [
            "Uncoll Amt",
            "Uncollected Amount",
            "Pending Amount"
        ],
    }

    selected = {
        name: find_col(df, aliases)
        for name, aliases in mapping.items()
    }

    required = [
        "from", "to", "date", "passengers", "collected"
    ]

    missing = [
        column
        for column in required
        if selected[column] is None
    ]

    if missing:
        raise ValueError(
            "The uploaded CSV is missing required columns: "
            + ", ".join(missing)
        )

    out = pd.DataFrame()

    for name, source in selected.items():
        if source is not None:
            out[name] = df[source]
        else:
            out[name] = (
                ""
                if name in ["waybill", "ticket", "time"]
                else 0
            )

    out["from"] = (
        out["from"].fillna("Unknown").astype(str).str.strip()
    )

    out["to"] = (
        out["to"].fillna("Unknown").astype(str).str.strip()
    )

    out["route"] = out["from"] + " – " + out["to"]

    out["date"] = pd.to_datetime(
        out["date"],
        errors="coerce",
        dayfirst=False
    )

    bad_dates = out["date"].isna()

    if bad_dates.any():
        out.loc[bad_dates, "date"] = pd.to_datetime(
            df.loc[bad_dates, selected["date"]],
            errors="coerce",
            dayfirst=True
        )

    for column in [
        "passengers",
        "collected",
        "uncollected"
    ]:
        out[column] = pd.to_numeric(
            out[column],
            errors="coerce"
        ).fillna(0)

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
    """Apply consistent readable chart text and responsive sizing."""

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

def show_table(*args, **kwargs):
    """Render every dataframe with Streamlit's light table theme."""
    kwargs.setdefault("theme", "light")
    return st.dataframe(*args, **kwargs)

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
    data_error = (
        "No dataset found. Add your file at data/tickets.csv "
        "or upload a CSV from Upload Dataset."
    )

# ---------------------------- Sidebar ----------------------------

with st.sidebar:
    brand_image = ROOT / "brand_panel.png.jpeg"
    logo_image = ROOT / "logo.png.jpeg"

    if brand_image.exists():
        st.image(str(brand_image), use_container_width=True)
    elif logo_image.exists():
        st.image(str(logo_image), use_container_width=True)
    else:
        st.markdown(
            "<div style='text-align:center;padding:20px 8px;color:#64243D'>"
            "<div style='font-size:3rem'>🚌</div>"
            "<h2>BUS ANALYTICS</h2>"
            "<small>Intelligent Bus Ticket Data Platform</small></div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div style='height:1px;background:#E5C8CF;margin:12px 0 14px'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='height:1px;background:#E5C8CF;margin:12px 0 18px'></div>"
        "<p style='font-weight:800;letter-spacing:1px;font-size:.85rem'>"
        "NAVIGATION</p>",
        unsafe_allow_html=True
    )

    pages = [
        ("Home", "⌂"),
        ("Ticket Records", "▤"),
        ("Dashboard", "▦"),
        ("Route Analysis", "⌁"),
        ("Revenue Analysis", "₹"),
        ("Passenger Insights", "♙"),
        ("Demand Prediction", "↗"),
        ("Smart Insights", "✧"),
        ("AI Website Assistant", "✦"),
        ("Reports", "▧"),
        ("Upload Dataset", "⇧")
    ]

    for page_name, symbol in pages:
        label = f"{symbol}   {page_name}"

        if st.button(
            label,
            key=f"nav_{page_name}",
            type=(
                "primary"
                if st.session_state.current_page == page_name
                else "secondary"
            )
        ):
            go_to(page_name)
            st.rerun()

    st.markdown(
        "<div style='height:1px;background:#E5C8CF;margin:18px 0'></div>"
        "<p style='color:#987984;font-size:.8rem;letter-spacing:1px'>"
        "BOOK • ANALYZE • PREDICT</p>"
        "<p style='color:#987984;font-size:.82rem'>"
        "Created by <b>CRACKER HEADS ♡</b></p>",
        unsafe_allow_html=True
    )

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

    for col, (label, destination) in zip(
        first_row, mobile_nav_items[:5]
    ):
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

    for col, (label, destination) in zip(
        second_row, mobile_nav_items[5:]
    ):
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
    st.markdown(
        f"<div style='color:{MUTED};font-size:.8rem;font-weight:700;"
        "letter-spacing:1.4px'>CRACKER HEADS / BUS OPERATIONS</div>",
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        f"<div style='text-align:right;color:{BURGUNDY};"
        "font-weight:700;padding-top:3px'>🚌 BUS ANALYTICS</div>",
        unsafe_allow_html=True
    )
    # ---------------------------- Shared validation ----------------------------

if data_error:
    st.warning(data_error)

# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">BOOK • ANALYZE • PREDICT</div>
            <h1>Welcome to BUS ANALYTICS</h1>
            <p>Intelligent Bus Ticket Data Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    banner = ROOT / "bus_banner.png.jpeg"

    if banner.exists():
        st.image(str(banner), use_container_width=True)

    st.markdown(
        "<div class='section-title'>Your Bus Data, Made Meaningful</div>",
        unsafe_allow_html=True
    )

    st.write(
        "Explore ticket records, understand passenger activity, "
        "compare routes and review revenue through one simple platform."
    )

    if not data.empty:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Tickets", f"{len(data):,}")
        c2.metric(
            "Total Passengers",
            f"{int(data['passengers'].sum()):,}"
        )
        c3.metric(
            "Collected Revenue",
            money(data["collected"].sum())
        )
        c4.metric(
            "Uncollected Amount",
            money(data["uncollected"].sum())
        )

    else:
        st.info("Upload your ticket dataset to see the statistics.")

    st.markdown(
        "<div class='section-title'>Explore Platform Features</div>",
        unsafe_allow_html=True
    )

    features = [
        ("🎫 Ticket Records", "Search and review ticket information."),
        ("📊 Dashboard", "View ticket, passenger and revenue statistics."),
        ("🛣️ Route Analysis", "Compare route performance."),
        ("💰 Revenue Analysis", "Understand collected and uncollected amounts."),
        ("👥 Passenger Insights", "Explore passenger activity and boarding points."),
        ("🔮 Demand Prediction", "Review observed demand patterns."),
    ]

    cols = st.columns(3)

    for index, (title, description) in enumerate(features):
        with cols[index % 3]:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if index % 3 == 2:
                st.write("")


# ============================================================
# TICKET RECORDS
# ============================================================

elif page == "Ticket Records":

    st.title("🎫 Ticket Records")
    st.caption("Search, filter and explore bus ticket records.")

    if not data.empty:

        filtered = data.copy()

        c1, c2, c3 = st.columns(3)

        with c1:
            search_text = st.text_input(
                "Search ticket, waybill or stop",
                key="ticket_search"
            )

        with c2:
            route_options = [
                "All Routes"
            ] + sorted(data["route"].dropna().unique().tolist())

            selected_route = st.selectbox(
                "Select Route",
                route_options
            )

        with c3:
            available_dates = data["date"].dropna()

            if not available_dates.empty:

                min_date = available_dates.min().date()
                max_date = available_dates.max().date()

                selected_dates = st.date_input(
                    "Select Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="ticket_date_filter"
                )
            else:
                selected_dates = None

        if selected_route != "All Routes":
            filtered = filtered[
                filtered["route"] == selected_route
            ]

        if search_text:
            search_mask = filtered.astype(str).apply(
                lambda column: column.str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            filtered = filtered[search_mask]

        if selected_dates and len(selected_dates) == 2:

            start_date, end_date = selected_dates

            filtered = filtered[
                filtered["date"].dt.date.between(
                    start_date,
                    end_date
                )
            ]

        display = filtered.rename(
            columns={
                "waybill": "Waybill Number",
                "ticket": "Ticket Number",
                "from": "From Stop",
                "to": "To Stop",
                "date": "Date",
                "time": "Time",
                "passengers": "Passengers",
                "collected": "Collected Amount",
                "uncollected": "Uncollected Amount",
                "route": "Route"
            }
        )

        st.markdown(
            f"### {len(filtered):,} Records Found"
        )

        show_table(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Filtered Records",
            filtered.to_csv(index=False).encode("utf-8"),
            "ticket_records.csv",
            "text/csv"
        )

    else:
        st.info("Upload a CSV dataset to view ticket records.")


# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.title("📊 Operations Dashboard")
    st.caption("A consolidated view of bus ticket activity.")

    if not data.empty:

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Tickets", f"{len(data):,}")
        c2.metric(
            "Passengers",
            f"{int(data['passengers'].sum()):,}"
        )
        c3.metric(
            "Collected Revenue",
            money(data["collected"].sum())
        )
        c4.metric(
            "Uncollected",
            money(data["uncollected"].sum())
        )

        left, right = st.columns(2)

        with left:

            date_summary = (
                data.dropna(subset=["date"])
                .groupby(data["date"].dt.date)
                .size()
                .reset_index(name="Tickets")
            )

            date_summary.columns = ["Date", "Tickets"]

            fig = px.line(
                date_summary,
                x="Date",
                y="Tickets",
                markers=True,
                title="Ticket Bookings Trend",
                color_discrete_sequence=[BURGUNDY]
            )

            st.plotly_chart(
                style_chart(fig, 380),
                use_container_width=True
            )

        with right:

            top_routes = (
                data.groupby("route")
                .size()
                .sort_values(ascending=False)
                .head(10)
                .reset_index(name="Tickets")
            )

            fig = px.bar(
                top_routes.sort_values("Tickets"),
                x="Tickets",
                y="route",
                orientation="h",
                title="Top 10 Routes by Ticket Count",
                color_discrete_sequence=[ROSE],
                text="Tickets"
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            fig.update_layout(
                yaxis_title="",
                xaxis_title="Number of Tickets",
                margin=dict(l=15, r=35, t=55, b=20)
            )

            st.plotly_chart(
                style_chart(fig, 420),
                use_container_width=True
            )

    else:
        st.info("Upload your ticket dataset to view the dashboard.")


# ============================================================
# ROUTE ANALYSIS
# ============================================================

elif page == "Route Analysis":

    st.title("🛣️ Route Analysis")

    if not data.empty:

        route_summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
            .sort_values("Tickets", ascending=False)
        )

        st.markdown("### Route Performance Table")

        show_table(
            route_summary,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            route_summary.head(15).sort_values("Passengers"),
            x="Passengers",
            y="route",
            orientation="h",
            title="Top Routes by Passenger Count",
            color_discrete_sequence=[BURGUNDY],
            text="Passengers"
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        st.plotly_chart(
            style_chart(fig, 480),
            use_container_width=True
        )

        # Route Performance Score
        st.markdown("### Route Performance Score")

        def normalise(series):

            minimum = series.min()
            maximum = series.max()

            if maximum == minimum:
                return pd.Series(
                    [50.0] * len(series),
                    index=series.index
                )

            return (
                (series - minimum)
                / (maximum - minimum)
                * 100
            )

        score_data = route_summary.copy()

        score_data["Ticket Score"] = normalise(
            score_data["Tickets"]
        )

        score_data["Passenger Score"] = normalise(
            score_data["Passengers"]
        )

        score_data["Revenue Score"] = normalise(
            score_data["Revenue"]
        )

        score_data["Performance Score"] = (
            score_data["Ticket Score"] * 0.35
            + score_data["Passenger Score"] * 0.35
            + score_data["Revenue Score"] * 0.30
        ).round(1)

        score_data = score_data.sort_values(
            "Performance Score",
            ascending=False
        )

        best_route = score_data.iloc[0]

        st.success(
            f"Top-performing route in this dataset: "
            f"{best_route['route']} — "
            f"{best_route['Performance Score']:.1f}/100"
        )

        st.caption(
            "Score calculation: 35% tickets, 35% passengers "
            "and 30% collected revenue. This is a relative "
            "dataset score, not an official service-quality rating."
        )

        fig = px.bar(
            score_data.head(10).sort_values("Performance Score"),
            x="Performance Score",
            y="route",
            orientation="h",
            title="Top 10 Route Performance Scores",
            text="Performance Score",
            color_discrete_sequence=[ROSE]
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        fig.update_layout(
            xaxis_range=[0, 115],
            xaxis_title="Relative score out of 100",
            yaxis_title="",
            margin=dict(l=15, r=40, t=55, b=20)
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True
        )

    else:
        st.info("Upload a dataset to analyse routes.")


# ============================================================
# REVENUE ANALYSIS
# ============================================================

elif page == "Revenue Analysis":

    st.title("💰 Revenue Analysis")

    if not data.empty:

        collected = data["collected"].sum()
        uncollected = data["uncollected"].sum()
        total = collected + uncollected

        c1, c2, c3 = st.columns(3)

        c1.metric("Collected Revenue", money(collected))
        c2.metric("Uncollected Amount", money(uncollected))
        c3.metric("Total Recorded Amount", money(total))

        if total > 0:
            collection_rate = collected / total * 100
        else:
            collection_rate = 0

        st.progress(
            min(max(collection_rate / 100, 0), 1)
        )

        st.write(
            f"**Collection Rate: {collection_rate:.1f}%**"
        )

        revenue_by_route = (
            data.groupby("route")
            .agg(
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
            .sort_values("Collected", ascending=False)
            .head(15)
        )

        fig = px.bar(
            revenue_by_route,
            x="route",
            y=["Collected", "Uncollected"],
            barmode="group",
            title="Collected and Uncollected Revenue by Route",
            color_discrete_sequence=[BURGUNDY, GOLD]
        )

        fig.update_layout(
            xaxis_title="Route",
            yaxis_title="Amount (₹)",
            xaxis_tickangle=-35
        )

        st.plotly_chart(
            style_chart(fig, 460),
            use_container_width=True
        )

        show_table(
            revenue_by_route,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Upload a dataset to analyse revenue.")


# ============================================================
# PASSENGER INSIGHTS
# ============================================================

elif page == "Passenger Insights":

    st.title("👥 Passenger Insights")

    if not data.empty:

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Passengers",
            f"{int(data['passengers'].sum()):,}"
        )

        c2.metric(
            "Average Passengers per Ticket",
            f"{data['passengers'].mean():.2f}"
        )

        c3.metric(
            "Boarding Stops",
            f"{data['from'].nunique():,}"
        )

        passenger_routes = (
            data.groupby("route")["passengers"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            passenger_routes.sort_values("passengers"),
            x="passengers",
            y="route",
            orientation="h",
            title="Top Routes by Passenger Count",
            color_discrete_sequence=[ROSE],
            text="passengers"
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True
        )

        boarding = (
            data.groupby("from")["passengers"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        boarding.columns = [
            "Boarding Stop",
            "Passengers"
        ]

        st.markdown("### Top Boarding Stops")

        show_table(
            boarding,
            use_container_width=True,
            hide_index=True
        )

        destination = (
            data.groupby("to")["passengers"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        destination.columns = [
            "Destination Stop",
            "Passengers"
        ]

        st.markdown("### Popular Destination Stops")

        show_table(
            destination,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Upload a dataset to view passenger insights.")


# ============================================================
# DEMAND PREDICTION
# ============================================================

elif page == "Demand Prediction":

    st.title("🔮 Demand Prediction")

    st.caption(
        "Explore observed hourly ticket activity and demand patterns."
    )

    if not data.empty:

        demand_data = data.copy()

        demand_data["hour"] = pd.to_datetime(
            demand_data["time"].astype(str),
            format="%H:%M:%S",
            errors="coerce"
        ).dt.hour

        missing_hours = demand_data["hour"].isna()

        demand_data.loc[missing_hours, "hour"] = pd.to_datetime(
            demand_data.loc[missing_hours, "time"].astype(str),
            format="%H:%M",
            errors="coerce"
        ).dt.hour

        demand_data = demand_data.dropna(
            subset=["hour"]
        )

        if not demand_data.empty:

            demand_data["hour"] = (
                demand_data["hour"].astype(int)
            )

            hourly = (
                demand_data.groupby("hour")
                .agg(
                    Tickets=("ticket", "count"),
                    Passengers=("passengers", "sum")
                )
                .reset_index()
            )

            fig = px.line(
                hourly,
                x="hour",
                y="Tickets",
                markers=True,
                title="Hourly Ticket Activity",
                color_discrete_sequence=[BURGUNDY]
            )

            fig.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="Number of Tickets",
                xaxis=dict(
                    tickmode="linear",
                    dtick=1
                )
            )

            st.plotly_chart(
                style_chart(fig, 400),
                use_container_width=True
            )

            peak = hourly.sort_values(
                "Tickets",
                ascending=False
            ).iloc[0]

            st.success(
                f"Busiest recorded hour: "
                f"{int(peak['hour']):02d}:00 "
                f"with {int(peak['Tickets'])} tickets."
            )

            st.markdown("### Hourly Demand Data")

            show_table(
                hourly,
                use_container_width=True,
                hide_index=True
            )

            st.info(
                "The current dataset contains limited historical dates. "
                "This page shows observed demand patterns, not a "
                "machine-learning forecast of future demand."
            )

        else:
            st.warning(
                "Time values could not be interpreted for hourly analysis."
            )

    else:
        st.info("Upload a dataset to analyse demand.")


# ============================================================
# SMART INSIGHTS
# ============================================================

elif page == "Smart Insights":

    st.title("✨ Smart Insights")

    st.caption(
        "Six intelligent analysis sections that convert ticket "
        "records into useful operational observations."
    )

    if not data.empty:

        total_tickets = len(data)
        total_passengers = data["passengers"].sum()
        total_revenue = data["collected"].sum()
        total_uncollected = data["uncollected"].sum()

        route_summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
            .sort_values("Tickets", ascending=False)
        )

        # 1. SMART DEMAND RECOMMENDATIONS

        st.markdown(
            "<div class='section-title'>"
            "1. Smart Demand Recommendations</div>",
            unsafe_allow_html=True
        )

        if not route_summary.empty:

            busiest = route_summary.iloc[0]

            st.success(
                f"Highest ticket activity is recorded on "
                f"{busiest['route']} with "
                f"{int(busiest['Tickets'])} tickets."
            )

            st.write(
                "Recommendation: Review passenger demand on this "
                "route when planning bus frequency and scheduling."
            )

            fig = px.bar(
                route_summary.head(10).sort_values("Tickets"),
                x="Tickets",
                y="route",
                orientation="h",
                title="High-Demand Routes",
                color_discrete_sequence=[BURGUNDY],
                text="Tickets"
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            st.plotly_chart(
                style_chart(fig, 400),
                use_container_width=True
            )

        # 2. ROUTE INTELLIGENCE

        st.markdown(
            "<div class='section-title'>"
            "2. Route Intelligence</div>",
            unsafe_allow_html=True
        )

        if not route_summary.empty:

            lowest = route_summary.sort_values(
                "Tickets"
            ).iloc[0]

            st.info(
                f"Lowest recorded ticket activity: "
                f"{lowest['route']} with "
                f"{int(lowest['Tickets'])} tickets."
            )

            st.write(
                "Recommendation: Review route usage and passenger "
                "requirements before making operational changes."
            )

            show_table(
                route_summary,
                use_container_width=True,
                hide_index=True
            )

        # 3. REVENUE INTELLIGENCE

        st.markdown(
            "<div class='section-title'>"
            "3. Revenue Intelligence</div>",
            unsafe_allow_html=True
        )

        total_recorded = (
            total_revenue + total_uncollected
        )

        collection_rate = (
            total_revenue / total_recorded * 100
            if total_recorded > 0
            else 0
        )

        a, b, c = st.columns(3)

        a.metric(
            "Collected Revenue",
            money(total_revenue)
        )

        b.metric(
            "Uncollected Amount",
            money(total_uncollected)
        )

        c.metric(
            "Collection Rate",
            f"{collection_rate:.1f}%"
        )

        revenue_fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Collected", "Uncollected"],
                    values=[
                        total_revenue,
                        total_uncollected
                    ],
                    hole=.58,
                    marker=dict(
                        colors=[BURGUNDY, GOLD]
                    ),
                    textinfo="label+percent",
                    textfont=dict(
                        color=PLUM,
                        size=13
                    )
                )
            ]
        )

        revenue_fig.update_layout(
            title="Revenue Collection Breakdown",
            showlegend=True
        )

        st.plotly_chart(
            style_chart(revenue_fig, 350),
            use_container_width=True
        )

        if total_uncollected > 0:
            st.warning(
                "Uncollected amounts are present. "
                "Review the relevant ticket records."
            )
        else:
            st.success(
                "No uncollected amount is recorded."
            )

        # 4. PEAK-HOUR INTELLIGENCE AND HEATMAP

        st.markdown(
            "<div class='section-title'>"
            "4. Peak-Hour Intelligence & Heatmap</div>",
            unsafe_allow_html=True
        )

        time_data = data.copy()

        time_data["hour"] = pd.to_datetime(
            time_data["time"].astype(str),
            format="%H:%M:%S",
            errors="coerce"
        ).dt.hour

        missing_hours = time_data["hour"].isna()

        time_data.loc[missing_hours, "hour"] = pd.to_datetime(
            time_data.loc[missing_hours, "time"].astype(str),
            format="%H:%M",
            errors="coerce"
        ).dt.hour

        time_data = time_data.dropna(
            subset=["hour"]
        )

        if not time_data.empty:

            time_data["hour"] = (
                time_data["hour"].astype(int)
            )

            hourly = (
                time_data.groupby("hour")
                .agg(
                    Tickets=("ticket", "count"),
                    Passengers=("passengers", "sum")
                )
                .reset_index()
            )

            peak = hourly.sort_values(
                "Tickets",
                ascending=False
            ).iloc[0]

            st.success(
                f"Peak recorded hour: "
                f"{int(peak['hour']):02d}:00"
            )

            heatmap_data = (
                time_data.groupby("hour")
                .size()
                .reset_index(name="Tickets")
            )

            fig = px.density_heatmap(
                heatmap_data,
                x="hour",
                y="Tickets",
                z="Tickets",
                title="Hourly Ticket Activity Heatmap",
                color_continuous_scale=[
                    "#F8E6E5",
                    "#C77B8C",
                    "#64243D"
                ]
            )

            st.plotly_chart(
                style_chart(fig, 350),
                use_container_width=True
            )

            st.write(
                "Recommendation: Review the busiest recorded "
                "hours while planning operational schedules."
            )

        else:
            st.info(
                "Time information is unavailable for this analysis."
            )

        # 5. UNUSUAL ACTIVITY DETECTION

        st.markdown(
            "<div class='section-title'>"
            "5. Unusual Activity Detection</div>",
            unsafe_allow_html=True
        )

        unusual_records = []

        for column, label in [
            ("passengers", "Passenger Count"),
            ("collected", "Collected Amount")
        ]:

            values = data[column]

            if len(values) >= 4 and values.std() > 0:

                threshold = (
                    values.mean() + 2 * values.std()
                )

                flagged = data[
                    values > threshold
                ].copy()

                if not flagged.empty:

                    flagged["Detected Metric"] = label

                    unusual_records.append(
                        flagged[
                            [
                                "ticket",
                                "route",
                                "date",
                                column,
                                "Detected Metric"
                            ]
                        ]
                    )

        if unusual_records:

            unusual_df = pd.concat(
                unusual_records,
                ignore_index=True
            )

            st.warning(
                f"{len(unusual_df)} statistical flags "
                "were identified for review."
            )

            show_table(
                unusual_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No unusually high values were identified "
                "using the selected statistical check."
            )

        st.caption(
            "Statistical flags are only indicators for review. "
            "They do not prove fraud or incorrect transactions."
        )

        # 6. MANAGEMENT RECOMMENDATIONS

        st.markdown(
            "<div class='section-title'>"
            "6. Management Recommendations</div>",
            unsafe_allow_html=True
        )

        recommendations = []

        if not route_summary.empty:

            recommendations.append(
                (
                    "Route Planning",
                    "Review high-activity routes when planning "
                    "bus frequency and service schedules."
                )
            )

        if total_uncollected > 0:

            recommendations.append(
                (
                    "Revenue Review",
                    "Check uncollected ticket amounts and "
                    "reconcile the relevant records."
                )
            )

        if not time_data.empty:

            recommendations.append(
                (
                    "Peak-Hour Planning",
                    "Use observed peak-hour activity when "
                    "reviewing operational schedules."
                )
            )

        recommendations.append(
            (
                "Future Data Collection",
                "Collect ticket records across multiple dates "
                "to improve trend analysis and future forecasting."
            )
        )

        recommendations.append(
            (
                "Monitoring",
                "Continue monitoring route-wise passenger "
                "counts and revenue patterns."
            )
        )

        for number, (title, description) in enumerate(
            recommendations,
            start=1
        ):

            st.markdown(
                f"""
                <div class="card" style="margin-bottom:12px;">
                    <h3>{number}. {title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.caption(
            "Smart Insights uses rule-based and statistical analysis "
            "of the available ticket records. It is not a trained "
            "machine-learning model."
        )

    else:
        st.info(
            "Upload your ticket dataset to generate Smart Insights."
        )


# ============================================================
# AI WEBSITE ASSISTANT
# ============================================================

elif page == "AI Website Assistant":

    st.title("🤖 AI Website Assistant")

    st.caption(
        "Ask questions about the platform, ticket data, "
        "routes and revenue analysis."
    )

    st.markdown(
        """
        <div class="card">
            <h3>How can I help you?</h3>
            <p>
                Ask me how to use the dashboard, understand the
                analytics, explore routes or interpret your data.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if "assistant_history" not in st.session_state:
        st.session_state.assistant_history = []

    def assistant_answer(question):

        q = question.lower().strip()

        if not q:
            return "Please type a question so I can help."

        answers = {

            "what is bus analytics":
                "Bus Analytics is a data analysis platform "
                "designed to examine bus ticket records. It "
                "organises ticket information and helps users "
                "understand passenger activity, route performance "
                "and revenue collection.",

            "what is dashboard":
                "The Dashboard provides a quick overview of the "
                "uploaded ticket dataset. It displays total tickets, "
                "passengers, collected revenue and ticket trends. "
                "It also highlights the busiest routes so that "
                "users can understand overall activity quickly.",

            "what is route analysis":
                "Route Analysis compares individual routes using "
                "ticket counts, passenger counts and collected "
                "revenue. It also calculates a relative route "
                "performance score using ticket volume, passenger "
                "volume and revenue.",

            "what is revenue analysis":
                "Revenue Analysis examines the money collected "
                "and the amount that remains uncollected. It "
                "calculates the collection percentage and compares "
                "revenue across different routes. This can help "
                "management identify where financial review is needed.",

            "what is passenger insights":
                "Passenger Insights studies passenger counts "
                "across routes and stops. It identifies popular "
                "boarding points and destinations, helping "
                "management understand passenger movement.",

            "what is demand prediction":
                "Demand Prediction currently analyses observed "
                "hourly ticket activity. It identifies the busiest "
                "recorded hours. More historical dates are needed "
                "before a reliable future-demand forecasting model "
                "can be trained.",

            "what is smart insights":
                "Smart Insights contains six analysis sections: "
                "Smart Demand Recommendations, Route Intelligence, "
                "Revenue Intelligence, Peak-Hour Intelligence, "
                "Unusual Activity Detection and Management "
                "Recommendations. These sections convert recorded "
                "data into useful operational observations.",

            "how to upload":
                "Open Upload Dataset from the navigation panel. "
                "Choose a CSV file containing the ticket records. "
                "Preview the uploaded data and select Use This "
                "Dataset. The uploaded dataset will then be used "
                "by the dashboard during your current session.",

            "who created":
                "This project was developed by CRACKER HEADS.",

            "what is project objective":
                "The objective is to convert bus ticket records "
                "into useful information. The platform helps "
                "analyse passenger activity, compare routes, "
                "understand revenue collection and support "
                "operational decision-making.",

        }

        for keyword, answer in answers.items():

            if keyword in q:
                return answer

        # Questions about the actual loaded dataset

        if any(word in q for word in [
            "total ticket", "number of ticket", "how many ticket"
        ]):

            return (
                f"The uploaded dataset contains {len(data):,} "
                "ticket records."
                if not data.empty
                else "No ticket dataset is currently loaded."
            )

        if "passenger" in q and not data.empty:

            return (
                f"The uploaded dataset contains "
                f"{int(data['passengers'].sum()):,} passengers. "
                "Open Passenger Insights to see route-wise "
                "passenger activity and popular boarding stops."
            )

        if any(word in q for word in [
            "revenue", "collection", "collected amount"
        ]) and not data.empty:

            return (
                f"The total collected revenue is "
                f"{money(data['collected'].sum())}. "
                f"The uncollected amount is "
                f"{money(data['uncollected'].sum())}. "
                "Open Revenue Analysis for a detailed comparison."
            )

        if "route" in q and not data.empty:

            route_count = data["route"].nunique()

            busiest = (
                data.groupby("route")
                .size()
                .sort_values(ascending=False)
            )

            if not busiest.empty:

                return (
                    f"There are {route_count} distinct routes "
                    f"in the uploaded dataset. The route with "
                    f"the highest ticket count is {busiest.index[0]}, "
                    f"with {int(busiest.iloc[0])} tickets. "
                    "Open Route Analysis for the complete comparison."
                )

        if "help" in q:

            return (
                "I can explain the main features of this platform. "
                "For example, ask me about the dashboard, route "
                "analysis, revenue analysis, passenger insights, "
                "demand prediction, Smart Insights or how to upload "
                "a dataset. You can also ask about the statistics "
                "in the currently uploaded records."
            )

        return (
            "I couldn't identify the exact question. Please try "
            "asking about a particular feature, such as Route "
            "Analysis, Revenue Analysis, Passenger Insights or "
            "Smart Insights. You can also ask me about the total "
            "tickets, passenger count or collected revenue in "
            "the uploaded dataset."
        )

    # Display previous messages

    for message in st.session_state.assistant_history:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    # Chat input

    question = st.chat_input(
        "Type your question here...",
        key="bus_assistant_input"
    )

    if question:

        st.session_state.assistant_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        answer = assistant_answer(question)

        st.session_state.assistant_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

    if st.button(
        "Clear Conversation",
        key="clear_assistant_chat"
    ):

        st.session_state.assistant_history = []
        st.rerun()

    st.caption(
        "The current assistant uses programmed responses and "
        "dataset-based answers. A live generative AI service "
        "would require an API integration."
    )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("📑 Reports")

    if not data.empty:

        summary = pd.DataFrame({
            "Metric": [
                "Total Tickets",
                "Total Passengers",
                "Total Routes",
                "Total Collected Revenue",
                "Total Uncollected Amount",
                "Total Recorded Amount"
            ],
            "Value": [
                len(data),
                int(data["passengers"].sum()),
                data["route"].nunique(),
                data["collected"].sum(),
                data["uncollected"].sum(),
                (
                    data["collected"].sum()
                    + data["uncollected"].sum()
                )
            ]
        })

        st.markdown("### Dataset Summary")

        show_table(
            summary,
            use_container_width=True,
            hide_index=True
        )

        route_report = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        st.markdown("### Route Report")

        show_table(
            route_report,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Summary Report",
            summary.to_csv(index=False).encode("utf-8"),
            "bus_summary_report.csv",
            "text/csv"
        )

        st.download_button(
            "⬇️ Download Route Report",
            route_report.to_csv(index=False).encode("utf-8"),
            "bus_route_report.csv",
            "text/csv"
        )

    else:
        st.info("Upload a dataset to generate reports.")


# ============================================================
# UPLOAD DATASET
# ============================================================

elif page == "Upload Dataset":

    st.title("📂 Upload Dataset")

    st.write(
        "Upload your bus ticket records in CSV format."
    )

    uploaded_file = st.file_uploader(
        "Choose your CSV file",
        type=["csv"],
        key="dataset_upload"
    )

    if uploaded_file is not None:

        try:

            uploaded_raw = pd.read_csv(uploaded_file)

            preview = prepare_data(
                uploaded_raw
            )

            st.success(
                f"File loaded successfully. "
                f"{len(preview):,} records found."
            )

            st.markdown("### Preview")

            show_table(
                preview.head(20),
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                "Use This Dataset",
                type="primary"
            ):

                st.session_state.uploaded_raw = (
                    uploaded_raw
                )

                st.success(
                    "Dataset successfully applied."
                )

                st.rerun()

        except Exception as error:

            st.error(
                f"Unable to read this CSV file: {error}"
            )

    if st.session_state.uploaded_raw is not None:

        st.success(
            "A session-uploaded dataset is currently active."
        )

        if st.button("Restore Repository Dataset"):

            st.session_state.uploaded_raw = None
            st.rerun()

    st.caption(
        "Uploaded data is available for the current Streamlit "
        "session. It does not permanently replace the repository CSV."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:18px 5px;
        color:#64243D;
    ">
        <h3 style="
            font-family:'Playfair Display',serif;
            color:#64243D;
            margin-bottom:5px;
        ">
            BUS ANALYTICS
        </h3>

        <p style="
            color:#624D57;
            margin:0;
            font-size:13px;
        ">
            Intelligent Bus Ticket Data Platform
        </p>

        <p style="
            color:#64243D;
            font-weight:700;
            margin-top:10px;
        ">
            Created by CRACKER HEADS
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------- Shared validation ----------------------------

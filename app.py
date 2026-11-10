
from pathlib import Path
import base64
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# BUS ANALYTICS | CRACKER HEADS
# =========================================================

st.set_page_config(
    page_title="Bus Analytics | CRACKER HEADS",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tickets.csv"

# APPROVED COLOURS - DO NOT CHANGE
BG = "#FFF8F5"
PINK = "#F8E6E5"
BURGUNDY = "#64243D"
PLUM = "#351324"
ROSE = "#C77B8C"
GOLD = "#D7A66B"
INK = "#382832"
MUTED = "#8B737D"

# =========================================================
# ANIMATIONS + RESPONSIVE DESIGN
# =========================================================

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

html,body,.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {{
 background:#FFF8F5 !important;
 color:#382832 !important;
 color-scheme:light !important;
 font-family:'DM Sans',sans-serif;
}}

[data-testid="stHeader"] {{
 background:rgba(255,248,245,.95);
}}

.block-container {{
 max-width:1600px;
 padding:1.2rem 2rem 2rem !important;
}}

[data-testid="stSidebar"] {{
 background:linear-gradient(180deg,#FBEAE7,#F5DFE2);
 border-right:1px solid #EAD1D5;
}}

[data-testid="stSidebar"] img {{
 border-radius:17px;
}}

[data-testid="stSidebar"] .stButton button {{
 width:100%;
 min-height:43px;
 text-align:left;
 border-radius:12px;
 color:#64243D;
 background:transparent;
 border:1px solid transparent;
 font-weight:600;
 white-space:normal;
}}

[data-testid="stSidebar"] .stButton button:hover {{
 background:#F4D5D8;
 border-color:#E8BFC7;
}}

[data-testid="stMetric"] {{
 background:linear-gradient(135deg,#FFFFFF,#FCEDEF);
 border:1px solid #EBD8DC;
 border-radius:17px;
 padding:16px;
 box-shadow:0 4px 16px rgba(85,35,55,.05);
}}

[data-testid="stMetricLabel"] p {{
 color:#624D57 !important;
 font-weight:600;
}}

[data-testid="stMetricValue"] {{
 color:#351324 !important;
 font-weight:800;
 overflow-wrap:anywhere;
}}

.card {{
 background:white;
 border:1px solid #EAD9DD;
 border-radius:19px;
 padding:20px;
 box-shadow:0 5px 18px rgba(73,32,50,.045);
 height:100%;
}}

.card h3 {{
 color:#64243D;
 margin:0 0 9px;
 font-size:1.08rem;
}}

.card p {{
 color:#624D57;
 line-height:1.6;
 margin:0;
}}

.hero {{
 border-radius:22px;
 padding:32px;
 min-height:190px;
 background:linear-gradient(105deg,#351324,#64243D,#92536A);
 margin-bottom:20px;
 animation:fadeUp .7s ease both;
}}

.hero .eyebrow {{
 color:#F5D4C9;
 font-size:.76rem;
 font-weight:700;
 letter-spacing:2px;
}}

.hero h1 {{
 color:#FFF4ED !important;
 font-family:'Playfair Display',serif;
 font-size:clamp(2rem,4vw,3.1rem);
 margin:10px 0;
}}

.hero p {{
 color:#F8E7E4 !important;
 line-height:1.6;
 max-width:700px;
}}

.section-title {{
 color:#64243D;
 font-size:1.25rem;
 font-weight:800;
 margin:1.3rem 0 .8rem;
}}

h1,h2,h3,h4 {{
 color:#64243D;
 overflow-wrap:anywhere;
}}

p,label {{
 color:#382832;
}}

.stButton button[kind="primary"] {{
 background:#64243D;
 color:white;
 border:0;
 border-radius:12px;
 font-weight:700;
 min-height:42px;
}}

.stDownloadButton button {{
 background:#F3DDE1;
 color:#64243D;
 border:1px solid #E6C4CB;
 border-radius:12px;
 min-height:42px;
 font-weight:700;
 white-space:normal;
}}

[data-testid="stDataFrame"] {{
 border:1px solid #EAD9DD;
 border-radius:14px;
}}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
 color:#624D57 !important;
}}

hr {{
 border-color:#EAD5DA !important;
}}

footer {{
 visibility:hidden;
}}

/* CHART TEXT CONTRAST */
.js-plotly-plot .plotly text {{
 fill:#351324 !important;
}}

.js-plotly-plot .gtitle {{
 fill:#64243D !important;
}}

.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .legend text {{
 fill:#351324 !important;
}}

/* ANIMATIONS */
@keyframes fadeUp {{
 from {{opacity:0;transform:translateY(15px);}}
 to {{opacity:1;transform:translateY(0);}}
}}

@keyframes logoIn {{
 0% {{opacity:0;transform:scale(.8);}}
 70% {{opacity:1;transform:scale(1.04);}}
 100% {{opacity:1;transform:scale(1);}}
}}

@keyframes shimmer {{
 from {{background-position:-200% 0;}}
 to {{background-position:200% 0;}}
}}

.block-container {{
 animation:fadeUp .4s ease both;
}}

.card {{
 animation:fadeUp .5s ease both;
}}

.bus-splash {{
 position:fixed;
 inset:0;
 z-index:999999;
 display:flex;
 flex-direction:column;
 align-items:center;
 justify-content:center;
 text-align:center;
 padding:20px;
 background:radial-gradient(circle,#FFFDFB,#FBE8E8 55%,#EFCFD6);
}}

.bus-splash img {{
 width:min(75vw,310px);
 max-height:230px;
 object-fit:contain;
 border-radius:20px;
 animation:logoIn .9s ease both;
}}

.bus-splash h1 {{
 color:#64243D;
 font-family:'Playfair Display',serif;
 margin-top:20px;
}}

.bus-splash p {{
 color:#755F69;
 letter-spacing:1px;
}}

.bus-loading {{
 width:150px;
 height:4px;
 border-radius:20px;
 margin-top:20px;
 background:linear-gradient(90deg,#D7A66B,#C77B8C,#64243D,#D7A66B);
 background-size:200% 100%;
 animation:shimmer 1.2s linear infinite;
}}

/* MOBILE NAVIGATION */
.st-key-mobile_nav {{
 display:none;
}}

@media(max-width:768px) {{

 .block-container {{
  width:100% !important;
  max-width:100% !important;
  padding:.65rem .7rem 145px !important;
 }}

 .hero {{
  padding:21px 17px;
  min-height:unset;
  border-radius:17px;
 }}

 .hero h1 {{
  font-size:1.7rem;
 }}

 .hero p {{
  font-size:.92rem;
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

 [data-testid="stMetric"] {{
  padding:12px;
 }}

 [data-testid="stMetricValue"] {{
  font-size:1.3rem !important;
 }}

 .card {{
  padding:16px;
 }}

 [data-testid="stPlotlyChart"] {{
  width:100% !important;
  max-width:100% !important;
  overflow:hidden !important;
  padding:2px !important;
 }}

 [data-testid="stDataFrame"] {{
  max-width:100% !important;
  overflow-x:auto !important;
 }}

 [data-testid="stSidebar"] {{
  min-width:min(85vw,310px) !important;
 }}

 .st-key-mobile_nav {{
  display:block !important;
  position:fixed !important;
  bottom:max(8px,env(safe-area-inset-bottom)) !important;
  left:7px !important;
  right:7px !important;
  width:auto !important;
  z-index:99990 !important;
  background:rgba(255,248,245,.98) !important;
  border:1px solid #E5C8CF !important;
  border-radius:16px !important;
  padding:7px !important;
  box-shadow:0 5px 22px rgba(53,19,36,.18);
  backdrop-filter:blur(12px);
 }}

 .st-key-mobile_nav [data-testid="stHorizontalBlock"] {{
  display:flex !important;
  flex-direction:row !important;
  flex-wrap:nowrap !important;
  gap:3px !important;
 }}

 .st-key-mobile_nav [data-testid="column"] {{
  min-width:0 !important;
  width:20% !important;
  flex:1 1 20% !important;
  padding:0 !important;
 }}

 .st-key-mobile_nav .stButton button {{
  width:100% !important;
  min-height:39px !important;
  padding:4px 1px !important;
  border-radius:9px !important;
  font-size:10px !important;
  line-height:1.2 !important;
  text-align:center !important;
  white-space:normal !important;
  overflow-wrap:anywhere !important;
  background:#FFFDFB !important;
  color:#64243D !important;
  border:1px solid #EBD8DC !important;
 }}

 .st-key-mobile_nav .stButton button[kind="primary"] {{
  background:#64243D !important;
  color:white !important;
 }}
}}

@media(max-width:380px) {{
 .block-container {{
  padding-left:.5rem !important;
  padding-right:.5rem !important;
 }}
 .hero h1 {{font-size:1.45rem;}}
}}

@media(prefers-reduced-motion:reduce) {{
 *,*::before,*::after {{
  animation-duration:.01ms !important;
  animation-iteration-count:1 !important;
 }}
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGO INTRO - 2.2 SECONDS, ONCE PER SESSION
# =========================================================

if "intro_seen" not in st.session_state:
    st.session_state.intro_seen = False

if not st.session_state.intro_seen:

    placeholder = st.empty()
    logo_path = ROOT / "logo.png.jpeg"

    if not logo_path.exists():
        logo_path = ROOT / "brand_panel.png.jpeg"

    if logo_path.exists():
        try:
            encoded = base64.b64encode(
                logo_path.read_bytes()
            ).decode("utf-8")

            mime = (
                "image/jpeg"
                if logo_path.suffix.lower() in [".jpg", ".jpeg"]
                else "image/png"
            )

            logo_html = (
                f'<img src="data:{mime};base64,{encoded}" '
                'alt="Bus Analytics logo">'
            )
        except Exception:
            logo_html = "<h1>🚌 BUS ANALYTICS</h1>"
    else:
        logo_html = "<h1>🚌 BUS ANALYTICS</h1>"

    placeholder.markdown(f"""
    <div class="bus-splash">
        {logo_html}
        <h1>BUS ANALYTICS</h1>
        <p>INTELLIGENT BUS TICKET DATA PLATFORM</p>
        <div class="bus-loading"></div>
        <p>CREATED BY CRACKER HEADS</p>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2.2)
    placeholder.empty()
    st.session_state.intro_seen = True

# =========================================================
# DATA PROCESSING
# =========================================================

def find_col(frame, candidates):
    lookup = {
        str(c).strip().lower(): c
        for c in frame.columns
    }

    for name in candidates:
        if name.lower() in lookup:
            return lookup[name.lower()]

    for name in candidates:
        for key, original in lookup.items():
            if name.lower() in key:
                return original

    return None

def prepare_data(raw):
    df = raw.copy()

    mapping = {
        "waybill": ["Waybill Number", "Waybill"],
        "ticket": ["Ticket Number", "Ticket No"],
        "from": ["From Stop", "From", "Origin"],
        "to": ["To Stop", "To", "Destination"],
        "date": ["Date", "Journey Date", "Travel Date"],
        "time": ["Time", "Journey Time"],
        "passengers": ["Total Psgr", "Total Passenger", "Passengers"],
        "collected": ["Coll Amt", "Collected Amount", "Fare"],
        "uncollected": ["Uncoll Amt", "Uncollected Amount"]
    }

    selected = {
        key: find_col(df, values)
        for key, values in mapping.items()
    }

    required = [
        "from", "to", "date", "passengers", "collected"
    ]

    missing = [
        key for key in required
        if selected[key] is None
    ]

    if missing:
        raise ValueError(
            "Missing CSV columns: " + ", ".join(missing)
        )

    out = pd.DataFrame()

    for key, source in selected.items():
        if source is not None:
            out[key] = df[source]
        else:
            out[key] = (
                "" if key in ["waybill", "ticket", "time"]
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
        out["date"], errors="coerce"
    )

    bad = out["date"].isna()

    if bad.any():
        out.loc[bad, "date"] = pd.to_datetime(
            df.loc[bad, selected["date"]],
            errors="coerce",
            dayfirst=True
        )

    for col in ["passengers", "collected", "uncollected"]:
        out[col] = pd.to_numeric(
            out[col], errors="coerce"
        ).fillna(0).clip(lower=0)

    out["ticket"] = out["ticket"].astype(str)
    out["waybill"] = out["waybill"].astype(str)

    # Extract hour from ticket time for demand analysis.
    out["hour"] = pd.to_datetime(
        out["time"].astype(str),
        format="mixed",
        errors="coerce"
    ).dt.hour

    return out

def money(value):
    return f"₹{value:,.0f}"

def style_chart(fig, height=360):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, Arial",
            color=PLUM,
            size=13
        ),
        title_font=dict(
            color=BURGUNDY,
            size=18
        ),
        margin=dict(l=15, r=25, t=55, b=35),
        autosize=True,
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=BURGUNDY,
            font=dict(color=PLUM)
        )
    )

    fig.update_xaxes(
        tickfont=dict(color=PLUM, size=12),
        title_font=dict(color=BURGUNDY),
        gridcolor="#EADDE0"
    )

    fig.update_yaxes(
        tickfont=dict(color=PLUM, size=12),
        title_font=dict(color=BURGUNDY),
        gridcolor="#EADDE0"
    )

    return fig

def go_to(destination):
    st.session_state.current_page = destination

# =========================================================
# LOAD DATA
# =========================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "uploaded_raw" not in st.session_state:
    st.session_state.uploaded_raw = None

raw = st.session_state.uploaded_raw

if raw is None and DATA_FILE.exists():
    try:
        raw = pd.read_csv(DATA_FILE)
    except Exception as error:
        st.error(f"Dataset error: {error}")

if raw is not None:
    try:
        data = prepare_data(raw)
        data_error = None
    except Exception as error:
        data = pd.DataFrame()
        data_error = str(error)
else:
    data = pd.DataFrame()
    data_error = "Upload a dataset or add data/tickets.csv to GitHub."

# =========================================================
# SIDEBAR
# =========================================================

pages = [
    ("Home", "⌂"),
    ("Ticket Records", "▤"),
    ("Dashboard", "▦"),
    ("Route Analysis", "⌁"),
    ("Revenue Analysis", "₹"),
    ("Passenger Insights", "♙"),
    ("Demand Prediction", "↗"),
    ("Smart Insights", "✧"),
    ("Reports", "▧"),
    ("Upload Dataset", "⇧")
]

with st.sidebar:

    brand = ROOT / "brand_panel.png.jpeg"
    logo = ROOT / "logo.png.jpeg"

    if brand.exists():
        st.image(str(brand), use_container_width=True)
    elif logo.exists():
        st.image(str(logo), use_container_width=True)
    else:
        st.markdown("## 🚌 BUS ANALYTICS")

    st.markdown("### NAVIGATION")

    for name, symbol in pages:
        if st.button(
            f"{symbol}  {name}",
            key=f"side_{name}",
            type=(
                "primary"
                if st.session_state.current_page == name
                else "secondary"
            )
        ):
            go_to(name)
            st.rerun()

    st.markdown("---")
    st.markdown("BOOK • ANALYZE • PREDICT")
    st.caption("Created by CRACKER HEADS ♡")

page = st.session_state.current_page

# =========================================================
# FIXED MOBILE BOTTOM NAVIGATION
# =========================================================

mobile_items = [
    ("Home", "Home"),
    ("Records", "Ticket Records"),
    ("Dashboard", "Dashboard"),
    ("Routes", "Route Analysis"),
    ("Revenue", "Revenue Analysis"),
    ("Passengers", "Passenger Insights"),
    ("Demand", "Demand Prediction"),
    ("Insights", "Smart Insights"),
    ("Reports", "Reports"),
    ("Upload", "Upload Dataset")
]

with st.container(key="mobile_nav"):

    row1 = st.columns(5)

    for col, (label, destination) in zip(
        row1, mobile_items[:5]
    ):
        with col:
            if st.button(
                label,
                key=f"mobile_{destination}",
                type=(
                    "primary"
                    if page == destination
                    else "secondary"
                ),
                use_container_width=True
            ):
                go_to(destination)
                st.rerun()

    row2 = st.columns(5)

    for col, (label, destination) in zip(
        row2, mobile_items[5:]
    ):
        with col:
            if st.button(
                label,
                key=f"mobile_{destination}",
                type=(
                    "primary"
                    if page == destination
                    else "secondary"
                ),
                use_container_width=True
            ):
                go_to(destination)
                st.rerun()

# =========================================================
# HEADER
# =========================================================

left, right = st.columns([5, 1])

with left:
    st.caption("CRACKER HEADS / BUS OPERATIONS")

with right:
    st.markdown(
        f"<div style='text-align:right;color:{BURGUNDY};"
        "font-weight:800'>🚌 BUS ANALYTICS</div>",
        unsafe_allow_html=True
    )

if data_error and page != "Upload Dataset":
    st.warning(data_error)

# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">
            INTELLIGENT TRANSPORTATION ANALYTICS
        </div>
        <h1>Welcome to Bus Analytics</h1>
        <p>
            Monitor ticket activity, understand passenger movement
            and explore route performance with your ticket records.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not data.empty:

        a, b, c, d = st.columns(4)

        a.metric("Total Tickets", f"{len(data):,}")
        b.metric("Total Revenue", money(data.collected.sum()))
        c.metric("Total Passengers", f"{int(data.passengers.sum()):,}")
        d.metric("Active Routes", f"{data.route.nunique():,}")

        st.markdown(
            '<div class="section-title">Ticket Activity Overview</div>',
            unsafe_allow_html=True
        )

        trend = (
            data.dropna(subset=["date"])
            .groupby(data.date.dt.date)
            .size()
            .reset_index(name="Tickets")
        )
        trend.columns = ["Date", "Tickets"]

        if not trend.empty:
            fig = px.area(
                trend,
                x="Date",
                y="Tickets",
                title="Ticket Bookings Trend"
            )
            fig.update_traces(
                line_color=BURGUNDY,
                fillcolor="rgba(199,123,140,.25)"
            )
            st.plotly_chart(
                style_chart(fig, 340),
                use_container_width=True
            )

        st.markdown(
            '<div class="section-title">Top Routes by Tickets</div>',
            unsafe_allow_html=True
        )

        top = (
            data.groupby("route").size()
            .nlargest(7).sort_values()
            .reset_index(name="Tickets")
        )

        fig = px.bar(
            top,
            x="Tickets",
            y="route",
            orientation="h",
            text="Tickets",
            color_discrete_sequence=[ROSE]
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_title="")
        st.plotly_chart(
            style_chart(fig, 350),
            use_container_width=True
        )

        st.markdown(
            '<div class="section-title">Explore Your Analytics</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        cards = [
            ("↗ Demand Prediction",
             "Explore historical demand and travel hours.",
             "Demand Prediction"),
            ("✧ Smart Insights",
             "Understand route and passenger observations.",
             "Smart Insights"),
            ("▧ Generate Reports",
             "Download your ticket and route reports.",
             "Reports")
        ]

        for col, (title, description, destination) in zip(
            [c1, c2, c3], cards
        ):
            with col:
                st.markdown(
                    f'<div class="card"><h3>{title}</h3>'
                    f'<p>{description}</p></div>',
                    unsafe_allow_html=True
                )
                if st.button(
                    "Explore",
                    key=f"explore_{destination}",
                    use_container_width=True
                ):
                    go_to(destination)
                    st.rerun()

    else:
        st.info("Upload your ticket dataset to start analytics.")
        if st.button("Upload Dataset", type="primary"):
            go_to("Upload Dataset")
            st.rerun()

# =========================================================
# TICKET RECORDS
# =========================================================

elif page == "Ticket Records":

    st.title("Ticket Records")
    st.caption("Search, review and download ticket records.")

    if not data.empty:

        search = st.text_input(
            "Search ticket, waybill, route or stop"
        )

        view = data.copy()

        if search.strip():
            mask = view.astype(str).apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False,
                    regex=False
                )
            ).any(axis=1)
            view = view[mask]

        st.write(f"**{len(view):,} records found**")

        display = view[[
            "waybill", "ticket", "from", "to", "date",
            "time", "passengers", "collected", "uncollected"
        ]].rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from": "From Stop",
            "to": "To Stop",
            "date": "Date",
            "time": "Time",
            "passengers": "Passengers",
            "collected": "Collected Amount",
            "uncollected": "Uncollected Amount"
        })

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Filtered Records",
            view.to_csv(index=False).encode("utf-8"),
            "ticket_records.csv",
            "text/csv"
        )

    else:
        st.info("Upload a dataset to view records.")

# =========================================================
# DASHBOARD
# =========================================================

elif page == "Dashboard":

    st.title("Operations Dashboard")

    if not data.empty:

        a, b, c, d = st.columns(4)

        a.metric("Tickets", f"{len(data):,}")
        b.metric("Passengers", f"{int(data.passengers.sum()):,}")
        c.metric("Collected", money(data.collected.sum()))
        d.metric("Uncollected", money(data.uncollected.sum()))

        day = (
            data.dropna(subset=["date"])
            .groupby(data.date.dt.day_name())
            .size()
            .reindex([
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ])
            .dropna()
            .reset_index()
        )
        day.columns = ["Day", "Tickets"]

        fig = px.bar(
            day,
            x="Day",
            y="Tickets",
            title="Tickets by Day of Week",
            color_discrete_sequence=[ROSE]
        )
        st.plotly_chart(
            style_chart(fig, 360),
            use_container_width=True
        )

        # Clean top-origin chart: no crowded donut labels.
        origins = (
            data.groupby("from")
            .agg(
                Tickets=("ticket", "size"),
                Passengers=("passengers", "sum")
            )
            .reset_index()
            .sort_values("Tickets", ascending=False)
        )

        top_origins = origins.head(10).copy()

        if len(origins) > 10:
            other = pd.DataFrame([{
                "from": "Other stops",
                "Tickets": origins.iloc[10:]["Tickets"].sum(),
                "Passengers": origins.iloc[10:]["Passengers"].sum()
            }])
            top_origins = pd.concat(
                [top_origins, other],
                ignore_index=True
            )

        top_origins = top_origins.sort_values("Tickets")

        fig = px.bar(
            top_origins,
            x="Tickets",
            y="from",
            orientation="h",
            title="Top Ticket Origins",
            text="Tickets",
            color_discrete_sequence=[BURGUNDY]
        )
        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        fig.update_layout(
            yaxis_title="",
            margin=dict(l=15, r=45, t=55, b=20)
        )
        st.plotly_chart(
            style_chart(fig, 430),
            use_container_width=True
        )

    else:
        st.info("Upload your ticket dataset.")

# =========================================================
# ROUTE ANALYSIS
# =========================================================

elif page == "Route Analysis":

    st.title("Route Analysis")

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

        st.dataframe(
            routes,
            use_container_width=True,
            hide_index=True
        )

        top = (
            routes.nlargest(15, "Passengers")
            .sort_values("Passengers")
        )

        fig = px.bar(
            top,
            x="Passengers",
            y="route",
            orientation="h",
            title="Top 15 Routes by Passenger Count",
            text="Passengers",
            color_discrete_sequence=[BURGUNDY]
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        fig.update_layout(
            yaxis_title="",
            margin=dict(l=15, r=45, t=55, b=20)
        )

        st.plotly_chart(
            style_chart(fig, 520),
            use_container_width=True
        )

    else:
        st.info("Upload your ticket dataset.")

# =========================================================
# REVENUE ANALYSIS
# =========================================================

elif page == "Revenue Analysis":

    st.title("Revenue Analysis")

    if not data.empty:

        a, b, c = st.columns(3)

        a.metric("Collected", money(data.collected.sum()))
        b.metric("Uncollected", money(data.uncollected.sum()))
        c.metric(
            "Total Recorded",
            money(data.collected.sum() + data.uncollected.sum())
        )

        rev = (
            data.groupby("route")
            .agg(
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
            .nlargest(12, "Collected")
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
            xaxis_title="",
            margin=dict(l=15, r=15, t=55, b=100)
        )

        st.plotly_chart(
            style_chart(fig, 430),
            use_container_width=True
        )

    else:
        st.info("Upload your ticket dataset.")

# =========================================================
# PASSENGER INSIGHTS
# =========================================================

elif page == "Passenger Insights":

    st.title("Passenger Insights")

    if not data.empty:

        a, b, c = st.columns(3)

        a.metric(
            "Total Passengers",
            f"{int(data.passengers.sum()):,}"
        )
        b.metric(
            "Average Passengers per Ticket",
            f"{data.passengers.mean():.2f}"
        )
        c.metric(
            "Boarding Stops",
            f"{data['from'].nunique():,}"
        )

        board = (
            data.groupby("from")
            .agg(
                Passengers=("passengers", "sum")
            )
            .reset_index()
            .nlargest(12, "Passengers")
            .sort_values("Passengers")
        )

        fig = px.bar(
            board,
            x="Passengers",
            y="from",
            orientation="h",
            title="Busiest Boarding Stops",
            text="Passengers",
            color_discrete_sequence=[ROSE]
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )
        fig.update_layout(
            yaxis_title="",
            margin=dict(l=15, r=45, t=55, b=20)
        )

        st.plotly_chart(
            style_chart(fig, 440),
            use_container_width=True
        )

    else:
        st.info("Upload your ticket dataset.")

# =========================================================
# DEMAND PREDICTION
# =========================================================

elif page == "Demand Prediction":

    st.title("Demand Prediction")

    st.caption(
        "Explore hourly ticket demand and passenger movement."
    )

    if not data.empty:

        hourly_data = data.dropna(subset=["hour"]).copy()

        if not hourly_data.empty:

            hourly = (
                hourly_data.groupby("hour")
                .agg(
                    Tickets=("ticket", "size"),
                    Passengers=("passengers", "sum")
                )
                .reindex(range(24), fill_value=0)
                .reset_index()
            )

            hourly["Time Slot"] = hourly["hour"].apply(
                lambda x: f"{int(x):02d}:00"
            )

            peak = hourly.loc[hourly["Tickets"].idxmax()]
            busiest_hour = f"{int(peak['hour']):02d}:00"

            top_route = (
                data.groupby("route")
                .size()
                .idxmax()
            )

            a, b, c = st.columns(3)

            a.metric("Recorded Tickets", f"{len(data):,}")
            b.metric("Busiest Hour", busiest_hour)
            c.metric("Busiest Route", top_route)

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
                color_continuous_scale=[
                    "#F3DDE1", BURGUNDY
                ]
            )

            fig.update_layout(
                coloraxis_showscale=False,
                xaxis_title="Time of Day",
                yaxis_title="Number of Tickets",
                xaxis=dict(
                    tickmode="array",
                    tickvals=[
                        f"{h:02d}:00"
                        for h in range(0, 24, 3)
                    ],
                    tickangle=-30
                )
            )

            st.plotly_chart(
                style_chart(fig, 390),
                use_container_width=True,
                config={"responsive": True, "displayModeBar": False}
            )

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
                xaxis_title="Time of Day",
                yaxis_title="Passengers",
                xaxis=dict(
                    tickmode="array",
                    tickvals=[
                        f"{h:02d}:00"
                        for h in range(0, 24, 3)
                    ],
                    tickangle=-30
                )
            )

            st.plotly_chart(
                style_chart(fig2, 350),
                use_container_width=True
            )

            st.markdown(
                '<div class="section-title">Top Routes by Demand</div>',
                unsafe_allow_html=True
            )

            route_demand = (
                data.groupby("route")
                .size()
                .nlargest(8)
                .sort_values()
                .reset_index(name="Tickets")
            )

            fig3 = px.bar(
                route_demand,
                x="Tickets",
                y="route",
                orientation="h",
                text="Tickets",
                title="Most Used Routes",
                color_discrete_sequence=[ROSE]
            )

            fig3.update_traces(
                textposition="outside",
                cliponaxis=False
            )
            fig3.update_layout(
                yaxis_title="",
                margin=dict(l=15, r=45, t=55, b=20)
            )

            st.plotly_chart(
                style_chart(fig3, 370),
                use_container_width=True
            )

            distinct_dates = data["date"].dropna().dt.date.nunique()

            if distinct_dates <= 1:
                st.info(
                    "Your current dataset contains records for one "
                    "travel date. These charts describe that day's "
                    "hourly activity. Daily trend analysis and reliable "
                    "future forecasting need records from multiple dates."
                )
            else:
                st.success(
                    f"Your dataset covers {distinct_dates} distinct "
                    "travel dates. Historical daily demand can now "
                    "be compared across dates."
                )

        else:
            st.warning(
                "The dataset has no readable Time values. "
                "Check the Time column to enable hourly analysis."
            )

    else:
        st.info("Upload your ticket dataset.")

# =========================================================
# SMART INSIGHTS
# =========================================================

elif page == "Smart Insights":

    st.title("Smart Insights")

    if not data.empty:

        stats = (
            data.groupby("route")
            .agg(
                Tickets=("route", "size"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum")
            )
            .sort_values("Tickets", ascending=False)
        )

        busiest = stats.index[0]
        passenger_route = stats["Passengers"].idxmax()
        revenue_route = stats["Revenue"].idxmax()

        observations = [
            (
                "✧ Busiest Route",
                f"{busiest} has {int(stats.loc[busiest, 'Tickets']):,} ticket records."
            ),
            (
                "♙ Passenger Movement",
                f"{passenger_route} has the highest recorded passenger total: {int(stats.loc[passenger_route, 'Passengers']):,}."
            ),
            (
                "₹ Revenue Observation",
                f"{revenue_route} has the highest collected amount: {money(stats.loc[revenue_route, 'Revenue'])}."
            ),
            (
                "◷ Uncollected Amount",
                f"{money(data.uncollected.sum())} is recorded as uncollected."
            )
        ]

        for title, description in observations:
            st.markdown(
                f'<div class="card"><h3>{title}</h3>'
                f'<p>{description}</p></div>',
                unsafe_allow_html=True
            )
            st.write("")

    else:
        st.info("Upload your ticket dataset.")

# =========================================================
# REPORTS
# =========================================================

elif page == "Reports":

    st.title("Reports")
    st.caption("Download ticket and route analysis reports.")

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

        st.subheader("Dataset Summary")

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Full Ticket Data (CSV)",
            data.to_csv(index=False).encode("utf-8"),
            "bus_ticket_records.csv",
            "text/csv",
            use_container_width=True
        )

        st.download_button(
            "Download Summary (CSV)",
            summary.to_csv(index=False).encode("utf-8"),
            "bus_analytics_summary.csv",
            "text/csv",
            use_container_width=True
        )

        route_report = (
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
            "Download Route Report (CSV)",
            route_report.to_csv(index=False).encode("utf-8"),
            "route_analysis_report.csv",
            "text/csv",
            use_container_width=True
        )

    else:
        st.info("Upload your ticket dataset to generate reports.")

# =========================================================
# UPLOAD DATASET
# =========================================================

elif page == "Upload Dataset":

    st.title("Upload Dataset")

    st.caption(
        "Upload a CSV containing bus ticket records."
    )

    uploaded = st.file_uploader(
        "Choose Ticket Data (CSV)",
        type=["csv"]
    )

    if uploaded is not None:

        try:
            candidate = pd.read_csv(uploaded)
            checked = prepare_data(candidate)

            st.session_state.uploaded_raw = candidate

            st.success(
                f"Dataset loaded successfully: "
                f"{len(checked):,} records."
            )

            st.dataframe(
                checked.head(10),
                use_container_width=True,
                hide_index=True
            )

            if st.button("Use Repository Dataset Instead"):
                st.session_state.uploaded_raw = None
                st.rerun()

        except Exception as error:
            st.error(f"Could not use this CSV: {error}")

    elif DATA_FILE.exists():

        st.success(
            "Repository dataset found: data/tickets.csv"
        )

    else:

        st.warning(
            "Add data/tickets.csv to your repository "
            "or upload a CSV above."
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<hr>
<div style="
 text-align:center;
 color:#987984;
 font-size:.82rem;
 padding:10px 0 5px;
">
 BOOK • ANALYZE • PREDICT
 &nbsp; | &nbsp;
 Created by <b>CRACKER HEADS ♡</b>
</div>
""", unsafe_allow_html=True)

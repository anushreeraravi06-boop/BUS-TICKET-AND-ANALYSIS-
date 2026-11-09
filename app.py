
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ------------------------------------------------------------
# BUS ANALYTICS | CRACKER HEADS
# Responsive dashboard using the approved prototype
# ------------------------------------------------------------

st.set_page_config(
    page_title="Bus Analytics | CRACKER HEADS",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tickets.csv"

# Approved prototype colours
BG = "#FFF8F5"
PINK = "#F8E6E5"
BURGUNDY = "#64243D"
PLUM = "#351324"
ROSE = "#C77B8C"
GOLD = "#D7A66B"
INK = "#382832"
MUTED = "#8B737D"

# Global high-contrast Plotly theme
BUS_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(
            family="DM Sans, Arial, sans-serif",
            size=13,
            color=PLUM
        ),
        title=dict(
            font=dict(
                family="DM Sans, Arial, sans-serif",
                size=18,
                color=BURGUNDY
            )
        ),
        xaxis=dict(
            tickfont=dict(color=PLUM, size=12),
            title_font=dict(color=BURGUNDY, size=13),
            color=PLUM,
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
            zerolinecolor="#D8C5CB"
        ),
        yaxis=dict(
            tickfont=dict(color=PLUM, size=12),
            title_font=dict(color=BURGUNDY, size=13),
            color=PLUM,
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
            zerolinecolor="#D8C5CB"
        ),
        legend=dict(
            font=dict(color=PLUM, size=12)
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor=BURGUNDY,
            font=dict(color=PLUM, size=13)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
)

pio.templates["bus_analytics"] = BUS_TEMPLATE
pio.templates.default = "bus_analytics"

# ------------------------------------------------------------
# CSS DESIGN
# ------------------------------------------------------------

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

html, body,
[data-testid="stAppViewContainer"] {{
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
    background:linear-gradient(
        180deg,#FBEAE7 0%,#F5DFE2 100%
    );
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
    white-space:normal;
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
    background:linear-gradient(
        135deg,#FFF 0%,#FCEDEF 100%
    );
    border:1px solid #EBD8DC;
    border-radius:18px;
    padding:17px 18px;
    box-shadow:0 4px 16px rgba(85,35,55,.045);
}}

[data-testid="stMetricLabel"] p {{
    color:#624D57 !important;
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
    color:#624D57;
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
    color:#FFF4ED !important;
    font-family:'Playfair Display',serif;
    font-size:clamp(2rem,4vw,3.1rem);
    line-height:1.08;
    margin:8px 0;
}}

.hero p {{
    color:#F8E7E4 !important;
    font-size:1rem;
    max-width:650px;
    margin:0;
    line-height:1.6;
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

h1, h2, h3, h4 {{
    color:var(--burgundy);
    overflow-wrap:anywhere;
}}

.stButton button[kind="primary"] {{
    background:var(--burgundy);
    color:white;
    border:0;
    border-radius:12px;
    font-weight:700;
    min-height:42px;
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
    min-height:42px;
    white-space:normal;
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

/* -----------------------------------------
   LAPTOP AND DESKTOP TEXT CONTRAST FIX
----------------------------------------- */

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
    color:#64243D;
}}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
    color:#624D57 !important;
}}

[data-testid="stDataFrame"] {{
    color:#351324 !important;
}}

/* Make chart text dark and readable */
.js-plotly-plot .plotly text {{
    fill:#351324 !important;
}}

.js-plotly-plot .gtitle {{
    fill:#64243D !important;
}}

.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text {{
    fill:#351324 !important;
}}

.js-plotly-plot .legend text {{
    fill:#351324 !important;
}}

.js-plotly-plot .hovertext text {{
    fill:#351324 !important;
}}

/* -----------------------------------------
   TABLET AND MOBILE RESPONSIVENESS
----------------------------------------- */

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
        width:100% !important;
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

@media (max-width:380px) {{
    .block-container {{
        padding-left:.5rem !important;
        padding-right:.5rem !important;
    }}

    .hero h1 {{
        font-size:1.48rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size:1.15rem !important;
    }}
}}

@media (max-width:900px) {{
    .block-container {{
        padding:.7rem .8rem 1.5rem .8rem !important;
    }}

    .hero {{
        padding:23px 20px;
        min-height:unset;
    }}

    .hero h1 {{
        font-size:2rem;
    }}

    [data-testid="stMetric"] {{
        padding:12px 13px;
    }}

    [data-testid="stSidebar"] {{
        min-width:min(82vw,310px);
    }}
}}

@media (max-width:600px) {{
    .block-container {{
        padding-left:.65rem !important;
        padding-right:.65rem !important;
    }}

    .hero {{
        border-radius:17px;
        padding:20px 17px;
    }}

    .hero h1 {{
        font-size:1.75rem;
    }}

    .card {{
        padding:16px;
    }}

    [data-testid="stMetricValue"] {{
        font-size:1.35rem !important;
    }}

    [data-testid="stSidebar"] {{
        min-width:min(86vw,300px);
    }}
}}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# DATA HELPERS
# ------------------------------------------------------------

def find_col(frame, candidates):
    lookup = {
        str(c).strip().lower(): c
        for c in frame.columns
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
        "waybill": [
            "Waybill Number", "Waybill", "waybill_number"
        ],
        "ticket": [
            "Ticket Number", "Ticket No", "ticket_number"
        ],
        "from": [
            "From Stop", "From", "Origin"
        ],
        "to": [
            "To Stop", "To", "Destination"
        ],
        "date": [
            "Date", "Journey Date", "Travel Date"
        ],
        "time": [
            "Time", "Journey Time"
        ],
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
        ],
    }

    selected = {
        name: find_col(df, aliases)
        for name, aliases in mapping.items()
    }

    required = [
        "from", "to", "date",
        "passengers", "collected"
    ]

    missing = [
        x for x in required
        if selected[x] is None
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
                "" if name in ["waybill", "ticket", "time"]
                else 0
            )

    out["from"] = (
        out["from"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    out["to"] = (
        out["to"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    out["route"] = (
        out["from"] + " – " + out["to"]
    )

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

    for col in [
        "passengers", "collected", "uncollected"
    ]:
        out[col] = pd.to_numeric(
            out[col],
            errors="coerce"
        ).fillna(0).clip(lower=0)

    out["ticket"] = out["ticket"].astype(str)
    out["waybill"] = out["waybill"].astype(str)

    return out

def load_default_data():
    if not DATA_FILE.exists():
        return None

    return pd.read_csv(DATA_FILE)

def money(value):
    return f"₹{value:,.0f}"

def go_to(page):
    st.session_state.current_page = page

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
        title_font=dict(
            color=BURGUNDY,
            size=18
        ),
        margin=dict(
            l=15, r=15, t=55, b=15
        ),
        autosize=True
    )

    fig.update_xaxes(
        tickfont=dict(color=PLUM, size=12),
        title_font=dict(color=BURGUNDY),
        color=PLUM
    )

    fig.update_yaxes(
        tickfont=dict(color=PLUM, size=12),
        title_font=dict(color=BURGUNDY),
        color=PLUM
    )

    return fig

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "uploaded_raw" not in st.session_state:
    st.session_state.uploaded_raw = None

# ------------------------------------------------------------
# LOAD DATASET
# ------------------------------------------------------------

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
        "No dataset found. Add your file at "
        "data/tickets.csv or upload a CSV from Upload Dataset."
    )

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    brand_image = ROOT / "brand_panel.png.jpeg"
    logo_image = ROOT / "logo.png.jpeg"

    if brand_image.exists():
        st.image(
            str(brand_image),
            use_container_width=True
        )

    elif logo_image.exists():
        st.image(
            str(logo_image),
            use_container_width=True
        )

    else:
        st.markdown("""
        <div style="text-align:center;padding:20px 8px;color:#64243D">
            <div style="font-size:3rem">🚌</div>
            <h2>BUS ANALYTICS</h2>
            <small>Intelligent Bus Ticket Data Platform</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height:1px;background:#E5C8CF;margin:12px 0 18px"></div>
    <p style="font-weight:800;letter-spacing:1px;font-size:.85rem">
        NAVIGATION
    </p>
    """, unsafe_allow_html=True)

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

    st.markdown("""
    <div style="height:1px;background:#E5C8CF;margin:18px 0"></div>
    <p style="color:#987984;font-size:.8rem;letter-spacing:1px">
        BOOK • ANALYZE • PREDICT
    </p>
    <p style="color:#987984;font-size:.82rem">
        Created by <b>CRACKER HEADS ♡</b>
    </p>
    """, unsafe_allow_html=True)

page = st.session_state.current_page

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        f"""
        <div style="color:{MUTED};font-size:.8rem;
        font-weight:700;letter-spacing:1.4px">
        CRACKER HEADS / BUS OPERATIONS
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        f"""
        <div style="text-align:right;color:{BURGUNDY};
        font-weight:700;padding-top:3px">
        🚌 BUS ANALYTICS
        </div>
        """,
        unsafe_allow_html=True
    )

if data_error and page != "Upload Dataset":
    st.warning(data_error)

# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">
            INTELLIGENT TRANSPORTATION ANALYTICS
        </div>
        <h1>Welcome to Bus Analytics</h1>
        <p>
            Monitor ticket activity, understand passenger
            movement and explore route performance with
            your bus ticket records.
        </p>
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

        st.markdown(
            '<div class="section-title">'
            'Ticket Activity Overview</div>',
            unsafe_allow_html=True
        )

        chart_left, chart_right = st.columns([1.25, 1])

        with chart_left:

            trend = (
                data.dropna(subset=["date"])
                .groupby(data["date"].dt.date)
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

                style_chart(fig, 330)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info(
                    "No usable date values were found for the trend chart."
                )

        with chart_right:

            top_routes = (
                data.groupby("route")
                .agg(
                    Tickets=("route", "size"),
                    Passengers=("passengers", "sum")
                )
                .reset_index()
                .nlargest(7, "Tickets")
                .sort_values("Tickets")
            )

            if not top_routes.empty:

                fig = px.bar(
                    top_routes,
                    x="Tickets",
                    y="route",
                    orientation="h",
                    title="Top Routes by Tickets",
                    text="Tickets"
                )

                fig.update_traces(
                    marker_color=ROSE,
                    textposition="outside",
                    cliponaxis=False
                )

                fig.update_layout(
                    yaxis_title="",
                    xaxis_title="Tickets"
                )

                style_chart(fig, 330)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        st.markdown(
            '<div class="section-title">'
            'Explore Your Analytics</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown("""
            <div class="card">
                <h3>↗ Demand Prediction</h3>
                <p>
                    Explore historical ticket demand and
                    simple upcoming demand estimates.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "Explore Demand",
                key="home_demand",
                use_container_width=True
            ):
                go_to("Demand Prediction")
                st.rerun()

        with c2:

            st.markdown("""
            <div class="card">
                <h3>✧ Smart Insights</h3>
                <p>
                    Find useful observations from routes,
                    passengers and collections.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "Explore Insights",
                key="home_insights",
                use_container_width=True
            ):
                go_to("Smart Insights")
                st.rerun()

        with c3:

            st.markdown("""
            <div class="card">
                <h3>▧ Generate Reports</h3>
                <p>
                    Export ticket records and summary data
                    for further review.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "Explore Reports",
                key="home_reports",
                use_container_width=True
            ):
                go_to("Reports")
                st.rerun()

    else:

        st.markdown("""
        <div class="card">
            <h3>Your Analytics Workspace Is Ready</h3>
            <p>
                Upload the ticket dataset to populate ticket
                totals, revenue, passenger insights,
                route charts and reports.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Upload Ticket Dataset",
            type="primary"
        ):
            go_to("Upload Dataset")
            st.rerun()

# ============================================================
# TICKET RECORDS
# ============================================================

elif page == "Ticket Records":

    st.title("Ticket Records")

    st.caption(
        "Search, review and export the ticket records "
        "in your dataset."
    )

    if not data.empty:

        search = st.text_input(
            "Search by ticket, waybill, route or stop",
            placeholder="Type a ticket number, route or stop..."
        )

        view = data.copy()

        if search.strip():

            mask = (
                view.astype(str)
                .apply(
                    lambda col: col.str.contains(
                        search,
                        case=False,
                        na=False,
                        regex=False
                    )
                )
                .any(axis=1)
            )

            view = view[mask]

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

        st.write(f"**{len(view):,} records found**")

        st.dataframe(
            display[[
                "Waybill Number",
                "Ticket Number",
                "From Stop",
                "To Stop",
                "Date",
                "Time",
                "Passengers",
                "Collected Amount (₹)",
                "Uncollected Amount (₹)"
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Filtered Records (CSV)",
            view.to_csv(index=False).encode("utf-8"),
            "ticket_records.csv",
            "text/csv"
        )

    else:
        st.info("Upload a CSV dataset to view ticket records.")

# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.title("Operations Dashboard")

    st.caption(
        "A consolidated view of ticketing and bus operation activity."
    )

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
                    "Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"
                ])
                .dropna()
                .reset_index()
            )

            by_day.columns = ["Day", "Tickets"]

            fig = px.bar(
                by_day,
                x="Day",
                y="Tickets",
                title="Tickets by Day of Week",
                color_discrete_sequence=[ROSE]
            )

            style_chart(fig, 350)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with y:

            fig = px.pie(
                data,
                names="from",
                title="Ticket Origins",
                hole=.55
            )

            style_chart(fig, 350)

            fig.update_layout(
                legend_title_text="From Stop"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:
        st.info("Upload your ticket CSV to see the dashboard.")

# ============================================================
# ROUTE ANALYSIS
# ============================================================

elif page == "Route Analysis":

    st.title("Route Analysis")

    st.caption(
        "Compare route activity, passenger volume and collected amounts."
    )

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

        fig = px.bar(
            routes.head(15).sort_values("Passengers"),
            x="Passengers",
            y="route",
            orientation="h",
            title="Top 15 Routes by Passenger Count",
            color_discrete_sequence=[BURGUNDY]
        )

        style_chart(fig, 520)

        fig.update_layout(
            margin=dict(l=10, r=15, t=55, b=10),
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Upload your ticket CSV to analyse routes.")

# ============================================================
# REVENUE ANALYSIS
# ============================================================

elif page == "Revenue Analysis":

    st.title("Revenue Analysis")

    st.caption(
        "Review collected and uncollected ticket amounts."
    )

    if not data.empty:

        a, b, c = st.columns(3)

        a.metric(
            "Collected Amount",
            money(data.collected.sum())
        )

        b.metric(
            "Uncollected Amount",
            money(data.uncollected.sum())
        )

        c.metric(
            "Total Recorded Amount",
            money(
                data.collected.sum()
                + data.uncollected.sum()
            )
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

        style_chart(fig, 430)

        fig.update_layout(
            margin=dict(l=10, r=10, t=55, b=100),
            xaxis_title="",
            legend_title_text="Amount"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Upload your ticket CSV to analyse revenue.")

# ============================================================
# PASSENGER INSIGHTS
# ============================================================

elif page == "Passenger Insights":

    st.title("Passenger Insights")

    st.caption(
        "Understand passenger volumes and the busiest boarding points."
    )

    if not data.empty:

        a, b, c = st.columns(3)

        a.metric(
            "Total Passengers",
            f"{int(data.passengers.sum()):,}"
        )

        b.metric(
            "Average Passengers / Ticket",
            f"{data.passengers.mean():.2f}"
        )

        c.metric(
            "Boarding Stops",
            f"{data['from'].nunique():,}"
        )

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
            x="Passengers",
            y="from",
            orientation="h",
            title="Busiest Boarding Stops",
            color_discrete_sequence=[ROSE]
        )

        style_chart(fig, 440)

        fig.update_layout(
            margin=dict(l=10, r=15, t=55, b=10),
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Upload your ticket CSV to view passenger insights.")

# ============================================================
# DEMAND PREDICTION
# ============================================================

elif page == "Demand Prediction":

    st.title("Demand Prediction")

    st.caption(
        "A simple historical baseline to help explore ticket demand. "
        "This is not a trained or validated forecasting model."
    )

    if not data.empty:

        daily = (
            data.dropna(subset=["date"])
            .groupby(data.date.dt.date)
            .size()
            .rename("Tickets")
            .reset_index()
        )

        daily.columns = ["Date", "Tickets"]

        if len(daily) >= 2:

            daily["7-day average"] = (
                daily["Tickets"]
                .rolling(7, min_periods=1)
                .mean()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=daily.Date,
                    y=daily.Tickets,
                    name="Actual Tickets",
                    mode="lines+markers",
                    line=dict(
                        color=BURGUNDY,
                        width=3
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=daily.Date,
                    y=daily["7-day average"],
                    name="7-day Rolling Average",
                    mode="lines",
                    line=dict(
                        color=GOLD,
                        width=3,
                        dash="dash"
                    )
                )
            )

            style_chart(fig, 430)

            fig.update_layout(
                title="Historical Daily Demand",
                legend=dict(
                    orientation="h",
                    y=1.12
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.metric(
                "Latest 7-day Average",
                f"{daily['7-day average'].iloc[-1]:.1f} tickets/day"
            )

            st.info(
                "The average is a descriptive baseline from historical "
                "records, not a guarantee of future demand."
            )

        else:
            st.info(
                "At least two distinct dates are needed "
                "to show a demand trend."
            )

    else:
        st.info("Upload your ticket CSV to explore demand.")

# ============================================================
# SMART INSIGHTS
# ============================================================

elif page == "Smart Insights":

    st.title("Smart Insights")

    st.caption(
        "Automatically generated observations based on "
        "the uploaded ticket records."
    )

    if not data.empty:

        route_stats = (
            data.groupby("route")
            .agg(
                Tickets=("route", "size"),
                Passengers=("passengers", "sum"),
                Collected=("collected", "sum")
            )
            .sort_values("Tickets", ascending=False)
        )

        busiest = route_stats.index[0]
        most_passenger = route_stats["Passengers"].idxmax()
        highest_revenue = route_stats["Collected"].idxmax()
        avg = data.passengers.mean()

        st.markdown(f"""
        <div class="card">
            <h3>✧ Busiest Route</h3>
            <p>
                <b>{busiest}</b> has the highest number of
                ticket records
                ({int(route_stats.loc[busiest, 'Tickets']):,}).
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown(f"""
        <div class="card">
            <h3>♙ Passenger Movement</h3>
            <p>
                <b>{most_passenger}</b> has the largest recorded
                passenger total
                ({int(route_stats.loc[most_passenger, 'Passengers']):,}).
                Average passengers per ticket: {avg:.2f}.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown(f"""
        <div class="card">
            <h3>₹ Revenue Observation</h3>
            <p>
                <b>{highest_revenue}</b> has the highest collected
                amount
                ({money(route_stats.loc[highest_revenue, 'Collected'])}).
            </p>
        </div>
        """, unsafe_allow_html=True)

        if data.uncollected.sum() > 0:

            st.write("")

            st.markdown(f"""
            <div class="card">
                <h3>◷ Uncollected Amount</h3>
                <p>
                    {money(data.uncollected.sum())} is recorded
                    as uncollected in the dataset.
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Upload your ticket CSV to generate observations.")

# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("Reports")

    st.caption(
        "Download the dataset and summary tables for reporting."
    )

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
            type="primary"
        )

        st.download_button(
            "Download Summary (CSV)",
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
            "Download Route Report (CSV)",
            route_summary.to_csv(index=False).encode("utf-8"),
            "route_analysis_report.csv",
            "text/csv"
        )

    else:
        st.info("Upload your ticket CSV to generate reports.")

# ============================================================
# UPLOAD DATASET
# ============================================================

elif page == "Upload Dataset":

    st.title("Upload Dataset")

    st.caption(
        "Upload a CSV containing bus ticket records. "
        "Your repository dataset remains the default source "
        "after app restarts."
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
                f"Dataset loaded successfully — "
                f"{len(checked):,} ticket records detected."
            )

            st.dataframe(
                checked.head(10),
                use_container_width=True,
                hide_index=True
            )

            if st.button("Use Repository Dataset Instead"):

                st.session_state.uploaded_raw = None
                st.rerun()

        except Exception as exc:

            st.error(
                f"This CSV could not be used: {exc}"
            )

    else:

        if DATA_FILE.exists():

            st.success(
                "Repository dataset found: data/tickets.csv"
            )

            st.caption(
                "The app will load this dataset automatically "
                "when no temporary upload is active."
            )

        else:

            st.warning(
                "No repository dataset found yet. Upload a CSV "
                "or add data/tickets.csv to your GitHub repository."
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<hr>
<div style="
    text-align:center;
    color:#987984;
    font-size:.82rem;
    padding:8px 0 2px;
">
    BOOK • ANALYZE • PREDICT
    &nbsp; | &nbsp;
    Created by <b>CRACKER HEADS ♡</b>
</div>
""", unsafe_allow_html=True)

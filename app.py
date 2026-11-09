
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# BUS ANALYTICS | CRACKER HEADS
# Responsive dashboard based on the approved prototype
# ============================================================

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

# ----------------------------- CSS -----------------------------

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {{
    --bg: {BG};
    --pink: {PINK};
    --burgundy: {BURGUNDY};
    --plum: {PLUM};
    --rose: {ROSE};
    --gold: {GOLD};
    --ink: {INK};
    --muted: {MUTED};
}}

html, body, [data-testid="stAppViewContainer"] {{
    background: var(--bg);
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
}}

[data-testid="stHeader"] {{
    background: rgba(255,248,245,.96);
}}

[data-testid="stToolbar"] {{
    right: 1rem;
}}

.block-container {{
    max-width: 1700px;
    padding: 1.2rem 2rem 2rem 2rem !important;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg,#FBEAE7 0%,#F5DFE2 100%);
    border-right: 1px solid #EAD1D5;
    min-width: 260px;
}}

[data-testid="stSidebar"] > div:first-child {{
    padding: 1rem .9rem;
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color: var(--burgundy);
}}

[data-testid="stSidebar"] [data-testid="stImage"] img {{
    border-radius: 17px;
}}

[data-testid="stSidebar"] .stButton button {{
    width: 100%;
    min-height: 43px;
    text-align: left;
    border: 1px solid transparent;
    border-radius: 13px;
    background: transparent;
    color: var(--burgundy);
    font-weight: 600;
    padding: .55rem .8rem;
    white-space: normal;
}}

[data-testid="stSidebar"] .stButton button:hover {{
    background: #F4D5D8;
    border-color: #E8BFC7;
    color: var(--plum);
}}

[data-testid="stSidebar"] .stButton button[kind="primary"] {{
    background: linear-gradient(100deg,#C77B8C,#E7A5A5);
    color: white;
    border: 0;
}}

h1, h2, h3 {{
    color: var(--burgundy);
    overflow-wrap: anywhere;
}}

h1 {{
    font-family: 'Playfair Display', serif;
}}

p, label, span, div {{
    overflow-wrap: anywhere;
}}

.hero {{
    border-radius: 22px;
    padding: 32px 36px;
    color: white;
    min-height: 205px;
    background:
      linear-gradient(100deg,rgba(45,17,36,.96),rgba(91,35,61,.78)),
      linear-gradient(120deg,#54243D,#A45D72);
    border: 1px solid #6E3A50;
    margin-bottom: 22px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.hero .eyebrow {{
    color: #F5D4C9;
    letter-spacing: 2px;
    font-size: .76rem;
    font-weight: 700;
}}

.hero h1 {{
    color: #FFF4ED;
    font-family: 'Playfair Display',serif;
    font-size: clamp(2rem,4vw,3.2rem);
    line-height: 1.12;
    margin: 9px 0;
}}

.hero p {{
    color: #F8E7E4;
    font-size: 1rem;
    max-width: 700px;
    line-height: 1.6;
    margin: 0;
}}

.section-title {{
    color: var(--burgundy);
    font-size: 1.25rem;
    font-weight: 800;
    margin: 1.2rem 0 .8rem 0;
}}

.small-note {{
    color: var(--muted);
    font-size: .85rem;
}}

[data-testid="stMetric"] {{
    background: linear-gradient(135deg,#FFFFFF 0%,#FCEDEF 100%);
    border: 1px solid #EBD8DC;
    border-radius: 18px;
    padding: 17px 18px;
    box-shadow: 0 4px 16px rgba(85,35,55,.045);
    min-width: 0;
}}

[data-testid="stMetricLabel"] p {{
    color: #806B75 !important;
    font-weight: 600;
    font-size: .88rem;
}}

[data-testid="stMetricValue"] {{
    color: var(--plum) !important;
    font-weight: 800;
    font-size: clamp(1.25rem,2vw,2rem) !important;
}}

.card {{
    background: #FFFFFF;
    border: 1px solid #EAD9DD;
    border-radius: 20px;
    padding: 21px 22px;
    box-shadow: 0 5px 18px rgba(73,32,50,.045);
    height: 100%;
    min-height: 125px;
}}

.card h3 {{
    color: var(--burgundy);
    margin: 0 0 9px 0;
    font-size: 1.05rem;
}}

.card p {{
    color: #755F69;
    margin: 0;
    line-height: 1.6;
}}

.stButton button[kind="primary"] {{
    background: var(--burgundy);
    color: white;
    border: 0;
    border-radius: 12px;
    font-weight: 700;
    min-height: 42px;
}}

.stButton button[kind="primary"]:hover {{
    background: var(--plum);
    color: white;
}}

.stDownloadButton button {{
    background: #F3DDE1;
    color: var(--burgundy);
    border: 1px solid #E6C4CB;
    border-radius: 12px;
    font-weight: 700;
    min-height: 42px;
    white-space: normal;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid #EAD9DD;
    border-radius: 14px;
    overflow: hidden;
}}

[data-testid="stPlotlyChart"] {{
    background: white;
    border: 1px solid #EAD9DD;
    border-radius: 18px;
    padding: 8px;
    box-shadow: 0 4px 14px rgba(73,32,50,.035);
}}

[data-testid="stTextInput"] input {{
    border-radius: 12px;
    border-color: #E5C8CF;
}}

[data-testid="stFileUploader"] {{
    background: #FFF;
    border: 1px dashed #D7A6B1;
    border-radius: 16px;
    padding: 12px;
}}

hr {{
    border-color: #EAD5DA !important;
}}

footer {{
    visibility: hidden;
}}

/* Tablet */
@media (max-width: 1100px) {{
    .block-container {{
        padding: 1rem 1.2rem 2rem 1.2rem !important;
    }}

    .hero {{
        padding: 25px;
    }}
}}

/* Mobile */
@media (max-width: 700px) {{
    .block-container {{
        padding: .7rem .75rem 1.5rem .75rem !important;
    }}

    .hero {{
        border-radius: 17px;
        padding: 21px 18px;
        min-height: 175px;
    }}

    .hero h1 {{
        font-size: 1.8rem;
    }}

    .hero p {{
        font-size: .9rem;
    }}

    .card {{
        padding: 16px;
        min-height: auto;
    }}

    [data-testid="stMetric"] {{
        padding: 12px;
    }}

    [data-testid="stMetricLabel"] p {{
        font-size: .78rem;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.25rem !important;
    }}

    [data-testid="stSidebar"] {{
        min-width: min(85vw,310px);
    }}

    [data-testid="stPlotlyChart"] {{
        padding: 2px;
    }}

    h1 {{
        font-size: 1.8rem !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------- DATA HELPERS -----------------------------

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

    selected = {
        name: find_col(df, aliases)
        for name, aliases in mapping.items()
    }

    required = ["from", "to", "date", "passengers", "collected"]
    missing = [x for x in required if selected[x] is None]

    if missing:
        raise ValueError(
            "The CSV is missing required columns: " + ", ".join(missing)
        )

    out = pd.DataFrame()

    for name, source in selected.items():
        if source is not None:
            out[name] = df[source]
        else:
            out[name] = (
                "" if name in ["waybill", "ticket", "time"] else 0
            )

    out["from"] = (
        out["from"].fillna("Unknown").astype(str).str.strip()
    )
    out["to"] = (
        out["to"].fillna("Unknown").astype(str).str.strip()
    )

    out["route"] = out["from"] + " – " + out["to"]

    out["date"] = pd.to_datetime(
        out["date"], errors="coerce", dayfirst=False
    )

    bad_dates = out["date"].isna()

    if bad_dates.any():
        out.loc[bad_dates, "date"] = pd.to_datetime(
            df.loc[bad_dates, selected["date"]],
            errors="coerce",
            dayfirst=True
        )

    for col in ["passengers", "collected", "uncollected"]:
        out[col] = pd.to_numeric(
            out[col], errors="coerce"
        ).fillna(0)

        out[col] = out[col].clip(lower=0)

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

def chart_layout(fig, height=350):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=INK, family="DM Sans"),
        title_font=dict(color=BURGUNDY, size=17),
        margin=dict(l=12, r=15, t=55, b=15),
        autosize=True,
    )
    return fig

# ----------------------------- SESSION STATE -----------------------------

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "uploaded_raw" not in st.session_state:
    st.session_state.uploaded_raw = None

# ----------------------------- LOAD DATA -----------------------------

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
        "No dataset found. Add your CSV at data/tickets.csv "
        "or upload it from Upload Dataset."
    )

# ----------------------------- SIDEBAR -----------------------------

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
    ("Upload Dataset", "⇧"),
]

with st.sidebar:

    brand_image = ROOT / "brand_panel.png.jpeg"
    logo_image = ROOT / "logo.png.jpeg"

    if brand_image.exists():
        st.image(str(brand_image), use_container_width=True)
    elif logo_image.exists():
        st.image(str(logo_image), use_container_width=True)
    else:
        st.markdown(
            """
            <div style="text-align:center;padding:20px 5px;color:#64243D">
                <div style="font-size:3rem">🚌</div>
                <h2>BUS ANALYTICS</h2>
                <small>Intelligent Bus Ticket Data Platform</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <hr>
        <p style="font-weight:800;letter-spacing:1px;font-size:.85rem">
        NAVIGATION
        </p>
        """,
        unsafe_allow_html=True
    )

    for page_name, symbol in pages:
        if st.button(
            f"{symbol}   {page_name}",
            key=f"nav_{page_name}",
            type=(
                "primary"
                if st.session_state.current_page == page_name
                else "secondary"
            ),
            use_container_width=True,
        ):
            go_to(page_name)
            st.rerun()

    st.markdown(
        """
        <hr>
        <p style="color:#987984;font-size:.8rem;letter-spacing:1px">
        BOOK • ANALYZE • PREDICT
        </p>
        <p style="color:#987984;font-size:.82rem">
        Created by <b>CRACKER HEADS ♡</b>
        </p>
        """,
        unsafe_allow_html=True
    )

page = st.session_state.current_page

# ----------------------------- TOP HEADER -----------------------------

header_left, header_right = st.columns([5, 2])

with header_left:
    st.markdown(
        """
        <div style="color:#8B737D;font-size:.8rem;
        font-weight:700;letter-spacing:1.4px;padding-top:8px">
        CRACKER HEADS / BUS OPERATIONS
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        f"""
        <div style="text-align:right;color:{BURGUNDY};
        font-weight:800;padding-top:5px">
        🚌 BUS ANALYTICS
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

if data_error and page != "Upload Dataset":
    st.warning(data_error)

# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">
                INTELLIGENT TRANSPORTATION ANALYTICS
            </div>
            <h1>Welcome to Bus Analytics</h1>
            <p>
                A smart bus ticket data platform to monitor ticket activity,
                understand passenger movement and explore route performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
            '<div class="section-title">Ticket Activity Overview</div>',
            unsafe_allow_html=True
        )

        chart_left, chart_right = st.columns([1.2, 1])

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

                chart_layout(fig, 360)
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("No usable dates were found for the trend chart.")

        with chart_right:

            top_routes = (
                data.groupby("route")
                .agg(Tickets=("route", "size"))
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

                chart_layout(fig, 360)
                fig.update_layout(
                    yaxis_title="",
                    xaxis_title="Tickets"
                )

                st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            '<div class="section-title">Explore Your Analytics</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                """
                <div class="card">
                    <h3>↗ Demand Prediction</h3>
                    <p>Explore historical ticket demand and simple demand trends.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("Explore Demand", key="home_demand",
                         use_container_width=True):
                go_to("Demand Prediction")
                st.rerun()

        with c2:
            st.markdown(
                """
                <div class="card">
                    <h3>✧ Smart Insights</h3>
                    <p>Discover useful observations from routes, passengers and collections.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("Explore Insights", key="home_insights",
                         use_container_width=True):
                go_to("Smart Insights")
                st.rerun()

        with c3:
            st.markdown(
                """
                <div class="card">
                    <h3>▧ Generate Reports</h3>
                    <p>Download ticket records and summary data for review.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button("Explore Reports", key="home_reports",
                         use_container_width=True):
                go_to("Reports")
                st.rerun()

    else:

        st.markdown(
            """
            <div class="card">
                <h3>Your Analytics Workspace Is Ready</h3>
                <p>
                Upload your ticket dataset to display ticket totals,
                revenue, passenger insights, route charts and reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Upload Ticket Dataset", type="primary"):
            go_to("Upload Dataset")
            st.rerun()

# ============================================================
# TICKET RECORDS
# ============================================================

elif page == "Ticket Records":

    st.title("Ticket Records")
    st.caption(
        "Search, review and download ticket records from your dataset."
    )

    if not data.empty:

        search = st.text_input(
            "Search by ticket, waybill, route or stop",
            placeholder="Enter ticket number, route or stop..."
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

        display = view.rename(
            columns={
                "waybill": "Waybill Number",
                "ticket": "Ticket Number",
                "from": "From Stop",
                "to": "To Stop",
                "date": "Date",
                "time": "Time",
                "passengers": "Passengers",
                "collected": "Collected Amount (₹)",
                "uncollected": "Uncollected Amount (₹)",
            }
        )

        st.dataframe(
            display[
                [
                    "Waybill Number",
                    "Ticket Number",
                    "From Stop",
                    "To Stop",
                    "Date",
                    "Time",
                    "Passengers",
                    "Collected Amount (₹)",
                    "Uncollected Amount (₹)",
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Filtered Records (CSV)",
            view.to_csv(index=False).encode("utf-8"),
            "ticket_records.csv",
            "text/csv",
            use_container_width=True
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

        a.metric("Total Tickets", f"{len(data):,}")
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

            chart_layout(fig, 370)
            st.plotly_chart(fig, use_container_width=True)

        with y:

            fig = px.pie(
                data,
                names="from",
                title="Ticket Origins",
                hole=.55
            )

            chart_layout(fig, 370)
            fig.update_layout(legend_title_text="From Stop")

            st.plotly_chart(fig, use_container_width=True)

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

        st.subheader("Route Performance")
        st.dataframe(routes, use_container_width=True, hide_index=True)

        fig = px.bar(
            routes.head(15).sort_values("Passengers"),
            x="Passengers",
            y="route",
            orientation="h",
            title="Top 15 Routes by Passenger Count",
            color_discrete_sequence=[BURGUNDY]
        )

        chart_layout(fig, 520)
        fig.update_layout(yaxis_title="")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Upload your ticket CSV to analyse routes.")

# ============================================================
# REVENUE ANALYSIS
# ============================================================

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

        chart_layout(fig, 440)

        fig.update_layout(
            margin=dict(l=12, r=12, t=55, b=110),
            xaxis_title="",
            legend_title_text="Amount"
        )

        st.plotly_chart(fig, use_container_width=True)

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

        chart_layout(fig, 450)
        fig.update_layout(yaxis_title="")

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Upload your ticket CSV to view passenger insights.")

# ============================================================
# DEMAND PREDICTION
# ============================================================

elif page == "Demand Prediction":

    st.title("Demand Prediction")

    st.caption(
        "Explore historical ticket demand using a simple rolling average. "
        "This is a baseline, not a trained forecasting model."
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
                daily["Tickets"].rolling(7, min_periods=1).mean()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=daily.Date,
                    y=daily.Tickets,
                    name="Actual Tickets",
                    mode="lines+markers",
                    line=dict(color=BURGUNDY, width=3)
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=daily.Date,
                    y=daily["7-day average"],
                    name="7-Day Rolling Average",
                    mode="lines",
                    line=dict(color=GOLD, width=3, dash="dash")
                )
            )

            fig.update_layout(
                title="Historical Daily Demand",
                legend=dict(orientation="h", y=1.12)
            )

            chart_layout(fig, 450)
            st.plotly_chart(fig, use_container_width=True)

            st.metric(
                "Latest 7-Day Average",
                f"{daily['7-day average'].iloc[-1]:.1f} tickets/day"
            )

            st.info(
                "This average describes historical ticket activity. "
                "It does not guarantee future demand."
            )

        else:
            st.info(
                "At least two distinct dates are needed to show a demand trend."
            )

    else:
        st.info("Upload your ticket CSV to explore demand.")

# ============================================================
# SMART INSIGHTS
# ============================================================

elif page == "Smart Insights":

    st.title("Smart Insights")

    st.caption(
        "Automatically generated observations based on your ticket records."
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
        average_passengers = data.passengers.mean()

        st.markdown(
            f"""
            <div class="card">
                <h3>✧ Busiest Route</h3>
                <p><b>{busiest}</b> has the highest number of ticket
                records ({int(route_stats.loc[busiest, 'Tickets']):,}).</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f"""
            <div class="card">
                <h3>♙ Passenger Movement</h3>
                <p><b>{most_passenger}</b> has the largest recorded
                passenger total ({int(route_stats.loc[most_passenger, 'Passengers']):,}).
                Average passengers per ticket: {average_passengers:.2f}.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f"""
            <div class="card">
                <h3>₹ Revenue Observation</h3>
                <p><b>{highest_revenue}</b> has the highest collected
                amount ({money(route_stats.loc[highest_revenue, 'Collected'])}).</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if data.uncollected.sum() > 0:

            st.write("")

            st.markdown(
                f"""
                <div class="card">
                    <h3>◷ Uncollected Amount</h3>
                    <p>{money(data.uncollected.sum())} is recorded
                    as uncollected in the dataset.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("Upload your ticket CSV to generate observations.")

# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("Reports")
    st.caption(
        "Download ticket records and summary tables for reporting."
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

        st.markdown(
            '<div class="section-title">Download Reports</div>',
            unsafe_allow_html=True
        )

        st.download_button(
            "Download Full Ticket Data (CSV)",
            data.to_csv(index=False).encode("utf-8"),
            "bus_ticket_records.csv",
            "text/csv",
            type="primary",
            use_container_width=True
        )

        st.download_button(
            "Download Summary (CSV)",
            summary.to_csv(index=False).encode("utf-8"),
            "bus_analytics_summary.csv",
            "text/csv",
            use_container_width=True
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
            "text/csv",
            use_container_width=True
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
        "Your repository dataset remains the default source after app restarts."
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

            st.error(f"This CSV could not be used: {exc}")

    else:

        if DATA_FILE.exists():

            st.success(
                "Repository dataset found: data/tickets.csv"
            )

            st.caption(
                "The app loads this dataset automatically when "
                "no temporary upload is active."
            )

        else:

            st.warning(
                "No repository dataset found. Upload a CSV or add "
                "data/tickets.csv to your GitHub repository."
            )

# ----------------------------- FOOTER -----------------------------

st.markdown(
    """
    <hr>
    <div style="text-align:center;color:#987984;
    font-size:.82rem;padding:12px 0 5px">
        BOOK • ANALYZE • PREDICT
        &nbsp; | &nbsp;
        Created by <b>CRACKER HEADS ♡</b>
    </div>
    """,
    unsafe_allow_html=True
)

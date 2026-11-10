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
# ------------------------------------------------------------

st.set_page_config(
    page_title="Bus Analytics | CRACKER HEADS",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tickets.csv"

# Approved colour palette
BG = "#FFF8F5"
PINK = "#F8E6E5"
BURGUNDY = "#64243D"
PLUM = "#351324"
ROSE = "#C77B8C"
GOLD = "#D7A66B"
INK = "#382832"
MUTED = "#8B737D"

BUS_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(family="DM Sans, Arial, sans-serif", size=13, color=PLUM),
        title=dict(font=dict(size=18, color=BURGUNDY)),
        xaxis=dict(tickfont=dict(color=PLUM), title_font=dict(color=BURGUNDY),
                   gridcolor="#EADDE0", linecolor="#CDB8BF"),
        yaxis=dict(tickfont=dict(color=PLUM), title_font=dict(color=BURGUNDY),
                   gridcolor="#EADDE0", linecolor="#CDB8BF"),
        legend=dict(font=dict(color=PLUM)),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor=BURGUNDY,
                        font=dict(color=PLUM)),
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
 --bg:{BG}; --pink:{PINK}; --burgundy:{BURGUNDY};
 --plum:{PLUM}; --rose:{ROSE}; --gold:{GOLD};
 --ink:{INK}; --muted:{MUTED};
}}

html, body, .stApp,
[data-testid="stAppViewContainer"] {{
 background:#FFF8F5 !important;
 color:#382832 !important;
 font-family:'DM Sans',sans-serif;
 color-scheme:light !important;
}}

[data-testid="stHeader"] {{ background:rgba(255,248,245,.92); }}
.block-container {{ padding-top:1.15rem !important; max-width:1600px; }}

[data-testid="stSidebar"] {{
 background:linear-gradient(180deg,#FBEAE7 0%,#F5DFE2 100%);
 border-right:1px solid #EAD1D5;
}}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] span {{
 color:#64243D !important;
}}

[data-testid="stSidebar"] .stButton button {{
 width:100%;
 text-align:left;
 border:1px solid transparent;
 border-radius:13px;
 background:transparent;
 color:#64243D !important;
 font-weight:700;
 padding:.65rem .8rem;
}}

[data-testid="stSidebar"] .stButton button:hover {{
 background:#F4D5D8;
 border-color:#E8BFC7;
 color:#351324 !important;
}}

[data-testid="stMetric"] {{
 background:linear-gradient(135deg,#FFF 0%,#FCEDEF 100%);
 border:1px solid #EBD8DC;
 border-radius:18px;
 padding:17px 18px;
}}

[data-testid="stMetricLabel"] p {{ color:#624D57 !important; }}
[data-testid="stMetricValue"] {{ color:#351324 !important; font-weight:800; }}

.card {{
 background:#FFFFFF;
 border:1px solid #EAD9DD;
 border-radius:20px;
 padding:20px 22px;
 box-shadow:0 5px 18px rgba(73,32,50,.045);
 height:100%;
}}
.card h3 {{ color:#64243D; margin:0 0 8px 0; }}
.card p {{ color:#755F69; line-height:1.55; }}

.hero {{
 border-radius:22px;
 padding:30px 34px;
 color:white;
 min-height:190px;
 background:linear-gradient(105deg,rgba(45,17,36,.96),rgba(91,35,61,.78));
 border:1px solid #6E3A50;
 margin-bottom:20px;
}}
.hero .eyebrow {{ color:#F5D4C9; letter-spacing:2px; font-size:.75rem; }}
.hero h1 {{
 color:#FFF4ED !important;
 font-family:'Playfair Display',serif;
 font-size:clamp(2rem,4vw,3.1rem);
}}
.hero p {{ color:#F8E7E4 !important; }}

h1, h2, h3, h4 {{ color:#64243D !important; }}
p, label {{ color:#382832; }}
[data-testid="stCaptionContainer"] p {{ color:#624D57 !important; }}

.stButton button[kind="primary"] {{
 background:#64243D;
 color:white !important;
 border:0;
 border-radius:12px;
 font-weight:700;
}}
.stDownloadButton button {{
 background:#F3DDE1;
 color:#64243D !important;
 border:1px solid #E6C4CB;
 border-radius:12px;
 font-weight:700;
}}

[data-testid="stDataFrame"] {{
 border:1px solid #EAD9DD;
 border-radius:14px;
}}

hr {{ border-color:#EAD5DA !important; }}
footer {{ visibility:hidden; }}

@media (max-width:768px) {{
 .block-container {{ padding:.65rem .7rem 1.5rem !important; }}
 [data-testid="stHorizontalBlock"] {{
   flex-direction:column !important;
   gap:.8rem !important;
 }}
 [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
   width:100% !important;
   min-width:100% !important;
 }}
 .hero {{ padding:21px 17px !important; }}
 .hero h1 {{ font-size:1.7rem !important; }}
 .card {{ padding:16px !important; }}
}}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# DATA HELPERS
# ------------------------------------------------------------

def money(value):
    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"


def find_column(df, possible_names):
    normalised = {
        str(col).strip().lower().replace("_", " ").replace("-", " "): col
        for col in df.columns
    }
    for name in possible_names:
        key = name.strip().lower().replace("_", " ").replace("-", " ")
        if key in normalised:
            return normalised[key]
    return None


def prepare_data(raw):
    if raw is None or raw.empty:
        return pd.DataFrame()

    df = raw.copy()

    aliases = {
        "waybill": ["Waybill Number", "Waybill", "Waybill No"],
        "ticket": ["Ticket Number", "Ticket No", "Ticket"],
        "from": ["From Stop", "From", "Origin"],
        "to": ["To Stop", "To", "Destination"],
        "date": ["Date", "Travel Date"],
        "time": ["Time", "Ticket Time"],
        "passengers": ["Total Psgr", "Total Passenger", "Passengers"],
        "collected": ["Coll Amt", "Collected Amount", "Collection"],
        "uncollected": ["Uncoll Amt", "Uncollected Amount"],
    }

    renamed = {}
    for standard, names in aliases.items():
        found = find_column(df, names)
        if found is not None:
            renamed[found] = standard

    df = df.rename(columns=renamed)

    required = ["from", "to"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    defaults = {
        "waybill": "",
        "ticket": "",
        "date": pd.NaT,
        "time": "",
        "passengers": 1,
        "collected": 0,
        "uncollected": 0,
    }

    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default

    for col in ["passengers", "collected", "uncollected"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["from"] = df["from"].astype(str).str.strip()
    df["to"] = df["to"].astype(str).str.strip()
    df["route"] = df["from"] + " → " + df["to"]

    return df


def style_chart(fig, height=380):
    fig.update_layout(
        template="bus_analytics",
        height=height,
        margin=dict(l=15, r=15, t=55, b=15),
        font=dict(color=PLUM),
    )
    return fig


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

if "uploaded_raw" not in st.session_state:
    st.session_state.uploaded_raw = None

if st.session_state.uploaded_raw is not None:
    raw_data = st.session_state.uploaded_raw
elif DATA_FILE.exists():
    raw_data = pd.read_csv(DATA_FILE)
else:
    raw_data = pd.DataFrame()

try:
    data = prepare_data(raw_data)
except Exception as exc:
    data = pd.DataFrame()
    st.error(f"Dataset error: {exc}")


# ------------------------------------------------------------
# NAVIGATION
# ------------------------------------------------------------

PAGES = [
    "Home",
    "Ticket Records",
    "Dashboard",
    "Route Analysis",
    "Revenue Analysis",
    "Passenger Insights",
    "Demand Prediction",
    "Smart Insights",
    "Reports",
    "Upload Dataset",
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    logo_path = ROOT / "logo.png.jpeg"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)

    st.markdown(
        "<h2 style='text-align:center;color:#64243D !important;'>BUS ANALYTICS</h2>"
        "<p style='text-align:center;color:#64243D !important;'>CRACKER HEADS</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    for item in PAGES:
        if st.button(
            item,
            key="nav_" + item,
            type="primary" if st.session_state.page == item else "secondary",
            use_container_width=True,
        ):
            st.session_state.page = item
            st.rerun()

page = st.session_state.page

# ------------------------------------------------------------
# COMMON METRICS
# ------------------------------------------------------------

total_tickets = len(data)
total_passengers = int(data["passengers"].sum()) if not data.empty else 0
total_collected = float(data["collected"].sum()) if not data.empty else 0
total_uncollected = float(data["uncollected"].sum()) if not data.empty else 0
route_count = data["route"].nunique() if not data.empty else 0

route_stats = pd.DataFrame()
if not data.empty:
    route_stats = (
        data.groupby("route")
        .agg(
            Tickets=("ticket", "size"),
            Passengers=("passengers", "sum"),
            Collected=("collected", "sum"),
            Uncollected=("uncollected", "sum"),
        )
        .reset_index()
        .sort_values("Tickets", ascending=False)
    )


# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------

if page == "Home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">BOOK • ANALYZE • PREDICT</div>
      <h1>BUS ANALYTICS</h1>
      <p>Intelligent Bus Ticket Data Platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='section-title'>Welcome to your transport analytics platform</div>",
        unsafe_allow_html=True,
    )

    if not data.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Tickets", f"{total_tickets:,}")
        c2.metric("Total Passengers", f"{total_passengers:,}")
        c3.metric("Collected Revenue", money(total_collected))
        c4.metric("Active Routes", f"{route_count:,}")

        left, right = st.columns(2)

        with left:
            daily = data.dropna(subset=["date"]).groupby("date").size().reset_index(name="Tickets")
            if not daily.empty:
                fig = px.line(
                    daily, x="date", y="Tickets", markers=True,
                    title="Ticket Booking Trend",
                )
                st.plotly_chart(style_chart(fig), use_container_width=True)

        with right:
            top_routes = route_stats.head(8)
            fig = px.bar(
                top_routes, x="Tickets", y="route", orientation="h",
                title="Top Routes by Ticket Records",
                color="Tickets",
                color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(style_chart(fig), use_container_width=True)

    else:
        st.info("Add your ticket dataset using the Upload Dataset page.")

    st.markdown("<div class='section-title'>Platform Features</div>", unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("<div class='card'><h3>Ticket Records</h3><p>View and search recorded bus ticket information.</p></div>", unsafe_allow_html=True)
    with f2:
        st.markdown("<div class='card'><h3>Route Analysis</h3><p>Understand passenger movement and route activity.</p></div>", unsafe_allow_html=True)
    with f3:
        st.markdown("<div class='card'><h3>Smart Insights</h3><p>Explore rule-based findings and operational recommendations.</p></div>", unsafe_allow_html=True)


# ------------------------------------------------------------
# TICKET RECORDS
# ------------------------------------------------------------

elif page == "Ticket Records":
    st.title("Ticket Records")
    st.caption("Search, filter and inspect the recorded ticket data.")

    if not data.empty:
        search = st.text_input("Search ticket, waybill, stop or route")
        filtered = data.copy()

        if search:
            mask = filtered.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False)
            ).any(axis=1)
            filtered = filtered[mask]

        col1, col2 = st.columns(2)
        with col1:
            from_options = ["All"] + sorted(data["from"].dropna().unique().tolist())
            selected_from = st.selectbox("From stop", from_options)
        with col2:
            to_options = ["All"] + sorted(data["to"].dropna().unique().tolist())
            selected_to = st.selectbox("To stop", to_options)

        if selected_from != "All":
            filtered = filtered[filtered["from"] == selected_from]
        if selected_to != "All":
            filtered = filtered[filtered["to"] == selected_to]

        st.caption(f"Showing {len(filtered):,} of {len(data):,} records")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

        st.download_button(
            "Download filtered records",
            filtered.to_csv(index=False).encode("utf-8"),
            "filtered_ticket_records.csv",
            "text/csv",
        )
    else:
        st.info("No ticket records found. Upload a CSV dataset.")


# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------

elif page == "Dashboard":
    st.title("Analytics Dashboard")
    st.caption("A summary of the ticket dataset.")

    if not data.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Tickets", f"{total_tickets:,}")
        c2.metric("Passengers", f"{total_passengers:,}")
        c3.metric("Collected", money(total_collected))
        c4.metric("Uncollected", money(total_uncollected))

        left, right = st.columns(2)

        with left:
            fig = px.bar(
                route_stats.head(10),
                x="route", y="Tickets",
                title="Top 10 Routes",
                color="Tickets",
                color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
            )
            fig.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with right:
            fig = px.pie(
                route_stats.head(8),
                names="route", values="Passengers",
                title="Passenger Share by Route",
                hole=.48,
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.subheader("Route summary")
        st.dataframe(route_stats, use_container_width=True, hide_index=True)
    else:
        st.info("Upload a ticket dataset to view dashboard analytics.")


# ------------------------------------------------------------
# ROUTE ANALYSIS
# ------------------------------------------------------------

elif page == "Route Analysis":
    st.title("Route Analysis")
    st.caption("Compare route-level ticket, passenger and collection performance.")

    if not data.empty:
        metric_choice = st.selectbox(
            "Compare routes by",
            ["Tickets", "Passengers", "Collected", "Uncollected"],
        )
        route_view = route_stats.sort_values(metric_choice, ascending=False)

        fig = px.bar(
            route_view.head(15),
            x=metric_choice, y="route", orientation="h",
            title=f"Routes ranked by {metric_choice}",
            color=metric_choice,
            color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
        )
        st.plotly_chart(style_chart(fig, 480), use_container_width=True)

        st.subheader("Route Performance Score")
        st.caption("A relative comparison score based on tickets, passengers and collected revenue.")
        scored = route_stats.copy()

        def normalise(series):
            maximum = series.max()
            return series / maximum * 100 if maximum else series * 0

        scored["Performance Score"] = (
            normalise(scored["Tickets"]) * .35
            + normalise(scored["Passengers"]) * .35
            + normalise(scored["Collected"]) * .30
        ).round(1)

        scored = scored.sort_values("Performance Score", ascending=False)
        st.dataframe(scored, use_container_width=True, hide_index=True)
    else:
        st.info("Upload a ticket dataset to analyse routes.")


# ------------------------------------------------------------
# REVENUE ANALYSIS
# ------------------------------------------------------------

elif page == "Revenue Analysis":
    st.title("Revenue Analysis")
    st.caption("Review collected and uncollected amounts in the ticket records.")

    if not data.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Collected Amount", money(total_collected))
        c2.metric("Uncollected Amount", money(total_uncollected))
        collection_total = total_collected + total_uncollected
        collection_rate = (
            total_collected / collection_total * 100
            if collection_total else 0
        )
        c3.metric("Collection Rate", f"{collection_rate:.1f}%")

        revenue_fig = px.bar(
            route_stats.sort_values("Collected", ascending=False).head(12),
            x="Collected", y="route", orientation="h",
            title="Collected Revenue by Route",
            color="Collected",
            color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
        )
        st.plotly_chart(style_chart(revenue_fig, 450), use_container_width=True)

        st.subheader("Revenue records")
        st.dataframe(
            route_stats.sort_values("Collected", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Upload a ticket dataset to view revenue analysis.")


# ------------------------------------------------------------
# PASSENGER INSIGHTS
# ------------------------------------------------------------

elif page == "Passenger Insights":
    st.title("Passenger Insights")
    st.caption("Explore passenger movement across recorded routes.")

    if not data.empty:
        passenger_route = route_stats.sort_values("Passengers", ascending=False).iloc[0]
        busiest_route = route_stats.sort_values("Tickets", ascending=False).iloc[0]

        c1, c2 = st.columns(2)
        c1.metric("Highest Passenger Route", passenger_route["route"])
        c2.metric("Most Ticketed Route", busiest_route["route"])

        fig = px.bar(
            route_stats.sort_values("Passengers", ascending=False).head(15),
            x="Passengers", y="route", orientation="h",
            title="Passenger Count by Route",
            color="Passengers",
            color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
        )
        st.plotly_chart(style_chart(fig, 470), use_container_width=True)

        st.subheader("Passenger totals")
        st.dataframe(
            route_stats.sort_values("Passengers", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Upload a ticket dataset to view passenger insights.")


# ------------------------------------------------------------
# DEMAND PREDICTION
# ------------------------------------------------------------

elif page == "Demand Prediction":
    st.title("Demand Prediction")
    st.caption("Historical demand patterns to support planning.")

    if not data.empty:
        parsed_time = pd.to_datetime(
            data["time"].astype(str).str.strip(),
            errors="coerce",
        )
        timed = data.copy()
        timed["Hour"] = parsed_time.dt.hour
        timed = timed.dropna(subset=["Hour"])

        if not timed.empty:
            timed["Hour"] = timed["Hour"].astype(int)
            hourly = (
                timed.groupby("Hour")
                .agg(
                    Tickets=("ticket", "size"),
                    Passengers=("passengers", "sum"),
                )
                .reindex(range(24), fill_value=0)
                .reset_index()
            )

            peak = hourly.loc[hourly["Tickets"].idxmax()]
            st.metric(
                "Busiest Recorded Hour",
                f"{int(peak['Hour']):02d}:00",
                f"{int(peak['Tickets']):,} tickets",
            )

            fig = px.line(
                hourly, x="Hour", y="Tickets",
                markers=True,
                title="Hourly Ticket Activity",
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

            st.subheader("Hourly passenger activity")
            passenger_fig = px.bar(
                hourly, x="Hour", y="Passengers",
                title="Passengers by Hour",
                color="Passengers",
                color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
            )
            st.plotly_chart(style_chart(passenger_fig), use_container_width=True)

            st.info(
                "This page shows historical hourly activity. Reliable future "
                "forecasting requires records from multiple travel dates."
            )
        else:
            st.info("The dataset does not contain readable time values.")
    else:
        st.info("Upload a ticket dataset to analyse demand.")


# ------------------------------------------------------------
# SMART INSIGHTS — SIX EXPANDABLE FEATURES
# ------------------------------------------------------------

elif page == "Smart Insights":
    st.title("Smart Insights")
    st.caption(
        "Six expandable intelligence features based on your recorded ticket data."
    )

    if not data.empty:
        busiest_route = route_stats.sort_values("Tickets", ascending=False).iloc[0]
        passenger_route = route_stats.sort_values("Passengers", ascending=False).iloc[0]
        revenue_route = route_stats.sort_values("Collected", ascending=False).iloc[0]
        lower_activity = route_stats.sort_values("Tickets", ascending=True).head(5)

        # 1. SMART DEMAND RECOMMENDATIONS
        with st.expander("➜ 1. Smart Demand Recommendations", expanded=False):
            st.subheader("High-demand routes")
            st.dataframe(
                route_stats.sort_values("Tickets", ascending=False).head(10),
                use_container_width=True,
                hide_index=True,
            )
            st.success(
                f"{busiest_route['route']} has the highest ticket activity. "
                "Review service frequency and staffing for this route."
            )

        # 2. ROUTE INTELLIGENCE
        with st.expander("➜ 2. Route Intelligence", expanded=False):
            st.subheader("Route performance comparison")

            max_tickets = route_stats["Tickets"].max()
            max_passengers = route_stats["Passengers"].max()
            max_revenue = route_stats["Collected"].max()

            scored = route_stats.copy()
            scored["Performance Score"] = (
                (scored["Tickets"] / max_tickets * 35 if max_tickets else 0)
                + (scored["Passengers"] / max_passengers * 35 if max_passengers else 0)
                + (scored["Collected"] / max_revenue * 30 if max_revenue else 0)
            ).round(1)

            st.dataframe(
                scored.sort_values("Performance Score", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown("**Routes with lower recorded ticket activity**")
            st.dataframe(
                lower_activity,
                use_container_width=True,
                hide_index=True,
            )

        # 3. REVENUE INTELLIGENCE
        with st.expander("➜ 3. Revenue Intelligence", expanded=False):
            st.metric("Total Collected", money(total_collected))
            st.metric("Total Uncollected", money(total_uncollected))

            total_amount = total_collected + total_uncollected
            rate = total_collected / total_amount * 100 if total_amount else 0
            st.metric("Collection Rate", f"{rate:.1f}%")

            revenue_fig = px.bar(
                route_stats.sort_values("Uncollected", ascending=False).head(10),
                x="Uncollected", y="route", orientation="h",
                title="Routes with Highest Recorded Uncollected Amount",
                color_discrete_sequence=[BURGUNDY],
            )
            st.plotly_chart(
                style_chart(revenue_fig, 360),
                use_container_width=True,
            )

            if total_uncollected > 0:
                st.warning(
                    f"{money(total_uncollected)} is recorded as uncollected. "
                    "Reconcile the related tickets and payment records."
                )
            else:
                st.success("No uncollected amount is recorded in this dataset.")

        # 4. PEAK-HOUR INTELLIGENCE & HEATMAP
        with st.expander("➜ 4. Peak-Hour Intelligence & Heatmap", expanded=False):
            parsed_time = pd.to_datetime(
                data["time"].astype(str).str.strip(),
                errors="coerce",
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
                        Passengers=("passengers", "sum"),
                    )
                    .reindex(range(24), fill_value=0)
                    .reset_index()
                )

                peak_row = hourly.loc[hourly["Tickets"].idxmax()]
                peak_hour = int(peak_row["Hour"])
                peak_count = int(peak_row["Tickets"])

                st.metric(
                    "Busiest recorded hour",
                    f"{peak_hour:02d}:00–{(peak_hour + 1) % 24:02d}:00",
                    f"{peak_count:,} tickets",
                )

                hourly_fig = px.bar(
                    hourly, x="Hour", y="Tickets",
                    title="Ticket Activity by Hour",
                    color="Tickets",
                    color_continuous_scale=["#F8E6E5", ROSE, BURGUNDY],
                )
                st.plotly_chart(
                    style_chart(hourly_fig, 350),
                    use_container_width=True,
                )

                heat_source = timed.dropna(subset=["date"]).copy()
                if not heat_source.empty:
                    heat_source["Travel Date"] = heat_source["date"].dt.strftime("%d %b %Y")
                    heat = (
                        heat_source.groupby(["Travel Date", "Hour"])
                        .size()
                        .reset_index(name="Tickets")
                    )
                    pivot = heat.pivot(
                        index="Travel Date",
                        columns="Hour",
                        values="Tickets",
                    ).fillna(0)
                    pivot = pivot.reindex(columns=range(24), fill_value=0)

                    heat_fig = go.Figure(
                        data=go.Heatmap(
                            z=pivot.values,
                            x=[f"{hour:02d}:00" for hour in range(24)],
                            y=pivot.index.tolist(),
                            colorscale=[
                                [0, "#FBECEF"],
                                [0.5, "#DFAAB7"],
                                [1, BURGUNDY],
                            ],
                            colorbar=dict(title="Tickets"),
                        )
                    )
                    heat_fig.update_layout(
                        title="Peak-Hour Heatmap",
                        xaxis_title="Hour of day",
                        yaxis_title="Travel date",
                    )
                    st.plotly_chart(
                        style_chart(heat_fig, 350),
                        use_container_width=True,
                    )

                st.info(
                    f"Planning suggestion: review staffing and timetable "
                    f"coverage around {peak_hour:02d}:00."
                )
            else:
                st.info("Readable time values are needed for peak-hour analysis.")

        # 5. UNUSUAL ACTIVITY DETECTION
        with st.expander("➜ 5. Unusual Activity Detection", expanded=False):
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
                            f"{route_stats.loc[idx, 'route']}: ticket count "
                            f"is unusually {direction} compared with the "
                            "route average. Review the source records."
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

        # 6. MANAGEMENT RECOMMENDATIONS
        with st.expander("➜ 6. Management Recommendations", expanded=False):
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

            if not lower_activity.empty:
                recommendations.append(
                    "Investigate low-activity routes before changing their service allocation."
                )

            for number, recommendation in enumerate(recommendations, start=1):
                st.markdown(
                    f"<div class='card'><h3>Recommendation {number}</h3>"
                    f"<p>{recommendation}</p></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.caption(
            "These insights use transparent statistical rules on historical "
            "ticket records. They are decision-support suggestions, not a "
            "trained AI model or live bus tracking. Reliable daily forecasting "
            "requires records from multiple travel dates."
        )

    else:
        st.info("Upload a valid ticket dataset to activate Intelligent Transport Insights.")


# ------------------------------------------------------------
# REPORTS
# ------------------------------------------------------------

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
                "Distinct Routes",
            ],
            "Value": [
                len(data),
                int(data["passengers"].sum()),
                data["collected"].sum(),
                data["uncollected"].sum(),
                data["route"].nunique(),
            ],
        })

        st.subheader("Dataset summary")
        st.dataframe(summary, use_container_width=True, hide_index=True)

        st.download_button(
            "Download full ticket data (CSV)",
            data.to_csv(index=False).encode("utf-8"),
            "bus_ticket_records.csv",
            "text/csv",
            type="primary",
        )

        st.download_button(
            "Download summary (CSV)",
            summary.to_csv(index=False).encode("utf-8"),
            "bus_analytics_summary.csv",
            "text/csv",
        )

        route_summary = (
            data.groupby("route")
            .agg(
                Tickets=("route", "size"),
                Passengers=("passengers", "sum"),
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum"),
            )
            .reset_index()
        )

        st.download_button(
            "Download route report (CSV)",
            route_summary.to_csv(index=False).encode("utf-8"),
            "route_analysis_report.csv",
            "text/csv",
        )
    else:
        st.info("Upload your ticket CSV to generate reports.")


# ------------------------------------------------------------
# UPLOAD DATASET
# ------------------------------------------------------------

elif page == "Upload Dataset":
    st.title("Upload Dataset")
    st.caption(
        "Upload a CSV containing bus ticket records. Your repository "
        "dataset remains the default source after app restarts."
    )

    uploaded = st.file_uploader("Choose ticket data (CSV)", type=["csv"])

    if uploaded is not None:
        try:
            candidate = pd.read_csv(uploaded)
            checked = prepare_data(candidate)

            st.session_state.uploaded_raw = candidate

            st.success(
                f"Dataset loaded successfully — {len(checked):,} "
                "ticket records detected."
            )
            st.dataframe(
                checked.head(10),
                use_container_width=True,
                hide_index=True,
            )

            if st.button("Use repository dataset instead"):
                st.session_state.uploaded_raw = None
                st.rerun()

        except Exception as exc:
            st.error(f"This CSV could not be used: {exc}")

    elif DATA_FILE.exists():
        st.success("Repository dataset found: data/tickets.csv")
        st.caption(
            "The app will load this dataset automatically when no "
            "temporary upload is active."
        )
    else:
        st.warning(
            "No repository dataset found yet. Upload a CSV or add "
            "data/tickets.csv to your GitHub repository."
        )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown(
    "<hr><div style='text-align:center;color:#987984;font-size:.82rem;"
    "padding:8px 0 2px'>BOOK • ANALYZE • PREDICT &nbsp; | &nbsp; "
    "Created by <b>CRACKER HEADS ♡</b></div>",
    unsafe_allow_html=True,
)

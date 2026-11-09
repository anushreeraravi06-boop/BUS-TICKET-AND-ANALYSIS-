
import os
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# BUS ANALYTICS - CRACKER HEADS
# =========================================================

st.set_page_config(
    page_title="Bus Analytics | Cracker Heads",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- COLOUR THEME -----------------------

BG = "#FFF8F6"
BURGUNDY = "#7B243F"
DARK = "#3E1727"
ROSE = "#C85B70"
PEACH = "#FCE9DC"
PINK = "#FBE8E8"
MUTED = "#806B70"
BORDER = "#F0D9D9"
GREEN = "#27834A"

# -------------------- CUSTOM CSS ------------------------

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
}}

.stApp {{
    background: {BG};
    color: {DARK};
}}

[data-testid="stHeader"] {{
    background: {BG};
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg,#FFF0ED,#F9E4E5);
    border-right: 1px solid {BORDER};
}}

[data-testid="stSidebar"] * {{
    color: {DARK};
}}

.brand-title {{
    color: {BURGUNDY};
    font-size: 25px;
    font-weight: 800;
}}

.brand-sub {{
    color: {MUTED};
    font-size: 12px;
}}

.page-title {{
    color: {BURGUNDY};
    font-size: 30px;
    font-weight: 800;
}}

.section-head {{
    color: {BURGUNDY};
    font-size: 18px;
    font-weight: 800;
    margin-top: 12px;
}}

.metric-card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 17px;
    padding: 16px;
    min-height: 105px;
    box-shadow: 0 3px 12px rgba(103,42,61,0.04);
}}

.metric-label {{
    color: {MUTED};
    font-size: 12px;
    font-weight: 600;
}}

.metric-value {{
    color: {BURGUNDY};
    font-size: 25px;
    font-weight: 800;
    margin-top: 5px;
}}

.metric-note {{
    color: {GREEN};
    font-size: 11px;
}}

.soft-card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 17px;
    padding: 16px;
    margin-bottom: 12px;
}}

div.stButton > button {{
    background: {BURGUNDY};
    color: white;
    border: 0;
    border-radius: 12px;
    font-weight: 700;
}}

div.stButton > button:hover {{
    background: {ROSE};
    color: white;
}}

[data-testid="stMetric"] {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 12px;
}}

footer {{
    visibility: hidden;
}}

#MainMenu {{
    visibility: hidden;
}}
</style>
""", unsafe_allow_html=True)

# -------------------- IMAGE FILES -----------------------

def find_asset(name):
    possible_names = [
        f"assets/{name}.png.jpeg",
        f"assets/{name}.png",
        f"{name}.png.jpeg",
        f"{name}.png"
    ]

    for path in possible_names:
        if os.path.exists(path):
            return path

    return None

def show_asset(name, **kwargs):
    path = find_asset(name)

    if path:
        st.image(path, **kwargs)

# -------------------- DATA PROCESSING --------------------

def find_column(df, choices):
    columns = {str(c).strip().lower(): c for c in df.columns}

    for choice in choices:
        if choice in columns:
            return columns[choice]

    for choice in choices:
        for column in df.columns:
            if choice in str(column).strip().lower():
                return column

    return None

def prepare_data(raw):
    df = raw.copy()
    df.columns = [str(c).strip() for c in df.columns]

    aliases = {
        "date": ["date", "ticket date", "journey date"],
        "from": ["from stop", "from", "source", "origin"],
        "to": ["to stop", "to", "destination"],
        "passengers": ["total psgr", "total passenger", "passengers", "psgr"],
        "amount": ["coll amt", "collection amount", "revenue", "amount", "fare"],
        "uncollected": ["uncoll amt", "uncollected amount"],
        "ticket": ["ticket number", "ticket no", "ticket"]
    }

    cols = {
        key: find_column(df, values)
        for key, values in aliases.items()
    }

    if cols["date"]:
        df["_date"] = pd.to_datetime(
            df[cols["date"]], errors="coerce", dayfirst=True
        )
    else:
        df["_date"] = pd.NaT

    if cols["passengers"]:
        df["_passengers"] = pd.to_numeric(
            df[cols["passengers"]], errors="coerce"
        ).fillna(0)
    else:
        df["_passengers"] = 1

    if cols["amount"]:
        df["_amount"] = pd.to_numeric(
            df[cols["amount"]].astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False),
            errors="coerce"
        ).fillna(0)
    else:
        df["_amount"] = 0.0

    if cols["uncollected"]:
        df["_uncollected"] = pd.to_numeric(
            df[cols["uncollected"]].astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False),
            errors="coerce"
        ).fillna(0)
    else:
        df["_uncollected"] = 0.0

    df["_from"] = (
        df[cols["from"]].astype(str).str.strip()
        if cols["from"] else "Unknown"
    )

    df["_to"] = (
        df[cols["to"]].astype(str).str.strip()
        if cols["to"] else "Unknown"
    )

    df["_route"] = df["_from"] + " – " + df["_to"]

    df["_ticket"] = (
        df[cols["ticket"]].astype(str)
        if cols["ticket"] else df.index.astype(str)
    )

    return df

def demo_data():
    rows = [
        ("2026-10-01", "Ballari", "Hubli", 2, 520),
        ("2026-10-01", "Ballari", "Hyderabad", 3, 900),
        ("2026-10-02", "Mysore", "Bangalore", 2, 460),
        ("2026-10-02", "Bangalore", "Ballari", 1, 350),
        ("2026-10-03", "Hubli", "Bangalore", 2, 620),
        ("2026-10-03", "Ballari", "Hubli", 1, 260),
        ("2026-10-04", "Ballari", "Hyderabad", 2, 600),
        ("2026-10-04", "Mysore", "Bangalore", 3, 690),
        ("2026-10-05", "Bangalore", "Ballari", 2, 700),
        ("2026-10-05", "Hubli", "Bangalore", 1, 310),
        ("2026-10-06", "Ballari", "Hubli", 3, 780),
        ("2026-10-07", "Mysore", "Bangalore", 2, 460)
    ]

    df = pd.DataFrame(
        rows,
        columns=["date", "from", "to", "passengers", "amount"]
    )

    return prepare_data(df)

def money(value):
    return f"₹{value:,.0f}"

# -------------------- SESSION STATE ----------------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None

if "bookings" not in st.session_state:
    st.session_state.bookings = []

# -------------------- LOAD DATA --------------------------

DATA_PATH = "data/tickets.csv"

if st.session_state.uploaded_df is not None:
    data = prepare_data(st.session_state.uploaded_df)
    data_source = "Uploaded dataset"

elif os.path.exists(DATA_PATH):
    try:
        data = prepare_data(pd.read_csv(DATA_PATH))
        data_source = "Repository dataset"
    except Exception:
        data = demo_data()
        data_source = "Sample demonstration data"

else:
    data = demo_data()
    data_source = "Sample demonstration data"

# -------------------- NAVIGATION ------------------------

PAGES = [
    "Home",
    "Book Ticket",
    "Dashboard",
    "Route Analysis",
    "Revenue Analysis",
    "Passenger Insights",
    "Demand Prediction",
    "Smart Insights",
    "Reports",
    "Upload Dataset"
]

# -------------------- SIDEBAR ---------------------------

with st.sidebar:

    show_asset("logo", use_container_width=True)

    if not find_asset("logo"):
        st.markdown(
            '<div class="brand-title">BUS ANALYTICS</div>',
            unsafe_allow_html=True
        )
        st.caption("Intelligent Bus Ticket Data Platform")

    st.markdown("---")

    selected_page = st.radio(
        "NAVIGATION",
        PAGES,
        index=PAGES.index(st.session_state.page),
        key="navigation"
    )

    st.session_state.page = selected_page

    st.markdown("---")
    st.caption("BOOK  •  ANALYZE  •  PREDICT")
    st.caption("Created by CRACKER HEADS ♡")

# -------------------- COMMON STATISTICS -----------------

total_tickets = len(data)
total_passengers = int(data["_passengers"].sum())
total_revenue = float(data["_amount"].sum())
total_uncollected = float(data["_uncollected"].sum())
active_routes = int(data["_route"].nunique())

route_counts = (
    data.groupby("_route").size()
    .sort_values(ascending=False)
)

valid_dates = data.dropna(subset=["_date"])

# -------------------- HOME PAGE -------------------------

if st.session_state.page == "Home":

    show_asset("bus_banner", use_container_width=True)

    if not find_asset("bus_banner"):
        st.markdown("""
        <div style="background:#FBE8E8;padding:30px;border-radius:20px;">
        <h1 style="color:#7B243F;">Welcome to Bus Analytics</h1>
        Intelligent Bus Ticket Data Platform
        </div>
        """, unsafe_allow_html=True)

    if data_source == "Sample demonstration data":
        st.info(
            "Showing sample data for demonstration. "
            "Upload your actual ticket CSV to see real analytics."
        )

    else:
        st.caption(f"Data source: {data_source}")

    st.markdown("### Overview")

    a, b, c, d = st.columns(4)

    metrics = [
        (a, "TOTAL TICKETS", f"{total_tickets:,}", "Ticket records"),
        (b, "TOTAL REVENUE", money(total_revenue), "Collected amount"),
        (c, "TOTAL PASSENGERS", f"{total_passengers:,}", "Passenger count"),
        (d, "ACTIVE ROUTES", f"{active_routes:,}", "Unique routes")
    ]

    for col, label, value, note in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(
            '<div class="section-head">Ticket Bookings Trend</div>',
            unsafe_allow_html=True
        )

        if not valid_dates.empty:
            trend = (
                valid_dates.groupby(valid_dates["_date"].dt.date)
                .size().reset_index(name="Tickets")
            )

            fig = px.line(
                trend, x="_date", y="Tickets",
                markers=True
            ) if "_date" in trend.columns else px.line(trend)

            fig.update_traces(
                line_color=ROSE,
                fill="tozeroy",
                fillcolor="rgba(200,91,112,0.15)"
            )

            fig.update_layout(
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date information is unavailable.")

    with right:
        st.markdown(
            '<div class="section-head">Top Routes by Tickets</div>',
            unsafe_allow_html=True
        )

        top = route_counts.head(5).reset_index()
        top.columns = ["Route", "Tickets"]

        if not top.empty:
            fig = px.bar(
                top.sort_values("Tickets"),
                x="Tickets",
                y="Route",
                orientation="h"
            )

            fig.update_traces(marker_color=ROSE)
            fig.update_layout(
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Explore Bus Analytics")

    c1, c2, c3 = st.columns(3)

    cards = [
        (c1, "Demand Prediction", "Explore historical demand patterns."),
        (c2, "Smart Insights", "View summaries from ticket data."),
        (c3, "Generate Reports", "Download your analysis.")
    ]

    for col, title, description in cards:
        with col:
            st.markdown(
                f'<div class="soft-card"><b>{title}</b><br>{description}</div>',
                unsafe_allow_html=True
            )

            if st.button(f"Open {title}", key=title):
                destination = (
                    "Reports" if title == "Generate Reports" else title
                )
                st.session_state.page = destination
                st.rerun()

# -------------------- BOOK TICKET -----------------------

elif st.session_state.page == "Book Ticket":

    st.markdown('<div class="page-title">Book a Ticket</div>', unsafe_allow_html=True)

    st.warning(
        "This is a demonstration booking form. "
        "It does not reserve real seats or process payments."
    )

    with st.form("booking_form"):

        left, right = st.columns(2)

        with left:
            name = st.text_input("Passenger Name")
            source = st.text_input("From")
            journey_date = st.date_input(
                "Journey Date",
                min_value=date.today()
            )

        with right:
            phone = st.text_input("Phone Number")
            destination = st.text_input("To")
            passengers = st.number_input(
                "Number of Passengers",
                min_value=1,
                max_value=6,
                value=1
            )

        submit = st.form_submit_button("Submit Demo Booking")

    if submit:

        if not name.strip() or not source.strip() or not destination.strip():
            st.error("Please fill in the required details.")

        else:
            booking = {
                "Booking ID": f"DEMO-{len(st.session_state.bookings)+1:04d}",
                "Passenger": name,
                "Phone": phone,
                "From": source,
                "To": destination,
                "Date": str(journey_date),
                "Passengers": passengers,
                "Status": "Demo only"
            }

            st.session_state.bookings.append(booking)

            st.success(f"Demo booking created: {booking['Booking ID']}")
            st.dataframe(
                pd.DataFrame([booking]),
                use_container_width=True
            )

    if st.session_state.bookings:
        st.markdown("### Demo Booking History")
        st.dataframe(
            pd.DataFrame(st.session_state.bookings),
            use_container_width=True
        )

# -------------------- DASHBOARD -------------------------

elif st.session_state.page == "Dashboard":

    st.markdown('<div class="page-title">Analytics Dashboard</div>', unsafe_allow_html=True)

    st.caption(f"Data source: {data_source}")

    a, b, c, d = st.columns(4)

    a.metric("Total Tickets", f"{total_tickets:,}")
    b.metric("Passengers", f"{total_passengers:,}")
    c.metric("Revenue", money(total_revenue))
    d.metric("Uncollected", money(total_uncollected))

    st.markdown("### Ticket Records")
    st.dataframe(data.head(100), use_container_width=True)

# -------------------- ROUTE ANALYSIS --------------------

elif st.session_state.page == "Route Analysis":

    st.markdown('<div class="page-title">Route Analysis</div>', unsafe_allow_html=True)

    summary = data.groupby("_route").agg(
        Tickets=("_ticket", "count"),
        Passengers=("_passengers", "sum"),
        Revenue=("_amount", "sum")
    ).reset_index()

    summary.rename(columns={"_route": "Route"}, inplace=True)

    st.dataframe(summary, use_container_width=True)

    if not summary.empty:
        fig = px.bar(summary, x="Route", y="Tickets", color="Revenue")
        st.plotly_chart(fig, use_container_width=True)

# -------------------- REVENUE ANALYSIS ------------------

elif st.session_state.page == "Revenue Analysis":

    st.markdown('<div class="page-title">Revenue Analysis</div>', unsafe_allow_html=True)

    a, b = st.columns(2)
    a.metric("Collected Revenue", money(total_revenue))
    b.metric("Uncollected Amount", money(total_uncollected))

    summary = (
        data.groupby("_route")["_amount"]
        .sum().reset_index()
    )

    summary.columns = ["Route", "Revenue"]

    fig = px.bar(summary, x="Route", y="Revenue", color="Revenue")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(summary, use_container_width=True)

# -------------------- PASSENGER INSIGHTS ----------------

elif st.session_state.page == "Passenger Insights":

    st.markdown('<div class="page-title">Passenger Insights</div>', unsafe_allow_html=True)

    st.metric("Total Passengers", f"{total_passengers:,}")

    summary = (
        data.groupby("_route")["_passengers"]
        .sum().reset_index()
    )

    summary.columns = ["Route", "Passengers"]

    fig = px.bar(
        summary,
        x="Passengers",
        y="Route",
        orientation="h"
    )

    fig.update_traces(marker_color=ROSE)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(summary, use_container_width=True)

# -------------------- DEMAND PREDICTION -----------------

elif st.session_state.page == "Demand Prediction":

    st.markdown('<div class="page-title">Demand Prediction</div>', unsafe_allow_html=True)

    st.info(
        "This prototype uses a simple historical average. "
        "It is not yet a validated machine-learning forecast."
    )

    if not valid_dates.empty:

        daily = (
            valid_dates.groupby(valid_dates["_date"].dt.date)
            .size().reset_index(name="Tickets")
        )

        daily["7-day Average"] = (
            daily["Tickets"].rolling(7, min_periods=1).mean()
        )

        st.line_chart(
            daily.set_index("_date")[["Tickets", "7-day Average"]]
        )

        estimate = daily["Tickets"].tail(7).mean()

        st.metric("Baseline Daily Estimate", f"{estimate:.1f} tickets")

    else:
        st.warning("A valid date column is required.")

# -------------------- SMART INSIGHTS --------------------

elif st.session_state.page == "Smart Insights":

    st.markdown('<div class="page-title">Smart Insights</div>', unsafe_allow_html=True)

    st.caption("Automatically calculated observations from the dataset.")

    if not route_counts.empty:
        st.success(
            f"Most frequent route: {route_counts.index[0]} "
            f"({route_counts.iloc[0]} ticket records)"
        )

    if total_tickets:
        st.write(
            f"Average passengers per ticket record: "
            f"{total_passengers / total_tickets:.2f}"
        )

        st.write(
            f"Average collected amount per record: "
            f"{money(total_revenue / total_tickets)}"
        )

    st.write(f"Total uncollected amount: {money(total_uncollected)}")

    if data_source == "Sample demonstration data":
        st.warning("These insights currently use sample data.")

# -------------------- REPORTS ---------------------------

elif st.session_state.page == "Reports":

    st.markdown('<div class="page-title">Generate Reports</div>', unsafe_allow_html=True)

    st.download_button(
        "Download Ticket Data CSV",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="bus_analytics_ticket_data.csv",
        mime="text/csv"
    )

    summary = data.groupby("_route").agg(
        Tickets=("_ticket", "count"),
        Passengers=("_passengers", "sum"),
        Revenue=("_amount", "sum"),
        Uncollected=("_uncollected", "sum")
    ).reset_index()

    summary.rename(columns={"_route": "Route"}, inplace=True)

    st.download_button(
        "Download Route Summary CSV",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="bus_analytics_route_summary.csv",
        mime="text/csv"
    )

    st.dataframe(summary, use_container_width=True)

# -------------------- UPLOAD DATASET --------------------

elif st.session_state.page == "Upload Dataset":

    st.markdown('<div class="page-title">Upload Dataset</div>', unsafe_allow_html=True)

    st.info(
        "Upload a CSV file of bus ticket records. "
        "This upload is available for the current app session."
    )

    uploaded = st.file_uploader(
        "Choose your ticket dataset",
        type=["csv"]
    )

    if uploaded is not None:

        try:
            new_df = pd.read_csv(uploaded)

            st.session_state.uploaded_df = new_df

            st.success(
                f"Successfully loaded {len(new_df)} records."
            )

            st.markdown("### Dataset Preview")
            st.dataframe(new_df.head(30), use_container_width=True)

            if st.button("Apply Uploaded Dataset"):
                st.rerun()

        except Exception as error:
            st.error(f"Unable to read file: {error}")

    if st.session_state.uploaded_df is not None:

        if st.button("Clear Uploaded Dataset"):
            st.session_state.uploaded_df = None
            st.rerun()

# -------------------- FOOTER ----------------------------

st.markdown(f"""
<hr style="border-top:1px solid {BORDER};">

<div style="text-align:center;color:{MUTED};padding:15px;">
    Created by
    <b style="color:{BURGUNDY};">CRACKER HEADS ♡</b>
    <br>
    Bus Analytics | Intelligent Bus Ticket Data Platform
</div>
""", unsafe_allow_html=True)

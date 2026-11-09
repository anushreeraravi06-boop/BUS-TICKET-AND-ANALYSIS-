
import os
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# BUS ANALYTICS | CRACKER HEADS
# =========================================================

st.set_page_config(
    page_title="BUS ANALYTICS | CRACKER HEADS",
    page_icon="🚌",
    layout="wide"
)

# -------------------- COLOUR THEME -----------------------

BG = "#FFF8F6"
BURGUNDY = "#76283F"
DARK = "#452333"
ROSE = "#C96F80"
PEACH = "#FBE8DF"
PINK = "#F9E8ED"
GOLD = "#D6A66D"
MUTED = "#806E73"
BORDER = "#F0D9D9"
GREEN = "#31865B"

# -------------------- CUSTOM CSS -------------------------

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
    background: linear-gradient(180deg,#FFF0EC,#F8E3E6);
    border-right: 1px solid {BORDER};
}}

[data-testid="stSidebar"] * {{
    color: {DARK};
}}

.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 1rem;
    max-width: 1600px;
}}

.brand-title {{
    color: {BURGUNDY};
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 1px;
}}

.page-title {{
    color: {BURGUNDY};
    font-size: 30px;
    font-weight: 800;
}}

.section-title {{
    color: {BURGUNDY};
    font-size: 18px;
    font-weight: 800;
    margin-top: 15px;
    margin-bottom: 10px;
}}

.metric-card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 16px;
    min-height: 105px;
    box-shadow: 0 3px 12px rgba(103,42,61,.04);
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
    margin-top: 6px;
}}

.metric-note {{
    color: {GREEN};
    font-size: 11px;
    margin-top: 3px;
}}

.feature-card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 17px;
    min-height: 115px;
}}

div.stButton > button {{
    background: {BURGUNDY};
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}}

div.stButton > button:hover {{
    background: {ROSE};
    color: white;
}}

[data-testid="stMetric"] {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 13px;
    padding: 12px;
}}

footer {{
    visibility: hidden;
}}

#MainMenu {{
    visibility: hidden;
}}

@media (max-width: 900px) {{
    .page-title {{
        font-size: 24px;
    }}
    .metric-value {{
        font-size: 20px;
    }}
    .block-container {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}
}}
</style>
""", unsafe_allow_html=True)

# -------------------- IMAGE HELPERS ----------------------

def find_image(name):
    possible = [
        f"{name}.png.jpeg",
        f"{name}.png",
        f"assets/{name}.png.jpeg",
        f"assets/{name}.png"
    ]

    for path in possible:
        if os.path.exists(path):
            return path

    return None

def show_image(name, **kwargs):
    path = find_image(name)
    if path:
        st.image(path, **kwargs)

# -------------------- DATA PROCESSING --------------------

def find_column(df, names):
    columns = {
        str(c).strip().lower(): c
        for c in df.columns
    }

    for name in names:
        if name.lower() in columns:
            return columns[name.lower()]

    for name in names:
        for column in df.columns:
            if name.lower() in str(column).strip().lower():
                return column

    return None

def prepare_data(raw):
    df = raw.copy()
    df.columns = [str(c).strip() for c in df.columns]

    aliases = {
        "date": ["date", "ticket date", "journey date"],
        "time": ["time", "ticket time"],
        "from": ["from stop", "from", "source", "origin"],
        "to": ["to stop", "to", "destination"],
        "passengers": [
            "total psgr", "total passenger",
            "passengers", "psgr"
        ],
        "amount": [
            "coll amt", "collection amount",
            "collected amount", "revenue"
        ],
        "uncollected": [
            "uncoll amt", "uncollected amount"
        ],
        "ticket": ["ticket number", "ticket no"],
        "waybill": ["waybill number", "waybill no"]
    }

    cols = {
        key: find_column(df, values)
        for key, values in aliases.items()
    }

    if cols["date"]:
        df["_date"] = pd.to_datetime(
            df[cols["date"]],
            errors="coerce",
            dayfirst=True
        )
    else:
        df["_date"] = pd.NaT

    def numeric_column(column):
        if not column:
            return pd.Series(0.0, index=df.index)

        cleaned = (
            df[column].astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.strip()
        )

        return pd.to_numeric(
            cleaned, errors="coerce"
        ).fillna(0)

    df["_passengers"] = (
        numeric_column(cols["passengers"])
        if cols["passengers"] else 1
    )

    df["_amount"] = numeric_column(cols["amount"])
    df["_uncollected"] = numeric_column(cols["uncollected"])

    df["_from"] = (
        df[cols["from"]].fillna("Unknown").astype(str).str.strip()
        if cols["from"] else "Unknown"
    )

    df["_to"] = (
        df[cols["to"]].fillna("Unknown").astype(str).str.strip()
        if cols["to"] else "Unknown"
    )

    df["_route"] = df["_from"] + " – " + df["_to"]

    df["_ticket"] = (
        df[cols["ticket"]].astype(str)
        if cols["ticket"] else df.index.astype(str)
    )

    df["_waybill"] = (
        df[cols["waybill"]].astype(str)
        if cols["waybill"] else "Not available"
    )

    df["_time"] = (
        df[cols["time"]].astype(str)
        if cols["time"] else "Not available"
    )

    return df

def money(value):
    return f"₹{value:,.0f}"

# -------------------- SESSION STATE ----------------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# -------------------- LOAD ACTUAL DATA -------------------

DATA_PATH = "data/tickets.csv"

if st.session_state.uploaded_data is not None:
    data = prepare_data(st.session_state.uploaded_data)
    data_source = "Uploaded dataset"

elif os.path.exists(DATA_PATH):
    try:
        data = prepare_data(pd.read_csv(DATA_PATH))
        data_source = "Repository ticket dataset"
    except Exception as error:
        st.error(f"Could not read ticket dataset: {error}")
        data = pd.DataFrame()
        data_source = "Dataset error"

else:
    data = pd.DataFrame()
    data_source = "Dataset not found"

# -------------------- NAVIGATION -------------------------

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
    "Upload Dataset"
]

# -------------------- SIDEBAR ----------------------------

with st.sidebar:

    show_image("logo", use_container_width=True)

    if not find_image("logo"):
        st.markdown(
            '<div class="brand-title">BUS ANALYTICS</div>',
            unsafe_allow_html=True
        )
        st.caption("Intelligent Bus Ticket Data Platform")

    st.markdown("---")

    selected = st.radio(
        "NAVIGATION",
        PAGES,
        index=PAGES.index(st.session_state.page),
        key="navigation"
    )

    st.session_state.page = selected

    st.markdown("---")
    st.caption("BOOK • ANALYZE • PREDICT")
    st.caption("Created by CRACKER HEADS ♡")

# -------------------- COMMON STATISTICS -----------------

total_tickets = len(data)

if not data.empty:
    total_passengers = int(data["_passengers"].sum())
    total_revenue = float(data["_amount"].sum())
    total_uncollected = float(data["_uncollected"].sum())
    active_routes = int(data["_route"].nunique())
else:
    total_passengers = 0
    total_revenue = 0
    total_uncollected = 0
    active_routes = 0

# -------------------- HOME PAGE -------------------------

if st.session_state.page == "Home":

    show_image("bus_banner", use_container_width=True)

    if not find_image("bus_banner"):
        st.markdown(f"""
        <div class="feature-card">
            <h1 style="color:{BURGUNDY};">Welcome to Bus Analytics</h1>
            Intelligent Bus Ticket Data Platform
        </div>
        """, unsafe_allow_html=True)

    st.caption(f"Data source: {data_source}")

    if data.empty:
        st.warning("No ticket records loaded. Check data/tickets.csv.")

    st.markdown(
        '<div class="section-title">Overview</div>',
        unsafe_allow_html=True
    )

    columns = st.columns(4)

    metrics = [
        ("TOTAL TICKETS", f"{total_tickets:,}", "Ticket records"),
        ("TOTAL REVENUE", money(total_revenue), "Collected amount"),
        ("TOTAL PASSENGERS", f"{total_passengers:,}", "Passenger count"),
        ("ACTIVE ROUTES", f"{active_routes:,}", "Unique routes")
    ]

    for col, item in zip(columns, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{item[0]}</div>
                <div class="metric-value">{item[1]}</div>
                <div class="metric-note">{item[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(
            '<div class="section-title">Ticket Bookings Trend</div>',
            unsafe_allow_html=True
        )

        if not data.empty and data["_date"].notna().any():

            dated = data.dropna(subset=["_date"])

            trend = (
                dated.groupby(dated["_date"].dt.date)
                .size()
                .reset_index(name="Tickets")
            )

            trend.columns = ["Date", "Tickets"]

            fig = px.line(
                trend,
                x="Date",
                y="Tickets",
                markers=True
            )

            fig.update_traces(
                line_color=ROSE,
                fill="tozeroy",
                fillcolor="rgba(201,111,128,0.13)"
            )

            fig.update_layout(
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Date information is not available.")

    with right:
        st.markdown(
            '<div class="section-title">Top Routes by Tickets</div>',
            unsafe_allow_html=True
        )

        if not data.empty:
            top = data["_route"].value_counts().head(5)
            route_df = top.reset_index()
            route_df.columns = ["Route", "Tickets"]

            fig = px.bar(
                route_df.sort_values("Tickets"),
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
        else:
            st.info("Route information is not available.")

    st.markdown("### Explore Analytics")

    c1, c2, c3 = st.columns(3)

    features = [
        (c1, "Demand Prediction", "Explore historical demand patterns."),
        (c2, "Smart Insights", "Understand ticket data observations."),
        (c3, "Generate Reports", "Download your analysis.")
    ]

    for col, title, description in features:
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <b style="color:{BURGUNDY};">{title}</b><br>
                {description}
            </div>
            """, unsafe_allow_html=True)

            if st.button("Explore", key=f"home_{title}"):
                destination = (
                    "Reports"
                    if title == "Generate Reports"
                    else title
                )
                st.session_state.page = destination
                st.rerun()

# -------------------- TICKET RECORDS --------------------

elif st.session_state.page == "Ticket Records":

    st.markdown(
        '<div class="page-title">Ticket Records</div>',
        unsafe_allow_html=True
    )

    st.caption("Search and inspect historical bus ticket records.")

    if data.empty:
        st.warning("No ticket records available.")
    else:
        search = st.text_input(
            "Search by ticket number, waybill, stop or route"
        )

        filtered = data.copy()

        if search:
            searchable = (
                filtered.astype(str)
                .agg(" ".join, axis=1)
                .str.contains(search, case=False, na=False)
            )
            filtered = filtered[searchable]

        st.write(f"Records found: {len(filtered):,}")

        display_columns = [
            c for c in [
                "_waybill", "_ticket", "_from", "_to",
                "_date", "_time", "_passengers",
                "_amount", "_uncollected"
            ] if c in filtered.columns
        ]

        display = filtered[display_columns].rename(columns={
            "_waybill": "Waybill Number",
            "_ticket": "Ticket Number",
            "_from": "From Stop",
            "_to": "To Stop",
            "_date": "Date",
            "_time": "Time",
            "_passengers": "Passengers",
            "_amount": "Collected Amount",
            "_uncollected": "Uncollected Amount"
        })

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download filtered records",
            data=display.to_csv(index=False).encode("utf-8"),
            file_name="filtered_ticket_records.csv",
            mime="text/csv"
        )

# -------------------- DASHBOARD -------------------------

elif st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="page-title">Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.caption(f"Data source: {data_source}")

    a, b, c, d = st.columns(4)

    a.metric("Total Tickets", f"{total_tickets:,}")
    b.metric("Passengers", f"{total_passengers:,}")
    c.metric("Collected Revenue", money(total_revenue))
    d.metric("Uncollected Amount", money(total_uncollected))

    if not data.empty:
        st.markdown("### Ticket Records Preview")
        st.dataframe(data.head(100), use_container_width=True)

# -------------------- ROUTE ANALYSIS --------------------

elif st.session_state.page == "Route Analysis":

    st.markdown(
        '<div class="page-title">Route Analysis</div>',
        unsafe_allow_html=True
    )

    if data.empty:
        st.warning("No route data available.")
    else:
        summary = data.groupby("_route").agg(
            Tickets=("_ticket", "count"),
            Passengers=("_passengers", "sum"),
            Revenue=("_amount", "sum")
        ).reset_index()

        summary.rename(
            columns={"_route": "Route"},
            inplace=True
        )

        summary = summary.sort_values(
            "Tickets", ascending=False
        )

        st.dataframe(summary, use_container_width=True)

        fig = px.bar(
            summary.head(10),
            x="Route",
            y="Tickets",
            color="Revenue"
        )

        fig.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------- REVENUE ANALYSIS ------------------

elif st.session_state.page == "Revenue Analysis":

    st.markdown(
        '<div class="page-title">Revenue Analysis</div>',
        unsafe_allow_html=True
    )

    a, b = st.columns(2)

    a.metric("Collected Revenue", money(total_revenue))
    b.metric("Uncollected Amount", money(total_uncollected))

    if not data.empty:
        summary = (
            data.groupby("_route")["_amount"]
            .sum()
            .reset_index()
        )

        summary.columns = ["Route", "Revenue"]
        summary = summary.sort_values(
            "Revenue", ascending=False
        )

        fig = px.bar(
            summary.head(10),
            x="Route",
            y="Revenue",
            color="Revenue"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(summary, use_container_width=True)

# -------------------- PASSENGER INSIGHTS ----------------

elif st.session_state.page == "Passenger Insights":

    st.markdown(
        '<div class="page-title">Passenger Insights</div>',
        unsafe_allow_html=True
    )

    st.metric("Total Passengers", f"{total_passengers:,}")

    if not data.empty:
        summary = (
            data.groupby("_route")["_passengers"]
            .sum()
            .reset_index()
        )

        summary.columns = ["Route", "Passengers"]

        summary = summary.sort_values(
            "Passengers", ascending=False
        )

        fig = px.bar(
            summary.head(10),
            x="Passengers",
            y="Route",
            orientation="h"
        )

        fig.update_traces(marker_color=ROSE)

        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(summary, use_container_width=True)

# -------------------- DEMAND PREDICTION -----------------

elif st.session_state.page == "Demand Prediction":

    st.markdown(
        '<div class="page-title">Demand Prediction</div>',
        unsafe_allow_html=True
    )

    st.info(
        "This prototype uses historical ticket counts "
        "to calculate a baseline estimate. It is not yet "
        "a validated machine-learning forecast."
    )

    if not data.empty and data["_date"].notna().any():

        dated = data.dropna(subset=["_date"])

        daily = (
            dated.groupby(dated["_date"].dt.date)
            .size()
            .reset_index(name="Tickets")
        )

        daily["7-Day Average"] = (
            daily["Tickets"].rolling(7, min_periods=1).mean()
        )

        daily.columns = [
            "Date", "Tickets", "7-Day Average"
        ]

        st.line_chart(
            daily.set_index("Date")
        )

        estimate = daily["Tickets"].tail(7).mean()

        st.metric(
            "Baseline Daily Estimate",
            f"{estimate:.1f} tickets"
        )

    else:
        st.warning("Valid ticket dates are required.")

# -------------------- SMART INSIGHTS --------------------

elif st.session_state.page == "Smart Insights":

    st.markdown(
        '<div class="page-title">Smart Insights</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Automatically calculated observations from ticket records."
    )

    if not data.empty:

        routes = data["_route"].value_counts()

        if not routes.empty:
            st.success(
                f"Most frequent route: {routes.index[0]} "
                f"with {routes.iloc[0]:,} ticket records."
            )

        st.write(
            f"Average passengers per record: "
            f"{total_passengers / total_tickets:.2f}"
        )

        st.write(
            f"Average collected amount per record: "
            f"{money(total_revenue / total_tickets)}"
        )

        st.write(
            f"Total uncollected amount: "
            f"{money(total_uncollected)}"
        )

        st.write(
            f"Number of unique routes: {active_routes}"
        )

    else:
        st.warning("No dataset available.")

# -------------------- REPORTS ---------------------------

elif st.session_state.page == "Reports":

    st.markdown(
        '<div class="page-title">Generate Reports</div>',
        unsafe_allow_html=True
    )

    if not data.empty:

        st.download_button(
            "Download Ticket Records CSV",
            data=data.to_csv(index=False).encode("utf-8"),
            file_name="bus_analytics_ticket_records.csv",
            mime="text/csv"
        )

        summary = data.groupby("_route").agg(
            Tickets=("_ticket", "count"),
            Passengers=("_passengers", "sum"),
            Revenue=("_amount", "sum"),
            Uncollected=("_uncollected", "sum")
        ).reset_index()

        summary.rename(
            columns={"_route": "Route"},
            inplace=True
        )

        st.download_button(
            "Download Route Summary CSV",
            data=summary.to_csv(index=False).encode("utf-8"),
            file_name="bus_analytics_route_summary.csv",
            mime="text/csv"
        )

        st.dataframe(summary, use_container_width=True)

    else:
        st.warning("No data available for reports.")

# -------------------- UPLOAD DATASET --------------------

elif st.session_state.page == "Upload Dataset":

    st.markdown(
        '<div class="page-title">Upload Dataset</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload a CSV file containing historical bus ticket records."
    )

    st.info(
        "Session uploads are temporary. For permanent cloud data, "
        "add the CSV to the repository at data/tickets.csv."
    )

    uploaded = st.file_uploader(
        "Choose your ticket dataset",
        type=["csv"]
    )

    if uploaded is not None:

        try:
            new_data = pd.read_csv(uploaded)

            st.session_state.uploaded_data = new_data

            st.success(
                f"Loaded {len(new_data):,} rows "
                f"and {len(new_data.columns)} columns."
            )

            st.markdown("### Dataset Preview")

            st.dataframe(
                new_data.head(30),
                use_container_width=True
            )

            if st.button("Apply Uploaded Dataset"):
                st.rerun()

        except Exception as error:
            st.error(f"Could not read CSV: {error}")

    if st.session_state.uploaded_data is not None:

        if st.button("Clear Uploaded Dataset"):
            st.session_state.uploaded_data = None
            st.rerun()

# -------------------- FOOTER ----------------------------

st.markdown(f"""
<hr style="border:0;border-top:1px solid {BORDER};margin-top:30px;">

<div style="text-align:center;color:{MUTED};padding:15px;font-size:12px;">
    Created by
    <b style="color:{BURGUNDY};letter-spacing:1px;">
        CRACKER HEADS ♡
    </b>
    <br>
    BUS ANALYTICS | Intelligent Bus Ticket Data Platform
</div>
""", unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import plotly.express as px
import time
from pathlib import Path

# ==========================================
# BUS ANALYTICS - CRACKER HEADS
# ==========================================

st.set_page_config(
    page_title="Bus Analytics | CRACKER HEADS",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- FILE PATHS ----------
ASSETS = Path("assets")
DATA = Path("data/tickets.csv")

# ---------- COLOUR THEME ----------
PLUM = "#2B1028"
DARK_PLUM = "#35152F"
ROSE = "#F18E83"
PEACH = "#F6B99F"
GOLD = "#F3D49B"
IVORY = "#FFF8F2"
INK = "#30202D"
MUTED = "#81717B"

# ---------- CSS DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #FFF8F2;
    color: #30202D;
}

[data-testid="stHeader"] {
    background: #FFF8F2;
}

[data-testid="stSidebar"] {
    background: #2B1028;
}

.block-container {
    padding: 1.2rem 1.5rem 2rem;
    max-width: 100%;
}

.brand-panel {
    background: linear-gradient(180deg,#38142F,#6D354E,#2B1028);
    border-radius: 18px;
    padding: 8px;
    overflow: hidden;
}

.nav-panel {
    background: #2B1028;
    border-radius: 18px;
    padding: 16px 10px;
    min-height: 650px;
}

.nav-title {
    color: #F3D49B;
    font-size: 19px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 22px;
}

.hero-title {
    color: #FFF8F2;
    font-size: 32px;
    font-weight: 800;
}

.metric-card {
    background: linear-gradient(135deg,#FFFFFF,#FCE8E6);
    border: 1px solid #F0D6D4;
    border-radius: 17px;
    padding: 17px;
    min-height: 105px;
    box-shadow: 0 5px 16px #4B20300C;
}

.metric-label {
    color: #796875;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #35152F;
    font-size: 25px;
    font-weight: 800;
}

.metric-note {
    color: #25834C;
    font-size: 12px;
    font-weight: 700;
}

.feature-card {
    background: #FFFFFF;
    border: 1px solid #EEDBD9;
    border-radius: 16px;
    padding: 16px;
    min-height: 115px;
}

.feature-card h4 {
    color: #35152F;
    margin: 0 0 8px;
}

.feature-card p {
    color: #81717B;
    font-size: 13px;
}

.section-heading {
    color: #35152F;
    font-size: 19px;
    font-weight: 800;
    margin-top: 15px;
}

.footer {
    background: #2B1028;
    color: #F3D49B;
    text-align: center;
    border-radius: 12px;
    padding: 16px;
    margin-top: 25px;
    letter-spacing: 2px;
}

.stButton button {
    background: linear-gradient(90deg,#F18E83,#F6B99F);
    color: #35152F;
    border: none;
    border-radius: 30px;
    font-weight: 800;
}

.stButton button:hover {
    color: #35152F;
    border: 1px solid #F3D49B;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
}

@media(max-width: 760px) {
    .block-container {
        padding: 0.5rem;
    }
    .hero-title {
        font-size: 23px;
    }
    .metric-value {
        font-size: 19px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
def load_data():
    if DATA.exists():
        try:
            data = pd.read_csv(DATA)
            if not data.empty:
                return data, True
        except Exception:
            pass

    # Clearly labelled prototype data
    return pd.DataFrame({
        "From Stop": [
            "Ballari", "Ballari", "Ballari", "Bangalore",
            "Bangalore", "Hubli", "Mysore"
        ],
        "To Stop": [
            "Hubli", "Hyderabad", "Hospet", "Ballari",
            "Mysore", "Bangalore", "Bangalore"
        ],
        "Date": pd.date_range("2026-10-01", periods=7),
        "Time": ["06:30", "08:15", "10:00", "12:30",
                 "14:00", "17:15", "19:30"],
        "Total Psgr": [373, 368, 323, 386, 319, 352, 373],
        "Coll Amt": [108090, 108925, 112715, 133456,
                     112715, 116227, 132577],
        "Uncoll Amt": [0, 500, 0, 250, 0, 100, 0]
    }), False

df, real_data = load_data()

# ---------- COLUMN DETECTION ----------
def find_column(possible_names):
    for col in df.columns:
        for name in possible_names:
            if name.lower() in str(col).lower():
                return col
    return None

date_col = find_column(["date"])
from_col = find_column(["from stop", "from"])
to_col = find_column(["to stop", "destination"])
passenger_col = find_column(["total psgr", "passenger"])
revenue_col = find_column(["coll amt", "collected amount", "revenue"])
uncollected_col = find_column(["uncoll amt", "uncollected"])

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)

for col in [passenger_col, revenue_col, uncollected_col]:
    if col:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

def total(col):
    return float(df[col].sum()) if col else 0

def currency(value):
    return f"₹{value:,.0f}"

if from_col and to_col:
    df["_Route"] = (
        df[from_col].astype(str) + " – " + df[to_col].astype(str)
    )
else:
    df["_Route"] = "Route information unavailable"

# ---------- TWO-SECOND INTRO ----------
if "intro_done" not in st.session_state:
    st.session_state.intro_done = False

if not st.session_state.intro_done:
    logo_path = ASSETS / "logo.png"

    st.markdown(
        f"""
        <div style="
        background:linear-gradient(135deg,#2B1028,#65304C);
        border-radius:22px;
        padding:35px;
        text-align:center;
        color:#F3D49B;">
        <h1>🚌 BUS ANALYTICS</h1>
        <p>Intelligent Bus Ticket Data Platform</p>
        <h3>CRACKER HEADS</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    if logo_path.exists():
        st.image(str(logo_path), width=220)

    time.sleep(2)
    st.session_state.intro_done = True
    st.rerun()

# ---------- MAIN PAGE LAYOUT ----------
brand_col, nav_col, main_col = st.columns(
    [0.90, 0.85, 3.5],
    gap="small"
)

# ---------- LEFT BRANDING PANEL ----------
with brand_col:
    panel = ASSETS / "brand_panel.png"

    if panel.exists():
        st.image(str(panel), use_container_width=True)
    else:
        st.markdown("""
        <div class="brand-panel">
        <h1 style="color:#F3D49B;text-align:center">
        🚌 BUS ANALYTICS
        </h1>
        <p style="color:white;text-align:center">
        Intelligent Bus Ticket Data Platform
        </p>
        <hr>
        <p style="color:#F3D49B;text-align:center">
        BOOK • ANALYZE • PREDICT
        </p>
        <br><br>
        <p style="color:white;text-align:center">
        Created by<br><b>CRACKER HEADS</b>
        </p>
        </div>
        """, unsafe_allow_html=True)

# ---------- NAVIGATION ----------
with nav_col:
    st.markdown(
        '<div class="nav-title">🚌 BUS ANALYTICS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="color:#F3D49B;text-align:center">'
        'NAVIGATION</p>',
        unsafe_allow_html=True
    )

    pages = [
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

    page = st.radio(
        "Choose a section",
        pages,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        '<p style="color:#F3D49B;text-align:center">'
        'Created by<br><b>CRACKER HEADS ♡</b></p>',
        unsafe_allow_html=True
    )

# ---------- CHART FUNCTIONS ----------
def make_route_chart():
    routes = (
        df.groupby("_Route")
        .size()
        .reset_index(name="Tickets")
        .sort_values("Tickets", ascending=False)
        .head(5)
    )

    fig = px.bar(
        routes,
        x="Tickets",
        y="_Route",
        orientation="h",
        text="Tickets",
        color_discrete_sequence=["#A83270"]
    )

    fig.update_layout(
        height=300,
        margin=dict(l=5,r=20,t=10,b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#35152F",
        yaxis_title="",
        xaxis_title=""
    )
    return fig

def make_trend_chart():
    if date_col and df[date_col].notna().any():
        trend = (
            df.dropna(subset=[date_col])
            .groupby(df[date_col].dt.date)
            .size()
            .reset_index(name="Tickets")
        )
        trend.columns = ["Date", "Tickets"]
        trend = trend.sort_values("Date")
        x_col = "Date"
    else:
        trend = df.groupby("_Route").size().reset_index(name="Tickets")
        x_col = "_Route"

    fig = px.line(
        trend,
        x=x_col,
        y="Tickets",
        markers=True
    )

    fig.update_traces(
        line_color="#A83270",
        marker_color="#A83270",
        fill="tozeroy",
        fillcolor="rgba(241,142,131,0.18)"
    )

    fig.update_layout(
        height=300,
        margin=dict(l=5,r=5,t=10,b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#35152F",
        xaxis_title="",
        yaxis_title=""
    )
    return fig

# ---------- MAIN CONTENT ----------
with main_col:

    # Header
    h1, h2, h3 = st.columns([3, 1, 0.5])

    with h1:
        st.markdown(
            '<h3 style="color:#35152F">🚌 Bus Analytics</h3>',
            unsafe_allow_html=True
        )

    with h2:
        st.text_input(
            "Search",
            placeholder="Search route, ticket or bus...",
            label_visibility="collapsed"
        )

    with h3:
        st.markdown("🔔　👤")

    st.markdown("---")

    # ---------- HOME ----------
    if page == "Home":

        banner = ASSETS / "bus_banner.png"

        if banner.exists():
            st.image(str(banner), use_container_width=True)
        else:
            st.markdown("""
            <div style="
            background:linear-gradient(100deg,#2B1028,#8D4962);
            padding:30px;
            border-radius:18px;
            color:white;">
            <h1>Welcome to Bus Analytics</h1>
            <p>A Smart Transportation Analytics Platform</p>
            <p>To Monitor, Analyze and Optimize Bus Operations.</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🚌 Book a Ticket"):
            st.session_state.page = "Book Ticket"
            st.rerun()

        # Four statistics
        tickets = len(df)
        revenue = total(revenue_col)
        passengers = total(passenger_col)
        routes = df["_Route"].nunique()

        st.markdown(
            '<p class="section-heading">Platform Overview</p>',
            unsafe_allow_html=True
        )

        m1, m2, m3, m4 = st.columns(4)

        metrics = [
            (m1, "🎟️ Total Tickets", f"{tickets:,}"),
            (m2, "🪙 Total Revenue", currency(revenue)),
            (m3, "👥 Total Passengers", f"{passengers:,.0f}"),
            (m4, "⌁ Active Routes", f"{routes:,}")
        ]

        for col, label, value in metrics:
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">From current dataset</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Charts
        st.markdown(
            '<p class="section-heading">Analytics Overview</p>',
            unsafe_allow_html=True
        )

        chart1, chart2 = st.columns(2)

        with chart1:
            st.markdown("### 📈 Ticket Bookings Trend")
            st.plotly_chart(
                make_trend_chart(),
                use_container_width=True
            )

        with chart2:
            st.markdown("### 📊 Top Routes by Tickets")
            st.plotly_chart(
                make_route_chart(),
                use_container_width=True
            )

        # Feature cards
        st.markdown(
            '<p class="section-heading">Explore Smart Features</p>',
            unsafe_allow_html=True
        )

        f1, f2, f3 = st.columns(3)

        with f1:
            st.markdown("""
            <div class="feature-card">
            <h4>📈 Demand Prediction</h4>
            <p>Forecast future ticket demand for each route.</p>
            </div>
            """, unsafe_allow_html=True)

        with f2:
            st.markdown("""
            <div class="feature-card">
            <h4>💡 Smart Insights ✨</h4>
            <p>Data-driven suggestions for better operations.</p>
            </div>
            """, unsafe_allow_html=True)

        with f3:
            st.markdown("""
            <div class="feature-card">
            <h4>📄 Generate Reports</h4>
            <p>Download analytics reports in CSV format.</p>
            </div>
            """, unsafe_allow_html=True)

        if real_data:
            st.success("Real uploaded dataset is active.")
        else:
            st.info(
                "Prototype mode: demonstration data is currently "
                "displayed. Real ticket data will be connected next."
            )

    # ---------- BOOK TICKET ----------
    elif page == "Book Ticket":

        st.title("🎟️ Book Your Bus Ticket")
        st.write("Enter your journey details.")

        c1, c2 = st.columns(2)

        with c1:
            origin = st.text_input("From")
            journey_date = st.date_input("Journey Date")

        with c2:
            destination = st.text_input("To")
            passengers = st.number_input(
                "Number of Passengers",
                min_value=1,
                max_value=10,
                value=1
            )

        name = st.text_input("Passenger Name")

        if st.button("Check Booking Details"):
            if not origin or not destination or not name:
                st.error("Please fill in all details.")
            elif origin.lower() == destination.lower():
                st.error("From and To locations must be different.")
            else:
                st.success("Booking demonstration completed!")
                st.write({
                    "Passenger": name,
                    "From": origin,
                    "To": destination,
                    "Date": str(journey_date),
                    "Passengers": passengers
                })

        st.caption(
            "Prototype only: no real seat reservation or payment is "
            "processed."
        )

    # ---------- DASHBOARD ----------
    elif page == "Dashboard":

        st.title("📊 Analytics Dashboard")

        a, b = st.columns(2)

        with a:
            st.plotly_chart(
                make_trend_chart(),
                use_container_width=True
            )

        with b:
            st.plotly_chart(
                make_route_chart(),
                use_container_width=True
            )

        st.subheader("Ticket Records")
        st.dataframe(df, use_container_width=True)

    # ---------- ROUTE ANALYSIS ----------
    elif page == "Route Analysis":

        st.title("🛣️ Route Analysis")

        st.plotly_chart(
            make_route_chart(),
            use_container_width=True
        )

        st.dataframe(
            df.groupby("_Route").size()
            .reset_index(name="Total Tickets")
            .sort_values("Total Tickets", ascending=False),
            use_container_width=True
        )

    # ---------- REVENUE ----------
    elif page == "Revenue Analysis":

        st.title("💰 Revenue Intelligence")

        a, b = st.columns(2)

        with a:
            st.metric(
                "Collected Revenue",
                currency(total(revenue_col))
            )

        with b:
            st.metric(
                "Uncollected Amount",
                currency(total(uncollected_col))
            )

        if revenue_col:
            st.plotly_chart(
                px.histogram(
                    df,
                    x=revenue_col,
                    color_discrete_sequence=["#A83270"]
                ),
                use_container_width=True
            )

    # ---------- PASSENGERS ----------
    elif page == "Passenger Insights":

        st.title("👥 Passenger Insights")

        if passenger_col and from_col:
            passenger_data = (
                df.groupby(from_col)[passenger_col]
                .sum()
                .reset_index()
            )

            st.plotly_chart(
                px.bar(
                    passenger_data,
                    x=from_col,
                    y=passenger_col,
                    color_discrete_sequence=["#B34B78"]
                ),
                use_container_width=True
            )

        else:
            st.warning("Passenger or boarding-stop data is unavailable.")

    # ---------- DEMAND PREDICTION ----------
    elif page == "Demand Prediction":

        st.title("📈 Demand Prediction")

        st.info(
            "Prototype forecast: average historical ticket records "
            "over the latest seven available dates."
        )

        if date_col and df[date_col].notna().any():
            daily = (
                df.dropna(subset=[date_col])
                .groupby(df[date_col].dt.date)
                .size()
            )

            if len(daily) >= 2:
                average = daily.tail(7).mean()
                st.metric(
                    "Estimated daily ticket records",
                    f"{average:.1f}"
                )
                st.caption(
                    "This is a simple baseline, not a validated AI forecast."
                )
            else:
                st.warning("More dates are needed for a forecast.")
        else:
            st.warning("Date information is required.")

    # ---------- SMART INSIGHTS ----------
    elif page == "Smart Insights":

        st.title("✨ Smart Insights")

        counts = df["_Route"].value_counts()

        if not counts.empty:
            st.success(
                f"Most frequent route: {counts.index[0]} "
                f"({counts.iloc[0]} ticket records)."
            )

        if from_col:
            top_stop = df[from_col].value_counts()

            if not top_stop.empty:
                st.info(
                    f"Most frequent boarding stop: "
                    f"{top_stop.index[0]}."
                )

        st.caption(
            "These are descriptive data observations, not "
            "automated operational recommendations."
        )

    # ---------- REPORTS ----------
    elif page == "Reports":

        st.title("📄 Reports & Downloads")

        st.download_button(
            "Download Ticket Data",
            df.to_csv(index=False).encode("utf-8"),
            "bus_ticket_data.csv",
            "text/csv"
        )

        route_report = (
            df.groupby("_Route")
            .size()
            .reset_index(name="Tickets")
        )

        st.download_button(
            "Download Route Report",
            route_report.to_csv(index=False).encode("utf-8"),
            "route_report.csv",
            "text/csv"
        )

        st.dataframe(route_report, use_container_width=True)

    # ---------- UPLOAD DATASET ----------
    elif page == "Upload Dataset":

        st.title("☁️ Upload Ticket Dataset")

        uploaded = st.file_uploader(
            "Upload a CSV ticket dataset",
            type=["csv"]
        )

        if uploaded:
            try:
                uploaded_data = pd.read_csv(uploaded)
                st.success(
                    f"Successfully previewed {len(uploaded_data)} records."
                )
                st.dataframe(
                    uploaded_data.head(30),
                    use_container_width=True
                )
                st.info(
                    "To make this your permanent deployed dataset, "
                    "save the cleaned CSV as data/tickets.csv in GitHub."
                )
            except Exception as error:
                st.error(f"Unable to read the CSV: {error}")

    # ---------- FOOTER ----------
    st.markdown(
        '<div class="footer">CREATED BY ✦ CRACKER HEADS ♡</div>',
        unsafe_allow_html=True
    )

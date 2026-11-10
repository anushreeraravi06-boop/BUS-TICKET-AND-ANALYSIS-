from pathlib import Path
from datetime import datetime
import base64
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ============================================================
# BUS ANALYTICS | CRACKER HEADS
# ============================================================

st.set_page_config(
    page_title="Bus Analytics | CRACKER HEADS",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "tickets.csv"

BG = "#FFF8F5"
PINK = "#F8E6E5"
BURGUNDY = "#64243D"
PLUM = "#351324"
ROSE = "#C77B8C"
GOLD = "#D7A66B"
INK = "#382832"
MUTED = "#8B737D"

# ============================================================
# CHART THEME
# ============================================================

BUS_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(
            family="DM Sans, Arial, sans-serif",
            size=13,
            color=PLUM
        ),
        title=dict(
            font=dict(size=18, color=BURGUNDY)
        ),
        xaxis=dict(
            tickfont=dict(color=PLUM),
            title_font=dict(color=BURGUNDY),
            gridcolor="#EADDE0"
        ),
        yaxis=dict(
            tickfont=dict(color=PLUM),
            title_font=dict(color=BURGUNDY),
            gridcolor="#EADDE0"
        ),
        legend=dict(font=dict(color=PLUM)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
)

pio.templates["bus_analytics"] = BUS_TEMPLATE
pio.templates.default = "bus_analytics"

# ============================================================
# COMPLETE DESIGN STYLING
# ============================================================

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
}}

html, body, .stApp,
[data-testid="stAppViewContainer"] {{
    background:var(--bg) !important;
    color:var(--ink) !important;
    font-family:'DM Sans',sans-serif;
    color-scheme:light !important;
}}

[data-testid="stHeader"] {{
    background:rgba(255,248,245,.95);
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

[data-testid="stSidebar"] button {{
    width:100%;
    text-align:left;
    border-radius:13px;
    font-weight:700;
    min-height:43px;
    color:#64243D !important;
}}

[data-testid="stSidebar"] button[kind="primary"] {{
    background:#64243D !important;
    color:white !important;
}}

[data-testid="stSidebar"] button[kind="secondary"] {{
    background:rgba(255,255,255,.46) !important;
    border:1px solid #E8CCD2 !important;
}}

[data-testid="stSidebar"] button:hover {{
    background:#F4D5D8 !important;
}}

[data-testid="stSidebar"] button p,
[data-testid="stSidebar"] button span {{
    color:inherit !important;
    opacity:1 !important;
}}

[data-testid="stMetric"] {{
    background:linear-gradient(135deg,#FFF,#FCEDEF);
    border:1px solid #EBD8DC;
    border-radius:18px;
    padding:17px 18px;
    box-shadow:0 4px 16px rgba(85,35,55,.045);
}}

[data-testid="stMetricLabel"] p {{
    color:#806B75 !important;
}}

[data-testid="stMetricValue"] {{
    color:#351324 !important;
    font-weight:800;
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
    color:#64243D;
    margin:0 0 8px 0;
}}

.card p {{
    color:#755F69;
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
}}

.hero p {{
    color:#F8E7E4 !important;
    font-size:1rem;
}}

.section-title {{
    color:#64243D;
    font-size:1.25rem;
    font-weight:800;
    margin:1.2rem 0 .7rem 0;
}}

.small-note {{
    color:#8B737D;
    font-size:.84rem;
}}

.stButton button[kind="primary"] {{
    background:#64243D;
    color:white;
    border:0;
    border-radius:12px;
    font-weight:700;
}}

.stDownloadButton button {{
    background:#F3DDE1;
    color:#64243D;
    border:1px solid #E6C4CB;
    border-radius:12px;
    font-weight:700;
}}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stMarkdownContainer"] {{
    color:#382832;
}}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3 {{
    color:#64243D;
}}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
    color:#624D57 !important;
}}

[data-testid="stDataFrame"] {{
    border:1px solid #EAD9DD;
    border-radius:14px;
}}

[data-testid="stExpander"] {{
    background:#FFFFFF !important;
    border:1px solid #E7C9D0 !important;
    border-radius:14px !important;
    margin:10px 0 !important;
    overflow:hidden !important;
}}

[data-testid="stExpander"] details,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {{
    background:#FFFFFF !important;
    color:#64243D !important;
    font-weight:700 !important;
    opacity:1 !important;
}}

[data-testid="stExpander"] [data-testid="stMarkdownContainer"],
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {{
    color:#382832 !important;
    opacity:1 !important;
}}

[data-testid="stAlert"] {{
    background:#FFF1F0 !important;
    color:#351324 !important;
}}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {{
    color:#351324 !important;
}}

hr {{
    border-color:#EAD5DA !important;
}}

footer {{
    visibility:hidden;
}}

@keyframes busFadeUp {{
    from {{opacity:0;transform:translateY(16px);}}
    to {{opacity:1;transform:translateY(0);}}
}}

@keyframes busLogoIn {{
    0% {{opacity:0;transform:scale(.82);}}
    70% {{opacity:1;transform:scale(1.035);}}
    100% {{opacity:1;transform:scale(1);}}
}}

.block-container {{
    animation:busFadeUp .45s ease both;
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
    padding:24px;
    background:radial-gradient(
        circle at 50% 35%,
        #FFFDFB 0%,
        #FBE8E8 48%,
        #EFCFD6 100%
    );
}}

.bus-splash-logo {{
    width:min(72vw,310px);
    max-height:220px;
    object-fit:contain;
    border-radius:22px;
    animation:busLogoIn .85s ease both;
}}

.bus-splash-title {{
    margin-top:20px;
    color:#64243D;
    font-family:'Playfair Display',serif;
    font-size:clamp(25px,5vw,38px);
    font-weight:700;
}}

.bus-splash-subtitle {{
    margin-top:8px;
    color:#755F69;
    font-size:14px;
    letter-spacing:1.4px;
}}

.bus-splash-line {{
    width:150px;
    height:3px;
    margin-top:24px;
    border-radius:99px;
    background:linear-gradient(
        90deg,#D7A66B,#C77B8C,#64243D,#D7A66B
    );
}}

@media(max-width:768px) {{
    .block-container {{
        padding:.65rem .7rem 2rem .7rem !important;
    }}

    [data-testid="stHorizontalBlock"] {{
        flex-wrap:wrap !important;
    }}

    [data-testid="stMetric"] {{
        padding:12px !important;
    }}

    .hero {{
        padding:21px 17px !important;
    }}

    .hero h1 {{
        font-size:1.7rem !important;
    }}

    .card {{
        padding:16px !important;
    }}
}}

@media(prefers-reduced-motion:reduce) {{
    *,*::before,*::after {{
        animation-duration:.01ms !important;
        animation-iteration-count:1 !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# TWO-SECOND LOGO SPLASH
# ============================================================

if "bus_splash_shown" not in st.session_state:
    st.session_state.bus_splash_shown = False

if not st.session_state.bus_splash_shown:
    splash = st.empty()

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
                f'<img class="bus-splash-logo" '
                f'src="data:{mime};base64,{encoded}">'
            )
        except Exception:
            logo_html = "<div style='font-size:76px'>🚌</div>"
    else:
        logo_html = "<div style='font-size:76px'>🚌</div>"

    splash.markdown(
        f"""
        <div class="bus-splash">
            {logo_html}
            <div class="bus-splash-title">BUS ANALYTICS</div>
            <div class="bus-splash-subtitle">
                INTELLIGENT BUS TICKET DATA PLATFORM
            </div>
            <div class="bus-splash-line"></div>
            <div style="margin-top:22px;color:#8B737D">
                CREATED BY CRACKER HEADS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(2)
    splash.empty()
    st.session_state.bus_splash_shown = True


# ============================================================
# DATA HELPERS
# ============================================================

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
        "waybill": ["Waybill Number", "Waybill"],
        "ticket": ["Ticket Number", "Ticket No"],
        "from": ["From Stop", "From", "Origin"],
        "to": ["To Stop", "To", "Destination"],
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
            "Missing required CSV columns: "
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

    for col in ["passengers", "collected", "uncollected"]:
        out[col] = pd.to_numeric(
            out[col],
            errors="coerce"
        ).fillna(0).clip(lower=0)

    out["ticket"] = out["ticket"].astype(str)
    out["waybill"] = out["waybill"].astype(str)

    return out


def money(value):
    return f"₹{value:,.0f}"


def style_chart(fig, height=360):
    fig.update_layout(
        template="bus_analytics",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PLUM, size=13),
        margin=dict(l=15, r=25, t=55, b=25),
        autosize=True
    )
    return fig


def go_to(page):
    st.session_state.current_page = page


# ============================================================
# LOAD DATA
# ============================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "uploaded_raw" not in st.session_state:
    st.session_state.uploaded_raw = None

raw_data = st.session_state.uploaded_raw

if raw_data is None:
    try:
        if DATA_FILE.exists():
            raw_data = pd.read_csv(DATA_FILE)
    except Exception as exc:
        st.error(f"Could not read dataset: {exc}")
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
    data_error = "No dataset found. Upload your CSV file."


# ============================================================
# SIDEBAR AND LANGUAGE SELECTOR
# ============================================================

with st.sidebar:

    brand_image = ROOT / "brand_panel.png.jpeg"
    logo_image = ROOT / "logo.png.jpeg"

    if brand_image.exists():
        st.image(str(brand_image), use_container_width=True)
    elif logo_image.exists():
        st.image(str(logo_image), use_container_width=True)
    else:
        st.markdown(
            "<h2 style='color:#64243D'>🚌 BUS ANALYTICS</h2>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    language_choice = st.selectbox(
        "🌐 Language / ಭಾಷೆ / भाषा",
        [
            "English",
            "ಕನ್ನಡ (Kannada)",
            "हिन्दी (Hindi)"
        ],
        key="app_language"
    )

    st.markdown("### NAVIGATION")

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
        if st.button(
            f"{symbol}  {page_name}",
            key=f"nav_{page_name}",
            type=(
                "primary"
                if st.session_state.current_page == page_name
                else "secondary"
            )
        ):
            go_to(page_name)
            st.rerun()

    st.markdown("---")
    st.markdown(
        "<p style='color:#987984'>"
        "BOOK • ANALYZE • PREDICT<br>"
        "Created by <b>CRACKER HEADS ♡</b>"
        "</p>",
        unsafe_allow_html=True
    )


page = st.session_state.current_page


# ============================================================
# HEADER
# ============================================================

left, right = st.columns([5, 1])

with left:
    st.markdown(
        "<p style='color:#8B737D;font-weight:700'>"
        "CRACKER HEADS / BUS OPERATIONS</p>",
        unsafe_allow_html=True
    )

with right:
    st.markdown(
        "<p style='text-align:right;color:#64243D;"
        "font-weight:700'>🚌 BUS ANALYTICS</p>",
        unsafe_allow_html=True
    )

if data_error and page != "Upload Dataset":
    st.warning(data_error)


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="eyebrow">
            INTELLIGENT TRANSPORTATION ANALYTICS
        </div>
        <h1>Welcome to Bus Analytics</h1>
        <p>
            Monitor ticket activity, understand passenger movement
            and explore route performance with your bus ticket records.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not data.empty:

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Total Tickets", f"{len(data):,}")
        m2.metric("Total Revenue", money(data["collected"].sum()))
        m3.metric(
            "Total Passengers",
            f"{int(data['passengers'].sum()):,}"
        )
        m4.metric("Active Routes", f"{data['route'].nunique():,}")

        st.markdown(
            "<div class='section-title'>"
            "Ticket activity overview</div>",
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

                st.plotly_chart(
                    style_chart(fig, 330),
                    use_container_width=True
                )

        with chart_right:

            top_routes = (
                data.groupby("route")
                .size()
                .reset_index(name="Tickets")
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
                    color_discrete_sequence=[ROSE]
                )

                st.plotly_chart(
                    style_chart(fig, 330),
                    use_container_width=True
                )

        st.markdown(
            "<div class='section-title'>"
            "Explore your analytics</div>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                "<div class='card'><h3>↗ Demand Prediction</h3>"
                "<p>Explore historical ticket demand and "
                "travel patterns.</p></div>",
                unsafe_allow_html=True
            )

            if st.button("Explore demand", key="home_demand"):
                go_to("Demand Prediction")
                st.rerun()

        with c2:
            st.markdown(
                "<div class='card'><h3>✧ Smart Insights</h3>"
                "<p>Explore intelligent observations about "
                "routes, passengers and revenue.</p></div>",
                unsafe_allow_html=True
            )

            if st.button("Explore insights", key="home_insights"):
                go_to("Smart Insights")
                st.rerun()

        with c3:
            st.markdown(
                "<div class='card'><h3>▧ Reports</h3>"
                "<p>Download ticket records and analytics reports.</p></div>",
                unsafe_allow_html=True
            )

            if st.button("Explore reports", key="home_reports"):
                go_to("Reports")
                st.rerun()

    else:

        st.markdown(
            "<div class='card'><h3>Your analytics workspace is ready</h3>"
            "<p>Upload the ticket dataset to populate ticket totals, "
            "revenue, passenger insights and route charts.</p></div>",
            unsafe_allow_html=True
        )

        if st.button("Upload ticket dataset", type="primary"):
            go_to("Upload Dataset")
            st.rerun()


# ============================================================
# PART 1 ENDS HERE
# PART 2 WILL START WITH TICKET RECORDS
# ============================================================
# ============================================================
# TICKET RECORDS
# ============================================================

elif page == "Ticket Records":

    st.title("Ticket Records")
    st.caption("Explore and filter the uploaded bus ticket records.")

    if data.empty:
        st.info("Please upload a valid ticket dataset first.")

    else:
        search = st.text_input(
            "Search ticket, waybill, route or passenger details",
            placeholder="Enter a ticket number, waybill or stop name..."
        )

        f1, f2 = st.columns(2)

        with f1:
            route_options = ["All Routes"] + sorted(
                data["route"].dropna().unique().tolist()
            )

            selected_route = st.selectbox(
                "Filter by route",
                route_options
            )

        with f2:
            date_values = sorted(
                data["date"].dropna().dt.date.unique().tolist()
            )

            if date_values:
                selected_date = st.selectbox(
                    "Filter by date",
                    ["All Dates"] + date_values
                )
            else:
                selected_date = "All Dates"

        filtered = data.copy()

        if selected_route != "All Routes":
            filtered = filtered[
                filtered["route"] == selected_route
            ]

        if selected_date != "All Dates":
            filtered = filtered[
                filtered["date"].dt.date == selected_date
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

        st.metric("Matching Records", f"{len(filtered):,}")

        display_data = filtered.rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from": "From Stop",
            "to": "To Stop",
            "route": "Route",
            "date": "Date",
            "time": "Time",
            "passengers": "Total Passengers",
            "collected": "Collected Amount",
            "uncollected": "Uncollected Amount"
        })

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Filtered Records",
            data=display_data.to_csv(index=False).encode("utf-8"),
            file_name="filtered_ticket_records.csv",
            mime="text/csv"
        )


# ============================================================
# DASHBOARD
# ============================================================

elif page == "Dashboard":

    st.title("Analytics Dashboard")
    st.caption("A consolidated view of your bus ticket data.")

    if data.empty:
        st.info("Upload a dataset to view the dashboard.")

    else:
        a, b, c, d = st.columns(4)

        a.metric("Total Tickets", f"{len(data):,}")
        b.metric(
            "Passengers",
            f"{int(data['passengers'].sum()):,}"
        )
        c.metric("Revenue", money(data["collected"].sum()))
        d.metric(
            "Uncollected",
            money(data["uncollected"].sum())
        )

        st.markdown(
            "<div class='section-title'>Route-wise performance</div>",
            unsafe_allow_html=True
        )

        route_summary = (
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
            route_summary.head(12),
            x="route",
            y="Tickets",
            color="Revenue",
            title="Route-wise Ticket and Revenue Overview",
            color_continuous_scale=["#F3DDE1", "#64243D"]
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True
        )

        st.markdown(
            "<div class='section-title'>Revenue distribution</div>",
            unsafe_allow_html=True
        )

        revenue_route = (
            data.groupby("route")["collected"]
            .sum()
            .reset_index()
            .sort_values("collected", ascending=False)
            .head(8)
        )

        fig = px.pie(
            revenue_route,
            names="route",
            values="collected",
            hole=0.55,
            title="Revenue by Route",
            color_discrete_sequence=[
                "#64243D", "#C77B8C", "#D7A66B",
                "#E8BFC8", "#936276", "#F0D9D6"
            ]
        )

        st.plotly_chart(
            style_chart(fig, 400),
            use_container_width=True
        )


# ============================================================
# ROUTE ANALYSIS
# ============================================================

elif page == "Route Analysis":

    st.title("Route Analysis")
    st.caption("Understand route activity and performance.")

    if data.empty:
        st.info("Upload a dataset to analyse routes.")

    else:
        route_summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        route_summary["Average Revenue per Ticket"] = (
            route_summary["Revenue"]
            / route_summary["Tickets"].replace(0, 1)
        )

        total_tickets = max(route_summary["Tickets"].sum(), 1)
        total_passengers = max(route_summary["Passengers"].sum(), 1)
        total_revenue = max(route_summary["Revenue"].sum(), 1)

        route_summary["Route Performance Score"] = (
            35 * route_summary["Tickets"] / total_tickets
            + 35 * route_summary["Passengers"] / total_passengers
            + 30 * route_summary["Revenue"] / total_revenue
        ) * 100

        top = route_summary.sort_values(
            "Route Performance Score",
            ascending=False
        ).head(10)

        fig = px.bar(
            top.sort_values("Route Performance Score"),
            x="Route Performance Score",
            y="route",
            orientation="h",
            title="Top Routes by Performance Score",
            color_discrete_sequence=[BURGUNDY]
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True
        )

        st.subheader("Route performance table")

        st.dataframe(
            route_summary.sort_values(
                "Route Performance Score",
                ascending=False
            ).round(2),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Route Analysis",
            route_summary.to_csv(index=False).encode("utf-8"),
            "route_analysis.csv",
            "text/csv"
        )


# ============================================================
# REVENUE ANALYSIS
# ============================================================

elif page == "Revenue Analysis":

    st.title("Revenue Analysis")
    st.caption("Explore collected and uncollected ticket amounts.")

    if data.empty:
        st.info("Upload a dataset to view revenue analysis.")

    else:
        total_revenue = data["collected"].sum()
        total_pending = data["uncollected"].sum()
        total_amount = total_revenue + total_pending

        collection_rate = (
            total_revenue / total_amount * 100
            if total_amount > 0 else 0
        )

        a, b, c = st.columns(3)

        a.metric("Collected Revenue", money(total_revenue))
        b.metric("Uncollected Amount", money(total_pending))
        c.metric("Collection Rate", f"{collection_rate:.1f}%")

        revenue_route = (
            data.groupby("route")
            .agg(
                Collected=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
            .sort_values("Collected", ascending=False)
        )

        fig = px.bar(
            revenue_route.head(12),
            x="route",
            y=["Collected", "Uncollected"],
            title="Collected vs Uncollected Revenue",
            barmode="group",
            color_discrete_sequence=[BURGUNDY, ROSE]
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True
        )

        st.subheader("Revenue details")

        st.dataframe(
            revenue_route,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PASSENGER INSIGHTS
# ============================================================

elif page == "Passenger Insights":

    st.title("Passenger Insights")
    st.caption("Understand passenger distribution across routes.")

    if data.empty:
        st.info("Upload a dataset to view passenger insights.")

    else:
        total_passengers = int(data["passengers"].sum())

        a, b = st.columns(2)

        a.metric("Total Passengers", f"{total_passengers:,}")
        b.metric(
            "Average Passengers per Ticket",
            f"{data['passengers'].mean():.2f}"
        )

        passenger_route = (
            data.groupby("route")["passengers"]
            .sum()
            .reset_index()
            .sort_values("passengers", ascending=False)
            .head(12)
        )

        fig = px.bar(
            passenger_route,
            x="route",
            y="passengers",
            title="Passenger Count by Route",
            color_discrete_sequence=[ROSE]
        )

        st.plotly_chart(
            style_chart(fig, 420),
            use_container_width=True
        )

        fig = px.histogram(
            data,
            x="passengers",
            nbins=15,
            title="Passenger Count Distribution",
            color_discrete_sequence=[BURGUNDY]
        )

        st.plotly_chart(
            style_chart(fig, 350),
            use_container_width=True
        )


# ============================================================
# DEMAND PREDICTION
# ============================================================

elif page == "Demand Prediction":

    st.title("Demand Prediction")
    st.caption(
        "Explore historical hourly demand patterns. "
        "This is an indicative analysis, not a future forecast."
    )

    if data.empty:
        st.info("Upload a dataset to analyse demand.")

    else:
        time_data = data.copy()

        time_data["hour"] = pd.to_datetime(
            time_data["time"].astype(str),
            errors="coerce"
        ).dt.hour

        time_data = time_data.dropna(subset=["hour"])
        time_data["hour"] = time_data["hour"].astype(int)

        if time_data.empty:
            st.warning(
                "The uploaded dataset does not contain readable time values."
            )

        else:
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
                "Busiest Recorded Hour",
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
                style_chart(fig, 390),
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
                style_chart(fig, 350),
                use_container_width=True
            )

            st.dataframe(
                hourly,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# SMART INSIGHTS
# ============================================================

elif page == "Smart Insights":

    st.title("Smart Insights")
    st.caption(
        "Statistical observations and rule-based recommendations "
        "from your ticket dataset."
    )

    if data.empty:
        st.info("Upload a dataset to generate smart insights.")

    else:
        route_summary = (
            data.groupby("route")
            .agg(
                Tickets=("ticket", "count"),
                Passengers=("passengers", "sum"),
                Revenue=("collected", "sum"),
                Uncollected=("uncollected", "sum")
            )
            .reset_index()
        )

        total_revenue = data["collected"].sum()
        total_uncollected = data["uncollected"].sum()

        # 1. SMART DEMAND RECOMMENDATIONS

        with st.expander(
            "✧ 1. Smart Demand Recommendations",
            expanded=False
        ):

            st.markdown("### High-demand routes")

            high_demand = route_summary.sort_values(
                "Tickets",
                ascending=False
            ).head(5)

            st.dataframe(
                high_demand,
                use_container_width=True,
                hide_index=True
            )

            if not high_demand.empty:
                st.success(
                    "Review the frequency and capacity of "
                    "the routes with the highest ticket activity."
                )

        # 2. ROUTE INTELLIGENCE

        with st.expander(
            "⌁ 2. Route Intelligence",
            expanded=False
        ):

            st.markdown("### Route comparison")

            st.dataframe(
                route_summary.sort_values(
                    "Passengers",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

            if len(route_summary) > 1:
                low_route = route_summary.sort_values(
                    "Tickets"
                ).iloc[0]

                st.info(
                    f"Lowest recorded ticket activity: "
                    f"{low_route['route']} "
                    f"({int(low_route['Tickets'])} tickets). "
                    "Review demand before changing the service."
                )

        # 3. REVENUE INTELLIGENCE

        with st.expander(
            "₹ 3. Revenue Intelligence",
            expanded=False
        ):

            total_amount = total_revenue + total_uncollected

            rate = (
                total_revenue / total_amount * 100
                if total_amount else 0
            )

            a, b, c = st.columns(3)

            a.metric("Collected", money(total_revenue))
            b.metric("Uncollected", money(total_uncollected))
            c.metric("Collection Rate", f"{rate:.1f}%")

            st.markdown("#### Route-wise revenue")

            st.dataframe(
                route_summary.sort_values(
                    "Revenue",
                    ascending=False
                ),
                use_container_width=True,
                hide_index=True
            )

            if total_uncollected > 0:
                st.warning(
                    "Review uncollected amounts and reconcile "
                    "them with the original ticket records."
                )

        # 4. PEAK-HOUR INTELLIGENCE AND HEATMAP

        with st.expander(
            "◷ 4. Peak-Hour Intelligence & Heatmap",
            expanded=False
        ):

            time_data = data.copy()

            time_data["hour"] = pd.to_datetime(
                time_data["time"].astype(str),
                errors="coerce"
            ).dt.hour

            time_data = time_data.dropna(subset=["hour"])
            time_data["hour"] = time_data["hour"].astype(int)

            if time_data.empty:
                st.warning(
                    "No readable time values are available "
                    "for peak-hour analysis."
                )

            else:
                hourly = (
                    time_data.groupby("hour")
                    .size()
                    .reset_index(name="Tickets")
                )

                busiest = hourly.loc[
                    hourly["Tickets"].idxmax()
                ]

                st.metric(
                    "Busiest Recorded Hour",
                    f"{int(busiest['hour']):02d}:00"
                )

                fig = px.bar(
                    hourly,
                    x="hour",
                    y="Tickets",
                    title="Peak-Hour Ticket Activity",
                    color="Tickets",
                    color_continuous_scale=[
                        "#F6DDE2", "#C77B8C", "#64243D"
                    ]
                )

                st.plotly_chart(
                    style_chart(fig, 330),
                    use_container_width=True
                )

                heat_data = time_data.copy()

                heat_data["travel_date"] = (
                    heat_data["date"].dt.strftime("%d %b %Y")
                )

                heat = (
                    heat_data.groupby(
                        ["travel_date", "hour"]
                    )
                    .size()
                    .reset_index(name="Tickets")
                )

                if not heat.empty:
                    pivot = heat.pivot(
                        index="travel_date",
                        columns="hour",
                        values="Tickets"
                    ).fillna(0)

                    fig = px.imshow(
                        pivot,
                        aspect="auto",
                        color_continuous_scale=[
                            "#F8E6E5", "#C77B8C", "#64243D"
                        ],
                        labels=dict(
                            x="Hour",
                            y="Travel Date",
                            color="Tickets"
                        ),
                        title="Peak-Hour Demand Heatmap"
                    )

                    st.plotly_chart(
                        style_chart(fig, 350),
                        use_container_width=True
                    )

        # 5. UNUSUAL ACTIVITY DETECTION

        with st.expander(
            "⚑ 5. Unusual Activity Detection",
            expanded=False
        ):

            st.markdown(
                "This section flags statistically unusual "
                "ticket counts and collection amounts for review."
            )

            route_stats = route_summary.copy()

            if len(route_stats) >= 3:

                ticket_mean = route_stats["Tickets"].mean()
                ticket_std = route_stats["Tickets"].std()

                revenue_mean = route_stats["Revenue"].mean()
                revenue_std = route_stats["Revenue"].std()

                if ticket_std > 0:
                    unusual_tickets = route_stats[
                        (route_stats["Tickets"] - ticket_mean).abs()
                        > 2 * ticket_std
                    ]
                else:
                    unusual_tickets = route_stats.iloc[0:0]

                if revenue_std > 0:
                    unusual_revenue = route_stats[
                        (route_stats["Revenue"] - revenue_mean).abs()
                        > 2 * revenue_std
                    ]
                else:
                    unusual_revenue = route_stats.iloc[0:0]

                st.markdown("#### Unusual ticket activity")

                if unusual_tickets.empty:
                    st.success("No statistical ticket-count outliers detected.")
                else:
                    st.dataframe(
                        unusual_tickets,
                        use_container_width=True,
                        hide_index=True
                    )

                st.markdown("#### Unusual revenue activity")

                if unusual_revenue.empty:
                    st.success("No statistical revenue outliers detected.")
                else:
                    st.dataframe(
                        unusual_revenue,
                        use_container_width=True,
                        hide_index=True
                    )

            else:
                st.info(
                    "At least three routes are needed "
                    "for this comparison."
                )

            st.caption(
                "An unusual value is only a review flag. "
                "It does not prove fraud or misconduct."
            )

        # 6. MANAGEMENT RECOMMENDATIONS

        with st.expander(
            "✦ 6. Management Recommendations",
            expanded=False
        ):

            top_route = route_summary.sort_values(
                "Tickets",
                ascending=False
            ).iloc[0]

            st.markdown("### Suggested actions")

            st.write(
                f"1. Review service frequency on "
                f"{top_route['route']}, the route with the "
                f"highest recorded ticket count."
            )

            st.write(
                "2. Review passenger demand before "
                "allocating additional buses."
            )

            st.write(
                "3. Reconcile uncollected ticket amounts "
                "with the original records."
            )

            st.write(
                "4. Use hourly ticket activity to review "
                "staffing and scheduling."
            )

            st.write(
                "5. Collect data across multiple dates "
                "to identify daily and seasonal trends."
            )

            st.caption(
                "Recommendations are generated from the "
                "available records and should be reviewed "
                "by transport management."
            )


# ============================================================
# AI WEBSITE ASSISTANT
# ============================================================

elif page == "AI Website Assistant":

    st.title("AI Website Assistant")

    st.caption(
        "Ask questions about the Bus Analytics website, "
        "its pages and available features."
    )

    responses = {

        "English": {
            "dashboard": (
                "The Dashboard provides a consolidated view "
                "of tickets, passengers, revenue and route performance."
            ),
            "ticket": (
                "Ticket Records lets you search, filter and download "
                "ticket information."
            ),
            "route": (
                "Route Analysis compares ticket counts, passengers "
                "and revenue across routes."
            ),
            "revenue": (
                "Revenue Analysis shows collected amounts, "
                "uncollected amounts and collection rate."
            ),
            "passenger": (
                "Passenger Insights displays passenger counts "
                "and their distribution across routes."
            ),
            "demand": (
                "Demand Prediction displays historical hourly "
                "ticket and passenger patterns. It is not a "
                "future forecasting model."
            ),
            "smart": (
                "Smart Insights provides six sections: demand "
                "recommendations, route intelligence, revenue "
                "intelligence, peak-hour analysis, unusual activity "
                "detection and management recommendations."
            ),
            "upload": (
                "Open Upload Dataset and select your CSV file. "
                "The CSV should contain route, date, passenger "
                "and collected amount columns."
            ),
            "report": (
                "Open Reports to download the available "
                "analytics summaries and ticket data."
            ),
            "hello": (
                "Hello! Welcome to Bus Analytics. "
                "Ask me about any page or feature."
            ),
            "help": (
                "I can explain Dashboard, Ticket Records, "
                "Route Analysis, Revenue Analysis, Passenger "
                "Insights, Demand Prediction, Smart Insights, "
                "Reports and Upload Dataset."
            ),
            "ai": (
                "This assistant currently uses rule-based "
                "question matching. It is not connected to "
                "a generative AI service."
            )
        },

        "ಕನ್ನಡ (Kannada)": {
            "dashboard": (
                "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ ಟಿಕೆಟ್‌ಗಳು, ಪ್ರಯಾಣಿಕರು, "
                "ಆದಾಯ ಮತ್ತು ಮಾರ್ಗಗಳ ಕಾರ್ಯಕ್ಷಮತೆಯನ್ನು ನೋಡಬಹುದು."
            ),
            "ticket": (
                "ಟಿಕೆಟ್ ದಾಖಲೆಗಳಲ್ಲಿ ಟಿಕೆಟ್ ಮಾಹಿತಿಯನ್ನು ಹುಡುಕಬಹುದು, "
                "ಫಿಲ್ಟರ್ ಮಾಡಬಹುದು ಮತ್ತು ಡೌನ್‌ಲೋಡ್ ಮಾಡಬಹುದು."
            ),
            "route": (
                "ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ಟಿಕೆಟ್‌ಗಳು, ಪ್ರಯಾಣಿಕರು "
                "ಮತ್ತು ಆದಾಯವನ್ನು ಹೋಲಿಸಬಹುದು."
            ),
            "revenue": (
                "ಆದಾಯ ವಿಶ್ಲೇಷಣೆಯಲ್ಲಿ ಸಂಗ್ರಹಿಸಿದ ಮೊತ್ತ, "
                "ಬಾಕಿ ಮೊತ್ತ ಮತ್ತು ಸಂಗ್ರಹ ದರವನ್ನು ನೋಡಬಹುದು."
            ),
            "passenger": (
                "ಪ್ರಯಾಣಿಕರ ಒಳನೋಟಗಳಲ್ಲಿ ಮಾರ್ಗವಾರು "
                "ಪ್ರಯಾಣಿಕರ ಸಂಖ್ಯೆಯನ್ನು ನೋಡಬಹುದು."
            ),
            "demand": (
                "ಬೇಡಿಕೆ ವಿಭಾಗವು ಹಿಂದಿನ ಗಂಟೆವಾರು ಟಿಕೆಟ್ "
                "ಮಾದರಿಗಳನ್ನು ತೋರಿಸುತ್ತದೆ. ಇದು ಭವಿಷ್ಯದ "
                "ಖಚಿತ ಮುನ್ಸೂಚನೆ ಅಲ್ಲ."
            ),
            "smart": (
                "ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳಲ್ಲಿ ಬೇಡಿಕೆ, ಮಾರ್ಗ, ಆದಾಯ, "
                "ಪೀಕ್ ಅವರ್, ಅಸಾಮಾನ್ಯ ಚಟುವಟಿಕೆ ಮತ್ತು "
                "ನಿರ್ವಹಣಾ ಶಿಫಾರಸುಗಳಿವೆ."
            ),
            "upload": (
                "Upload Dataset ತೆರೆಯಿರಿ ಮತ್ತು CSV ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ. "
                "ಅಗತ್ಯ ಕಾಲಮ್‌ಗಳು ಫೈಲ್‌ನಲ್ಲಿ ಇರಬೇಕು."
            ),
            "report": (
                "Reports ವಿಭಾಗದಲ್ಲಿ ಲಭ್ಯವಿರುವ ವರದಿಗಳನ್ನು "
                "ಡೌನ್‌ಲೋಡ್ ಮಾಡಬಹುದು."
            ),
            "hello": (
                "ನಮಸ್ಕಾರ! Bus Analytics ಗೆ ಸ್ವಾಗತ. "
                "ಯಾವುದೇ ವಿಭಾಗದ ಬಗ್ಗೆ ಕೇಳಿ."
            ),
            "help": (
                "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್, ಟಿಕೆಟ್ ದಾಖಲೆಗಳು, ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆ, "
                "ಆದಾಯ, ಪ್ರಯಾಣಿಕರು, ಬೇಡಿಕೆ, ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳು "
                "ಮತ್ತು ವರದಿಗಳ ಬಗ್ಗೆ ಕೇಳಬಹುದು."
            ),
            "ai": (
                "ಈ ಸಹಾಯಕವು ಪ್ರಸ್ತುತ ನಿಯಮಾಧಾರಿತ ಪ್ರಶ್ನೆ ಹೊಂದಾಣಿಕೆಯನ್ನು "
                "ಬಳಸುತ್ತದೆ. ಇದು ಜನರೇಟಿವ್ AI ಸೇವೆಗೆ ಸಂಪರ್ಕಗೊಂಡಿಲ್ಲ."
            )
        },

        "हिन्दी (Hindi)": {
            "dashboard": (
                "डैशबोर्ड में टिकट, यात्री, राजस्व और "
                "रूट प्रदर्शन की जानकारी मिलती है।"
            ),
            "ticket": (
                "टिकट रिकॉर्ड में टिकट खोज सकते हैं, "
                "फ़िल्टर कर सकते हैं और डाउनलोड कर सकते हैं।"
            ),
            "route": (
                "रूट विश्लेषण में टिकट, यात्री और राजस्व "
                "की तुलना की जाती है।"
            ),
            "revenue": (
                "राजस्व विश्लेषण में एकत्र राशि, बकाया राशि "
                "और संग्रह दर दिखाई जाती है।"
            ),
            "passenger": (
                "यात्री जानकारी में अलग-अलग रूट पर "
                "यात्रियों की संख्या दिखाई जाती है।"
            ),
            "demand": (
                "डिमांड सेक्शन ऐतिहासिक घंटेवार टिकट पैटर्न "
                "दिखाता है। यह भविष्य का निश्चित अनुमान नहीं है।"
            ),
            "smart": (
                "स्मार्ट इनसाइट्स में मांग, रूट, राजस्व, "
                "पीक-आवर, असामान्य गतिविधि और प्रबंधन "
                "सुझाव शामिल हैं।"
            ),
            "upload": (
                "Upload Dataset खोलें और अपनी CSV फ़ाइल चुनें। "
                "फ़ाइल में आवश्यक कॉलम होने चाहिए।"
            ),
            "report": (
                "Reports सेक्शन में उपलब्ध रिपोर्ट डाउनलोड कर सकते हैं।"
            ),
            "hello": (
                "नमस्ते! Bus Analytics में आपका स्वागत है। "
                "किसी भी फीचर के बारे में पूछें।"
            ),
            "help": (
                "आप डैशबोर्ड, टिकट रिकॉर्ड, रूट विश्लेषण, "
                "राजस्व, यात्री, मांग, स्मार्ट इनसाइट्स "
                "और रिपोर्ट के बारे में पूछ सकते हैं।"
            ),
            "ai": (
                "यह सहायक अभी नियम-आधारित प्रश्न मिलान का "
                "उपयोग करता है। यह जनरेटिव AI सेवा से जुड़ा नहीं है।"
            )
        }
    }

    language = language_choice
    answer_set = responses.get(language, responses["English"])

    question = st.text_input(
        "Ask your question",
        placeholder="Example: How can I analyse revenue?"
    )

    if st.button("Ask Assistant", type="primary"):

        q = question.lower().strip()

        if not q:
            st.warning("Please enter a question.")

        else:
            if any(word in q for word in [
                "hello", "hi", "hey", "ನಮಸ್ಕಾರ", "नमस्ते"
            ]):
                answer = answer_set["hello"]

            elif any(word in q for word in [
                "dashboard", "ಡ್ಯಾಶ್", "डैशबोर्ड"
            ]):
                answer = answer_set["dashboard"]

            elif any(word in q for word in [
                "ticket", "record", "ಟಿಕೆಟ್", "टिकट"
            ]):
                answer = answer_set["ticket"]

            elif any(word in q for word in [
                "route", "ಮಾರ್ಗ", "रूट"
            ]):
                answer = answer_set["route"]

            elif any(word in q for word in [
                "revenue", "money", "income", "ಆದಾಯ", "राजस्व"
            ]):
                answer = answer_set["revenue"]

            elif any(word in q for word in [
                "passenger", "ಪ್ರಯಾಣಿಕ", "यात्री"
            ]):
                answer = answer_set["passenger"]

            elif any(word in q for word in [
                "demand", "predict", "ಬೇಡಿಕೆ", "मांग"
            ]):
                answer = answer_set["demand"]

            elif any(word in q for word in [
                "smart", "insight", "intelligence",
                "ಸ್ಮಾರ್ಟ್", "स्मार्ट"
            ]):
                answer = answer_set["smart"]

            elif any(word in q for word in [
                "upload", "dataset", "csv", "ಅಪ್‌ಲೋಡ್", "अपलोड"
            ]):
                answer = answer_set["upload"]

            elif any(word in q for word in [
                "report", "download", "ವರದಿ", "रिपोर्ट"
            ]):
                answer = answer_set["report"]

            elif any(word in q for word in [
                "ai", "artificial intelligence",
                "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ", "कृत्रिम बुद्धिमत्ता"
            ]):
                answer = answer_set["ai"]

            else:
                answer = answer_set["help"]

            st.markdown(
                f"""
                <div class="card">
                    <h3>✦ AI Website Assistant</h3>
                    <p>{answer}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.markdown("#### Try asking")

    examples = [
        "How do I upload a dataset?",
        "What is Smart Insights?",
        "How can I analyse revenue?",
        "What does Demand Prediction show?"
    ]

    for example in examples:
        st.caption("• " + example)


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("Reports")
    st.caption("Download reports generated from your ticket records.")

    if data.empty:
        st.info("Upload a dataset before generating reports.")

    else:
        st.markdown(
            "<div class='section-title'>Available reports</div>",
            unsafe_allow_html=True
        )

        ticket_report = data.rename(columns={
            "waybill": "Waybill Number",
            "ticket": "Ticket Number",
            "from": "From Stop",
            "to": "To Stop",
            "route": "Route",
            "date": "Date",
            "time": "Time",
            "passengers": "Passengers",
            "collected": "Collected Amount",
            "uncollected": "Uncollected Amount"
        })

        st.download_button(
            "Download Complete Ticket Report",
            ticket_report.to_csv(index=False).encode("utf-8"),
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

        st.download_button(
            "Download Route Summary",
            route_report.to_csv(index=False).encode("utf-8"),
            "route_summary.csv",
            "text/csv",
            use_container_width=True
        )

        revenue_report = pd.DataFrame({
            "Metric": [
                "Total Tickets",
                "Total Passengers",
                "Collected Revenue",
                "Uncollected Amount"
            ],
            "Value": [
                len(data),
                int(data["passengers"].sum()),
                data["collected"].sum(),
                data["uncollected"].sum()
            ]
        })

        st.download_button(
            "Download Revenue Summary",
            revenue_report.to_csv(index=False).encode("utf-8"),
            "revenue_summary.csv",
            "text/csv",
            use_container_width=True
        )


# ============================================================
# UPLOAD DATASET
# ============================================================

elif page == "Upload Dataset":

    st.title("Upload Dataset")

    st.caption(
        "Upload a CSV file containing bus ticket records."
    )

    st.markdown(
        "<div class='card'>"
        "<h3>Dataset requirements</h3>"
        "<p>Your CSV should contain columns for From Stop, "
        "To Stop, Date, Total Passengers and Collected Amount. "
        "Waybill, Ticket Number, Time and Uncollected Amount "
        "are also supported.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose your ticket CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            preview = pd.read_csv(uploaded_file)

            st.success(
                f"File loaded successfully: {len(preview):,} rows."
            )

            st.subheader("Dataset preview")

            st.dataframe(
                preview.head(10),
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                "Use This Dataset",
                type="primary"
            ):

                st.session_state.uploaded_raw = preview
                st.session_state.bus_upload_success = True
                st.rerun()

            if st.session_state.get("bus_upload_success"):
                st.success(
                    "Dataset is now active for this session."
                )

        except Exception as exc:
            st.error(f"Could not process the uploaded file: {exc}")

    else:
        st.info(
            "The default repository dataset will be used "
            "when no new file is uploaded."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:18px 8px;
        color:#806B75;
        line-height:1.8;
    ">
        <div style="
            color:#64243D;
            font-size:18px;
            font-weight:800;
            letter-spacing:1px;
        ">
            🚌 BUS ANALYTICS
        </div>

        <div>
            Intelligent Bus Ticket Data Platform
        </div>

        <div style="
            color:#987984;
            font-size:13px;
            margin-top:8px;
        ">
            BOOK • ANALYZE • PREDICT
        </div>

        <div style="
            color:#64243D;
            font-weight:700;
            margin-top:8px;
        ">
            Created by CRACKER HEADS
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

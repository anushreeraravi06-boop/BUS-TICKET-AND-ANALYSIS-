from pathlib import Path
from datetime import datetime
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

# Readable Plotly chart theme
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
            tickfont=dict(color=PLUM, size=12),
            title_font=dict(color=BURGUNDY, size=13),
            color=PLUM,
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
        ),
        yaxis=dict(
            tickfont=dict(color=PLUM, size=12),
            title_font=dict(color=BURGUNDY, size=13),
            color=PLUM,
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
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

# ------------------------------------------------------------
# DESIGN AND VISIBILITY CSS
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

html, body, [data-testid="stAppViewContainer"] {{
    background:var(--bg);
    color:var(--ink);
    font-family:'DM Sans',sans-serif;
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
    background:linear-gradient(180deg,#FBEAE7 0%,#F5DFE2 100%);
    border-right:1px solid #EAD1D5;
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top:1rem;
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
    color:var(--burgundy) !important;
}}

[data-testid="stSidebar"] .stButton button {{
    width:100%;
    text-align:left;
    border:1px solid transparent;
    border-radius:13px;
    background:transparent;
    color:var(--burgundy) !important;
    font-weight:600;
    padding:.65rem .8rem;
}}

[data-testid="stSidebar"] .stButton button:hover {{
    background:#F4D5D8;
    border-color:#E8BFC7;
    color:var(--plum) !important;
}}

[data-testid="stMetric"] {{
    background:linear-gradient(135deg,#FFFFFF 0%,#FCEDEF 100%);
    border:1px solid #EBD8DC;
    border-radius:18px;
    padding:17px 18px;
    box-shadow:0 4px 16px rgba(85,35,55,.045);
}}

[data-testid="stMetricLabel"] p {{
    color:#624D57 !important;
    font-weight:700 !important;
}}

[data-testid="stMetricValue"] {{
    color:#351324 !important;
    font-weight:800 !important;
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
    color:#64243D !important;
    margin:0 0 8px 0;
    font-size:1.05rem;
}}

.card p {{
    color:#624D57 !important;
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
    color:#F5D4C9 !important;
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
}}

.section-title {{
    color:#64243D !important;
    font-size:1.25rem;
    font-weight:800;
    margin:1.2rem 0 .7rem 0;
}}

.small-note {{
    color:#624D57 !important;
    font-size:.84rem;
}}

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

hr {{
    border-color:#EAD5DA !important;
}}

footer {{
    visibility:hidden;
}}

/* Force a readable light interface */
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

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] span {{
    color:#382832;
}}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {{
    color:#64243D !important;
}}

[data-testid="stCaptionContainer"] p {{
    color:#624D57 !important;
    opacity:1 !important;
}}

/* Input and chat visibility */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stChatInput"] textarea,
[data-testid="stSelectbox"] div,
[data-testid="stDateInput"] input {{
    color:#351324 !important;
    -webkit-text-fill-color:#351324 !important;
    background-color:#FFFFFF !important;
    caret-color:#64243D !important;
}}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stChatInput"] textarea::placeholder {{
    color:#806B75 !important;
    opacity:1 !important;
}}

[data-testid="stChatMessage"] p {{
    color:#351324 !important;
    opacity:1 !important;
}}

/* Table visibility */
[data-testid="stDataFrame"] {{
    background:#FFFFFF !important;
    border:1px solid #EAD9DD;
    border-radius:14px;
    color:#351324 !important;
}}

/* Chart labels */
.js-plotly-plot .plotly text {{
    fill:#351324 !important;
}}

.js-plotly-plot .plotly .gtitle {{
    fill:#64243D !important;
}}

/* Mobile responsive layout */
@media (max-width:768px) {{
    .block-container {{
        padding:.65rem .7rem 1.5rem .7rem !important;
    }}

    [data-testid="stHorizontalBlock"] {{
        flex-direction:column !important;
        gap:.8rem !important;
    }}

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
        width:100% !important;
        min-width:100% !important;
    }}

    .hero {{
        padding:21px 17px !important;
        min-height:unset !important;
    }}

    .hero h1 {{
        font-size:1.7rem !important;
    }}

    [data-testid="stMetric"] {{
        padding:12px !important;
    }}

    .card {{
        padding:16px !important;
    }}

    [data-testid="stPlotlyChart"] {{
        width:100% !important;
        overflow-x:auto !important;
    }}

    .stButton button,
    .stDownloadButton button {{
        min-height:44px !important;
    }}
}}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# DATA PREPARATION FUNCTIONS
# ------------------------------------------------------------

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
        "from", "to", "date", "passengers", "collected"
    ]

    missing = [
        column for column in required
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
        "passengers", "collected", "uncollected"
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


# ------------------------------------------------------------
# SESSION STATE AND DATA LOADING
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------------------

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
            "<small>Intelligent Bus Ticket Data Platform</small>"
            "</div>",
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

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# SHARED VALIDATION
# ------------------------------------------------------------

if data_error and page != "Upload Dataset":
    st.warning(data_error)

# ------------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------------

if page == "Home":

    st.markdown("""
    <div class="hero">
      <div class="eyebrow">INTELLIGENT TRANSPORTATION ANALYTICS</div>
      <h1>Welcome to Bus Analytics</h1>
      <p>Monitor ticket activity, understand passenger movement and
      explore route performance with your bus ticket records.</p>
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
        m4.metric("Total Routes", f"{total_routes:,}")

        st.markdown(
            "<div class='section-title'>Ticket activity overview</div>",
            unsafe_allow_html=True
        )

        chart_left, chart_right = st.columns(2)

        with chart_left:

            date_summary = (
                data.dropna(subset=["date"])
                .groupby(data["date"].dt.date)
                .size()
                .reset_index(name="Tickets")
            )

            date_summary.columns = ["Date", "Tickets"]

            if not date_summary.empty:

                fig = px.area(
                    date_summary,
                    x="Date",
                    y="Tickets",
                    title="Ticket Bookings Trend"
                )

                fig.update_traces(
                    line_color=BURGUNDY,
                    fillcolor="rgba(199,123,140,.25)"
                )

                fig.update_layout(
                    height=330,
                    margin=dict(l=10, r=10, t=55, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=INK),
                    title_font=dict(color=BURGUNDY, size=17)
                )

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
                    height=330,
                    margin=dict(l=10, r=25, t=55, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=INK),
                    title_font=dict(color=BURGUNDY, size=17),
                    yaxis_title="",
                    xaxis_title="Tickets"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        st.markdown(
            "<div class='section-title'>Explore your analytics</div>",
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                "<div class='card'><h3>↗ Demand Prediction</h3>"
                "<p>Explore historical ticket demand and simple upcoming "
                "demand estimates.</p></div>",
                unsafe_allow_html=True
            )

            if st.button(
                "Explore demand",
                key="home_demand",
                use_container_width=True
            ):
                go_to("Demand Prediction")
                st.rerun()

        with c2:
            st.markdown(
                "<div class='card'><h3>✧ Smart Insights</h3>"
                "<p>Find useful observations from routes, passengers and "
                "collections.</p></div>",
                unsafe_allow_html=True
            )

            if st.button(
                "Explore insights",
                key="home_insights",
                use_container_width=True
            ):
                go_to("Smart Insights")
                st.rerun()

        with c3:
            st.markdown(
                "<div class='card'><h3>▧ Generate Reports</h3>"
                "<p>Export ticket records and summary data for further review.</p>"
                "</div>",
                unsafe_allow_html=True
            )

            if st.button(
                "Explore reports",
                key="home_reports",
                use_container_width=True
            ):
                go_to("Reports")
                st.rerun()

    else:

        st.markdown(
            "<div class='card'><h3>Your analytics workspace is ready</h3>"
            "<p>Upload the ticket dataset to populate ticket totals, revenue, "
            "passenger insights, route charts and reports.</p></div>",
            unsafe_allow_html=True
        )

        if st.button("Upload ticket dataset", type="primary"):
            go_to("Upload Dataset")
            st.rerun()


# ---------------------------- Ticket Records ----------------------------

elif page == "Ticket Records":

    st.title("Ticket Records")
    st.caption(
        "Search, review and export the ticket records in your dataset."
    )

    if not data.empty:

        search = st.text_input(
            "Search by ticket, waybill, route or stop",
            placeholder="Type a ticket number, route or stop..."
        )

        view = data.copy()

        if search.strip():

            mask = view.astype(str).apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            view = view[mask]

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
                "uncollected": "Uncollected Amount (₹)"
            }
        )

        st.write(f"**{len(view):,}** records found")

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
                color_discrete_sequence=[ROSE],
                text="Tickets"
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            fig.update_layout(
                height=350,
                margin=dict(t=55, l=10, r=10, b=10)
            )

            st.plotly_chart(
                style_chart(fig, 350),
                use_container_width=True
            )

        with y:

            origin_counts = (
                data.groupby("from")
                .size()
                .sort_values(ascending=False)
            )

            top_origins = origin_counts.head(10)
            other_count = int(origin_counts.iloc[10:].sum())

            origin_plot = top_origins.reset_index()
            origin_plot.columns = ["Origin", "Tickets"]

            if other_count > 0:

                origin_plot = pd.concat(
                    [
                        origin_plot,
                        pd.DataFrame([
                            {
                                "Origin": "Other stops",
                                "Tickets": other_count
                            }
                        ])
                    ],
                    ignore_index=True
                )

            fig = px.bar(
                origin_plot.sort_values("Tickets"),
                x="Tickets",
                y="Origin",
                orientation="h",
                title="Top Ticket Origins",
                text="Tickets",
                color_discrete_sequence=[ROSE]
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            fig.update_layout(
                height=420,
                margin=dict(t=55, l=10, r=35, b=10),
                yaxis_title="",
                xaxis_title="Number of Tickets",
                showlegend=False
            )

            st.plotly_chart(
                style_chart(fig, 420),
                use_container_width=True
            )

    else:
        st.info("Upload your ticket CSV to see the dashboard.")
        # ============================================================
# ROUTE ANALYSIS
# ============================================================

elif page == "Route Analysis":

    st.title("Route Analysis")
    st.caption("Compare routes, passenger activity and revenue.")

    if not data.empty:

        routes = (
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

        st.markdown("### Route Performance")

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
            text="Passengers",
            color_discrete_sequence=[BURGUNDY]
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        st.plotly_chart(
            style_chart(fig, 480),
            use_container_width=True
        )

        # Route performance score
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

        score = routes.copy()

        score["Ticket Score"] = normalise(score["Tickets"])
        score["Passenger Score"] = normalise(score["Passengers"])
        score["Revenue Score"] = normalise(score["Revenue"])

        score["Performance Score"] = (
            score["Ticket Score"] * 0.35
            + score["Passenger Score"] * 0.35
            + score["Revenue Score"] * 0.30
        ).round(1)

        score = score.sort_values(
            "Performance Score",
            ascending=False
        )

        best = score.iloc[0]

        st.success(
            f"Top-performing route: {best['route']} "
            f"with a score of {best['Performance Score']}/100."
        )

        st.caption(
            "Score calculation: 35% ticket count, "
            "35% passenger count and 30% collected revenue. "
            "This is a relative dataset score."
        )

        fig = px.bar(
            score.head(10).sort_values("Performance Score"),
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
            xaxis_title="Performance Score",
            yaxis_title=""
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

    st.title("Revenue Analysis")
    st.caption("Understand revenue collection and pending amounts.")

    if not data.empty:

        collected = data["collected"].sum()
        uncollected = data["uncollected"].sum()
        total = collected + uncollected

        a, b, c = st.columns(3)

        a.metric("Collected Revenue", money(collected))
        b.metric("Uncollected Amount", money(uncollected))
        c.metric("Total Recorded Amount", money(total))

        collection_rate = (
            collected / total * 100 if total > 0 else 0
        )

        st.markdown("### Collection Rate")

        st.progress(
            min(max(collection_rate / 100, 0), 1)
        )

        st.write(f"**{collection_rate:.1f}% collected**")

        revenue_routes = (
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
            revenue_routes,
            x="route",
            y=["Collected", "Uncollected"],
            barmode="group",
            title="Revenue by Route",
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

        st.markdown("### Route-wise Revenue Details")

        st.dataframe(
            revenue_routes,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Upload a dataset to analyse revenue.")


# ============================================================
# PASSENGER INSIGHTS
# ============================================================

elif page == "Passenger Insights":

    st.title("Passenger Insights")
    st.caption("Understand passenger movement and popular stops.")

    if not data.empty:

        a, b, c = st.columns(3)

        a.metric(
            "Total Passengers",
            f"{int(data['passengers'].sum()):,}"
        )

        b.metric(
            "Average Passengers per Ticket",
            f"{data['passengers'].mean():.2f}"
        )

        c.metric(
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
            text="passengers",
            color_discrete_sequence=[ROSE]
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

        st.markdown("### Popular Boarding Stops")

        st.dataframe(
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

        st.dataframe(
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

    st.title("Demand Prediction")
    st.caption(
        "Explore observed hourly ticket demand and activity patterns."
    )

    if not data.empty:

        demand = data.copy()

        demand["hour"] = pd.to_datetime(
            demand["time"].astype(str),
            format="%H:%M:%S",
            errors="coerce"
        ).dt.hour

        missing_hours = demand["hour"].isna()

        demand.loc[missing_hours, "hour"] = pd.to_datetime(
            demand.loc[missing_hours, "time"].astype(str),
            format="%H:%M",
            errors="coerce"
        ).dt.hour

        demand = demand.dropna(subset=["hour"])

        if not demand.empty:

            demand["hour"] = demand["hour"].astype(int)

            hourly = (
                demand.groupby("hour")
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

            st.markdown("### Hourly Demand Details")

            st.dataframe(
                hourly,
                use_container_width=True,
                hide_index=True
            )

            st.info(
                "This analysis identifies observed demand patterns. "
                "Reliable future forecasting requires historical "
                "records across multiple dates."
            )

        else:
            st.warning(
                "Time values could not be interpreted."
            )

    else:
        st.info("Upload a dataset to analyse demand.")


# ============================================================
# SMART INSIGHTS
# ============================================================

elif page == "Smart Insights":

    st.title("Smart Insights")

    st.caption(
        "Six intelligent analysis sections that turn ticket "
        "records into useful operational observations."
    )

    if not data.empty:

        total_tickets = len(data)
        total_passengers = data["passengers"].sum()
        total_revenue = data["collected"].sum()
        total_uncollected = data["uncollected"].sum()

        routes = (
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

        busiest = routes.iloc[0]

        st.success(
            f"Highest ticket activity: {busiest['route']} "
            f"with {int(busiest['Tickets'])} tickets."
        )

        st.write(
            "Recommendation: Review passenger demand on high-activity "
            "routes when planning bus frequency and schedules."
        )

        fig = px.bar(
            routes.head(10).sort_values("Tickets"),
            x="Tickets",
            y="route",
            orientation="h",
            title="High-Demand Routes",
            text="Tickets",
            color_discrete_sequence=[BURGUNDY]
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

        lowest = routes.sort_values("Tickets").iloc[0]

        st.info(
            f"Lowest recorded ticket activity: {lowest['route']} "
            f"with {int(lowest['Tickets'])} tickets."
        )

        st.write(
            "Recommendation: Review route usage and passenger "
            "requirements before making operational changes."
        )

        st.dataframe(
            routes,
            use_container_width=True,
            hide_index=True
        )

        # 3. REVENUE INTELLIGENCE

        st.markdown(
            "<div class='section-title'>"
            "3. Revenue Intelligence</div>",
            unsafe_allow_html=True
        )

        total_recorded = total_revenue + total_uncollected

        collection_rate = (
            total_revenue / total_recorded * 100
            if total_recorded > 0 else 0
        )

        a, b, c = st.columns(3)

        a.metric("Collected Revenue", money(total_revenue))
        b.metric("Uncollected Amount", money(total_uncollected))
        c.metric("Collection Rate", f"{collection_rate:.1f}%")

        revenue_fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Collected", "Uncollected"],
                    values=[
                        total_revenue,
                        total_uncollected
                    ],
                    hole=0.58,
                    marker=dict(
                        colors=[BURGUNDY, GOLD]
                    ),
                    textinfo="label+percent",
                    textfont=dict(color=PLUM, size=13)
                )
            ]
        )

        revenue_fig.update_layout(
            title="Revenue Collection Breakdown"
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

        time_data = time_data.dropna(subset=["hour"])

        if not time_data.empty:

            time_data["hour"] = time_data["hour"].astype(int)

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

            heatmap = (
                time_data.groupby("hour")
                .size()
                .reset_index(name="Tickets")
            )

            fig = px.bar(
                heatmap,
                x="hour",
                y="Tickets",
                title="Hourly Activity Heatmap",
                color="Tickets",
                color_continuous_scale=[
                    "#F8E6E5",
                    "#C77B8C",
                    "#64243D"
                ]
            )

            fig.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="Ticket Count"
            )

            st.plotly_chart(
                style_chart(fig, 360),
                use_container_width=True
            )

            st.write(
                "Recommendation: Consider observed peak hours "
                "when reviewing operational schedules."
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

                threshold = values.mean() + 2 * values.std()

                flagged = data[
                    values > threshold
                ].copy()

                if not flagged.empty:

                    flagged["Detected Metric"] = label

                    flagged["Detected Value"] = (
                        flagged[column]
                    )

                    unusual_records.append(
                        flagged[
                            [
                                "ticket",
                                "route",
                                "date",
                                "Detected Metric",
                                "Detected Value"
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

            st.dataframe(
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
            "Statistical flags are indicators for review. "
            "They do not prove fraud or incorrect transactions."
        )

        # 6. MANAGEMENT RECOMMENDATIONS

        st.markdown(
            "<div class='section-title'>"
            "6. Management Recommendations</div>",
            unsafe_allow_html=True
        )

        recommendations = [
            (
                "Route Planning",
                "Review high-activity routes when planning "
                "bus frequency and service schedules."
            ),
            (
                "Revenue Review",
                "Check uncollected ticket amounts and "
                "reconcile relevant records."
            ),
            (
                "Peak-Hour Planning",
                "Use observed peak-hour activity when "
                "reviewing operational schedules."
            ),
            (
                "Future Data Collection",
                "Collect ticket records across multiple dates "
                "to improve trend analysis and forecasting."
            ),
            (
                "Performance Monitoring",
                "Continue monitoring route-wise passenger "
                "counts and revenue patterns."
            )
        ]

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
            "of available ticket records. It is not a trained "
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

    st.title("AI Website Assistant")

    st.caption(
        "Ask questions about the platform, ticket records, "
        "routes, passengers and revenue."
    )

    st.markdown(
        """
        <div class="card">
            <h3>How can I help you?</h3>
            <p>
                Ask me how to use the dashboard, understand the
                analytics or interpret your uploaded dataset.
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
            return "Please type a question."

        # General platform questions

        if "what is bus analytics" in q:
            return (
                "Bus Analytics is a ticket data analysis platform. "
                "It helps examine ticket records, passenger activity, "
                "route performance and revenue collection. The goal "
                "is to turn raw ticket information into useful "
                "operational insights."
            )

        if "dashboard" in q:
            return (
                "The Dashboard gives an overview of the uploaded "
                "ticket dataset. It displays ticket totals, passenger "
                "counts, collected revenue, booking trends and popular "
                "routes. It helps users understand overall activity "
                "without manually examining every ticket."
            )

        if "route" in q:
            if not data.empty:

                route_counts = (
                    data.groupby("route")
                    .size()
                    .sort_values(ascending=False)
                )

                return (
                    f"The dataset contains {data['route'].nunique()} "
                    f"distinct routes. The highest ticket activity is "
                    f"on {route_counts.index[0]}, with "
                    f"{int(route_counts.iloc[0])} tickets. Open Route "
                    f"Analysis to compare all routes and their "
                    f"performance scores."
                )

            return (
                "Route Analysis compares ticket counts, passenger "
                "counts and revenue for each route."
            )

        if "revenue" in q or "collection" in q:

            if not data.empty:

                return (
                    f"The total collected amount is "
                    f"{money(data['collected'].sum())}. The total "
                    f"uncollected amount is "
                    f"{money(data['uncollected'].sum())}. Open Revenue "
                    f"Analysis to see the collection rate and "
                    f"route-wise comparison."
                )

            return (
                "Revenue Analysis compares collected and "
                "uncollected ticket amounts."
            )

        if "passenger" in q:

            if not data.empty:

                return (
                    f"The dataset contains "
                    f"{int(data['passengers'].sum()):,} passengers. "
                    "Passenger Insights identifies popular boarding "
                    "stops, destinations and passenger activity "
                    "across routes."
                )

            return (
                "Passenger Insights shows passenger counts, "
                "boarding points and popular destinations."
            )

        if "demand" in q or "prediction" in q:

            return (
                "Demand Prediction examines observed ticket activity "
                "by hour and identifies busy periods. Reliable future "
                "forecasting requires more historical dates than "
                "the current dataset provides."
            )

        if "smart insight" in q or "smart analysis" in q:

            return (
                "Smart Insights contains six sections: Smart Demand "
                "Recommendations, Route Intelligence, Revenue "
                "Intelligence, Peak-Hour Intelligence and Heatmap, "
                "Unusual Activity Detection, and Management "
                "Recommendations. These analyse the uploaded "
                "records and provide operational suggestions."
            )

        if "upload" in q or "dataset" in q:

            return (
                "Open Upload Dataset from the navigation menu. "
                "Select your CSV file, preview the records and "
                "click Use This Dataset. The uploaded data will "
                "be used during your current session."
            )

        if "report" in q:

            return (
                "Open Reports to view the dataset summary and "
                "route-wise report. You can download both as CSV files."
            )

        if "ticket" in q:

            return (
                f"The current dataset contains {len(data):,} ticket "
                "records. Open Ticket Records to search and examine "
                "individual records."
                if not data.empty
                else "Upload a ticket dataset to examine records."
            )

        if "objective" in q or "purpose" in q:

            return (
                "The project's objective is to convert bus ticket "
                "records into meaningful information. It supports "
                "route comparison, passenger analysis, revenue "
                "monitoring and operational decision-making."
            )

        if "who created" in q or "team" in q:

            return (
                "This project was developed by CRACKER HEADS."
            )

        return (
            "I can help explain the Bus Analytics platform. "
            "Try asking about the Dashboard, Ticket Records, "
            "Route Analysis, Revenue Analysis, Passenger Insights, "
            "Demand Prediction, Smart Insights or Reports."
        )

    # Display conversation history

    for message in st.session_state.assistant_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # Input box

    question = st.chat_input(
        "Type your question here..."
    )

    if question:

        answer = assistant_answer(question)

        st.session_state.assistant_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        st.session_state.assistant_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

    if st.button("Clear Conversation"):

        st.session_state.assistant_history = []
        st.rerun()

    st.caption(
        "The current assistant uses programmed explanations "
        "and dataset-based answers. It is not connected to a "
        "live generative AI service."
    )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    st.title("Reports")
    st.caption(
        "Generate and download summaries from the ticket dataset."
    )

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

        st.dataframe(
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

        st.dataframe(
            route_report,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Summary Report",
            summary.to_csv(index=False).encode("utf-8"),
            "bus_summary_report.csv",
            "text/csv"
        )

        st.download_button(
            "Download Route Report",
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

    st.title("Upload Dataset")

    st.caption(
        "Upload bus ticket records in CSV format."
    )

    st.markdown(
        """
        <div class="card">
            <h3>Upload your ticket data</h3>
            <p>
                Select a CSV file containing ticket information.
                Preview it before applying it to the dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            uploaded_raw = pd.read_csv(uploaded_file)
            preview = prepare_data(uploaded_raw)

            st.success(
                f"File loaded successfully: "
                f"{len(preview):,} records found."
            )

            st.markdown("### Preview Uploaded Data")

            st.dataframe(
                preview.head(20),
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                "Use This Dataset",
                type="primary"
            ):

                st.session_state.uploaded_raw = uploaded_raw

                st.success(
                    "Dataset applied successfully."
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
        "Uploaded data is available for the current session. "
        "It does not permanently replace the repository CSV."
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

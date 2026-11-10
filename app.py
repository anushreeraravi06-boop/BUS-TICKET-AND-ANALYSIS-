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

# Chart theme
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
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
        ),
        yaxis=dict(
            tickfont=dict(color=PLUM),
            title_font=dict(color=BURGUNDY),
            gridcolor="#EADDE0",
            linecolor="#CDB8BF",
        ),
        legend=dict(font=dict(color=PLUM)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
)

pio.templates["bus_analytics"] = BUS_TEMPLATE
pio.templates.default = "bus_analytics"

# ============================================================
# CUSTOM CSS
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

/* Readable text */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label {{
    color:#382832;
}}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {{
    color:#64243D;
}}

[data-testid="stCaptionContainer"] p {{
    color:#624D57 !important;
}}

/* Keep the approved light theme */
:root, html, body, .stApp,
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

/* Responsive layout */
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
}}

@media (max-width:768px) {{
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
    }}

    .hero h1 {{
        font-size:1.7rem !important;
    }}

    .card {{
        padding:16px !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size:1.3rem !important;
    }}

    [data-testid="stPlotlyChart"] {{
        width:100% !important;
        overflow-x:auto !important;
    }}

    .stButton button,
    .stDownloadButton button {{
        min-height:44px !important;
    }}

    [data-testid="stSidebar"] {{
        min-width:min(86vw,310px) !important;
    }}
}}
</style>
""", unsafe_allow_html=True)


# ============================================================
# LANGUAGE SUPPORT
# ============================================================

LANGUAGES = {
    "English": "en",
    "ಕನ್ನಡ": "kn",
    "हिन्दी": "hi",
}

TRANSLATIONS = {
    "en": {
        "Home": "Home",
        "Ticket Records": "Ticket Records",
        "Dashboard": "Dashboard",
        "Route Analysis": "Route Analysis",
        "Revenue Analysis": "Revenue Analysis",
        "Passenger Insights": "Passenger Insights",
        "Demand Prediction": "Demand Prediction",
        "Smart Insights": "Smart Insights",
        "AI Website Assistant": "AI Website Assistant",
        "Reports": "Reports",
        "Upload Dataset": "Upload Dataset",
        "Welcome": "Welcome to Bus Analytics",
        "Tagline": "Intelligent Bus Ticket Data Platform",
    },
    "kn": {
        "Home": "ಮುಖಪುಟ",
        "Ticket Records": "ಟಿಕೆಟ್ ದಾಖಲೆಗಳು",
        "Dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "Route Analysis": "ಮಾರ್ಗ ವಿಶ್ಲೇಷಣೆ",
        "Revenue Analysis": "ಆದಾಯ ವಿಶ್ಲೇಷಣೆ",
        "Passenger Insights": "ಪ್ರಯಾಣಿಕರ ಮಾಹಿತಿ",
        "Demand Prediction": "ಬೇಡಿಕೆ ಮುನ್ಸೂಚನೆ",
        "Smart Insights": "ಸ್ಮಾರ್ಟ್ ಒಳನೋಟಗಳು",
        "AI Website Assistant": "AI ವೆಬ್‌ಸೈಟ್ ಸಹಾಯಕ",
        "Reports": "ವರದಿಗಳು",
        "Upload Dataset": "ಡೇಟಾಸೆಟ್ ಅಪ್‌ಲೋಡ್",
        "Welcome": "ಬಸ್ ಅನಾಲಿಟಿಕ್ಸ್‌ಗೆ ಸ್ವಾಗತ",
        "Tagline": "ಬುದ್ಧಿವಂತ ಬಸ್ ಟಿಕೆಟ್ ಡೇಟಾ ವೇದಿಕೆ",
    },
    "hi": {
        "Home": "होम",
        "Ticket Records": "टिकट रिकॉर्ड",
        "Dashboard": "डैशबोर्ड",
        "Route Analysis": "रूट विश्लेषण",
        "Revenue Analysis": "राजस्व विश्लेषण",
        "Passenger Insights": "यात्री जानकारी",
        "Demand Prediction": "मांग पूर्वानुमान",
        "Smart Insights": "स्मार्ट इनसाइट्स",
        "AI Website Assistant": "AI वेबसाइट सहायक",
        "Reports": "रिपोर्ट",
        "Upload Dataset": "डेटासेट अपलोड",
        "Welcome": "बस एनालिटिक्स में आपका स्वागत है",
        "Tagline": "बुद्धिमान बस टिकट डेटा प्लेटफॉर्म",
    },
}


def tr(key):
    language = st.session_state.get("language", "en")
    return TRANSLATIONS.get(language, {}).get(
        key,
        TRANSLATIONS["en"].get(key, key)
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def safe_number(series):
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.strip(),
        errors="coerce"
    ).fillna(0)


def clean_columns(df):
    df = df.copy()
    df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    aliases = {
        "waybill_number": "waybill",
        "ticket_number": "ticket",
        "from_stop": "from",
        "to_stop": "to",
        "total_psgr": "passengers",
        "total_passengers": "passengers",
        "coll_amt": "collected",
        "collected_amount": "collected",
        "uncoll_amt": "uncollected",
        "uncollected_amount": "uncollected",
    }

    df = df.rename(columns=aliases)

    required = [
        "waybill", "ticket", "from", "to", "date",
        "time", "passengers", "collected", "uncollected"
    ]

    for column in required:
        if column not in df.columns:
            df[column] = None

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        dayfirst=True
    )

    df["time"] = df["time"].astype(str).str.strip()

    df["passengers"] = safe_number(df["passengers"])
    df["collected"] = safe_number(df["collected"])
    df["uncollected"] = safe_number(df["uncollected"])

    for column in ["waybill", "ticket", "from", "to"]:
        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    df["route"] = df["from"] + " → " + df["to"]

    df = df[
        required + ["route"]
    ]

    return df


@st.cache_data
def load_data(path):
    try:
        if Path(path).exists():
            raw = pd.read_csv(path)
            return clean_columns(raw)
    except Exception as error:
        st.error(f"Could not load dataset: {error}")

    return pd.DataFrame(
        columns=[
            "waybill", "ticket", "from", "to", "date",
            "time", "passengers", "collected",
            "uncollected", "route"
        ]
    )


def style_chart(fig, height=380):
    fig.update_layout(
        template="bus_analytics",
        height=height,
        margin=dict(l=15, r=15, t=55, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PLUM),
    )
    return fig


def image_path(name):
    path = ROOT / name
    return path if path.exists() else None


# ============================================================
# LOAD DATASET
# ============================================================

data = load_data(str(DATA_FILE))

if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

if st.session_state.uploaded_data is not None:
    data = st.session_state.uploaded_data.copy()


# ============================================================
# SIDEBAR AND NAVIGATION
# ============================================================

PAGES = [
    "Home",
    "Ticket Records",
    "Dashboard",
    "Route Analysis",
    "Revenue Analysis",
    "Passenger Insights",
    "Demand Prediction",
    "Smart Insights",
    "AI Website Assistant",
    "Reports",
    "Upload Dataset",
]

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "language" not in st.session_state:
    st.session_state.language = "en"

with st.sidebar:
    logo = image_path("logo.png.jpeg")

    if logo:
        st.image(str(logo), use_container_width=True)

    st.markdown(
        "<h2 style='color:#64243D;text-align:center;'>BUS ANALYTICS</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#8B737D;'>CRACKER HEADS</p>",
        unsafe_allow_html=True
    )

    st.divider()

    selected_language = st.selectbox(
        "🌐 Language / ಭಾಷೆ / भाषा",
        options=["English", "ಕನ್ನಡ", "हिन्दी"],
        index=["en", "kn", "hi"].index(
            st.session_state.language
        )
    )

    st.session_state.language = LANGUAGES[selected_language]

    st.markdown("### Navigation")

    for item in PAGES:
        if st.button(
            tr(item),
            key=f"nav_{item}",
            use_container_width=True
        ):
            st.session_state.page = item

    st.divider()

    st.caption("Created by CRACKER HEADS")

page = st.session_state.page


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">BOOK • ANALYZE • PREDICT</div>
            <h1>{tr("Welcome")}</h1>
            <p>{tr("Tagline")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    banner = image_path("bus_banner.png.jpeg")

    if banner:
        st.image(
            str(banner),
            use_container_width=True
        )

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
            f"{int(data.passengers.sum()):,}"
        )
        c3.metric(
            "Collected Revenue",
            money(data.collected.sum())
        )
        c4.metric(
            "Uncollected Amount",
            money(data.uncollected.sum())
        )
    else:
        st.info(
            "No ticket dataset is currently available. "
            "Use Upload Dataset to add a CSV file."
        )

    st.markdown(
        "<div class='section-title'>Explore Platform Features</div>",
        unsafe_allow_html=True
    )

    feature_columns = st.columns(3)

    features = [
        (
            "🎫 Ticket Records",
            "Search, filter and review ticket information."
        ),
        (
            "📊 Dashboard",
            "View key ticket, passenger and revenue statistics."
        ),
        (
            "🛣️ Route Analysis",
            "Compare routes and understand route performance."
        ),
        (
            "💰 Revenue Analysis",
            "Review collected and uncollected amounts."
        ),
        (
            "👥 Passenger Insights",
            "Explore passenger activity and boarding points."
        ),
        (
            "🔮 Demand Prediction",
            "Review observed demand patterns in the dataset."
        ),
    ]

    for index, feature in enumerate(features):
        with feature_columns[index % 3]:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{feature[0]}</h3>
                    <p>{feature[1]}</p>
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
    st.title("Ticket Records")
    st.caption(
        "Search and filter the uploaded bus ticket dataset."
    )

    if not data.empty:
        filtered = data.copy()

        left, middle, right = st.columns(3)

        with left:
            search_text = st.text_input(
                "Search ticket, waybill or stop"
            )

        with middle:
            route_options = ["All Routes"] + sorted(
                filtered["route"].dropna().unique().tolist()
            )

            selected_route = st.selectbox(
                "Select Route",
                route_options
            )

        with right:
            available_dates = filtered["date"].dropna()

            if not available_dates.empty:
                min_date = available_dates.min().date()
                max_date = available_dates.max().date()

                date_range = st.date_input(
                    "Select Date Range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
            else:
                date_range = None

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

        if date_range and len(date_range) == 2:
            start_date, end_date = date_range

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
                "collected": "Collected Amount (₹)",
                "uncollected": "Uncollected Amount (₹)",
                "route": "Route",
            }
        )

        st.write(f"**{len(filtered):,} records found**")

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Filtered Records (CSV)",
            filtered.to_csv(index=False).encode("utf-8"),
            "ticket_records.csv",
            "text/csv"
        )

    else:
        st.info(
            "Upload a CSV dataset to view ticket records."
        )


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
        b.metric(
            "Passengers",
            f"{int(data.passengers.sum()):,}"
        )
        c.metric(
            "Collected",
            money(data.collected.sum())
        )
        d.metric(
            "Uncollected",
            money(data.uncollected.sum())
        )

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
        st.info(
            "Upload your ticket CSV to see the dashboard."
        )


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

        st.plotly_chart(
            style_chart(fig, 520),
            use_container_width=True
        )

        st.markdown(
            "<div class='section-title'>Route Performance Score</div>",
            unsafe_allow_html=True
        )

        score_df = routes.copy()

        def normalise(series):
            low = series.min()
            high = series.max()

            if high == low:
                return pd.Series(
                    [50.0] * len(series),
                    index=series.index
                )

            return (series - low) / (high - low) * 100

        score_df["Ticket Score"] = normalise(
            score_df["Tickets"]
        )

        score_df["Passenger Score"] = normalise(
            score_df["Passengers"]
        )

        score_df["Revenue Score"] = normalise(
            score_df["Revenue"]
        )

        score_df["Performance Score"] = (
            score_df["Ticket Score"] * .35
            + score_df["Passenger Score"] * .35
            + score_df["Revenue Score"] * .30
        ).round(1)

        score_df = score_df.sort_values(
            "Performance Score",
            ascending=False
        )

        best = score_df.iloc[0]

        st.success(
            f"Top-performing route in this dataset: "
            f"{best['route']} — {best['Performance Score']:.1f}/100"
        )

        st.caption(
            "This is a relative comparison within the uploaded dataset: "
            "35% ticket volume, 35% passengers and 30% collected revenue. "
            "It is not an official service-quality rating."
        )

        st.dataframe(
            score_df[
                [
                    "route",
                    "Tickets",
                    "Passengers",
                    "Revenue",
                    "Performance Score"
                ]
            ].rename(
                columns={
                    "route": "Route",
                    "Revenue": "Collected Revenue (₹)"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

        score_chart = px.bar(
            score_df.head(10).sort_values("Performance Score"),
            x="Performance Score",
            y="route",
            orientation="h",
            title="Top 10 Routes by Performance Score",
            text="Performance Score",
            color_discrete_sequence=[ROSE]
        )

        score_chart.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        score_chart.update_layout(
            yaxis_title="",
            xaxis_title="Relative score out of 100",
            xaxis_range=[0, 115],
            margin=dict(l=12, r=45, t=55, b=20)
        )

        st.plotly_chart(
            style_chart(score_chart, 400),
            use_container_width=True
        )

    else:
        st.info(
            "Upload your ticket CSV to analyse routes."
        )


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

        revenue = (
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
            revenue,
            x="route",
            y=["Collected", "Uncollected"],
            barmode="group",
            title="Revenue by Route",
            color_discrete_sequence=[BURGUNDY, GOLD]
        )

        fig.update_layout(
            height=430,
            margin=dict(t=55, l=10, r=10, b=100),
            xaxis_title="",
            legend_title_text="Amount"
        )

        st.plotly_chart(
            style_chart(fig, 430),
            use_container_width=True
        )

    else:
        st.info(
            "Upload your ticket CSV to analyse revenue."
        )


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
            style_chart(fig, 430),
            use_container_width=True
        )

        boarding = (
            data.groupby("from")["passengers"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        boarding.columns = ["Boarding Stop", "Passengers"]

        st.markdown(
            "<div class='section-title'>Top Boarding Stops</div>",
            unsafe_allow_html=True
        )

        st.dataframe(
            boarding,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "Upload your ticket CSV to view passenger insights."
        )


# ============================================================
# DEMAND PREDICTION
# ============================================================

elif page == "Demand Prediction":
    st.title("Demand Prediction")
    st.caption(
        "Explore demand patterns from the available ticket records."
    )

    if not data.empty:
        hourly = data.copy()

        hourly["hour"] = pd.to_datetime(
            hourly["time"],
            format="%H:%M:%S",
            errors="coerce"
        ).dt.hour

        missing_hours = hourly["hour"].isna()

        hourly.loc[missing_hours, "hour"] = pd.to_datetime(
            hourly.loc[missing_hours, "time"],
            format="%H:%M",
            errors="coerce"
        ).dt.hour

        hourly = hourly.dropna(subset=["hour"])
        hourly["hour"] = hourly["hour"].astype(int)

        if not hourly.empty:
            hourly_summary = (
                hourly.groupby("hour")
                .agg(
                    Tickets=("ticket", "count"),
                    Passengers=("passengers", "sum")
                )
                .reset_index()
            )

            fig = px.line(
                hourly_summary,
                x="hour",
                y="Tickets",
                markers=True,
                title="Ticket Activity by Hour",
                color_discrete_sequence=[BURGUNDY]
            )

            st.plotly_chart(
                style_chart(fig, 400),
                use_container_width=True
            )

            peak = hourly_summary.sort_values(
                "Tickets",
                ascending=False
            ).iloc[0]

            st.success(
                f"Busiest recorded hour: {int(peak['hour']):02d}:00 "
                f"with {int(peak['Tickets'])} tickets."
            )

            st.caption(
                "This page describes observed activity. "
                "The uploaded dataset does not contain enough dates "
                "to train a reliable future-demand forecasting model."
            )

        else:
            st.warning(
                "The time column does not contain readable time values."
            )

    else:
        st.info(
            "Upload your ticket CSV to explore demand."
        )
        # ============================================================
# SMART INSIGHTS
# ============================================================

elif page == "Smart Insights":
    st.title("Smart Insights")
    st.caption(
        "Data-driven observations and recommendations "
        "based on recorded ticket activity."
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

        # 1. Smart Demand Recommendations
        st.markdown(
            "<div class='section-title'>"
            "1. Smart Demand Recommendations</div>",
            unsafe_allow_html=True
        )

        if not route_summary.empty:
            busiest = route_summary.iloc[0]

            st.success(
                f"Highest recorded ticket activity is on "
                f"{busiest['route']}, with "
                f"{int(busiest['Tickets'])} tickets."
            )

            st.write(
                "Recommendation: Review passenger demand on this "
                "route when planning bus frequency and scheduling."
            )

        # 2. Route Intelligence
        st.markdown(
            "<div class='section-title'>"
            "2. Route Intelligence</div>",
            unsafe_allow_html=True
        )

        if len(route_summary) > 1:
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
                "requirements before making service changes."
            )

        st.dataframe(
            route_summary,
            use_container_width=True,
            hide_index=True
        )

        # 3. Revenue Intelligence
        st.markdown(
            "<div class='section-title'>"
            "3. Revenue Intelligence</div>",
            unsafe_allow_html=True
        )

        total_recorded = total_revenue + total_uncollected

        if total_recorded > 0:
            collection_rate = (
                total_revenue / total_recorded
            ) * 100
        else:
            collection_rate = 0

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

        if total_uncollected > 0:
            st.warning(
                "There are uncollected amounts in the uploaded "
                "records. Review the corresponding transactions."
            )
        else:
            st.success(
                "No uncollected amount is recorded in this dataset."
            )

        # 4. Peak-Hour Intelligence
        st.markdown(
            "<div class='section-title'>"
            "4. Peak-Hour Intelligence</div>",
            unsafe_allow_html=True
        )

        time_data = data.copy()

        time_data["hour"] = pd.to_datetime(
            time_data["time"],
            format="%H:%M:%S",
            errors="coerce"
        ).dt.hour

        missing = time_data["hour"].isna()

        time_data.loc[missing, "hour"] = pd.to_datetime(
            time_data.loc[missing, "time"],
            format="%H:%M",
            errors="coerce"
        ).dt.hour

        time_data = time_data.dropna(subset=["hour"])

        if not time_data.empty:
            time_data["hour"] = (
                time_data["hour"].astype(int)
            )

            hourly_summary = (
                time_data.groupby("hour")
                .agg(
                    Tickets=("ticket", "count"),
                    Passengers=("passengers", "sum")
                )
                .reset_index()
            )

            peak_hour = hourly_summary.sort_values(
                "Tickets",
                ascending=False
            ).iloc[0]

            st.success(
                f"Peak recorded hour: "
                f"{int(peak_hour['hour']):02d}:00"
            )

            fig = px.bar(
                hourly_summary,
                x="hour",
                y="Tickets",
                title="Hourly Ticket Activity",
                color_discrete_sequence=[ROSE],
                text="Tickets"
            )

            fig.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            st.plotly_chart(
                style_chart(fig, 380),
                use_container_width=True
            )

            st.write(
                "Recommendation: Consider reviewing the busiest "
                "recorded hours while planning operations."
            )
        else:
            st.warning(
                "Hourly analysis is unavailable because the time "
                "values could not be interpreted."
            )

        # 5. Unusual Activity Detection
        st.markdown(
            "<div class='section-title'>"
            "5. Unusual Activity Detection</div>",
            unsafe_allow_html=True
        )

        unusual_found = False

        for column, label in [
            ("passengers", "Passenger count"),
            ("collected", "Collected amount")
        ]:
            values = data[column]

            if len(values) >= 4 and values.std() > 0:
                mean_value = values.mean()
                std_value = values.std()

                unusual = data[
                    values > mean_value + (2 * std_value)
                ]

                if not unusual.empty:
                    unusual_found = True

                    st.warning(
                        f"{len(unusual)} record(s) have unusually "
                        f"high {label.lower()} compared with the "
                        f"dataset average."
                    )

        if not unusual_found:
            st.success(
                "No unusually high values were identified "
                "using the selected statistical check."
            )

        st.caption(
            "These are statistical flags for review, not proof "
            "of fraud or incorrect transactions."
        )

        # 6. Management Recommendations
        st.markdown(
            "<div class='section-title'>"
            "6. Management Recommendations</div>",
            unsafe_allow_html=True
        )

        recommendations = []

        if not route_summary.empty:
            recommendations.append(
                "Review high-activity routes when planning "
                "service frequency."
            )

        if total_uncollected > 0:
            recommendations.append(
                "Check uncollected ticket amounts and "
                "reconcile the relevant records."
            )

        if not time_data.empty:
            recommendations.append(
                "Use observed peak-hour activity when "
                "reviewing operational schedules."
            )

        recommendations.append(
            "Continue collecting data across multiple dates "
            "to improve trend analysis and future forecasting."
        )

        for number, recommendation in enumerate(
            recommendations,
            start=1
        ):
            st.markdown(
                f"""
                <div class="card" style="margin-bottom:10px;">
                    <h3>Recommendation {number}</h3>
                    <p>{recommendation}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.caption(
            "Smart Insights uses statistical and rule-based "
            "analysis of the uploaded records. It is not a "
            "trained machine-learning model."
        )

    else:
        st.info(
            "Upload your ticket dataset to generate smart insights."
        )


# ============================================================
# AI WEBSITE ASSISTANT
# ============================================================

elif page == "AI Website Assistant":
    st.title("AI Website Assistant")

    st.caption(
        "Ask questions about the Bus Analytics platform "
        "and its available features."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    FAQ = {
        "what is bus analytics":
            "Bus Analytics is a ticket data analysis platform "
            "that helps users explore ticket records, routes, "
            "passenger activity and revenue.",

        "what is dashboard":
            "The Dashboard displays key statistics such as "
            "total tickets, passengers, collected revenue "
            "and ticket activity.",

        "what is route analysis":
            "Route Analysis compares routes using ticket "
            "counts, passenger counts and collected revenue.",

        "what is revenue analysis":
            "Revenue Analysis shows collected amounts, "
            "uncollected amounts and revenue by route.",

        "what is passenger insights":
            "Passenger Insights helps identify passenger "
            "activity, popular routes and boarding stops.",

        "what is demand prediction":
            "Demand Prediction displays observed hourly "
            "ticket activity. Reliable future forecasting "
            "requires more historical dates.",

        "what is smart insights":
            "Smart Insights provides statistical observations "
            "and recommendations based on the uploaded dataset.",

        "how to upload":
            "Open Upload Dataset, select your CSV file and "
            "click the upload button to load it.",

        "who created":
            "This project was created by CRACKER HEADS.",

        "what is this project":
            "This project analyses bus ticket records to "
            "understand route activity, passenger demand "
            "and revenue patterns."
    }

    def get_answer(question):
        question_lower = question.lower().strip()

        if not question_lower:
            return "Please enter a question."

        for keyword, answer in FAQ.items():
            if keyword in question_lower:
                return answer

        if "ticket" in question_lower:
            return (
                "Open Ticket Records to search and filter "
                "the available ticket information."
            )

        if "route" in question_lower:
            return (
                "Open Route Analysis to compare routes "
                "using ticket and passenger information."
            )

        if "revenue" in question_lower or "money" in question_lower:
            return (
                "Open Revenue Analysis to view collected "
                "and uncollected amounts."
            )

        if "passenger" in question_lower:
            return (
                "Open Passenger Insights to explore "
                "passenger counts and boarding stops."
            )

        if "upload" in question_lower or "dataset" in question_lower:
            return (
                "Open Upload Dataset and select your CSV file."
            )

        if "report" in question_lower:
            return (
                "Open Reports to view and download "
                "available analysis summaries."
            )

        return (
            "I can help you understand the Bus Analytics "
            "platform. Try asking about tickets, routes, "
            "revenue, passengers, demand prediction, "
            "smart insights or uploading a dataset."
        )

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input(
        "Ask something about Bus Analytics..."
    )

    if user_question:
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        with st.chat_message("user"):
            st.markdown(user_question)

        answer = get_answer(user_question)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.caption(
        "Note: This assistant currently uses predefined "
        "answers and keyword matching. It is not connected "
        "to a generative AI API."
    )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":
    st.title("Reports")
    st.caption(
        "View and download a summary of the uploaded ticket dataset."
    )

    if not data.empty:

        total_tickets = len(data)
        total_passengers = int(data["passengers"].sum())
        collected = float(data["collected"].sum())
        uncollected = float(data["uncollected"].sum())

        report = pd.DataFrame(
            {
                "Metric": [
                    "Total Tickets",
                    "Total Passengers",
                    "Total Routes",
                    "Total Collected Revenue",
                    "Total Uncollected Amount",
                    "Total Recorded Amount",
                ],
                "Value": [
                    total_tickets,
                    total_passengers,
                    data["route"].nunique(),
                    collected,
                    uncollected,
                    collected + uncollected,
                ]
            }
        )

        st.markdown(
            "<div class='section-title'>"
            "Dataset Summary</div>",
            unsafe_allow_html=True
        )

        st.dataframe(
            report,
            use_container_width=True,
            hide_index=True
        )

        st.markdown(
            "<div class='section-title'>"
            "Route Summary</div>",
            unsafe_allow_html=True
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

        st.dataframe(
            route_report,
            use_container_width=True,
            hide_index=True
        )

        csv_report = route_report.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Route Report",
            data=csv_report,
            file_name="bus_route_report.csv",
            mime="text/csv"
        )

        st.download_button(
            "Download Dataset Summary",
            data=report.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="bus_dataset_summary.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "Upload a dataset to generate reports."
        )


# ============================================================
# UPLOAD DATASET
# ============================================================

elif page == "Upload Dataset":
    st.title("Upload Dataset")

    st.caption(
        "Upload your bus ticket records in CSV format."
    )

    st.markdown(
        """
        <div class="card">
            <h3>📂 Upload your ticket data</h3>
            <p>
                Choose a CSV file containing ticket information.
                The platform will prepare it for analysis.
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

            uploaded_clean = clean_columns(
                uploaded_raw
            )

            st.success(
                f"File loaded successfully: "
                f"{len(uploaded_clean):,} records found."
            )

            st.markdown(
                "<div class='section-title'>"
                "Preview Uploaded Data</div>",
                unsafe_allow_html=True
            )

            st.dataframe(
                uploaded_clean.head(20),
                use_container_width=True,
                hide_index=True
            )

            if st.button(
                "Use This Dataset",
                type="primary"
            ):
                st.session_state.uploaded_data = (
                    uploaded_clean
                )

                st.success(
                    "Dataset applied successfully. "
                    "You can now explore the dashboard."
                )

                st.rerun()

        except Exception as error:
            st.error(
                f"Unable to read this CSV file: {error}"
            )

    if st.session_state.uploaded_data is not None:
        st.success(
            "A session-uploaded dataset is currently active."
        )

        if st.button("Restore Repository Dataset"):
            st.session_state.uploaded_data = None
            st.rerun()

    st.caption(
        "Uploaded data is stored in the current Streamlit "
        "session. It does not permanently replace the "
        "repository CSV file."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        padding:15px 5px;
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
            color:#8B737D;
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

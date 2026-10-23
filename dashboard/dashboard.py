import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="assets/bike.png" if False else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY       = "#0d1b2a"
NAVY_MID   = "#1b2f4b"
NAVY_LIGHT = "#243c5c"
ACCENT     = "#3b82f6"        
TEXT_MAIN  = "#ffffff"        
TEXT_SUB   = "#cbd5e1"      
BORDER     = "#1e3a5f"
CHART_BG   = "#111e2e"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
}}

/* Main App Container */
.stApp {{ 
    background-color: {NAVY} !important; 
    color: {TEXT_MAIN} !important;
}}
.main .block-container {{ padding: 2rem 2.5rem; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {NAVY_MID} !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] * {{ 
    color: {TEXT_MAIN} !important; 
}}

/* Metric Cards & Full Text Contrast Fix */
[data-testid="metric-container"] {{
    background-color: {NAVY_MID} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px;
    padding: 1.1rem 1.4rem;
    opacity: 1 !important;
}}
[data-testid="metric-container"] label,
[data-testid="stMetricLabel"],
[data-testid="metric-container"] [data-testid="stMetricLabel"] div,
[data-testid="metric-container"] p {{
    color: {TEXT_SUB} !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    opacity: 1 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="metric-value"],
[data-testid="stMetricValue"] div {{
    color: {TEXT_MAIN} !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}}

/* Modern & Sleek Tabs Styling */
.stTabs [data-baseweb="tab-list"] {{
    background-color: transparent !important;
    border-bottom: 2px solid {BORDER} !important;
    gap: 16px !important;
    padding: 0px !important;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    color: {TEXT_SUB} !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 10px 16px !important;
    transition: all 0.2s ease-in-out;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {TEXT_MAIN} !important;
}}
.stTabs [aria-selected="true"] {{
    background-color: transparent !important;
    color: {TEXT_MAIN} !important;
    border-bottom: 3px solid {ACCENT} !important;
}}

/* Multiselect & Input Boxes Fix */
[data-testid="stMultiSelect"] > div,
[data-testid="stDateInput"] input {{
    background-color: #ffffff !important;
    color: #0f172a !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
}}

/* Custom Multiselect Badges */
[data-baseweb="tag"] {{
    background-color: {NAVY_LIGHT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 4px !important;
}}
[data-baseweb="tag"] * {{
    color: {TEXT_MAIN} !important;
}}

/* Divider */
hr {{ border-color: {BORDER} !important; margin: 1.2rem 0; }}

/* Titles & Subtitles */
.sec-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {TEXT_MAIN};
    margin-bottom: 0.2rem;
}}
.sec-sub {{
    font-size: 0.82rem;
    color: {TEXT_SUB};
    margin-bottom: 1.2rem;
}}

/* Insight box */
.insight {{
    background-color: {NAVY_LIGHT};
    border-left: 4px solid {ACCENT};
    border-radius: 0 6px 6px 0;
    padding: 12px 16px;
    margin-top: 14px;
    color: {TEXT_SUB};
    font-size: 0.85rem;
    line-height: 1.6;
}}
.insight b {{ color: {TEXT_MAIN}; }}
</style>
""", unsafe_allow_html=True)

plt.rcParams.update({
    "figure.facecolor":  CHART_BG,
    "axes.facecolor":    CHART_BG,
    "axes.edgecolor":    BORDER,
    "axes.labelcolor":   TEXT_SUB,
    "axes.titlecolor":   TEXT_MAIN,
    "axes.titlesize":    12,
    "axes.titleweight":  "600",
    "axes.labelsize":    9,
    "xtick.color":       TEXT_SUB,
    "ytick.color":       TEXT_SUB,
    "xtick.labelsize":   8,
    "ytick.labelsize":   8,
    "grid.color":        BORDER,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "text.color":        TEXT_MAIN,
    "legend.facecolor":  NAVY_MID,
    "legend.edgecolor":  BORDER,
    "legend.labelcolor": TEXT_SUB,
    "legend.fontsize":   8,
    "font.family":       "DejaVu Sans",
})

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["dteday"]      = pd.to_datetime(df["dteday"])
    df["month_name"]  = df["dteday"].dt.strftime("%b")
    df["month_order"] = df["dteday"].dt.month
    df["day_name"]    = df["dteday"].dt.day_name()
    df["year_label"]  = df["yr"].map({0: "2011", 1: "2012"})
    df["temp_c"]      = df["temp"] * 41
    df["hum_pct"]     = df["hum"] * 100
    df["windspeed_kph"] = df["windspeed"] * 67
    return df

df_raw = load_data()

with st.sidebar:
    st.markdown("### Bike Sharing Dashboard")
    st.markdown(
        f"<span style='color:{TEXT_SUB};font-size:0.8rem;'>Capital Bikeshare · 2011–2012</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    min_d = df_raw["dteday"].min().date()
    max_d = df_raw["dteday"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_d, max_d),
        min_value=min_d,
        max_value=max_d,
    )

    st.markdown("---")

    all_seasons = ["Springer", "Summer", "Fall", "Winter"]
    sel_seasons = st.multiselect("Season", all_seasons, default=all_seasons)

    all_weather = ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Snow/Rain"]
    sel_weather = st.multiselect("Weather", all_weather, default=all_weather)

    st.markdown("---")

    day_type = st.radio("Day type", ["All", "Workday", "Holiday"], index=0)

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    s_date, e_date = date_range
else:
    s_date, e_date = min_d, max_d

df = df_raw[
    (df_raw["dteday"].dt.date >= s_date) &
    (df_raw["dteday"].dt.date <= e_date)
].copy()

if sel_seasons:
    df = df[df["season_label"].isin(sel_seasons)]
if sel_weather:
    df = df[df["weathersit_label"].isin(sel_weather)]
if day_type == "Workday":
    df = df[df["workingday"] == 1]
elif day_type == "Holiday":
    df = df[df["workingday"] == 0]

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

st.markdown(f"""
<div style="padding: 1rem 0 0.8rem 0; border-bottom: 1px solid {BORDER}; margin-bottom: 1.5rem;">
    <h1 style="color:{TEXT_MAIN}; font-size:1.75rem; font-weight:700; margin:0; letter-spacing:-0.3px;">
        Bike Sharing Dashboard
    </h1>
    <p style="color:{TEXT_SUB}; font-size:0.85rem; margin:0.3rem 0 0 0;">
        Capital Bikeshare · Washington D.C. · January 2011 – December 2012
    </p>
</div>
""", unsafe_allow_html=True)

total    = int(df["cnt"].sum())
avg_day  = int(df["cnt"].mean())
casual   = int(df["casual"].sum())
reg      = int(df["registered"].sum())
peak_val = int(df["cnt"].max())

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Rentals",    f"{total:,}")
c2.metric("Daily Average",    f"{avg_day:,}")
c3.metric("Casual Users",     f"{casual:,}")
c4.metric("Registered Users", f"{reg:,}")
c5.metric("Peak Day",         f"{peak_val:,}")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "Time Trend",
    "Season & Weather",
    "User Segments",
    "Environmental Factors",
])

with tab1:
    st.markdown('<p class="sec-title">Business Question 1 — How has bike rental demand changed over time?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Daily rental volume with 30-day moving average, monthly breakdown, and year-over-year comparison.</p>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(12, 3.8))
    ax.fill_between(df["dteday"], df["cnt"], alpha=0.15, color=ACCENT)
    ax.plot(df["dteday"], df["cnt"], color=ACCENT, linewidth=1, alpha=0.7)
    if len(df) >= 30:
        roll = df.set_index("dteday")["cnt"].rolling(30).mean()
        ax.plot(roll.index, roll.values, color=TEXT_MAIN, linewidth=1.8,
                linestyle="--", label="30-day avg")
        ax.legend()
    ax.set_title("Daily Rentals")
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    col_a, col_b = st.columns(2)

    with col_a:
        monthly = (
            df.groupby(["month_order", "month_name"])["cnt"]
            .mean().reset_index().sort_values("month_order")
        )
        fig2, ax2 = plt.subplots(figsize=(6, 3.8))
        ax2.bar(monthly["month_name"], monthly["cnt"],
                color=ACCENT, alpha=0.85, width=0.6, edgecolor=CHART_BG)
        ax2.set_title("Average Rentals by Month")
        ax2.set_xlabel("Month")
        ax2.set_ylabel("Avg Count")
        ax2.grid(axis="y", alpha=0.4)
        for bar in ax2.patches:
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 40,
                f"{int(bar.get_height()):,}",
                ha="center", va="bottom", fontsize=6.5, color=TEXT_SUB,
            )
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    with col_b:
        if df["year_label"].nunique() > 1:
            yearly = (
                df.groupby(["year_label", "month_order", "month_name"])["cnt"]
                .mean().reset_index().sort_values("month_order")
            )
            fig3, ax3 = plt.subplots(figsize=(6, 3.8))
            colors_yr = [ACCENT, TEXT_MAIN]
            for i, yr in enumerate(["2011", "2012"]):
                sub = yearly[yearly["year_label"] == yr]
                if not sub.empty:
                    ax3.plot(sub["month_name"], sub["cnt"],
                             marker="o", markersize=4, label=yr,
                             color=colors_yr[i], linewidth=1.8)
            ax3.set_title("Year-over-Year Comparison")
            ax3.set_xlabel("Month")
            ax3.set_ylabel("Avg Count")
            ax3.legend()
            ax3.grid(alpha=0.4)
            fig3.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> Rentals grew significantly from 2011 to 2012.
    Demand peaks between June and September, with the lowest usage in January and February.
    The 30-day moving average clearly shows a seasonal growth pattern.
    </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown('<p class="sec-title">Business Question 2 — How do season and weather conditions affect rental demand?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Average daily rentals segmented by season, weather condition, and their interaction.</p>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    with col_c:
        order_map = {"Springer": 1, "Summer": 2, "Fall": 3, "Winter": 4}
        s_agg = (
            df.groupby("season_label")["cnt"].mean().reset_index()
            .rename(columns={"cnt": "avg"})
        )
        s_agg["order"] = s_agg["season_label"].map(order_map)
        s_agg = s_agg.sort_values("order")

        colors_bar = [ACCENT if i == s_agg["avg"].argmax() else NAVY_LIGHT
                      for i in range(len(s_agg))]

        fig4, ax4 = plt.subplots(figsize=(5.5, 4))
        bars4 = ax4.bar(s_agg["season_label"], s_agg["avg"],
                        color=colors_bar, edgecolor=CHART_BG, width=0.55)
        ax4.set_title("Average Rentals by Season")
        ax4.set_xlabel("Season")
        ax4.set_ylabel("Avg Count / Day")
        ax4.grid(axis="y", alpha=0.4)
        for bar in bars4:
            ax4.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 50,
                f"{int(bar.get_height()):,}",
                ha="center", va="bottom", fontsize=8.5,
                fontweight="600", color=TEXT_MAIN,
            )
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    with col_d:
        w_agg = (
            df.groupby("weathersit_label")["cnt"].mean().reset_index()
            .rename(columns={"cnt": "avg"})
            .sort_values("avg", ascending=True)
        )
        colors_w = [ACCENT if i == len(w_agg) - 1 else NAVY_LIGHT
                    for i in range(len(w_agg))]

        fig5, ax5 = plt.subplots(figsize=(5.5, 4))
        bars5 = ax5.barh(w_agg["weathersit_label"], w_agg["avg"],
                         color=colors_w, edgecolor=CHART_BG, height=0.45)
        ax5.set_title("Average Rentals by Weather")
        ax5.set_xlabel("Avg Count / Day")
        ax5.grid(axis="x", alpha=0.4)
        for bar in bars5:
            ax5.text(
                bar.get_width() + 50,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width()):,}",
                ha="left", va="center", fontsize=8.5,
                fontweight="600", color=TEXT_MAIN,
            )
        fig5.tight_layout()
        st.pyplot(fig5)
        plt.close(fig5)

    st.markdown(f"<p class='sec-title' style='margin-top:1rem;'>Season × Weather Heatmap</p>", unsafe_allow_html=True)
    pivot = df.pivot_table(
        values="cnt", index="weathersit_label",
        columns="season_label", aggfunc="mean",
    ).reindex(columns=[c for c in all_seasons if c in df["season_label"].unique()])

    fig6, ax6 = plt.subplots(figsize=(9, 3.2))
    sns.heatmap(
        pivot, annot=True, fmt=".0f",
        cmap=sns.light_palette(ACCENT, as_cmap=True),
        ax=ax6, linewidths=0.5, linecolor=NAVY,
        annot_kws={"size": 10, "weight": "600", "color": NAVY},
        cbar_kws={"label": "Avg Rentals"},
    )
    ax6.set_title("Average Rentals: Season × Weather Condition")
    ax6.set_xlabel("Season")
    ax6.set_ylabel("")
    fig6.tight_layout()
    st.pyplot(fig6)
    plt.close(fig6)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> <b>Fall</b> records the highest average daily rentals, followed by Summer.
    Clear weather consistently produces the most rentals across all seasons.
    Rain or snow can reduce demand by up to 60% compared to clear days.
    </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown('<p class="sec-title">Business Question 3 — How do casual and registered users differ in behavior?</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Usage patterns across days of the week and months for each user segment.</p>', unsafe_allow_html=True)

    col_e, col_f = st.columns(2)

    with col_e:
        t_c = int(df["casual"].sum())
        t_r = int(df["registered"].sum())
        fig7, ax7 = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax7.pie(
            [t_c, t_r],
            labels=["Casual", "Registered"],
            autopct="%1.1f%%",
            colors=[NAVY_LIGHT, ACCENT],
            startangle=140,
            wedgeprops={"edgecolor": CHART_BG, "linewidth": 2},
            textprops={"color": TEXT_MAIN, "fontsize": 10},
        )
        for at in autotexts:
            at.set_fontsize(11)
            at.set_fontweight("600")
            at.set_color(TEXT_MAIN)
        ax7.set_title("User Proportion: Casual vs Registered")
        fig7.tight_layout()
        st.pyplot(fig7)
        plt.close(fig7)

    with col_f:
        day_order  = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        day_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        d_agg = (
            df.groupby("day_name")[["casual","registered"]]
            .mean().reindex(day_order).dropna().reset_index()
        )
        short_map = dict(zip(day_order, day_labels))
        x = np.arange(len(d_agg))
        w = 0.38
        fig8, ax8 = plt.subplots(figsize=(6, 4.5))
        ax8.bar(x - w/2, d_agg["casual"],    w, label="Casual",
                color=NAVY_LIGHT, edgecolor=CHART_BG)
        ax8.bar(x + w/2, d_agg["registered"], w, label="Registered",
                color=ACCENT, edgecolor=CHART_BG)
        ax8.set_title("Avg Rentals by Day of Week")
        ax8.set_xlabel("Day")
        ax8.set_ylabel("Avg Count")
        ax8.set_xticks(x)
        ax8.set_xticklabels([short_map.get(d, d) for d in d_agg["day_name"]])
        ax8.legend()
        ax8.grid(axis="y", alpha=0.4)
        fig8.tight_layout()
        st.pyplot(fig8)
        plt.close(fig8)

    st.markdown(f"<p class='sec-title' style='margin-top:1rem;'>Monthly Composition: Casual vs Registered</p>", unsafe_allow_html=True)
    m_user = (
        df.groupby(["month_order","month_name"])[["casual","registered"]]
        .mean().reset_index().sort_values("month_order")
    )
    fig9, ax9 = plt.subplots(figsize=(11, 3.8))
    ax9.stackplot(
        m_user["month_name"],
        m_user["casual"], m_user["registered"],
        labels=["Casual","Registered"],
        colors=[NAVY_LIGHT, ACCENT],
        alpha=0.9,
    )
    ax9.set_title("Monthly Rental Composition by User Type")
    ax9.set_xlabel("Month")
    ax9.set_ylabel("Avg Count")
    ax9.legend(loc="upper left")
    ax9.grid(alpha=0.3)
    fig9.tight_layout()
    st.pyplot(fig9)
    plt.close(fig9)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> <b>Registered users</b> account for ~80% of all rentals and peak on weekdays, suggesting commuter behavior.
    <b>Casual users</b> peak on weekends, indicating recreational use.
    Targeting weekend casual users with membership promotions could increase long-term registered user base.
    </div>""", unsafe_allow_html=True)

with tab4:
    st.markdown('<p class="sec-title">Advanced Analysis — Impact of Environmental Factors</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Correlation between temperature, humidity, wind speed, and rental volume.</p>', unsafe_allow_html=True)

    col_g, col_h = st.columns(2)

    with col_g:
        fig10, ax10 = plt.subplots(figsize=(6, 4.5))
        ax10.scatter(df["temp_c"], df["cnt"],
                     alpha=0.3, s=14, color=ACCENT)
        z = np.polyfit(df["temp_c"], df["cnt"], 1)
        p = np.poly1d(z)
        xl = np.linspace(df["temp_c"].min(), df["temp_c"].max(), 200)
        ax10.plot(xl, p(xl), color=TEXT_MAIN, linewidth=1.8,
                  linestyle="--", label="Linear trend")
        ax10.set_title("Temperature vs Rentals")
        ax10.set_xlabel("Temperature (°C)")
        ax10.set_ylabel("Count")
        ax10.legend()
        ax10.grid(alpha=0.4)
        fig10.tight_layout()
        st.pyplot(fig10)
        plt.close(fig10)

    with col_h:
        fig11, ax11 = plt.subplots(figsize=(6, 4.5))
        ax11.scatter(df["hum_pct"], df["cnt"],
                     alpha=0.3, s=14, color=ACCENT)
        z2 = np.polyfit(df["hum_pct"], df["cnt"], 1)
        p2 = np.poly1d(z2)
        xl2 = np.linspace(df["hum_pct"].min(), df["hum_pct"].max(), 200)
        ax11.plot(xl2, p2(xl2), color=TEXT_MAIN, linewidth=1.8,
                  linestyle="--", label="Linear trend")
        ax11.set_title("Humidity vs Rentals")
        ax11.set_xlabel("Humidity (%)")
        ax11.set_ylabel("Count")
        ax11.legend()
        ax11.grid(alpha=0.4)
        fig11.tight_layout()
        st.pyplot(fig11)
        plt.close(fig11)

    st.markdown(f"<p class='sec-title' style='margin-top:1rem;'>Correlation Matrix</p>", unsafe_allow_html=True)
    corr_rename = {
        "temp_c": "Temp (°C)", "hum_pct": "Humidity (%)",
        "windspeed_kph": "Wind Speed", "casual": "Casual",
        "registered": "Registered", "cnt": "Total",
    }
    corr_df = df[[c for c in corr_rename if c in df.columns]].rename(columns=corr_rename)
    corr_m  = corr_df.corr()

    fig12, ax12 = plt.subplots(figsize=(8, 4.8))
    sns.heatmap(
        corr_m, annot=True, fmt=".2f",
        cmap=sns.diverging_palette(220, 20, as_cmap=True),
        ax=ax12, vmin=-1, vmax=1,
        linewidths=0.5, linecolor=NAVY,
        annot_kws={"size": 9.5, "weight": "600"},
        cbar_kws={"label": "Pearson r"},
    )
    ax12.set_title("Environmental Factors — Correlation Matrix")
    fig12.tight_layout()
    st.pyplot(fig12)
    plt.close(fig12)

    st.markdown("""
    <div class="insight">
    <b>Insight:</b> <b>Temperature</b> has the strongest positive correlation with rentals (r ≈ 0.63).
    <b>Humidity</b> and <b>wind speed</b> show weak negative correlations.
    Fleet availability can be optimized by integrating daily weather forecasts.
    </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div style="border-top:1px solid {BORDER}; margin-top:2rem; padding-top:1rem;
     text-align:center; color:{TEXT_SUB}; font-size:0.76rem;">
    Bike Sharing Dashboard &nbsp;·&nbsp; Capital Bikeshare, Washington D.C.
    &nbsp;·&nbsp; Dicoding Data Analysis Project
</div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, date

# ─────────────────────────────────────────
#  PAGE CONFIG & GLOBAL STYLE
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🚲 Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #0f1117;
    }
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
        border: 1px solid #2e3250;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    [data-testid="metric-container"] label {
        color: #8b92b8 !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #e8eaf6 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        font-size: 0.8rem !important;
    }
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #4f6ef7 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .section-subtext {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
    /* Chart card wrapper */
    .chart-card {
        background: #1e2130;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #2e3250;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, #1a1f3a 0%, #1e2540 100%);
        border-left: 4px solid #4f6ef7;
        border-radius: 0 12px 12px 0;
        padding: 14px 18px;
        margin-top: 10px;
        color: #c5cae9;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #131722 0%, #1a1f35 100%);
        border-right: 1px solid #2e3250;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #e8eaf6;
    }
    /* Divider */
    hr { border-color: #2e3250; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e2130;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #2e3250;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #8b92b8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f6ef7, #8b5cf6) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  MATPLOTLIB DARK THEME
# ─────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#1e2130",
    "axes.facecolor":    "#1e2130",
    "axes.edgecolor":    "#2e3250",
    "axes.labelcolor":   "#c5cae9",
    "axes.titlecolor":   "#e8eaf6",
    "xtick.color":       "#8b92b8",
    "ytick.color":       "#8b92b8",
    "grid.color":        "#2e3250",
    "grid.linestyle":    "--",
    "grid.alpha":        0.6,
    "text.color":        "#e8eaf6",
    "legend.facecolor":  "#252840",
    "legend.edgecolor":  "#2e3250",
    "legend.labelcolor": "#c5cae9",
    "font.family":       "DejaVu Sans",
})

PALETTE = {
    "blue":   "#4f6ef7",
    "purple": "#8b5cf6",
    "teal":   "#14b8a6",
    "amber":  "#f59e0b",
    "rose":   "#f43f5e",
    "green":  "#22c55e",
    "sky":    "#38bdf8",
}

SEASON_COLORS = {
    "Springer": "#38bdf8",
    "Summer":   "#f59e0b",
    "Fall":     "#f43f5e",
    "Winter":   "#8b5cf6",
}

WEATHER_COLORS = {
    "Clear/Partly Cloudy": "#22c55e",
    "Mist/Cloudy":         "#f59e0b",
    "Light Snow/Rain":     "#4f6ef7",
}

# ─────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["month_name"] = df["dteday"].dt.strftime("%b")
    df["month_order"] = df["dteday"].dt.month
    df["day_name"] = df["dteday"].dt.day_name()
    df["year_label"] = df["yr"].map({0: "2011", 1: "2012"})
    # Denormalize temp (Bike Sharing normalized to [0,1] using 41°C as max)
    df["temp_c"] = df["temp"] * 41
    df["hum_pct"] = df["hum"] * 100
    df["windspeed_ms"] = df["windspeed"] * 67  # max 67 km/h
    return df

df_raw = load_data()

# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚲 Bike Sharing")
    st.markdown("**Analisis Data Dicoding**")
    st.markdown("---")

    st.markdown("### 🗓️ Rentang Tanggal")
    min_date = df_raw["dteday"].min().date()
    max_date = df_raw["dteday"].max().date()
    date_range = st.date_input(
        "Pilih periode analisis",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter data berdasarkan rentang tanggal",
    )

    st.markdown("### 🌿 Musim")
    all_seasons = ["Springer", "Summer", "Fall", "Winter"]
    selected_seasons = st.multiselect(
        "Pilih musim",
        options=all_seasons,
        default=all_seasons,
        help="Filter data berdasarkan musim",
    )

    st.markdown("### 🌤️ Cuaca")
    all_weather = ["Clear/Partly Cloudy", "Mist/Cloudy", "Light Snow/Rain"]
    selected_weather = st.multiselect(
        "Pilih kondisi cuaca",
        options=all_weather,
        default=all_weather,
        help="Filter data berdasarkan kondisi cuaca",
    )

    st.markdown("### 📅 Jenis Hari")
    day_type = st.radio(
        "Tampilkan hari",
        options=["Semua Hari", "Hari Kerja", "Hari Libur"],
        index=0,
    )

    st.markdown("---")
    st.markdown(
        "<div style='color:#6b7280;font-size:0.75rem;text-align:center'>"
        "Dataset: Capital Bikeshare<br>Periode: Jan 2011 – Des 2012"
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────
#  APPLY FILTERS
# ─────────────────────────────────────────
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df = df_raw[
    (df_raw["dteday"].dt.date >= start_date) &
    (df_raw["dteday"].dt.date <= end_date)
].copy()

if selected_seasons:
    df = df[df["season_label"].isin(selected_seasons)]
if selected_weather:
    df = df[df["weathersit_label"].isin(selected_weather)]
if day_type == "Hari Kerja":
    df = df[df["workingday"] == 1]
elif day_type == "Hari Libur":
    df = df[df["workingday"] == 0]

# Guard: empty dataframe
if df.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih. Silakan ubah filter Anda.")
    st.stop()

# ─────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1.5rem 0;">
    <div style="font-size:3rem; margin-bottom:0.3rem;">🚲</div>
    <h1 style="background:linear-gradient(90deg,#4f6ef7,#8b5cf6,#f43f5e);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               font-size:2.4rem;font-weight:800;margin:0;">
        Bike Sharing Dashboard
    </h1>
    <p style="color:#6b7280;font-size:1rem;margin-top:0.4rem;">
        Analisis Pola Peminjaman Sepeda · Capital Bikeshare 2011–2012
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  KPI METRICS
# ─────────────────────────────────────────
total_rentals  = int(df["cnt"].sum())
avg_daily      = int(df["cnt"].mean())
total_casual   = int(df["casual"].sum())
total_reg      = int(df["registered"].sum())
peak_day_row   = df.loc[df["cnt"].idxmax()]
peak_day_val   = int(peak_day_row["cnt"])
peak_day_label = peak_day_row["dteday"].strftime("%d %b %Y")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🚲 Total Peminjaman", f"{total_rentals:,}")
with col2:
    st.metric("📅 Rata-rata Harian", f"{avg_daily:,}")
with col3:
    st.metric("👤 Pengguna Kasual", f"{total_casual:,}")
with col4:
    st.metric("✅ Pengguna Terdaftar", f"{total_reg:,}")
with col5:
    st.metric("🏆 Hari Tersibuk", f"{peak_day_val:,}", help=f"Tanggal: {peak_day_label}")

st.markdown("---")

# ─────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren Waktu",
    "🌿 Musim & Cuaca",
    "📊 Pola Pengguna",
    "🌡️ Faktor Lingkungan",
])

# ══════════════════════════════════════════
#  TAB 1 – TREN WAKTU
# ══════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-header">📈 Pertanyaan Bisnis 1: Bagaimana tren peminjaman sepeda dari waktu ke waktu?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtext">Analisis tren harian dan bulanan untuk memahami pertumbuhan penggunaan layanan.</p>', unsafe_allow_html=True)

    # ── 1a. Tren Harian ────────────────────
    fig1, ax1 = plt.subplots(figsize=(12, 4))

    ax1.fill_between(df["dteday"], df["cnt"],
                     alpha=0.15, color=PALETTE["blue"])
    ax1.plot(df["dteday"], df["cnt"],
             color=PALETTE["blue"], linewidth=1.2, alpha=0.8)

    # Rolling average 30 hari
    if len(df) >= 30:
        rolling_avg = df.set_index("dteday")["cnt"].rolling(30).mean()
        ax1.plot(rolling_avg.index, rolling_avg.values,
                 color=PALETTE["rose"], linewidth=2.2,
                 label="Rata-rata 30 Hari", linestyle="--")

    ax1.set_title("Tren Peminjaman Sepeda Harian", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Tanggal", fontsize=10)
    ax1.set_ylabel("Jumlah Peminjaman", fontsize=10)
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.4)
    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

    # ── 1b. Rata-rata per Bulan ─────────────
    col_a, col_b = st.columns(2)

    with col_a:
        monthly = (
            df.groupby(["month_order", "month_name"])["cnt"]
            .mean()
            .reset_index()
            .sort_values("month_order")
        )
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        bars = ax2.bar(
            monthly["month_name"], monthly["cnt"],
            color=[plt.cm.cool(i / 11) for i in range(len(monthly))],
            edgecolor="#2e3250", linewidth=0.5, zorder=3,
        )
        ax2.set_title("Rata-rata Peminjaman per Bulan", fontsize=12, fontweight="bold")
        ax2.set_xlabel("Bulan")
        ax2.set_ylabel("Rata-rata Peminjaman")
        ax2.grid(axis="y", alpha=0.4, zorder=0)
        for bar in bars:
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 50,
                f"{int(bar.get_height()):,}",
                ha="center", va="bottom", fontsize=7, color="#c5cae9",
            )
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    with col_b:
        # Perbandingan 2011 vs 2012
        if "year_label" in df.columns and df["year_label"].nunique() > 1:
            yearly = (
                df.groupby(["year_label", "month_order", "month_name"])["cnt"]
                .mean()
                .reset_index()
                .sort_values("month_order")
            )
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            for yr, color in zip(["2011", "2012"], [PALETTE["sky"], PALETTE["amber"]]):
                subset = yearly[yearly["year_label"] == yr]
                if not subset.empty:
                    ax3.plot(subset["month_name"], subset["cnt"],
                             marker="o", markersize=5,
                             label=yr, color=color, linewidth=2)
            ax3.set_title("Perbandingan Bulanan: 2011 vs 2012", fontsize=12, fontweight="bold")
            ax3.set_xlabel("Bulan")
            ax3.set_ylabel("Rata-rata Peminjaman")
            ax3.legend()
            ax3.grid(alpha=0.4)
            fig3.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)
        else:
            st.info("Data hanya mencakup satu tahun, perbandingan 2011 vs 2012 tidak tersedia.")

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Insight:</strong> Peminjaman sepeda menunjukkan tren pertumbuhan yang signifikan dari 2011 ke 2012.
    Puncak penggunaan terjadi pada pertengahan tahun (Juni–September) yang bertepatan dengan musim panas,
    sementara bulan Januari–Februari mencatat angka paling rendah akibat cuaca dingin.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  TAB 2 – MUSIM & CUACA
# ══════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-header">🌿 Pertanyaan Bisnis 2: Bagaimana musim & cuaca memengaruhi jumlah peminjaman?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtext">Identifikasi kondisi optimal dan kondisi yang menghambat penggunaan sepeda.</p>', unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    # ── 2a. Peminjaman per Musim ────────────
    with col_c:
        season_agg = (
            df.groupby("season_label")["cnt"]
            .agg(["mean", "sum", "count"])
            .reset_index()
            .rename(columns={"mean": "avg", "sum": "total", "count": "days"})
        )
        season_agg = season_agg[season_agg["season_label"].isin(all_seasons)]
        # Sort by season order
        order_map = {"Springer": 1, "Summer": 2, "Fall": 3, "Winter": 4}
        season_agg["order"] = season_agg["season_label"].map(order_map)
        season_agg = season_agg.sort_values("order")

        fig4, ax4 = plt.subplots(figsize=(6, 4.5))
        colors_s = [SEASON_COLORS.get(s, PALETTE["blue"]) for s in season_agg["season_label"]]
        bars4 = ax4.bar(season_agg["season_label"], season_agg["avg"],
                        color=colors_s, edgecolor="#2e3250", linewidth=0.5,
                        width=0.55, zorder=3)
        ax4.set_title("Rata-rata Peminjaman per Musim", fontsize=12, fontweight="bold")
        ax4.set_xlabel("Musim")
        ax4.set_ylabel("Rata-rata Peminjaman/Hari")
        ax4.grid(axis="y", alpha=0.4, zorder=0)
        for bar in bars4:
            ax4.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 60,
                f"{int(bar.get_height()):,}",
                ha="center", va="bottom", fontsize=9, fontweight="bold", color="#e8eaf6",
            )
        fig4.tight_layout()
        st.pyplot(fig4)
        plt.close(fig4)

    # ── 2b. Peminjaman per Cuaca ────────────
    with col_d:
        weather_agg = (
            df.groupby("weathersit_label")["cnt"]
            .agg(["mean", "count"])
            .reset_index()
            .rename(columns={"mean": "avg", "count": "days"})
        )
        fig5, ax5 = plt.subplots(figsize=(6, 4.5))
        colors_w = [WEATHER_COLORS.get(w, PALETTE["blue"]) for w in weather_agg["weathersit_label"]]
        bars5 = ax5.barh(weather_agg["weathersit_label"], weather_agg["avg"],
                         color=colors_w, edgecolor="#2e3250", linewidth=0.5,
                         height=0.5, zorder=3)
        ax5.set_title("Rata-rata Peminjaman per Kondisi Cuaca", fontsize=12, fontweight="bold")
        ax5.set_xlabel("Rata-rata Peminjaman/Hari")
        ax5.grid(axis="x", alpha=0.4, zorder=0)
        for bar in bars5:
            ax5.text(
                bar.get_width() + 60,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width()):,}",
                ha="left", va="center", fontsize=9, fontweight="bold", color="#e8eaf6",
            )
        fig5.tight_layout()
        st.pyplot(fig5)
        plt.close(fig5)

    # ── 2c. Heatmap Musim × Cuaca ───────────
    st.markdown("#### 🔥 Heatmap: Rata-rata Peminjaman berdasarkan Musim & Cuaca")
    pivot = df.pivot_table(
        values="cnt",
        index="weathersit_label",
        columns="season_label",
        aggfunc="mean",
    ).reindex(columns=[c for c in all_seasons if c in df["season_label"].unique()])

    fig6, ax6 = plt.subplots(figsize=(9, 3.5))
    sns.heatmap(
        pivot, annot=True, fmt=".0f",
        cmap="YlOrRd", ax=ax6,
        linewidths=0.5, linecolor="#1e2130",
        annot_kws={"size": 11, "weight": "bold"},
        cbar_kws={"label": "Rata-rata Peminjaman"},
    )
    ax6.set_title("Heatmap: Musim x Kondisi Cuaca", fontsize=13, fontweight="bold", pad=10)
    ax6.set_xlabel("Musim", fontsize=10)
    ax6.set_ylabel("Kondisi Cuaca", fontsize=10)
    fig6.tight_layout()
    st.pyplot(fig6)
    plt.close(fig6)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Insight:</strong> Musim <strong>Fall (Gugur)</strong> mencatat rata-rata peminjaman tertinggi,
    diikuti musim Panas. Cuaca cerah/sebagian berawan secara konsisten mendorong lebih banyak peminjaman
    di semua musim. Hujan/salju ringan dapat memangkas peminjaman hingga ~60% dibanding hari cerah.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  TAB 3 – POLA PENGGUNA
# ══════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-header">📊 Pertanyaan Bisnis 3: Bagaimana pola peminjaman antara pengguna kasual vs terdaftar?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtext">Analisis perilaku dua segmen pengguna untuk strategi pemasaran yang tepat sasaran.</p>', unsafe_allow_html=True)

    col_e, col_f = st.columns(2)

    # ── 3a. Kasual vs Terdaftar – Pie ───────
    with col_e:
        total_c = df["casual"].sum()
        total_r = df["registered"].sum()
        fig7, ax7 = plt.subplots(figsize=(5, 5))
        wedges, texts, autotexts = ax7.pie(
            [total_c, total_r],
            labels=["Kasual", "Terdaftar"],
            autopct="%1.1f%%",
            colors=[PALETTE["amber"], PALETTE["blue"]],
            startangle=140,
            wedgeprops={"edgecolor": "#1e2130", "linewidth": 2},
            textprops={"color": "#e8eaf6", "fontsize": 11},
        )
        for at in autotexts:
            at.set_fontsize(12)
            at.set_fontweight("bold")
        ax7.set_title("Proporsi Pengguna Kasual vs Terdaftar", fontsize=12, fontweight="bold")
        fig7.tight_layout()
        st.pyplot(fig7)
        plt.close(fig7)

    # ── 3b. Kasual vs Terdaftar per Hari ────
    with col_f:
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_labels = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
        day_agg = (
            df.groupby("day_name")[["casual", "registered"]]
            .mean()
            .reindex(day_order)
            .dropna()
            .reset_index()
        )

        x = np.arange(len(day_agg))
        width = 0.38
        fig8, ax8 = plt.subplots(figsize=(6, 4.5))
        ax8.bar(x - width/2, day_agg["casual"],    width, label="Kasual",    color=PALETTE["amber"], edgecolor="#1e2130", zorder=3)
        ax8.bar(x + width/2, day_agg["registered"], width, label="Terdaftar", color=PALETTE["blue"],  edgecolor="#1e2130", zorder=3)
        ax8.set_title("Rata-rata Peminjaman per Hari dalam Seminggu", fontsize=12, fontweight="bold")
        ax8.set_xlabel("Hari")
        ax8.set_ylabel("Rata-rata Peminjaman")
        ax8.set_xticks(x)
        short_map = dict(zip(day_order, day_labels))
        ax8.set_xticklabels([short_map.get(d, d) for d in day_agg["day_name"]])
        ax8.legend()
        ax8.grid(axis="y", alpha=0.4, zorder=0)
        fig8.tight_layout()
        st.pyplot(fig8)
        plt.close(fig8)

    # ── 3c. Tren Bulanan Kasual vs Terdaftar ─
    st.markdown("#### 📅 Tren Bulanan: Kasual vs Terdaftar")
    monthly_user = (
        df.groupby(["month_order", "month_name"])[["casual", "registered"]]
        .mean()
        .reset_index()
        .sort_values("month_order")
    )
    fig9, ax9 = plt.subplots(figsize=(11, 4))
    ax9.stackplot(
        monthly_user["month_name"],
        monthly_user["casual"],
        monthly_user["registered"],
        labels=["Kasual", "Terdaftar"],
        colors=[PALETTE["amber"] + "cc", PALETTE["blue"] + "cc"],
        alpha=0.85,
    )
    ax9.set_title("Komposisi Peminjaman Bulanan: Kasual vs Terdaftar", fontsize=13, fontweight="bold")
    ax9.set_xlabel("Bulan")
    ax9.set_ylabel("Rata-rata Peminjaman")
    ax9.legend(loc="upper left")
    ax9.grid(alpha=0.3)
    fig9.tight_layout()
    st.pyplot(fig9)
    plt.close(fig9)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Insight:</strong> Pengguna <strong>terdaftar</strong> mendominasi (~80%) dan memiliki pola
    penggunaan tinggi di hari kerja (komuter), sementara pengguna <strong>kasual</strong> memuncak di
    akhir pekan—mengindikasikan penggunaan rekreasi. Strategi: tawarkan promo keanggotaan di akhir pekan
    untuk mengkonversi pengguna kasual menjadi terdaftar.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  TAB 4 – FAKTOR LINGKUNGAN
# ══════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-header">🌡️ Analisis Lanjutan: Pengaruh Faktor Lingkungan</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtext">Korelasi antara suhu, kelembaban, kecepatan angin, dan jumlah peminjaman.</p>', unsafe_allow_html=True)

    col_g, col_h = st.columns(2)

    # ── 4a. Scatter: Suhu vs Peminjaman ─────
    with col_g:
        fig10, ax10 = plt.subplots(figsize=(6, 4.5))
        season_labels = df["season_label"].unique()
        for s in season_labels:
            sub = df[df["season_label"] == s]
            ax10.scatter(
                sub["temp_c"], sub["cnt"],
                alpha=0.4, s=18,
                color=SEASON_COLORS.get(s, "#ffffff"),
                label=s,
            )
        # Trend line
        z = np.polyfit(df["temp_c"], df["cnt"], 1)
        p = np.poly1d(z)
        x_line = np.linspace(df["temp_c"].min(), df["temp_c"].max(), 200)
        ax10.plot(x_line, p(x_line), "--", color=PALETTE["rose"], linewidth=2, label="Tren Linear")
        ax10.set_title("Suhu vs Jumlah Peminjaman", fontsize=12, fontweight="bold")
        ax10.set_xlabel("Suhu (°C)")
        ax10.set_ylabel("Jumlah Peminjaman")
        ax10.legend(fontsize=7, loc="upper left")
        ax10.grid(alpha=0.4)
        fig10.tight_layout()
        st.pyplot(fig10)
        plt.close(fig10)

    # ── 4b. Scatter: Kelembaban vs Peminjaman ─
    with col_h:
        fig11, ax11 = plt.subplots(figsize=(6, 4.5))
        ax11.scatter(
            df["hum_pct"], df["cnt"],
            alpha=0.35, s=18,
            color=PALETTE["sky"],
        )
        z2 = np.polyfit(df["hum_pct"], df["cnt"], 1)
        p2 = np.poly1d(z2)
        x_line2 = np.linspace(df["hum_pct"].min(), df["hum_pct"].max(), 200)
        ax11.plot(x_line2, p2(x_line2), "--", color=PALETTE["rose"], linewidth=2, label="Tren Linear")
        ax11.set_title("Kelembaban vs Jumlah Peminjaman", fontsize=12, fontweight="bold")
        ax11.set_xlabel("Kelembaban (%)")
        ax11.set_ylabel("Jumlah Peminjaman")
        ax11.legend()
        ax11.grid(alpha=0.4)
        fig11.tight_layout()
        st.pyplot(fig11)
        plt.close(fig11)

    # ── 4c. Correlation Heatmap ─────────────
    st.markdown("#### 🔗 Matriks Korelasi Faktor Lingkungan")
    corr_cols = {
        "temp_c":       "Suhu (°C)",
        "hum_pct":      "Kelembaban (%)",
        "windspeed_ms": "Kec. Angin",
        "casual":       "Kasual",
        "registered":   "Terdaftar",
        "cnt":          "Total",
    }
    corr_df = df[[c for c in corr_cols.keys() if c in df.columns]].rename(columns=corr_cols)
    corr_matrix = corr_df.corr()

    fig12, ax12 = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        corr_matrix, annot=True, fmt=".2f",
        cmap="coolwarm", ax=ax12,
        vmin=-1, vmax=1,
        linewidths=0.5, linecolor="#1e2130",
        annot_kws={"size": 10, "weight": "bold"},
        cbar_kws={"label": "Korelasi Pearson"},
    )
    ax12.set_title("Matriks Korelasi: Faktor Lingkungan & Peminjaman", fontsize=13, fontweight="bold", pad=10)
    fig12.tight_layout()
    st.pyplot(fig12)
    plt.close(fig12)

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Insight:</strong> <strong>Suhu</strong> memiliki korelasi positif terkuat dengan jumlah peminjaman
    (r ~ 0.63), artinya cuaca hangat mendorong lebih banyak pengguna. Sebaliknya, <strong>kelembaban tinggi</strong>
    dan <strong>kecepatan angin</strong> berkorelasi negatif—kondisi lembab dan berangin membuat orang enggan bersepeda.
    Pengelola dapat mengoptimalkan ketersediaan armada berdasarkan prakiraan cuaca harian.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#4b5563; font-size:0.82rem; padding: 1rem 0;'>
    🚲 <strong style='color:#6b7280;'>Bike Sharing Dashboard</strong> &nbsp;|&nbsp;
    Dibuat dengan menggunakan Streamlit &nbsp;|&nbsp;
    Dataset: <em>Capital Bikeshare, Washington D.C.</em> &nbsp;|&nbsp;
    Dicoding Data Analysis Project
</div>
""", unsafe_allow_html=True)

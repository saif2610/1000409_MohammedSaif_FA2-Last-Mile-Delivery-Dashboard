import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Last Mile Delivery Dashboard",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
}

.dashboard-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 17px;
    color: #666666;
    margin-bottom: 25px;
}

.metric-card {
    padding: 18px;
    border-radius: 12px;
    background-color: white;
    border: 1px solid #e5e7eb;
    text-align: center;
}

.metric-title {
    font-size: 14px;
    color: #666666;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv("delivery_data.csv")

    return data


df = load_data()


# ============================================================
# DATA CLEANING
# ============================================================

# Convert numeric columns

numeric_columns = [
    "Agent_Age",
    "Agent_Rating",
    "Store_Latitude",
    "Store_Longitude",
    "Drop_Latitude",
    "Drop_Longitude",
    "Delivery_Time"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# Convert date

if "Order_Date" in df.columns:

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )


# Remove unnecessary spaces from text columns

text_columns = [
    "Weather",
    "Traffic",
    "Vehicle",
    "Area",
    "Category"
]

for column in text_columns:

    if column in df.columns:

        df[column] = df[column].astype(str).str.strip()


# Fill missing Agent Rating

if df["Agent_Rating"].isna().sum() > 0:

    df["Agent_Rating"] = df["Agent_Rating"].fillna(
        df["Agent_Rating"].median()
    )


# Fill missing Weather

if df["Weather"].isna().sum() > 0:

    df["Weather"] = df["Weather"].fillna(
        df["Weather"].mode()[0]
    )


# Remove rows missing important values

required_columns = [
    "Delivery_Time",
    "Weather",
    "Traffic",
    "Vehicle",
    "Area",
    "Category",
    "Agent_Rating",
    "Agent_Age"
]

df = df.dropna(
    subset=required_columns
)


# ============================================================
# CREATE NEW FIELDS
# ============================================================

# Average delivery time

average_delivery_time = df["Delivery_Time"].mean()


# Standard deviation

delivery_std = df["Delivery_Time"].std()


# Late delivery threshold
# According to FA-2:
# Delivery Time > Mean + 1 Standard Deviation

late_threshold = (
    average_delivery_time + delivery_std
)


# Late delivery column

df["Late_Delivery"] = np.where(
    df["Delivery_Time"] > late_threshold,
    "Late",
    "On Time"
)


# Late delivery percentage

late_percentage = (
    (df["Late_Delivery"] == "Late").mean() * 100
)


# Agent age groups

def create_age_group(age):

    if age < 25:
        return "Under 25"

    elif age <= 40:
        return "25–40"

    else:
        return "40+"


df["Agent_Age_Group"] = df["Agent_Age"].apply(
    create_age_group
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">🚚 Last Mile Delivery Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Analyzing delivery performance and identifying factors affecting delivery time'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")


# Weather filter

weather_options = sorted(
    df["Weather"].dropna().unique()
)

selected_weather = st.sidebar.multiselect(
    "🌦️ Weather",
    weather_options,
    default=weather_options
)


# Traffic filter

traffic_options = sorted(
    df["Traffic"].dropna().unique()
)

selected_traffic = st.sidebar.multiselect(
    "🚦 Traffic",
    traffic_options,
    default=traffic_options
)


# Vehicle filter

vehicle_options = sorted(
    df["Vehicle"].dropna().unique()
)

selected_vehicle = st.sidebar.multiselect(
    "🚗 Vehicle",
    vehicle_options,
    default=vehicle_options
)


# Category filter

category_options = sorted(
    df["Category"].dropna().unique()
)

selected_category = st.sidebar.multiselect(
    "📦 Product Category",
    category_options,
    default=category_options
)


# Area filter

area_options = sorted(
    df["Area"].dropna().unique()
)

selected_area = st.sidebar.multiselect(
    "📍 Area",
    area_options,
    default=area_options
)


# Age group filter

age_options = [
    "Under 25",
    "25–40",
    "40+"
]

selected_age = st.sidebar.multiselect(
    "👤 Agent Age Group",
    age_options,
    default=age_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["Weather"].isin(selected_weather))
    &
    (df["Traffic"].isin(selected_traffic))
    &
    (df["Vehicle"].isin(selected_vehicle))
    &
    (df["Category"].isin(selected_category))
    &
    (df["Area"].isin(selected_area))
    &
    (df["Agent_Age_Group"].isin(selected_age))
]


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Key Performance Indicators")


if len(filtered_df) > 0:

    filtered_average = filtered_df[
        "Delivery_Time"
    ].mean()

    filtered_late_percentage = (
        (filtered_df["Late_Delivery"] == "Late").mean()
        * 100
    )

    median_delivery = filtered_df[
        "Delivery_Time"
    ].median()

else:

    filtered_average = 0
    filtered_late_percentage = 0
    median_delivery = 0


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🚚 Deliveries",
        f"{len(filtered_df):,}"
    )


with col2:

    st.metric(
        "⏱️ Avg Delivery",
        f"{filtered_average:.2f} min"
    )


with col3:

    st.metric(
        "⚠️ Late Deliveries",
        f"{filtered_late_percentage:.2f}%"
    )


with col4:

    st.metric(
        "📈 Median Time",
        f"{median_delivery:.2f} min"
    )


with col5:

    st.metric(
        "⭐ Avg Rating",
        f"{filtered_df['Agent_Rating'].mean():.2f}"
        if len(filtered_df) > 0
        else "0"
    )


# ============================================================
# NO DATA MESSAGE
# ============================================================

if len(filtered_df) == 0:

    st.warning(
        "No deliveries match the selected filters. "
        "Please change the filters."
    )

    st.stop()


# ============================================================
# 1. DELAY ANALYZER
# ============================================================

st.header("1️⃣ Delay Analyzer")

delay_data = (
    filtered_df
    .groupby(
        ["Weather", "Traffic"],
        as_index=False
    )["Delivery_Time"]
    .mean()
)


fig_delay = px.bar(
    delay_data,
    x="Weather",
    y="Delivery_Time",
    color="Traffic",
    barmode="group",
    title="Average Delivery Time by Weather and Traffic",
    labels={
        "Delivery_Time": "Average Delivery Time (minutes)",
        "Weather": "Weather",
        "Traffic": "Traffic"
    },
    text_auto=".1f"
)


fig_delay.update_layout(
    height=500,
    legend_title="Traffic"
)


st.plotly_chart(
    fig_delay,
    use_container_width=True
)


# ============================================================
# 2. VEHICLE COMPARISON
# ============================================================

st.header("2️⃣ Vehicle Comparison")

vehicle_data = (
    filtered_df
    .groupby(
        "Vehicle",
        as_index=False
    )["Delivery_Time"]
    .mean()
    .sort_values(
        "Delivery_Time",
        ascending=False
    )
)


fig_vehicle = px.bar(
    vehicle_data,
    x="Vehicle",
    y="Delivery_Time",
    title="Average Delivery Time by Vehicle",
    labels={
        "Vehicle": "Vehicle Type",
        "Delivery_Time": "Average Delivery Time (minutes)"
    },
    text_auto=".1f"
)


fig_vehicle.update_layout(
    height=500
)


st.plotly_chart(
    fig_vehicle,
    use_container_width=True
)


# ============================================================
# 3. AGENT PERFORMANCE SCATTER PLOT
# ============================================================

st.header("3️⃣ Agent Performance")

fig_agent = px.scatter(
    filtered_df,
    x="Agent_Rating",
    y="Delivery_Time",
    color="Agent_Age_Group",
    hover_data=[
        "Agent_Age",
        "Vehicle",
        "Traffic",
        "Weather",
        "Area"
    ],
    title="Agent Rating vs Delivery Time",
    labels={
        "Agent_Rating": "Agent Rating",
        "Delivery_Time": "Delivery Time (minutes)",
        "Agent_Age_Group": "Agent Age Group"
    },
    opacity=0.65
)


fig_agent.update_layout(
    height=550
)


st.plotly_chart(
    fig_agent,
    use_container_width=True
)


# ============================================================
# 4. AREA HEATMAP
# ============================================================

st.header("4️⃣ Area Heatmap")

area_data = (
    filtered_df
    .groupby(
        "Area",
        as_index=False
    )["Delivery_Time"]
    .mean()
    .sort_values(
        "Delivery_Time",
        ascending=False
    )
)


fig_area = px.density_heatmap(
    area_data,
    x="Area",
    y="Delivery_Time",
    z="Delivery_Time",
    title="Average Delivery Time Across Areas",
    labels={
        "Area": "Area",
        "Delivery_Time": "Average Delivery Time"
    }
)


fig_area.update_layout(
    height=500
)


st.plotly_chart(
    fig_area,
    use_container_width=True
)


# ============================================================
# 5. CATEGORY BOXPLOT
# ============================================================

st.header("5️⃣ Category Visualizer")

fig_category = px.box(
    filtered_df,
    x="Category",
    y="Delivery_Time",
    color="Category",
    title="Distribution of Delivery Time Across Categories",
    labels={
        "Category": "Product Category",
        "Delivery_Time": "Delivery Time (minutes)"
    },
    points="outliers"
)


fig_category.update_layout(
    height=550,
    showlegend=False
)


st.plotly_chart(
    fig_category,
    use_container_width=True
)


# ============================================================
# EXTRA VISUALIZATION 1
# MONTHLY DELIVERY TREND
# ============================================================

st.header("➕ Extra Visualizations")


monthly_data = (
    filtered_df
    .dropna(subset=["Order_Date"])
    .groupby(
        filtered_df.loc[
            filtered_df.index,
            "Order_Date"
        ].dt.to_period("M").astype(str)
    )["Delivery_Time"]
    .mean()
    .reset_index()
)


if len(monthly_data) > 0:

    monthly_data.columns = [
        "Month",
        "Average_Delivery_Time"
    ]

    fig_month = px.line(
        monthly_data,
        x="Month",
        y="Average_Delivery_Time",
        markers=True,
        title="Monthly Average Delivery Time",
        labels={
            "Month": "Month",
            "Average_Delivery_Time":
                "Average Delivery Time (minutes)"
        }
    )

    fig_month.update_layout(
        height=450
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )


# ============================================================
# EXTRA VISUALIZATION 2
# DELIVERY TIME DISTRIBUTION
# ============================================================

fig_hist = px.histogram(
    filtered_df,
    x="Delivery_Time",
    nbins=30,
    title="Delivery Time Distribution",
    labels={
        "Delivery_Time": "Delivery Time (minutes)"
    }
)


fig_hist.update_layout(
    height=450
)


st.plotly_chart(
    fig_hist,
    use_container_width=True
)


# ============================================================
# EXTRA VISUALIZATION 3
# LATE DELIVERY BY TRAFFIC
# ============================================================

late_traffic = (
    filtered_df
    .groupby("Traffic", as_index=False)
    .agg(
        Late_Percentage=(
            "Late_Delivery",
            lambda x:
            (x == "Late").mean() * 100
        )
    )
)


fig_late_traffic = px.bar(
    late_traffic,
    x="Traffic",
    y="Late_Percentage",
    title="% Late Deliveries by Traffic Condition",
    labels={
        "Traffic": "Traffic Condition",
        "Late_Percentage": "Late Deliveries (%)"
    },
    text_auto=".1f"
)


fig_late_traffic.update_layout(
    height=450
)


st.plotly_chart(
    fig_late_traffic,
    use_container_width=True
)


# ============================================================
# EXTRA VISUALIZATION 4
# AGENT RECORDS BY AREA
# ============================================================

agent_area = (
    filtered_df
    .groupby("Area")
    .size()
    .reset_index(
        name="Delivery_Count"
    )
    .sort_values(
        "Delivery_Count",
        ascending=False
    )
)


fig_agent_area = px.bar(
    agent_area,
    x="Area",
    y="Delivery_Count",
    title="Number of Deliveries by Area",
    labels={
        "Area": "Area",
        "Delivery_Count": "Number of Deliveries"
    },
    text_auto=True
)


fig_agent_area.update_layout(
    height=450
)


st.plotly_chart(
    fig_agent_area,
    use_container_width=True
)


# ============================================================
# DATA QUALITY
# ============================================================

with st.expander("🔍 Data Quality Information"):

    st.write(
        "Original number of records:",
        f"{len(load_data()):,}"
    )

    st.write(
        "Records after cleaning:",
        f"{len(df):,}"
    )

    st.write(
        "Average delivery time:",
        f"{average_delivery_time:.2f} minutes"
    )

    st.write(
        "Standard deviation:",
        f"{delivery_std:.2f} minutes"
    )

    st.write(
        "Late delivery threshold:",
        f"{late_threshold:.2f} minutes"
    )

    st.write(
        "Late delivery percentage:",
        f"{late_percentage:.2f}%"
    )


# ============================================================
# FILTERED DATA
# ============================================================

st.header("📋 Filtered Delivery Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_delivery_data.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "FA-2 | Mathematics for AI-II | "
    "Last Mile Delivery Performance Analysis"
)

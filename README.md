# 🚚 Last Mile Delivery Performance Dashboard

## FA-2: Dashboarding and Deployment

### 📌 Project Overview

This project analyzes last-mile delivery data to identify factors that affect delivery performance.

The dashboard was developed using **Python, Pandas, Plotly, and Streamlit**. It allows users to explore delivery performance using interactive filters and visualizations.

The project focuses on delivery time, traffic, weather, vehicle type, delivery area, product category, and agent performance.

---

## 🎯 Objectives

The main objectives of this project are:

* Process and clean real-world delivery data.
* Identify missing values and handle them appropriately.
* Calculate average delivery time.
* Identify late deliveries using a statistical threshold.
* Compare delivery performance across different factors.
* Create meaningful and interactive visualizations.
* Build and deploy an interactive Streamlit dashboard.

---

## 📊 Dataset

The dataset contains information about last-mile deliveries, including:

* Order ID
* Agent Age
* Agent Rating
* Store Location
* Drop Location
* Order Date
* Order Time
* Pickup Time
* Weather
* Traffic
* Vehicle
* Area
* Delivery Time
* Product Category

The dataset contains **43,739 delivery records and 16 columns**.

---

## 🧹 Data Cleaning

The following data preparation steps were performed:

1. Numeric columns were converted into appropriate numeric data types.
2. Missing Agent Rating values were filled using the median.
3. Missing Weather values were filled using the most frequent value.
4. Rows with missing values in important analysis fields were removed.
5. A new `Late_Delivery` field was created.
6. Agent age was divided into three groups:

   * Under 25
   * 25–40
   * 40+

### Late Delivery Definition

A delivery is classified as **Late** when:

**Delivery Time > Mean Delivery Time + 1 Standard Deviation**

The percentage of late deliveries is then calculated from the cleaned dataset.

---

## 📈 Dashboard Visualizations

The dashboard contains the five required visualizations:

### 1. Delay Analyzer

A bar chart comparing average delivery time across different weather and traffic conditions.

### 2. Vehicle Comparison

A bar chart showing the average delivery time for different vehicle types.

### 3. Agent Performance

A scatter plot comparing Agent Rating with Delivery Time. Agents are grouped by age:

* Under 25
* 25–40
* 40+

### 4. Area Heatmap

A visualization showing average delivery time across different delivery areas.

### 5. Category Visualizer

A boxplot showing the distribution of delivery time across product categories.

---

## ➕ Additional Visualizations

The dashboard also includes additional analysis:

* Monthly average delivery time trend
* Delivery time distribution histogram
* Percentage of late deliveries by traffic condition
* Number of deliveries by area

---

## 🔎 Interactive Filters

Users can filter the dashboard using:

* 🌦️ Weather
* 🚦 Traffic
* 🚗 Vehicle
* 📦 Product Category
* 📍 Area
* 👤 Agent Age Group

All dashboard results update according to the selected filters.

---

## 📊 Key Performance Indicators

The dashboard displays:

* Total number of deliveries
* Average delivery time
* Percentage of late deliveries
* Median delivery time
* Average agent rating

---

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **NumPy**
* **Plotly**
* **Streamlit**
* **GitHub**
* **Streamlit Community Cloud**

---

## 📁 Project Structure

```text
FA2-Last-Mile-Delivery-Dashboard/
│
├── app.py
├── delivery_data.csv
├── requirements.txt
└── README.md
```

---

## 🚀 Deployment

The application was deployed using **Streamlit Community Cloud**.

The source code is maintained in a GitHub repository and the Streamlit application is connected directly to the repository.

### Live Dashboard

**Streamlit App:**
Paste your Streamlit public URL here.

### GitHub Repository

**GitHub:**
Paste your GitHub repository URL here.

---

## 💡 Key Insights

The dashboard helps identify how factors such as traffic, weather, vehicle type, area, and product category influence delivery time.

It also helps identify patterns in agent performance and late deliveries, allowing delivery performance to be analyzed using data-driven insights.

---

## 👨‍💻 Project Information

**Subject:** Mathematics for AI-II
**Assessment:** FA-2 – Dashboarding and Deployment
**Project:** Analyzing Last Mile Delivery Data for Performance Insights
**Platform:** Streamlit
**Language:** Python


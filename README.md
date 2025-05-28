# 💳 CapitalOne360 Financial Insights Dashboard

An interactive, end-to-end data analytics and intelligence dashboard built with **Streamlit**, based on mock transaction data from a fictional financial app "CapitalOne360".

🚀 [Live Demo on Streamlit Cloud](https://capitalone360-app-ggbxd2svsjwjqix5xf6y8x.streamlit.app/)

---

## 📊 Project Overview

This project provides a 360° view of user transaction behavior using uploaded `.csv` files, with powerful insights and machine learning features including:

- 🔎 **User Filtering** – Drill-down filters for User ID, Category, and City
- 📈 **Spend Analytics** – Total spend, monthly trends, and top merchants
- 🧠 **Fraud Detection** – Rule-based flags and suspicious transaction insights
- 🧩 **User Segmentation** – K-Means clustering to identify spending patterns
- 💡 **Smart Recommendations** – Personalized merchant suggestions per user

---

## 📂 Files Required

Ensure the following CSV files are present in the project directory:

- `CapitalOne_Mock_Transactions.csv`
- `CapitalOne_Fraud_Detected.csv`
- `CapitalOne_User_Segments.csv`

---

## 🧪 Features

### ✅ Spend Analysis
- KPIs: Total, Average Spend, Unique Users
- Monthly trend chart
- Top categories & merchants

### ✅ Fraud Detection
- Rule-based detection: high amount, rapid transactions, city change
- Visual fraud risk flags
- Filterable fraud transactions

### ✅ User Segmentation
- K-Means clustering into behavior-based segments
- Visual representation of segments
- Segment-wise transaction drill-down

### ✅ Smart Recommendations
- Cosine similarity-based merchant recommendations
- Personalized for each user

---

## 📦 Technologies Used

- **Python** (Pandas, NumPy, Scikit-learn)
- **Streamlit** for the interactive dashboard
- **Plotly / Matplotlib** (internal for graph generation)
- **CSV** files as lightweight data source (MySQL optional)

---

## ⚙️ Getting Started Locally

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/capitalone360-streamlit.git
cd capitalone360-streamlit
```
### 2. Install Requirements
```bash
pip install -r requirements.txt
```
### 3. Run the App
```bash
streamlit run app.py

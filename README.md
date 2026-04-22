# PhonePe Pulse Data Visualization and Exploration 📊

**An Interactive Fintech Analysis Dashboard for India (2018-2024)**

---

## 📌 Project Overview
This project is an end-to-end Data Engineering and Visualization solution. It automates the extraction of data from the official **PhonePe Pulse GitHub Repository**, processes it through a robust ETL pipeline, stores it in a MySQL database, and presents actionable insights through an interactive Streamlit dashboard.

---

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy, JSON
* **Database:** MySQL (Relational Storage)
* **Connectivity:** SQLAlchemy, mysql-connector-python
* **Visualization:** Streamlit, Plotly Express (Choropleth Maps & Charts)

---

## 🔄 Project Workflow (The ETL Pipeline)

### **1. Data Extraction**
I developed a custom script to clone the source repository and navigate its multi-layered JSON structure.
* **Source:** [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)
* **Logic:** Iteratively traversed the directory using the `os` module to capture metadata (State, Year, Quarter) directly from folder paths.

### **2. Data Transformation & Cleaning**
* **Flattening:** Processed thousands of nested JSON files into structured, flat DataFrames.
* **Cleaning:** Standardized state names, handled null values, and optimized data types.
* **Source Hierarchy Mapping:**

```text
data/
└── aggregated/ / map/ / top/
    └── transactions/ / users/
        └── country/ / india/
            └── state/
                └── [state_name]/
                    └── [year]/
                        └── [quarter].json
```

### **3. Schema Formation**
The extracted data was structured into the following schema before being injected into the database:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **State** | String | The Indian State/UT name |
| **Year** | Integer | The financial year (2018-2024) |
| **Quarter** | Integer | The specific quarter (1, 2, 3, or 4) |
| **Transaction_Type** | String | Category (e.g., Merchant payments, P2P) |
| **Transaction_Count** | BigInt | Total number of transactions |
| **Transaction_Amount** | Float | Total monetary value in Rupees |


---

## 🔌 Database Connectivity & Integration

To ensure the dashboard remains fast and scalable, I implemented a dedicated MySQL pipeline:

* **Workflow:** Used `mysql-connector-python` and `SQLAlchemy` to automate data loading.
* **Security:** Managed database credentials using **Environment Variables** to ensure no sensitive information is hardcoded in the scripts.
* **Performance:** Optimized SQL queries to fetch only the required data, reducing memory load on the Streamlit application.

---

---

## 💡 Business Problem Statements & Insights
The dashboard provides data-driven answers to critical business questions:
* **Market Leaders:** Top 10 States/Districts by transaction volume and value.
* **User Demographics:** District-wise distribution of registered users across India.
* **Brand Analysis:** Mobile device preferences among PhonePe users.
* **Growth Hotspots:** Identifying high-growth regions for merchant expansion.

---

## 🚀 How to Run Locally
1. **Clone Repo:** `git clone [Your-Repo-Link-Here]`
2. **Install Requirements:** `pip install -r requirements.txt`
3. **Database Setup:** Run extraction scripts to populate your MySQL instance.
4. **Launch App:** `streamlit run APP.py`
---
**Developed by Gulshan Kumar Nayak**

# PhonePe-Pulse-Data-Visualization
PhonePay Project - SQL+Python

---

### 📂 Data Hierarchy & Schema Formation

The core challenge of this project was converting PhonePe's multi-layered JSON structure into a clean, relational database.

#### **1. The Source Hierarchy (JSON Structure)**
The raw data is nested deep within the repository across thousands of files following this pattern:
```text
data/
└── aggregated/ / map/ / top/
    └── transactions/ / users/
        └── country/
            └── india/
                └── state/
                    └── [state_name]/
                        └── [year]/
                            └── [quarter].json  <-- Target Data


## 🛠️ Technology Stack
* **Python:** Data Extraction (os, json) and Transformation (Pandas).
* **MySQL:** Relational Database Management for structured storage.
* **Streamlit:** Interactive web application for data visualization.
* **Plotly:** Advanced geographical and statistical charts (India Map, Bar charts).

## 🚀 How to Use the Dashboard
1. **Select Navigation:** Use the sidebar to choose between **Home**, **Data Analysis**, or **Case Studies**.
2. **Filter Data:** Select specific **Years**, **Quarters**, and **Subjects** (Transaction/User) to update the visualizations in real-time.
3. **Explore Maps:** Hover over the India Map to see district-wise breakdowns of transaction volumes.
4. **Deep Dive:** Visit the "Case Studies" section to find answers to specific business questions (like top Insurance trends).



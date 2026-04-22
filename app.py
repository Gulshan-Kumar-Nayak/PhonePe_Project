import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import requests

# 1. DATABASE CONNECTION
def get_data(query):
    conn = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="0Rajeev@<3Me", 
        database="phonepe_db"
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="PhonePe Pulse", layout="wide")

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("📌 Navigation")
    page = st.radio("Go to", ["Home", "Data Analysis", "Case Studies"])
    st.divider()

    # Filters for Data Analysis
    if page == "Data Analysis":
        st.subheader("Analysis Filters")
        main_subject = st.selectbox("Main Subject", ["Aggregated Tables", "Map Tables", "Top Tables"])
        
        if main_subject == "Aggregated Tables":
            sub_options = ["aggregated_transaction", "aggregated_user", "aggregated_insurance"]
        elif main_subject == "Map Tables":
            sub_options = ["map_transaction", "map_user", "map_insurance"]
        else:
            sub_options = ["top_transaction", "top_user", "top_insurance"]
        
        sub_subject = st.selectbox("Sub-Subject", sub_options)

    # Filters for Case Studies (Updated to Radio format)
    elif page == "Case Studies":
        st.subheader("Case Study Filters")
        case_selection = st.radio("Select a Case Study", [
            "1. Decoding Transaction Dynamics",
            "2. Transaction analysis",
            "3. User register analysis",
            "4. Insurance penetration and growth potential",
            "5. Insurance Transaction analysis"
        ])

# --- DYNAMIC HOME PAGE QUERY ---
# Updated Query using confirmed column names from your Insurance table
home_stats_query = """
SELECT 
    MIN(Year) AS First_Year, 
    MAX(Year) AS Last_Year,
    SUM(Count) AS Total_Count,
    SUM(Amount) AS Total_Value
FROM aggregated_insurance;
"""

# --- 3. HOME PAGE ---
if page == "Home":
    try:
        df_home = get_data(home_stats_query)
        first_yr = int(df_home['First_Year'][0])
        last_yr = int(df_home['Last_Year'][0])
        total_pols = df_home['Total_Count'][0]
        total_val = df_home['Total_Value'][0]
    except:
        # Fallback values from your successful insurance query
        first_yr, last_yr, total_pols, total_val = 2018, 2024, 101609809, 140109048688

    # Custom CSS for a vibrant, data-heavy header background effect
    st.markdown("""
        <style>
        .hero-section {
            background: linear-gradient(rgba(95, 37, 159, 0.9), rgba(95, 37, 159, 0.7)), 
                        url('https://www.phonepe.com/pulse/static/7492c39e7939a85089e879a957297e59/pulse-logo.png');
            background-size: cover;
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        </style>
        <div class="hero-section">
            <h1>PhonePe Pulse Data Visualization</h1>
            <p>Analyzing India's Digital Financial Evolution</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        # header and project overview
        st.markdown("### 🚀 Project Overview")
    
        st.markdown(f"""
        This dashboard transforms millions of raw data points into actionable insights. By mapping over **{total_pols/1e6:.1f} Million** insurance transactions, we reveal how 
        digital trust is reshaping India's economy.
    
        **Key Analytical Pillars:**
        * 💸 **Financial Impact:** Visualizing over **₹{total_val/1e11:.2f} Lakh Crore** in value.
        * 📍 **Regional Penetration:** Data mapped across States, Districts, and Pincodes.
        * 🛡️ **Insurance Growth:** Identifying micro-markets with high potential.
        """)

        st.divider()

    # Data-Heavy Metrics Section
    st.write("### 📈 Live Project Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Insurance Policies", f"{total_pols/1e7:.2f} Cr")
    m2.metric("Transaction Value", f"₹{total_val/1e9:.1f} B")
    m3.metric("Data Scope", f"{first_yr} - {last_yr}")

    st.divider()

    # Professional Tech Stack Footer
    st.info("🛠️ **Built with:** Python (Pandas), MySQL, and Streamlit. Use the sidebar to explore 'Case Studies'.")

# --- 4. CASE STUDIES ---
elif page == "Case Studies":
    st.title(f"💡 {case_selection}")
    
    if case_selection == "1. Decoding Transaction Dynamics":
        st.header("Decoding Transaction Dynamics on PhonePe")
        st.markdown("**Scenario:** Leadership seeks to understand growth patterns and stagnation across regions to drive targeted strategies.")
        
        # Dropdown for questions
        selected_question = st.selectbox("Select a question to explore:", [
            "1. Are Transaction increasing or not?",
            "2. Which type of Transaction people use more?",
            "3. Are people using PhonePe every year?"
        ])

        st.divider()

        if selected_question == "1. Are Transaction increasing or not?":
            query_1 = """
            SELECT Year, SUM(Transaction_amount) AS Total_Amount 
            FROM aggregated_transaction 
            GROUP BY Year 
            ORDER BY Year
            """
            df_1 = get_data(query_1)

            if not df_1.empty:
                # Using a 2:1 ratio often aligns better for horizontal space
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 📈 Year-wise Transaction Growth")
                    fig_1 = px.line(df_1, x='Year', y='Total_Amount', markers=True, 
                                    labels={'Total_Amount': 'Total Amount (₹)'},
                                    template="plotly_dark")
                    fig_1.update_traces(line_color='#ff4b4b')
                    # Set a fixed height for the chart to match the table
                    fig_1.update_layout(height=450, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_1, use_container_width=True)

                with col_table:
                    st.write("#### 📊 Yearly Data")
                    df_display = df_1.copy()
                    df_display['Total_Amount'] = df_display['Total_Amount'].apply(lambda x: f"₹{x:,.0f}")
                    
                    # Setting height=450 to match the fig_1 layout height above
                    st.dataframe(df_display, hide_index=True, use_container_width=True, height=450)
                
                # Insight moved to full width below for a cleaner look
                st.info("The total transaction amount has shown a consistent upward trend from 2018 to 2024, indicating increasing adoption of PhonePe services over time.")

        elif selected_question == "2. Which type of Transaction people use more?":
            # 1. Fetch the Data
            query_2 = """
            SELECT Transaction_type, SUM(Transaction_count) AS Total_Count 
            FROM aggregated_transaction 
            GROUP BY Transaction_type 
            ORDER BY Total_Count DESC
            """
            df_2 = get_data(query_2)

            if not df_2.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 📊 Transaction Type Usage")
                    # Using log_y=True to match your notebook's scale
                    fig_2 = px.bar(df_2, x='Transaction_type', y='Total_Count', 
                                   color='Total_Count', color_continuous_scale='Reds',
                                   log_y=True,
                                   labels={'Total_Count': 'Total Count (Log Scale)', 'Transaction_type': 'Category'},
                                   template="plotly_dark")
                    fig_2.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_2, use_container_width=True)

                with col_table:
                    st.write("#### 📋 Category Breakdown")
                    df_display_2 = df_2.copy()
                    df_display_2['Total_Count'] = df_display_2['Total_Count'].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(df_display_2, hide_index=True, use_container_width=True, height=450)
                
                # Conclusion from your notebook
                st.info("Merchant payments dominate transaction usage, indicating that PhonePe is primarily used for business and retail transactions rather than just peer-to-peer transfers.")

        elif selected_question == "3. Are people using PhonePe every year?":
            # 1. Fetch the Data (Transaction Count per Year)
            query_3 = """
            SELECT Year, SUM(Transaction_count) AS Total_Transactions 
            FROM aggregated_transaction 
            GROUP BY Year 
            ORDER BY Year
            """
            df_3 = get_data(query_3)

            if not df_3.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 📅 Yearly Usage Frequency")
                    # Bar chart to show the volume of transactions per year
                    fig_3 = px.bar(df_3, x='Year', y='Total_Transactions', 
                                   color='Total_Transactions', color_continuous_scale='Reds',
                                   labels={'Total_Transactions': 'Total Transaction Count'},
                                   template="plotly_dark")
                    fig_3.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_3, use_container_width=True)

                with col_table:
                    st.write("#### 📋 Annual Stats")
                    df_display_3 = df_3.copy()
                    # Formatting numbers with commas for readability
                    df_display_3['Total_Transactions'] = df_display_3['Total_Transactions'].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(df_display_3, hide_index=True, use_container_width=True, height=450)
                
                # Insight based on the data trend
                st.success("Yes! The transaction volume has increased significantly every single year, proving that users are not only staying on the platform but using it more frequently over time.")
        
        else:
            st.info(f"Detailed analysis for '{selected_question}' is coming soon.")
        
        st.divider()
        st.subheader("📌 Key Business Summary")
        st.markdown("""
            The analysis reveals a **consistent and exponential increase** in transaction volume from 2018 to 2024, 
            underscoring the rapid adoption of digital payments in India. **Merchant payments** have emerged as the 
            most dominant transaction type, highlighting their critical role in everyday consumer behavior. 

            Furthermore, the data shows significant regional variance; **Telangana** currently leads in total transaction 
            value, suggesting that while digital adoption is growing nationwide, it remains uneven across different 
            geographic regions and transaction categories.
            """)
        st.caption("Data Source: PhonePe Pulse Aggregated Transaction Records")
    
    elif case_selection == "2. Transaction analysis":
        st.header("🔍 Transaction Analysis")
        st.markdown("**Scenario:** Identifying geographic hotspots to optimize regional infrastructure and marketing efforts.")
        
        # Dropdown for Case Study 2 with a unique variable and key
        selected_question_2 = st.selectbox(
            "Select a question to explore:", 
            [
                "1. Which states are more active?",
                "2. Which districts are more active?"
            ],
            key="case_2_dropdown"
        )

        st.divider()

        # --- Placeholder logic for the questions ---
        if selected_question_2 == "1. Which states are more active?":
            # 1. Fetching Data with refined query
            query_2a = """
            SELECT State, SUM(Transaction_amount) AS Total_Amount 
            FROM aggregated_transaction 
            GROUP BY State 
            ORDER BY Total_Amount DESC 
            LIMIT 10
            """
            df_2a = get_data(query_2a)

            if not df_2a.empty:
                # 2. Layout Alignment
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 🏆 Top 10 Most Active States by Value")
                    # Creating a cleaner horizontal bar chart
                    fig_2a = px.bar(df_2a, x='Total_Amount', y='State', 
                                   orientation='h',
                                   color='Total_Amount',
                                   color_continuous_scale='Reds',
                                   labels={'Total_Amount': 'Total Value (₹)', 'State': 'State'},
                                   template="plotly_dark")
                    
                    # Formatting: Inverting y-axis so the highest is on top
                    fig_2a.update_layout(height=450, showlegend=False, 
                                        yaxis={'categoryorder':'total ascending'},
                                        margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_2a, use_container_width=True)

                with col_table:
                    st.write("#### 📊 State Rankings")
                    df_display_2a = df_2a.copy()
                    # Formatting the amount for the table
                    df_display_2a['Total_Amount'] = df_display_2a['Total_Amount'].apply(lambda x: f"₹{x:,.0f}")
                    st.dataframe(df_display_2a, hide_index=True, use_container_width=True, height=450)
                
                # Business Insight
                st.info("Telangana leads in total transaction value, followed by Karnataka and Maharashtra, indicating strong digital payment adoption and high-value transactions in these major economic hubs.")
            
        elif selected_question_2 == "2. Which districts are more active?":
            # 1. Fetching District Data
            query_2b = """
            SELECT District, SUM(Amount) AS Total_Amount 
            FROM map_transaction 
            GROUP BY District 
            ORDER BY Total_Amount DESC 
            LIMIT 10
            """
            df_2b = get_data(query_2b)

            if not df_2b.empty:
                # 2. Layout Alignment
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 📍 Top 10 Most Active Districts")
                    # Creating the horizontal bar chart
                    fig_2b = px.bar(df_2b, x='Total_Amount', y='District', 
                                   orientation='h',
                                   color='Total_Amount',
                                   color_continuous_scale='Reds',
                                   labels={'Total_Amount': 'Total Value (₹)', 'District': 'District'},
                                   template="plotly_dark")
                    
                    # Inverting y-axis and formatting
                    fig_2b.update_layout(height=450, showlegend=False, 
                                        yaxis={'categoryorder':'total ascending'},
                                        margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_2b, use_container_width=True)

                with col_table:
                    st.write("#### 📊 District Stats")
                    df_display_2b = df_2b.copy()
                    # Formatting numbers with currency and commas
                    df_display_2b['Total_Amount'] = df_display_2b['Total_Amount'].apply(lambda x: f"₹{x:,.0f}")
                    st.dataframe(df_display_2b, hide_index=True, use_container_width=True, height=450)
                
                # Business Insight derived from your analysis
                st.success("Transaction activity is highly concentrated in urban hubs like **Bengaluru** and **Hyderabad**, reflecting strong digital infrastructure and higher population density in metropolitan regions.")

        # --- PERMANENT SUMMARY FOR CASE STUDY 2 ---
        st.divider()
        st.subheader("📌 Key Business Summary")
        
        st.markdown("""
            The analysis reveals that transaction activity is highly concentrated in specific states, namely **Telangana**, **Karnataka**, and **Maharashtra**. 
            At the district level, **Bengaluru Urban** and **Hyderabad** lead significantly in total transaction volume.

            This trend indicates that urban regions contribute disproportionately to digital transactions, highlighting the impact of robust digital 
            adoption and advanced infrastructure in metropolitan areas. 

            > **Note:** The concentration in urban areas is driven by higher population density, a greater volume of business entities, 
            and superior digital infrastructure, all of which naturally lead to higher transaction frequency and value.
            """)

        st.caption("Data Source: PhonePe Pulse Aggregated & Map Transaction Records")
    
    elif case_selection == "3. User register analysis":
        st.header("👥 User Register Analysis")
        st.markdown("**Scenario:** Analyzing user acquisition trends and geographic expansion to optimize marketing spend.")
        
        # Unique dropdown for Case Study 3
        selected_question_3 = st.selectbox(
            "Select a question to explore:", 
            [
                "1. Which states are growing fast?",
                "2. Which district are bringing new usage?",
                "3. Where they should focus there marketing?"
            ],
            key="case_3_dropdown"
        )

        st.divider()

        # --- Placeholder logic for Case Study 3 Questions ---
        if selected_question_3 == "1. Which states are growing fast?":
            # 1. Fetching Top States by Registered Users
            query_3a = """
            SELECT State, SUM(Registered_Users) AS Total_Users 
            FROM top_user 
            GROUP BY State 
            ORDER BY Total_Users DESC 
            LIMIT 10
            """
            df_3a = get_data(query_3a)

            if not df_3a.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 👥 Top 10 States by Registered Users")
                    # Horizontal Bar Chart
                    fig_3a = px.bar(df_3a, x='Total_Users', y='State', 
                                   orientation='h',
                                   color='Total_Users',
                                   color_continuous_scale='Reds',
                                   labels={'Total_Users': 'Total Registered Users', 'State': 'State'},
                                   template="plotly_dark")
                    
                    fig_3a.update_layout(height=450, showlegend=False, 
                                        yaxis={'categoryorder':'total ascending'},
                                        margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_3a, use_container_width=True)

                with col_table:
                    st.write("#### 📊 User Rankings")
                    df_display_3a = df_3a.copy()
                    # Formatting numbers with commas for the table
                    df_display_3a['Total_Users'] = df_display_3a['Total_Users'].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(df_display_3a, hide_index=True, use_container_width=True, height=450)
                
                # Business Insight
                st.info("States with large populations like **Maharashtra**, **Karnataka**, and **Andhra Pradesh** exhibit the highest registration volumes, indicating they are mature markets with high digital penetration.")
            
        elif selected_question_3 == "2. Which district are bringing new usage?":
            # 1. Fetching Top Districts by Registered Users
            query_3b = """
            SELECT Entity_Name AS District, SUM(Registered_Users) AS Total_Users 
            FROM top_user 
            WHERE Entity = 'District'
            GROUP BY Entity_Name
            ORDER BY Total_Users DESC 
            LIMIT 10
            """
            df_3b = get_data(query_3b)

            if not df_3b.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 📍 Top 10 Districts by Registered Users")
                    # Professional Horizontal Bar Chart
                    fig_3b = px.bar(df_3b, x='Total_Users', y='District', 
                                   orientation='h',
                                   color='Total_Users',
                                   color_continuous_scale='Reds',
                                   labels={'Total_Users': 'Registered Users', 'District': 'District'},
                                   template="plotly_dark")
                    
                    fig_3b.update_layout(height=450, showlegend=False, 
                                        yaxis={'categoryorder':'total ascending'},
                                        margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_3b, use_container_width=True)

                with col_table:
                    st.write("#### 📊 District Stats")
                    df_display_3b = df_3b.copy()
                    # Formatting numbers for clear readability
                    df_display_3b['Total_Users'] = df_display_3b['Total_Users'].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(df_display_3b, hide_index=True, use_container_width=True, height=450)
                
                # Business Insight derived from your analysis
                st.success("Urban districts dominate user registrations, suggesting that digital adoption is highest in metropolitan areas like **Bengaluru Urban** and **Pune** due to better internet penetration and tech awareness.")

        elif selected_question_3 == "3. Where they should focus there marketing?":
            # 1. Using your validated query structure for Year-wise growth
            query_3c = """
            SELECT 
                Year, 
                SUM(Registered_Users) AS Total_Users 
            FROM top_user 
            GROUP BY Year 
            ORDER BY Year
            """
            df_3c = get_data(query_3c)

            if not df_3c.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 📈 User Growth Trend (Marketing Saturation Check)")
                    # Clean Line Chart using Plotly for consistency
                    fig_3c = px.line(df_3c, x='Year', y='Total_Users', 
                                    markers=True,
                                    color_discrete_sequence=['#d62728'], # Matches your Red theme
                                    template="plotly_dark",
                                    labels={'Total_Users': 'Registered Users', 'Year': 'Fiscal Year'})
                    
                    fig_3c.update_layout(height=450, margin=dict(l=20, r=20, t=30, b=20))
                    # Adding an area fill to make it look more "marketing-oriented"
                    fig_3c.update_traces(fill='tozeroy') 
                    st.plotly_chart(fig_3c, use_container_width=True)

                with col_table:
                    st.write("#### 📊 Annual Growth")
                    df_display_3c = df_3c.copy()
                    # Formatting numbers
                    df_display_3c['Total_Users'] = df_display_3c['Total_Users'].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(df_display_3c, hide_index=True, use_container_width=True, height=450)
                
                # The Strategic Answer to the Question:
                st.info("""
                🎯 **Marketing Strategy Insight:** While the growth curve shows consistent upward momentum through 2024, the narrowing slope between 2023 and 2024 suggests **Market Saturation** in Tier-1 cities. 
                
                **Action:** Marketing focus should now shift from 'Acquisition' in urban hubs to 'Retention' and 'Rural Expansion' in Tier-2 and Tier-3 regions where the next wave of digital adoption is expected.
                """)

        # --- PERMANENT SUMMARY FOR CASE STUDY 3 ---
        st.divider()
        st.subheader("📌 Key Business Summary")
        
        st.markdown("""
            The analysis demonstrates that PhonePe user registrations are **constantly increasing** over time, signaling robust growth and sustained platform adoption. 
            States such as **Maharashtra** and **Karnataka** lead in total users, reflecting higher digital maturity in these regions.

            At the district level, urban hubs like **Bengaluru** and **Pune** dominate the rankings, highlighting the critical role major cities play in driving 
            digital payment penetration. Overall, the data suggests that PhonePe's expansion is most concentrated in **economically strong and 
            highly urbanized regions**.

            > **Strategic Takeaway:** While urban dominance is clear, the steady annual growth across the country indicates that the platform is 
            successfully moving toward becoming a national utility for digital finance.
            """)

        st.caption("Data Source: PhonePe Pulse Map & Top User Records")    


    elif case_selection == "4. Insurance penetration and growth potential":
        st.header("🛡️ Insurance Penetration & Growth")
        st.markdown("**Scenario:** Evaluating the adoption of insurance products to identify untapped market potential and growth trends.")
        
        # Unique dropdown for Case Study 4
        selected_question_4 = st.selectbox(
            "Select a question to explore:", 
            [
                "1. Are people buying Insurance?",
                "2. Which state is doing it more?",
                "3. Is it increasing overtime?"
            ],
            key="case_4_dropdown"
        )

        st.divider()

        # --- Placeholder logic for Case Study 4 Questions ---
        if selected_question_4 == "1. Are people buying Insurance?":
            # 1. Fetching Insurance Growth Data
            query_4a = """
            SELECT Year, SUM(Amount) AS Total_Amount 
            FROM aggregated_insurance 
            GROUP BY Year 
            ORDER BY Year
            """
            df_4a = get_data(query_4a)

            if not df_4a.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 🛡️ Annual Insurance Premium Growth")
                    # Creating a professional Area Chart
                    fig_4a = px.area(df_4a, x='Year', y='Total_Amount', 
                                    markers=True,
                                    color_discrete_sequence=['#d62728'], 
                                    template="plotly_dark",
                                    labels={'Total_Amount': 'Total Premium Value (₹)', 'Year': 'Year'})
                    
                    fig_4a.update_layout(height=450, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_4a, use_container_width=True)

                with col_table:
                    st.write("#### 📊 Annual Totals")
                    df_display_4a = df_4a.copy()
                    # Formatting numbers with currency and commas
                    df_display_4a['Total_Amount'] = df_display_4a['Total_Amount'].apply(lambda x: f"₹{x:,.0f}")
                    st.dataframe(df_display_4a, hide_index=True, use_container_width=True, height=450)
                
                # Business Insight
                st.success("The insurance sector shows a **consistent and steep growth trajectory** starting from 2020. This indicates a significant shift in consumer behavior, as users increasingly trust digital platforms for long-term financial protection products.")
            
        elif selected_question_4 == "2. Which state is doing it more?":
            # 1. Fetching Top 10 States by Insurance Amount
            query_4b = """
            SELECT State, SUM(Amount) AS Total_Amount 
            FROM aggregated_insurance 
            GROUP BY State 
            ORDER BY Total_Amount DESC 
            LIMIT 10
            """
            df_4b = get_data(query_4b)

            if not df_4b.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 🏆 Top 10 States by Insurance Usage")
                    # Horizontal Bar Chart for readability
                    fig_4b = px.bar(df_4b, x='Total_Amount', y='State', 
                                   orientation='h',
                                   color='Total_Amount',
                                   color_continuous_scale='Reds',
                                   labels={'Total_Amount': 'Total Insurance Amount', 'State': 'State'},
                                   template="plotly_dark")
                    
                    fig_4b.update_layout(height=450, showlegend=False, 
                                        yaxis={'categoryorder':'total ascending'},
                                        margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_4b, use_container_width=True)

                with col_table:
                    st.write("#### 📊 Regional Rankings")
                    df_display_4b = df_4b.copy()
                    # Formatting currency for professional look
                    df_display_4b['Total_Amount'] = df_display_4b['Total_Amount'].apply(lambda x: f"₹{x:,.0f}")
                    st.dataframe(df_display_4b, hide_index=True, use_container_width=True, height=450)
                
                # Insight from your notebook
                st.info("Insurance adoption is highest in economically active and digitally mature states, suggesting that **income levels and digital penetration** significantly influence insurance usage.")

        elif selected_question_4 == "3. Is it increasing overtime?":
            # 1. Fetching Policy Count vs Total Value
            query_4c = """
            SELECT 
                SUM(Count) AS Total_Policies, 
                SUM(Amount) AS Total_Value 
            FROM aggregated_insurance
            """
            df_4c = get_data(query_4c)

            if not df_4c.empty:
                # 2. Layout Alignment
                col_chart, col_stats = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### ⚖️ Insurance Market Scale: Volume vs. Value")
                    
                    # Preparing data for the chart (Scaling for visual comparison)
                    # We show Policies in Millions and Value in Billions as per your notebook logic
                    metrics = ['Policies (Millions)', 'Value (Billions)']
                    values = [df_4c['Total_Policies'][0] / 1e6, df_4c['Total_Value'][0] / 1e9]
                    
                    fig_4c = px.bar(x=metrics, y=values, 
                                   color=metrics,
                                   color_discrete_sequence=['#d62728', '#ff7f0e'],
                                   labels={'x': 'Metric Type', 'y': 'Scale'},
                                   template="plotly_dark")
                    
                    fig_4c.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_4c, use_container_width=True)

                with col_stats:
                    st.write("#### 📊 Grand Totals")
                    # Displaying large numbers clearly using streamlit metrics
                    st.metric("Total Policies Issued", f"{df_4c['Total_Policies'][0]/1e7:.2f} Cr")
                    st.metric("Total Premium Value", f"₹{df_4c['Total_Value'][0]/1e9:.2f} B")
                    
                    st.write("---")
                    st.write("**Data Point:**")
                    st.caption("The high policy count relative to total value indicates a strong presence of 'Micro-insurance' or affordable premium products.")

                # Insight from your notebook
                st.success("While the number of insurance policies is high, the total transaction value highlights that users are not only adopting insurance but are also investing in **significant premium products**, reflecting growing financial trust.")

        # --- PERMANENT SUMMARY FOR CASE STUDY 4 ---
        st.divider()
        st.subheader("📌 Key Business Summary")
        
        st.markdown("""
            The analysis indicates that insurance usage on PhonePe is on a **strong growth trajectory**. While there was a temporary fluctuation in 2021, 
            the subsequent years have shown rapid adoption. States like **Karnataka** and **Maharashtra** lead in total value due to higher digital 
            awareness and economic maturity, while populous states like **Uttar Pradesh** contribute significantly to transaction volume.

            The high correlation between the number of policies and total transaction value confirms **increasing user trust** in digital platforms 
            for long-term financial services. 

            > **Strategic Takeaway:** The transition from simple payments to insurance products suggests that PhonePe is successfully evolving 
            from a transactional tool into a comprehensive digital financial ecosystem.
            """)

        st.caption("Data Source: PhonePe Pulse Aggregated Insurance Records")


    elif case_selection == "5. Insurance Transaction analysis":
        st.header("📈 Insurance Transaction Analysis")
        st.markdown("**Scenario:** Deep-diving into regional performance and pinpointing specific geographic areas for business expansion.")
        
        # Unique dropdown for Case Study 5
        selected_question_5 = st.selectbox(
            "Select a question to explore:", 
            [
                "1. Which states use insurance the most?",
                "2. Which District/Pin code use it most?",
                "3. Where should be the focus of Insurance business?"
            ],
            key="case_5_dropdown"
        )

        st.divider()

        # --- Placeholder logic for Case Study 5 Questions ---
        if selected_question_5 == "1. Which states use insurance the most?":
            # 1. Fetching Top 10 States by Insurance Transaction Value
            query_5a = """
            SELECT 
                State, 
                SUM(Amount) AS Total_Amount 
            FROM top_insurance 
            GROUP BY State 
            ORDER BY Total_Amount DESC 
            LIMIT 10
            """
            df_5a = get_data(query_5a)

            if not df_5a.empty:
                # 2. Displaying visual and data side-by-side
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 🏆 Top States by Insurance Transaction Value")
                    
                    # Creating a horizontal bar chart with a warm color scale
                    fig_5a = px.bar(df_5a, x='Total_Amount', y='State', 
                                   orientation='h',
                                   color='Total_Amount',
                                   color_continuous_scale='OrRd',
                                   labels={'Total_Amount': 'Total Amount (₹)', 'State': 'State'},
                                   template="plotly_dark")
                    
                    fig_5a.update_layout(height=450, showlegend=False, 
                                        yaxis={'categoryorder':'total ascending'},
                                        margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_5a, use_container_width=True)

                with col_table:
                    st.write("#### 📊 Leaderboard")
                    df_display_5a = df_5a.copy()
                    # Formatting currency for better readability
                    df_display_5a['Total_Amount'] = df_display_5a['Total_Amount'].apply(lambda x: f"₹{x:,.0f}")
                    st.dataframe(df_display_5a, hide_index=True, use_container_width=True, height=450)

                # Insight from your analysis
                st.success("Insurance transactions are highly concentrated in **urban and economically strong regions**, with **Karnataka** and **Maharashtra** maintaining a significant lead in market share.")
            
        elif selected_question_5 == "2. Which District/Pin code use it most?":
            # 1. Fetching Top Pin Codes by Insurance Transaction Value
            query_5b = """
            SELECT 
                Entity_Name AS Pincode, 
                SUM(Amount) AS Total_Amount 
            FROM top_insurance 
            WHERE Entity = 'Pincode'
            GROUP BY Entity_Name 
            ORDER BY Total_Amount DESC 
            LIMIT 10
            """
            df_5b = get_data(query_5b)

            if not df_5b.empty:
                # 2. Layout Alignment (2:1 Ratio)
                col_chart, col_table = st.columns([2, 1], gap="medium")

                with col_chart:
                    st.write("#### 📍 Top 10 Pincodes by Insurance Value")
                    
                    # Creating the bar chart
                    # Converting Pincode to string to ensure discrete axis labels
                    df_5b['Pincode'] = df_5b['Pincode'].astype(str)
                    
                    fig_5b = px.bar(df_5b, x='Total_Amount', y='Pincode', 
                                   orientation='h',
                                   color='Total_Amount',
                                   color_continuous_scale='OrRd',
                                   labels={'Total_Amount': 'Total Value (₹)', 'Pincode': 'Pincode'},
                                   template="plotly_dark")
                    
                    fig_5b.update_layout(height=450, showlegend=False, 
                                        yaxis={'categoryorder':'total ascending'},
                                        margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_5b, use_container_width=True)

                with col_table:
                    st.write("#### 📊 Pincode Stats")
                    df_display_5b = df_5b.copy()
                    # Formatting currency
                    df_display_5b['Total_Amount'] = df_display_5b['Total_Amount'].apply(lambda x: f"₹{x:,.0f}")
                    st.dataframe(df_display_5b, hide_index=True, use_container_width=True, height=450)
                
                # Business Insight
                st.info("The concentration of high-value insurance transactions in specific pincodes highlights **hyper-local hotspots**. These areas likely represent high-income residential or commercial clusters where financial literacy and digital trust are at their peak.")

        elif selected_question_5 == "3. Where should be the focus of Insurance business?":
            # 1. Fetching Pincode-level data for micro-market analysis
            query_5c = """
            SELECT 
                Entity_Name AS Pincode, 
                SUM(Amount) AS Total_Amount 
            FROM top_insurance 
            WHERE Entity = 'Pincode'
            GROUP BY Entity_Name 
            ORDER BY Total_Amount DESC 
            LIMIT 10
            """
            df_5c = get_data(query_5c)

            if not df_5c.empty:
                st.write("#### 🎯 Strategic Business Focus: High-Potential Micro-Markets")
                
                # Plotting Pincode-level analysis to reveal micro-markets
                df_5c['Pincode'] = df_5c['Pincode'].astype(str)
                fig_5c = px.bar(df_5c, x='Total_Amount', y='Pincode', 
                               orientation='h',
                               color='Total_Amount',
                               color_continuous_scale='Reds',
                               labels={'Total_Amount': 'Market Potential (₹)', 'Pincode': 'Pincode Cluster'},
                               template="plotly_dark")
                
                fig_5c.update_layout(height=450, showlegend=False, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_5c, use_container_width=True)

                # 2. Strategic Insights Summary
                st.info("### 📋 Business Expansion Strategy")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **Primary Target Zones:**
                    * **Tier-1 Hubs:** Focus on Karnataka and Maharashtra which lead in total transaction value.
                    * **Urban Clusters:** Prioritize metropolitan districts like Bengaluru Urban and Pune where adoption is highest.
                    """)
                
                with col2:
                    st.markdown("""
                    **Growth Drivers:**
                    * **Micro-Markets:** Pincode-level analysis reveals specific clusters (e.g., 560068, 560076) with massive demand potential.
                    * **Digital Maturity:** Focus marketing in areas with established digital payment infrastructure.
                    """)

                st.success("""
                **Final Recommendation:** To maximize ROI, the insurance business should adopt a **hyper-local marketing strategy** targeting the top 10 identified pincodes while maintaining a strong brand presence in high-volume states like Uttar Pradesh.
                """)


        # --- PERMANENT SUMMARY FOR CASE STUDY 5 ---
        st.divider()
        st.subheader("📌 Case Study Conclusion")
        
        st.markdown("""
            The analysis confirms that insurance transactions are heavily concentrated in **digitally advanced states** like Karnataka and Maharashtra. 
            At the district level, urban hubs such as **Bengaluru** and **Pune** dominate the landscape, highlighting the critical role metropolitan 
            areas play in driving digital financial adoption.

            Furthermore, the data identifies high **localized demand** within specific pincode clusters, presenting clear opportunities for 
            hyper-targeted marketing and strategic business expansion. 

            > **Final Insight:** The steady rise in transaction volume and value across these regions reflects a deep-seated and growing 
            **trust in digital ecosystems** for essential financial services like insurance.
            """)

        st.caption("Data Source: PhonePe Pulse Top Insurance Records")


# --- 5. DATA ANALYSIS PAGE ---
elif page == "Data Analysis":
    st.title(f"🌍 {sub_subject.replace('_', ' ').title()} Analysis")

    c1, c2 = st.columns(2)
    with c1:
        if "insurance" in sub_subject:
            year_range = list(range(2020, 2025))
        elif sub_subject == "aggregated_user":
            year_range = list(range(2018, 2023))
        else:
            year_range = list(range(2018, 2025))
        selected_year = st.selectbox("Select Year", year_range)
    with c2:
        selected_quarter = st.selectbox("Select Quarter", [1, 2, 3, 4])

    # SQL LOGIC
    if sub_subject == "top_user":
        query_state = f"SELECT State, SUM(Registered_Users) as Display_Value FROM top_user WHERE Year = {selected_year} AND Quarter = {selected_quarter} GROUP BY State"
        metric_label, unit = "Total Registered Users", "Count"
    elif sub_subject in ["top_transaction", "top_insurance"]:
        query_state = f"SELECT State, SUM(Amount) as Display_Value FROM {sub_subject} WHERE Year = {selected_year} AND Quarter = {selected_quarter} GROUP BY State"
        metric_label, unit = "Total Amount", "₹"
    elif sub_subject == "map_user":
        query_state = f"SELECT State, SUM(Registered_Users) as Display_Value FROM map_user WHERE Year = {selected_year} AND Quarter = {selected_quarter} GROUP BY State"
        metric_label, unit = "Total Registered Users", "Count"
    elif sub_subject == "aggregated_user":
        query_state = f"SELECT State, AVG(Percentage * 100) as Display_Value FROM aggregated_user WHERE Year = {selected_year} AND Quarter = {selected_quarter} GROUP BY State"
        metric_label, unit = "Avg User %", "%"
    elif "insurance" in sub_subject or "map_transaction" in sub_subject:
        query_state = f"SELECT State, SUM(Amount) as Display_Value FROM {sub_subject} WHERE Year = {selected_year} AND Quarter = {selected_quarter} GROUP BY State"
        metric_label, unit = "Total Amount", "₹"
    else:
        query_state = f"SELECT State, SUM(Transaction_amount) as Display_Value FROM aggregated_transaction WHERE Year = {selected_year} AND Quarter = {selected_quarter} GROUP BY State"
        metric_label, unit = "Total Transaction Amount", "₹"

    try:
        df_state = get_data(query_state)
        
        if df_state.empty:
            st.warning(f"⚠️ Details not available for {selected_year} Q{selected_quarter}.")
        else:
            df_state['State'] = df_state['State'].str.replace('-', ' ').str.title()
            df_state_sorted = df_state.sort_values(by="Display_Value", ascending=False).reset_index(drop=True)

            m1, m2 = st.columns(2)
            m1.metric("Highest Performing State", df_state_sorted.iloc[0]['State'])
            total_val = df_state['Display_Value'].sum()
            m2.metric(metric_label, f"₹{total_val:,.0f}" if unit == "₹" else f"{total_val:,.0f}" if unit == "Count" else f"{df_state_sorted.iloc[0]['Display_Value']:.2f}%")
            
            st.divider()

            col_map, col_rank = st.columns([4, 2])
            with col_map:
                geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                india_states = requests.get(geojson_url).json()
                fig_state = px.choropleth(df_state, geojson=india_states, featureidkey='properties.ST_NM', locations='State', color='Display_Value', color_continuous_scale='Reds')
                fig_state.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig_state, use_container_width=True)

            with col_rank:
                st.write("#### 🏆 State Rankings")
                df_state_sorted['Rank'] = df_state_sorted.index + 1
                df_state_sorted['Formatted_Value'] = df_state_sorted['Display_Value'].apply(lambda x: f"₹{x:,.0f}" if unit == "₹" else f"{x:,.0f}" if unit == "Count" else f"{x:.2f}%")
                st.dataframe(df_state_sorted[['Rank', 'State', 'Formatted_Value']], hide_index=True, use_container_width=True, height=450)

            if main_subject in ["Map Tables", "Top Tables"]:
                st.divider()
                selected_state = st.selectbox("Select State for Detailed View", df_state_sorted['State'].unique())
                state_slug = selected_state.lower().replace(' ', '-')

                if main_subject == "Map Tables":
                    st.header(f"📍 {selected_state} District-wise Analysis")
                    dist_col = "Registered_Users" if "user" in sub_subject else "Amount"
                    query_dist = f"SELECT District, SUM({dist_col}) as Dist_Value FROM {sub_subject} WHERE Year = {selected_year} AND Quarter = {selected_quarter} AND State = '{state_slug}' GROUP BY District"
                    df_dist = get_data(query_dist)
                    
                    if not df_dist.empty:
                        df_dist['District'] = df_dist['District'].str.title()
                        df_dist_sorted = df_dist.sort_values(by="Dist_Value", ascending=False).reset_index(drop=True)
                        d_col1, d_col2 = st.columns([4, 2])
                        with d_col1:
                            fig_dist = px.bar(df_dist_sorted.head(10), x='Dist_Value', y='District', orientation='h', color='Dist_Value', color_continuous_scale='Reds')
                            st.plotly_chart(fig_dist, use_container_width=True)
                        with d_col2:
                            st.write("#### 🏆 District Rank")
                            df_dist_sorted['Rank'] = df_dist_sorted.index + 1
                            df_dist_sorted['Value'] = df_dist_sorted['Dist_Value'].apply(lambda x: f"{x:,.0f}" if "user" in sub_subject else f"₹{x:,.0f}")
                            st.dataframe(df_dist_sorted[['Rank', 'District', 'Value']], hide_index=True, use_container_width=True, height=400)

                elif main_subject == "Top Tables":
                    st.header(f"🔝 {selected_state} Top Specifics")
                    val_col = "Registered_Users" if "user" in sub_subject else "Amount"
                    fmt = "Count" if "user" in sub_subject else "₹"
                    
                    query_pin = f"SELECT Entity_Name as Pincode, SUM({val_col}) as Pin_Value FROM {sub_subject} WHERE Year = {selected_year} AND Quarter = {selected_quarter} AND State = '{state_slug}' AND Entity = 'Pincode' GROUP BY Entity_Name ORDER BY Pin_Value DESC LIMIT 10"
                    df_pin = get_data(query_pin)
                    if not df_pin.empty:
                        st.write("#### 📮 Top 10 Pincodes")
                        df_pin['Rank'] = range(1, len(df_pin) + 1)
                        df_pin['Value'] = df_pin['Pin_Value'].apply(lambda x: f"{x:,.0f}" if fmt == "Count" else f"₹{x:,.0f}")
                        st.dataframe(df_pin[['Rank', 'Pincode', 'Value']], hide_index=True, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing query: {e}")























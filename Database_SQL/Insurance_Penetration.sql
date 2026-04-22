use phonepe_db;

# Insurance Penetration and Growth Potential Analysis

# Is insurance usage increasing or not?
SELECT 
    Year,
    SUM(Amount) AS Total_Amount
FROM aggregated_insurance
GROUP BY Year
ORDER BY Year;


# Which states use insurance the most?
SELECT 
    State,
    SUM(Amount) AS Total_Amount
FROM aggregated_insurance
GROUP BY State
ORDER BY Total_Amount DESC
LIMIT 10;



# Is it increasing over time?
SELECT 
    SUM(Count) AS Total_Policies,
    SUM(Amount) AS Total_Value
FROM aggregated_insurance;

use phonepe_db;

# Insurance Transactions Analysis

# Which states generate highest insurance transaction value?
SELECT 
    State,
    SUM(Amount) AS Total_Amount
FROM top_insurance
GROUP BY State
ORDER BY Total_Amount DESC
LIMIT 10;


# Which districts use insurance the most?
SELECT 
    Entity_Name AS District,
    SUM(Amount) AS Total_Amount
FROM top_insurance
WHERE Entity = 'District'
GROUP BY Entity_Name
ORDER BY Total_Amount DESC
LIMIT 10;


# Micro-level insight — exactly where demand is highest
SELECT 
    Entity_Name AS Pincode,
    SUM(Amount) AS Total_Amount
FROM top_insurance
WHERE Entity = 'Pincode'
GROUP BY Entity_Name
ORDER BY Total_Amount DESC
LIMIT 10;


# Count → number of transactions
# Amount → value
SELECT 
    SUM(Count) AS Total_Count,
    SUM(Amount) AS Total_Amount
FROM top_insurance;

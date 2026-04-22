use phonepe_db;


#  User Registration Analysis

# Which states have the highest number of registered users?
SELECT 
    State,
    SUM(Registered_Users) AS Total_Users
FROM top_user
GROUP BY State
ORDER BY Total_Users DESC
LIMIT 10;


# Which districts have the most users?
SELECT 
    Entity_Name AS District,
    SUM(Registered_Users) AS Total_Users
FROM top_user
WHERE Entity = 'District'
GROUP BY Entity_Name
ORDER BY Total_Users DESC
LIMIT 10;


# Are users increasing every year?
SELECT 
    Year,
    SUM(Registered_Users) AS Total_Users
FROM top_user
GROUP BY Year
ORDER BY Year;



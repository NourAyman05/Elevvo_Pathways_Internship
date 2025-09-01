import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3  


conn = sqlite3.connect('Chinook_Sqlite.sqlite')  

# Revenue per Region 
query = """
SELECT 
    c.Country,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS TotalRevenue,
    COUNT(DISTINCT c.CustomerId) AS CustomerCount,
    ROUND(SUM(il.UnitPrice * il.Quantity) / COUNT(DISTINCT c.CustomerId), 2) AS AvgRevenuePerCustomer
FROM Invoice i
JOIN Customer c ON i.CustomerId = c.CustomerId
JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
GROUP BY c.Country
"""

df = pd.read_sql_query(query, conn)
conn.close()

sns.set_style("whitegrid")

plt.figure(figsize=(10, 8))
plt.pie(
    df['TotalRevenue'],
    labels=df['Country'],
    autopct='%1.1f%%',
    startangle=140,
    colors=sns.color_palette('plasma', len(df))
)
plt.title('Total Revenue Distribution by Country', fontsize=16)
plt.axis('equal')  
plt.savefig("outputs/Revenue_Per_Region_pie.png")
plt.show()

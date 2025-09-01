import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('Chinook_Sqlite.sqlite')  

# Monthly performance
query = """
SELECT 
    strftime('%Y-%m', i.InvoiceDate) AS Month,
    SUM(il.UnitPrice * il.Quantity) AS MonthlyRevenue
FROM InvoiceLine il
JOIN Invoice i ON il.InvoiceId = i.InvoiceId
GROUP BY Month
ORDER BY Month;
"""

df = pd.read_sql_query(query, conn)
conn.close()

df['Month'] = pd.to_datetime(df['Month'])
sns.set_style("whitegrid")

plt.figure(figsize=(12, 6))
plt.plot(df['Month'], df['MonthlyRevenue'], marker='o', color='teal', linewidth=2)
plt.title('Monthly Revenue Trend', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/Monthly_Performance_lineChart.png")
plt.show()

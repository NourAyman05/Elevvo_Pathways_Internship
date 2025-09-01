import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("Chinook_Sqlite.sqlite")

#Top selling products
query = """
SELECT 
    t.Name AS TrackName,
    a.Title AS Album,
    ar.Name AS Artist,
    SUM(il.Quantity) AS TotalUnitsSold
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
JOIN Album a ON t.AlbumId = a.AlbumId
JOIN Artist ar ON a.ArtistId = ar.ArtistId
GROUP BY t.TrackId
ORDER BY TotalUnitsSold DESC
LIMIT 50;
"""
df = pd.read_sql_query(query, conn)
conn.close()

df['Label'] = df['TrackName'] + " (" + df['Artist'] + ")"
plt.figure(figsize=(13,10))
plt.barh(df['Label'], df['TotalUnitsSold'], color='teal')
plt.xlabel("Total Units Sold ($)", fontsize=12)
plt.ylabel("Tracks by their Artists", fontsize=12)
plt.title("Top 50 Selling Tracks", fontsize=16, fontweight='bold')
plt.gca().invert_yaxis()  # Highest at the top
plt.tight_layout()
plt.savefig("outputs/top_selling_tracks.png")
plt.show()

#------------------------------------------

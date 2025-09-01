--TOP Selling products
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


--Revenue per Region and average revenue per customer
SELECT 
    c.Country,
    ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS TotalRevenue,
    COUNT(DISTINCT c.CustomerId) AS CustomerCount,
    ROUND(SUM(il.UnitPrice * il.Quantity) / COUNT(DISTINCT c.CustomerId), 2) AS AvgRevenuePerCustomer
FROM Invoice i
JOIN Customer c ON i.CustomerId = c.CustomerId
JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
GROUP BY c.Country
ORDER BY AvgRevenuePerCustomer DESC;

--Monthly performance
SELECT 
    strftime('%Y-%m', i.InvoiceDate) AS Month,
    SUM(il.UnitPrice * il.Quantity) AS MonthlyRevenue
FROM InvoiceLine il
JOIN Invoice i ON il.InvoiceId = i.InvoiceId
GROUP BY Month
ORDER BY Month;


--Bonus
SELECT Artist, Track, TotalSold
FROM (
    SELECT 
        ar.Name AS Artist,
        t.Name AS Track,
        SUM(il.Quantity) AS TotalSold,
        RANK() OVER (PARTITION BY ar.ArtistId ORDER BY SUM(il.Quantity) DESC) AS Rank
    FROM InvoiceLine il
    JOIN Track t ON il.TrackId = t.TrackId
    JOIN Album a ON t.AlbumId = a.AlbumId
    JOIN Artist ar ON a.ArtistId = ar.ArtistId
    GROUP BY ar.ArtistId, t.TrackId
)
WHERE Rank = 1;












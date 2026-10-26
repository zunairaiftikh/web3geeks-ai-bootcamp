-- Q1. Where are our customers? Customers per country, top 5.


-- Result (first five rows):
-- USA     13
-- Canada  8
-- Brazil  5
-- France  5
-- Germany 4

-- Business meaning:
--We have to focus more on these five countries as our main customers belong to these countries . The top 5 countries have 35 
--customers out of 59 that makes about 59% of total customers

SELECT Country, COUNT(*) AS total_customers
FROM Customer
GROUP BY Country
ORDER BY total_customers DESC
LIMIT 5;


--Q2. Which countries bring in the most revenue, and how much per customer? Top 5.
SELECT c.Country,
       ROUND(SUM(i.Total), 2) AS total_revenue,
       COUNT(DISTINCT c.CustomerId) AS customers,
       ROUND(SUM(i.Total) / COUNT(DISTINCT c.CustomerId), 2) AS revenue_per_customer
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY total_revenue DESC
LIMIT 5;

--Result
/*
Country	total_revenue	customers	revenue_per_customer
USA	523.06	13	40.24
Canada	303.96	8	37.99
France	195.1	5	39.02
Brazil	190.1	5	38.02
Germany	156.48	4	39.12



Business meaning: 
The USA earns the most ($523.06) with 13 customers, about $40 from each customer, The revenue from each customer is about 37 to 40USD thats almost 
same for the top countries, the main difference is of number of customer, more customers means more revenue as each customer spend almost the same.

*/
--Who are our 5 best customers by total spend, and where are they from?
SELECT c.CustomerId, c.FirstName, c.LastName, c.Country,
       ROUND(SUM(i.Total),2) as total_spent
FROM Customer c
JOIN Invoice i ON c.CustomerId=i.CustomerId
GROUP BY c.CustomerId
ORDER BY total_spent DESC
LIMIT 5;

/* Result:
CustomerId	FirstName	LastName	Country	total_spent
6	Helena	Holý	Czech Republic	49.62
26	Richard	Cunningham	USA	47.62
57	Luis	Rojas	Chile	46.62
45	Ladislav	Kovács	Hungary	45.62
46	Hugh	O'Reilly	Ireland	45.62
Business meaning: 
These are 5 best customers belong to 5 different countries that shows that our customers are spread accross different countries, the highest 
amount spent by Holy is 49.62 and the average amount these top 5 best customers are 39.4 usd.

*/

--Q4 Which genres earn the most? Revenue per genre and its share of total revenue, top 5.

SELECT g.Name AS genre,
       ROUND(SUM(il.UnitPrice * il.Quantity),2) as revenue,
       ROUND(100.0 * SUM(il.UnitPrice * il.Quantity)
             / (SELECT SUM(UnitPrice * Quantity) FROM InvoiceLine), 2) AS pct_of_total
FROM InvoiceLine il
JOIN Track t ON il.TrackId = t.TrackId
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY g.Name
ORDER BY revenue DESC
LIMIT 5;

/*
Result: genre	revenue	pct_of_total
Rock	826.65	35.5
Latin	382.14	16.41
Metal	261.36	11.22
Alternative & Punk	241.56	10.37
TV Shows	93.53	4.02

Business meaning: Rock is the genre which earns most with about 826.65usd revenue that makes 35.5% of the total revenue and the top 3 genres (Rock, Latin and Metal) together
 make 63% of all the sales

*/
--Q5 Which artists sell the most tracks? Top 5 by units sold.
-- Q5: Which artists sell the most tracks?
SELECT
    a.Name AS artist,
    SUM(il.Quantity) AS units_sold
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY a.ArtistId, a.Name
ORDER BY units_sold DESC
LIMIT 5;

/*
artist	units_sold
Iron Maiden	140
U2	107
Metallica	91
Led Zeppelin	87
Os Paralamas Do Sucesso	45

Business meaning: Iron Maiden is the top artist who sold 140 units . The total sold units are 2240 in which is 6% of totall and top 5 artist make 
21% of the total so our sales are spread among different artists.

*/
--Q6 Which support agent looks after the most valuable customers? Customers and revenue per agent?

SELECT
    e.FirstName,
    e.LastName,
    COUNT(DISTINCT c.CustomerId) AS customer_count,
    ROUND(SUM(i.Total), 2) AS total_revenue,
    ROUND(SUM(i.Total) / COUNT(DISTINCT c.CustomerId), 2) AS revenue_per_customer

FROM Employee e
LEFT JOIN Customer c
    ON e.EmployeeId = c.SupportRepId
LEFT JOIN Invoice i
    ON c.CustomerId = i.CustomerId
WHERE e.Title = 'Sales Support Agent'
GROUP BY e.EmployeeId, e.FirstName, e.LastName
ORDER BY total_revenue DESC;

/*  result:
FirstName	LastName	customer_count	total_revenue	revenue_per_customer
Jane	Peacock	21	833.04	39.67
Margaret	Park	20	775.4	38.77
Steve	Johnson	18	720.16	40.01


Business meaning:  Peacock looks after the most valuable customer group, 21 customers with 833.02 usd beacuse he has more customer
 , not because they spend more, since all three agents’ customers spend about $39 to $40 each.
*/

--Q7 How much of the catalogue has never sold? Tracks with no sales, out of all tracks.
SELECT
    COUNT(DISTINCT t.TrackId) as total_tracks,
    SUM(CASE WHEN il.TrackId IS NULL THEN 1 ELSE 0 END)
        AS never_sold_tracks,
    ROUND(
        100.0 * SUM(CASE WHEN il.TrackId IS NULL THEN 1 ELSE 0 END)
        / COUNT(DISTINCT t.TrackId),
        2
    ) AS never_sold_pct
FROM Track t
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId;
/*
result: 
total_tracks	never_sold_tracks	never_sold_pct
3503	1519	43.36

Business meaning: It shows that 1519 out of 3503 tracks are never sold that makes 43.36% of the total sales

*/
--Q8 Monthly revenue with a running total. In which month did total revenue pass $1,000?

WITH monthly AS (
    SELECT
        strftime('%Y-%m', InvoiceDate) AS month,
        SUM(Total) AS monthly_revenue
    FROM Invoice
    GROUP BY strftime('%Y-%m', InvoiceDate)
),
running AS (
    SELECT
        month,
        monthly_revenue,
        SUM(monthly_revenue) OVER (ORDER BY month) AS running_total
    FROM monthly
)
SELECT
    month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(running_total, 2) AS running_total
FROM running
WHERE running_total > 1000
ORDER BY month
LIMIT 1;
/*
result:month	monthly_revenue	running_total
2011-02	37.62	1006.15

business meaning: total revenue first exceeded  $1,000 in February 2011, reaching $1,006.15.

*/

--Q9 Month over month change: each month's revenue, the previous month's revenue and the % change. Which month had the biggest drop?

-- Q9: Which month had the biggest month-over-month revenue drop?

WITH monthly AS (
    SELECT
        strftime('%Y-%m', InvoiceDate) AS month,
        SUM(Total) AS monthly_revenue
    FROM Invoice
    GROUP BY strftime('%Y-%m', InvoiceDate)
),
previous_month AS (
    SELECT
        month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (ORDER BY month) AS previous_revenue
    FROM monthly
)
SELECT
    month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(previous_revenue, 2) AS previous_revenue,
    ROUND(
        100.0 * (monthly_revenue - previous_revenue)
        / previous_revenue,
        2
    ) AS change_pct
FROM previous_month
WHERE previous_revenue IS NOT NULL
ORDER BY change_pct ASC
LIMIT 1;
/*
month    monthly_revenue    previous_revenue    change_pct
2009-01    35.64        
2009-02    37.62    35.64    5.56
2009-03    37.62    37.62    0.0
2009-04    37.62    37.62    0.0
2009-05    37.62    37.62    0.0
2009-06    37.62    37.62    0.0
2009-07    37.62    37.62    0.0
2009-08    37.62    37.62    0.0
2009-09    37.62    37.62    0.0
2009-10    37.62    37.62    0.0
2009-11    37.62    37.62    0.0
2009-12    37.62    37.62    0.0
2010-01    52.62    37.62    39.87
2010-02    46.62    52.62    -11.4
2010-03    44.62    46.62    -4.29
2010-04    37.62    44.62    -15.69
2010-05    37.62    37.62    0.0
2010-06    37.62    37.62    0.0
2010-07    37.62    37.62    0.0
2010-08    37.62    37.62    0.0
2010-09    36.63    37.62    -2.63
2010-10    37.62    36.63    2.7
2010-11    37.62    37.62    0.0
2010-12    37.62    37.62    0.0
2011-01    37.62    37.62    0.0
2011-02    37.62    37.62    0.0
2011-03    37.62    37.62    0.0
2011-04    51.62    37.62    37.21
2011-05    42.62    51.62    -17.44
2011-06    50.62    42.62    18.77
2011-07    37.62    50.62    -25.68
2011-08    37.62    37.62    0.0
2011-09    37.62    37.62    0.0
2011-10    37.62    37.62    0.0
2011-11    23.76    37.62    -36.84
2011-12    37.62    23.76    58.33
2012-01    37.62    37.62    0.0
2012-02    37.62    37.62    0.0
2012-03    37.62    37.62    0.0
2012-04    37.62    37.62    0.0
2012-05    37.62    37.62    0.0
2012-06    37.62    37.62    0.0
2012-07    39.62    37.62    5.32
2012-08    47.62    39.62    20.19
2012-09    46.71    47.62    -1.91
2012-10    42.62    46.71    -8.76
2012-11    37.62    42.62    -11.73
2012-12    37.62    37.62    0.0
2013-01    37.62    37.62    0.0
2013-02    27.72    37.62    -26.32
2013-03    37.62    27.72    35.71
2013-04    33.66    37.62    -10.53
2013-05    37.62    33.66    11.76
2013-06    37.62    37.62    0.0
2013-07    37.62    37.62    0.0
2013-08    37.62    37.62    0.0
2013-09    37.62    37.62    0.0
2013-10    37.62    37.62    0.0
2013-11    49.62    37.62    31.9
2013-12    38.62    49.62    -22.17
month	monthly_revenue	previous_revenue	change_pct
2011-11	23.76	37.62	-36.84
business meaning: “Revenue is very steady at about $37.62 a month, with no change in 35 of 59 months. The biggest drop was November 2011, down 36.84% to $23.76, 
and December 2011 bounced back by 58.33%.”
*/

--Q10 For each month, rank the countries by revenue. Which country is number 1 most often?

WITH country_monthly AS (
    SELECT
        strftime('%Y-%m', i.InvoiceDate) AS month,
        c.Country,
        SUM(i.Total) AS monthly_revenue
    FROM Invoice i
    JOIN Customer c
        ON i.CustomerId = c.CustomerId
    GROUP BY
        strftime('%Y-%m', i.InvoiceDate),
        c.Country
),
ranked AS (
    SELECT
        month,
        Country,
        monthly_revenue,
        RANK() OVER (
            PARTITION BY month
            ORDER BY monthly_revenue DESC
        ) AS revenue_rank
    FROM country_monthly
)
SELECT
    Country,
    COUNT(*) AS months_at_number_1
FROM ranked
WHERE revenue_rank = 1
GROUP BY Country
ORDER BY months_at_number_1 DESC
LIMIT 1;
/* result:Country	months_at_number_1
USA	24

business meaning: USA is on number one inmonthly revenue
*/
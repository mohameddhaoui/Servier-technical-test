WITH RECURSIVE dates(date) AS (
  VALUES('2019-01-01')
  UNION ALL
  SELECT date(date, '+1 day')
  FROM dates
  WHERE date  < '2019-12-31'
)
SELECT DT.date as date, IFNULL(sum( TR.prod_price* TR.prod_qty),0) as ventes  FROM dates DT
left join TRANSACTIONS  TR
ON DT.date=TR.date
group by DT.date
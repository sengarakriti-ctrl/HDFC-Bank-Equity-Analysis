CREATE DATABASE HDFC_Analytics;
USE HDFC_Analytics;
CREATE TABLE Stock_Market_Data (
    Trade_Date DATE PRIMARY KEY,
    Open_Price DECIMAL(10, 2),
    High_Price DECIMAL(10, 2),
    Low_Price DECIMAL(10, 2),
    Close_Price DECIMAL(10, 2),
    Adj_Close_Price DECIMAL(10, 2),
    Volume BIGINT
);
INSERT INTO Stock_Market_Data (
CREATE TABLE Bank_Quarterly_Financials (
    Quarter_Year VARCHAR(10) PRIMARY KEY, -- e.g., 'Q1_2025'
    Net_Interest_Income DECIMAL(15, 2),    -- Earnings from loans
    Net_Profit DECIMAL(15, 2),            -- Bottom line
    Gross_NPA_Pct DECIMAL(5, 2),          -- Bad loans percentage
    Net_NPA_Pct DECIMAL(5, 2),
    CASA_Ratio DECIMAL(5, 2),             -- Current & Savings Account ratio
    Capital_Adequacy_Ratio DECIMAL(5, 2)
);
INSERT INTO Bank_Quarterly_Financials(Quarter_year, CASA_Ratio, Gross_NPA_Pct, Net_Interest_Income)
VALUES 
('2020_Q3', 37.70, 1.26, 3.40),
('2020_Q4', 38.20, 1.24, 3.44),
('2021_Q1', 36.30, 1.33, 3.47),
('2021_Q2', 35.30, 1.36, 3.46);
SELECT*FROM Bank_Quarterly_Financials;
INSERT INTO Bank_Quarterly_Financials(Quarter_year, CASA_Ratio, Gross_NPA_Pct, Net_Interest_Income)
VALUES 
('2020_Q3', 37.70, 1.26, 3.40),
('2020_Q4', 38.20, 1.24, 3.44);

WITH Quarterly_Stock AS (
    SELECT 
        CASE 
            WHEN Trade_Date BETWEEN '2020-07-01' AND '2020-09-30' THEN '2020_Q3'
            WHEN Trade_Date BETWEEN '2020-10-01' AND '2020-12-31' THEN '2020_Q4'
            WHEN Trade_Date BETWEEN '2021-01-01' AND '2021-03-31' THEN '2021_Q1'
            WHEN Trade_Date BETWEEN '2021-04-01' AND '2021-06-30' THEN '2021_Q2'
        END AS Quarter_Lookup,
        AVG(Close_Price) AS Avg_Stock_Price
    FROM Stock_Market_Data
    GROUP BY Quarter_Lookup
)
SELECT 
    m.Quarter_Year, m.CASA_Ratio, m.Gross_NPA_Pct, s.Avg_Stock_Price
FROM Bank_Quarterly_Financials m
JOIN Quarterly_Stock s ON m.Quarter_Year = s.Quarter_Lookup
WHERE s.Avg_Stock_Price IS NOT NULL;
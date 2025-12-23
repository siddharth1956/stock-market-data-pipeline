📊 Stock Market Daily Data Pipeline

📌 Project Overview

This project implements an end-to-end data engineering pipeline to ingest, process, model, and analyze daily stock market data using the Alpha Vantage API and Snowflake as the cloud data platform.

The pipeline handles semi-structured JSON data, transforms it into analytics-ready star schema tables, applies data quality checks, and automates processing using Snowflake Tasks.


🧭 Project Track & Platform
	•	Track: Track D — Stock Market Daily Pipeline
	•	Cloud Platform: Snowflake (AWS)
	•	Programming Language: Python & SQL


🔗 Data Source
	•	Alpha Vantage API
https://www.alphavantage.co/documentation/

The project uses the TIME_SERIES_DAILY endpoint to retrieve:
	•	Open price
	•	High price
	•	Low price
	•	Close price
	•	Volume


🏗️ Architecture Overview
Alpha Vantage API
        ↓
Python Ingestion Script
        ↓
Landing Zone (Raw JSON)
        ↓
Snowflake Internal Stage
        ↓
RAW Schema (VARIANT JSON)
        ↓
Flattened Relational View
        ↓
STAR Schema (Fact & Dimensions)
        ↓
Automated Refresh (Snowflake Task)

## 📂 Repository Structure

```text
stock-market-data-pipeline/
├── src/
│   └── ingest.py
├── sql/
│   ├── create_tables.sql
│   ├── star_schema.sql
│   └── automation.sql
├── docs/
│   ├── er_diagram.png
│   └── star_schema.png
├── landing_zone/
│   └── daily_stock_AAPL_*.json
├── README.md
└── requirements.txt

⚙️ Data Ingestion (Week 5)
	•	Data is fetched from Alpha Vantage using a Python script (ingest.py)
	•	API credentials are securely handled using environment variables
	•	Raw API responses are stored as JSON files in the landing zone

Secure API Key Handling
export ALPHAVANTAGE_API_KEY=your_api_key
🧱 Data Modeling (Week 6)
	•	A 3NF (normalized) schema was designed to eliminate redundancy
	•	An ER diagram documents entities and relationships
	•	Deduplication is handled using:
	•	Stock symbol
	•	Trade date as a natural key

⭐ Star Schema Design (Week 7)

To support analytical workloads, the data is transformed into a star schema:

Dimension Tables
	•	dim_stock — unique stock symbols
	•	dim_date — calendar attributes

Fact Table
	•	fact_daily_stock_price — daily stock prices and volume

This structure enables:
	•	Fast aggregations
	•	Time-series analysis
	•	BI and reporting use cases


🔍 Handling Semi-Structured Data
	•	Raw JSON is stored using Snowflake’s VARIANT data type
	•	Nested time-series data is transformed using:
	•	LATERAL FLATTEN()
	•	Each trading day becomes a relational row


🛡️ Governance & Data Quality (Week 8)

Data Quality Rules
	•	No negative prices
	•	No negative volume
	•	Mandatory stock symbol and trade date

Validation is enforced using:
	•	Filtered inserts
	•	Validation queries at the STAR layer

Example:
SELECT *
FROM STAR.fact_daily_stock_price
WHERE open_price < 0
   OR close_price < 0
   OR volume < 0;

🔐 Security Best Practices
	•	API keys are stored in environment variables
	•	No secrets are committed to GitHub
	•	.env files are excluded from version control


⏱️ Automation
	•	Snowflake Tasks are used to automate daily refresh of star schema tables
	•	The pipeline runs on a scheduled basis without manual intervention

🎥 Final Demonstration

A 5-minute demo video showcases:
	•	Data ingestion
	•	Snowflake RAW → STAR transformation
	•	Automation using Snowflake Tasks
	•	Final analytical tables


🚧 Challenges Faced
	•	Handling deeply nested JSON structures
	•	Managing Snowflake schema context
	•	Understanding VARIANT and FLATTEN usage
	•	Working within API rate limits


✅ Final Outcome

The project delivers:
	•	A fully automated, governed data pipeline
	•	Analytics-ready star schema tables
	•	Secure, scalable cloud implementation
	•	Complete documentation and version control


👤 Author

Siddharth Shetty
GitHub: https://github.com/siddharth1956

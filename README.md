# Globant Challenge

This project is a Proof of Concept (PoC) for a data migration solution. It allows ingestion of historical data from CSV files, reception of new data via REST API, and backup/restore of database content using AVRO format. Additionally, it includes a modern web-based UI for interaction and reporting.
> **Note:** The database starts empty. You must populate the tables using the web UI, CSV uploads for historical data an JSON upload for new data.

## 📁 Project Structure

```
globantchallenge/
├── app
│   ├── api.py 							# API endpoints for data ingestion
│   ├── db_dml.py 						#DB DML operations
│   ├── main.py 						# FastAPI app
│   ├── static 							# JS files (charts)
│   │   ├── above_average_chart.js
│   │   └── stacked_quarterly_chart.js
│   ├── templates 						# HTML templates (Jinja2)
│   │   └── index.html
│   └── utils 							# Python utilities
│       └── logger_manager.py 
├── backup 								# Avro backup files
├── data 								# CSV data
│   ├── departments.csv
│   ├── hired_employees.csv
│   └── jobs.csv
├── db
│   ├── database.py 					# DB engine and session management
│   └── models.py 						# SQLAlchemy models
├── logs 								# Logs of invalid data or errors
├── poc.db 								# SQLite Database
├── requirements.txt 					# Python dependencies
├── scripts								
│	├── backup.py						# Script to bulk load historical CSV data
│	├── load_csv.py						# Script to generate AVRO backups
│	└── restore.py						# Script to restore data from AVRO files
├── Dockerfile 							# Deployment config
└── README.md                  			# Project documentation
```

## 🚀 Features

- Upload CSV (historical data) and JSON (new data) data using a web interface.
- Validate and log invalid rows to persistent files.
- Insert clean data into a relational database.
- REST API endpoint for ingesting JSON-formatted transactions.
- AVRO-based backup and restore for the full database or specific tables.
- Interactive reports (Plotly charts) with date filtering to visualize:
  - Quarterly hires by department and job (default selected quarters 2021).
  - Departments hiring above average for a given year range (default select 2021).
- UI built with HTML + JavaScript + Plotly, powered by FastAPI backend.
- Deployable to Render using Docker.

## ⚙️ Setup Instructions

### 1. Prerequisites

- Python 3.10+
- SQLite
- Docker (optional, for deployment)
- pip (Python package manager)

### 2. Clone the Repository

```bash
git clone https://github.com/sergordon/GlobantChallenge.git
cd GlobantChallenge
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

Open your browser at `http://localhost:8000`.

## 🐳 Docker Deployment

Build and run the container:

```bash
docker build -t globant-challenge .
docker run -d -p 8000:8000 globant-challenge
```

## 🌐 Web Interface

The app provides an intuitive UI:

- **Upload CSV/JSON**: Supports all three tables (jobs, departments, hired_employees).
- **Backup & Restore**: Easily backup or restore full DB or specific tables.
- **Reports**: Explore two reports with date filters and interactive charts.
> **Note:** The database starts empty. You must upload your own data using the UI.

## 🧪 API Endpoints

- `POST /upload-csv/`
- `POST /upload-json/`
- `POST /backup/`
- `POST /restore/`
- `POST /api/{table_name}` (API ingestion)

## 📊 Reports

### Report 1: Quarterly Hiring by Department and Job
- Stacked bar chart
- Filter by date range
- Dropdown to filter by department

### Report 2: Above-Average Hiring Departments
- Shows the number of hires in departments above the average hiring rate for a parametrized year
- Displayed as horizontal bar chart

## 🔄 Backup and Restore

Backups are saved in `.avro` format and placed in the `backup/` folder.

- **Backup entire DB or individual tables**
- **Restore from `.avro` files easily**

## 📝 Logs

Logs are saved in the `logs/` folder:

- `sql_errors.log` — DB-related issues
- `api_invalid_rows.log` — invalid JSON rows from the API
- `historic_load_errors_table_*.log` — invalid CSV rows per table

---

## 📌 Notes

- **Empty DB**: In order to see logs for invalid rows and load data feature, **you must populate the database via the UI**.
- Invalid rows are logged; valid rows are inserted.
- Error and success messages are shown in the browser via dialogs.
---

## 🧪 Example Data

Sample payloads for testing:
For `jobs`:

```json
[
  {"id": 1, "job": "Data Engineer"},
  {"id": 2, "job": "ML Engineer"}
]
```

For `hired_employees`:

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "datetime": "2021-01-10T10:00:00Z",
    "department_id": 1,
    "job_id": 1
  }
]
```
## Access Online

🔗 [Open Render Deployment](https://globantchallenge.onrender.com/)


---
## 👤 Author

**Sergio Gordon**  
[GitHub](https://github.com/sergordon)

## 🛡️ License

This project is licensed under the MIT License.

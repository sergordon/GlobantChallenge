# Globant Challenge

This project is a Proof of Concept (PoC) for a data migration solution. It allows ingestion of historical data from CSV files, reception of new data via REST API, and backup/restore of database content using AVRO format. Additionally, it includes a modern web-based UI for interaction and reporting. The design follows next the data rules:
  - Transactions that don't accomplish the rules must not be inserted but they must be logged.
  - All the fields are required.

## 🌐 Live Demo

👉 [Access the UI on Render](https://globantchallenge.onrender.com/)

> **Note:** The database starts empty. You must populate the tables using the web UI, CSV uploads for historical data an JSON upload for new data.

## 📁 Project Structure

```
globantchallenge/
├── app
│   ├── api.py            # API endpoints for data ingestion
│   ├── db_dml.py 				#DB DML operations
│   ├── main.py 					# FastAPI app
│   ├── static            # JS files (charts)
│   │   ├── above_average_chart.js
│   │   └── stacked_quarterly_chart.js
│   ├── templates         # HTML templates (Jinja2)
│   │   └── index.html
│   └── utils             # Python utilities
│       └── logger_manager.py 
├── backup                # Avro backup files
├── data                  # CSV data
│   ├── departments.csv
│   ├── hired_employees.csv
│   └── jobs.csv
├── db
│   ├── database.py       # DB engine and session management
│   └── models.py         # SQLAlchemy models
├── logs                  # Logs of invalid data or errors
├── poc.db 								# SQLite Database
├── requirements.txt 			# Python dependencies
├── scripts								
│	├── backup.py						# Script to bulk load historical CSV data
│	├── load_csv.py					# Script to generate AVRO backups
│	└── restore.py					# Script to restore data from AVRO files
├── Dockerfile 						# Deployment config
└── README.md             # Project documentation
```

## ⚙️ Features

### ✅ CSV Upload
- Upload files for `jobs`, `departments`, and `hired_employees`.
- Validates data before inserting into DB.
- Invalid rows are logged in `logs/`.

### ✅ JSON Upload
- REST API endpoint for ingesting.
- Accepts JSON payload for insertion.
- Invalid entries are logged and do not break insertion of valid records.

### ✅ Backup & Restore
- Full or table-specific backup in AVRO format.
- Restore functionality from AVRO files.

### ✅ Charts and Reports
- Quarterly hires by department and job (default selected quarters 2021).
- Departments hiring above average for a given year range (default select 2021).
- Filters by date range.
- Data table + visual chart side by side.
- Automatic refresh on load and report button.

### ✅ Log Viewer
- View backend logs directly from the web UI.
---
## 📊 Technologies Used

- **Python 3.11+**
- **FastAPI**
- **SQLAlchemy**
- **SQLite (local DB)**
- **Pandas**
- **Plotly.js**
- **HTML/CSS + JS**
- **SweetAlert2 + Toastr for feedback**
---
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

## 🌐 Web Interface 👉 [Access the UI on Render](https://globantchallenge.onrender.com/)

The app provides an intuitive UI:

## Access Online

🔗 [Open Render Deployment](https://globantchallenge.onrender.com/)

- **Upload CSV/JSON**: Supports all three tables (jobs, departments, hired_employees).
- **Backup & Restore**: Easily backup or restore full DB or specific tables.
- **Reports**: Explore two reports with date filters and interactive charts.
- **Logs**: View log files from UI.
> **Note:** The database starts empty. You must upload your own data using the UI.

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
  {"id": 501, "job": "Data Engineer"},
  {"id": 502, "job": "ML Engineer"}
]
```

For `departments`:

```json
[
  {"id": 901, "department": "II+D"},
  {"id": 902, "department": "TI"}
]
```

For `hired_employees`:

```json
[
  {
    "id": 3000,
    "name": "Sergio Gordon",
    "datetime": "2025-06-01T10:00:00Z",
    "department_id": 901,
    "job_id": 501
  }
]

---
## 👤 Author

**Sergio Gordon**  
[GitHub](https://github.com/sergordon)

## 🛡️ License

This project is licensed under the MIT License.

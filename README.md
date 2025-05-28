# Globant Challenge

This project is a Proof of Concept (PoC) for a migration solution. It allows ingestion of historical data from CSV files, reception of new data via REST API, and backup/restore of database content using AVRO format. Additionally, it includes a modern web-based UI for interaction and reporting.

## 📁 Project Structure

```
globantchallenge/
├── app
│   ├── api.py 							        # API endpoints for data ingestion
│   ├── db_dml.py 						      #DB DML operations
│   ├── main.py 						        # FastAPI app
│   ├── static 							        # JS files (charts)
│   │   ├── above_average_chart.js
│   │   └── stacked_quarterly_chart.js
│   ├── templates 						      # HTML templates (Jinja2)
│   │   └── index.html
│   └── utils 							        # Python utilities
│       └── logger_manager.py 
├── backup 								          # Avro backup files
├── data 								            # CSV data
│   ├── departments.csv
│   ├── hired_employees.csv
│   └── jobs.csv
├── db
│   ├── database.py 					      # DB engine and session management
│   └── models.py 						      # SQLAlchemy models
├── logs 								            # Logs of invalid data or errors
├── poc.db 								          # SQLite Database
├── requirements.txt 					      # Python dependencies
├── scripts								
│	├── backup.py						          # Script to bulk load historical CSV data
│	├── load_csv.py						        # Script to generate AVRO backups
│	└── restore.py						        # Script to restore data from AVRO files
├── Dockerfile 							        # Deployment config
└── README.md                  			# Project documentation
```

## 🚀 Features

- Upload CSV (historical data) and JSON (new data) data using a web interface.
- Validate and log invalid rows to persistent files.
- Insert clean data into a relational database.
- REST API endpoint for ingesting JSON-formatted transactions.
- AVRO-based backup and restore for the full database or specific tables.
- Interactive reports (Plotly charts) to visualize:
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

## 🧪 API Endpoints

- `POST /upload-csv/`
- `POST /upload-json/`
- `POST /backup/`
- `POST /restore/`
- `POST /api/{table_name}` (API ingestion)

## 📊 Reports

- **Report 1**: Quarterly hiring visualized per department and job (stacked bar).
- **Report 2**: Horizontal bar chart of departments hiring above average.

## 📦 Backup Format

AVRO files are generated per table or for the full DB. These can be restored later, preserving schema compatibility.

## 📝 Logging

- Logs for invalid rows during CSV/JSON upload are saved in `logs/`.
- SQL errors and operational issues are also persisted with timestamps.

## 👤 Author

**Sergio Gordon**  
[GitHub](https://github.com/sergordon)

## 🛡️ License

This project is licensed under the MIT License.

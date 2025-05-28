from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Any
import shutil
import os
import json
from datetime import datetime
from scripts.load_csv import load_data_to_db, TB_SCHEMAS
from scripts.backup import backup_table, backup_all_tables
from scripts.restore import restore_table, restore_all_tables
from app.api import insertFromBatch
from app import api
from app.utils.logger_manager import LoggerManager

#Config logger
logger_api = LoggerManager("logs", "api_invalid_rows.log")

app = FastAPI()
app.include_router(api.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-csv/")
async def upload_csv(
    file: UploadFile = File(...),
    table_name: str = Form(...)
):
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", file.filename)
    
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Call loader
        column_list = TB_SCHEMAS.get(table_name)
        results = load_data_to_db(path, table_name, column_list)
        return {"result upload csv activity": results }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading CSV: {str(e)}")

@app.post("/upload-json/")
async def upload_json(table_name: str = Form(...), data: str = Form(...)):
    try:
        # Parse stringified JSON list
        items: list[dict[str, Any]] = json.loads(data)
        valid_items = []
        results_insert = {}
        for item in items:
            if any(v in (None, "", []) for v in item.values()):
                logger_api.log_error(f"{datetime.now().isoformat()} - Null or empty value in table {table_name} -  row {item}")
            else:
                valid_items.append(item)

        if valid_items:
            insert_result = insertFromBatch(table_name, valid_items)
            msg = insert_result["result_msg"]
            results_insert["result_msg"] = msg
            if "ERROR" in msg.upper():
                return insert_result
             
        if (len(items) - len(valid_items)) > 0:
            warn_msg = f"[WARN]: {len(items) - len(valid_items)} invalid rows were logged in api_invalid_rows.log"
            results_insert["result_msg"] += f"<br>{warn_msg}"
        return results_insert

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="[Error]: Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[Error]: Failed to process JSON: {str(e)}")

@app.post("/backup/")
async def backup(table_name: str = Form("")):
    try:
        if table_name:
            result = backup_table(table_name)            
        else:
            result = backup_all_tables()
        return {"Backup activity": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)}")

@app.post("/restore/")
async def restore(table_name: str = Form("")):
    try:
        if table_name:
            msg = restore_table(table_name)
            return {"message": msg}
        else:
            result = restore_all_tables()
            return {"message": "Restore completed", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restore failed: {str(e)}")
        
    

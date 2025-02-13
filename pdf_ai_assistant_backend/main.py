# main.py

from typing import List
from fastapi import FastAPI, UploadFile, File
from extraction import upload_files
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/files_request")
async def upload(files: List[UploadFile] = File(...)):
    try:
        files_data = await upload_files(files)
        return JSONResponse(content=files_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/request_employee")
async def request_employee(prompt):
    try:
        result = await 

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil
import uvicorn
import uuid
import datetime

app = FastAPI()

os.makedirs("./static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return JSONResponse(content={
        "message": "Hello, World!"
    })

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # path yyyy/mm/dd/uuid.ext
        save_path = datetime.datetime.now().strftime("%Y/%m/%d")
        file_path = os.path.join("static", save_path, f"{uuid.uuid4()}.{file.filename.split('.')[-1]}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(status_code=200, content={
            "filename": file.filename,
            "file_path": file_path
        })
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8080, reload=True)
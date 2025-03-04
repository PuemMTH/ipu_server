from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
import shutil
import uvicorn
import uuid
import datetime
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse

app = FastAPI()

load_dotenv()

os.makedirs("./static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/") # https://facebook.com/
async def read_root():
    return JSONResponse(content={
        "message": "Hello, World!"
    })

@app.post("/upload-file/") # https://facebook.com/upload-file/
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

@app.get("/images/") 
async def preview_image_file(file_path: str):
    try:
        # Ensure the file path is within the static directory
        full_path = os.path.join("static", file_path) if not file_path.startswith("static/") else file_path
        
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            return JSONResponse(status_code=404, content={"message": "File not found."})
        
        # Determine media type based on file extension
        file_extension = os.path.splitext(full_path)[1].lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".webp": "image/webp"
        }
        
        if file_extension not in media_types:
            return JSONResponse(status_code=400, content={"message": "Not a supported image format."})
        
        # Directly return the file
        return FileResponse(
            path=full_path, 
            media_type=media_types.get(file_extension),
            filename=os.path.basename(full_path)
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={"message": str(e)})
    
    
if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=int(os.getenv("INTERNAL_PORT", "80")), reload=True)
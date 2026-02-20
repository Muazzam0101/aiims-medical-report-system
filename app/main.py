import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.config import UPLOAD_DIR, MAX_FILE_SIZE
from app.orchestrator import Orchestrator

# Initialize FastAPI app
app = FastAPI(
    title="AIIMS Medical Report Analysis API",
    description="Backend API for clinical entity extraction, risk classification, and biomedical tagging.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Orchestrator instance
# Initialized at startup
orchestrator = None

@app.on_event("startup")
async def startup_event():
    global orchestrator
    logger.info("Application starting up...")
    try:
        orchestrator = Orchestrator()
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        logger.critical(f"Failed to initialize models on startup:\n{error_msg}")
        # We don't exit here to allow for manual intervention, but endpoints will fail

@app.get("/")
async def root():
    return {"message": "AIIMS Medical Analysis API is running."}

@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...)):
    # 1. Validate file type
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in [".pdf", ".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Unsupported file format. Use PDF or Image.")

    # 2. Save file temporarily
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Failed to save file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error saving file.")

    # 3. Check file size
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit.")

    # 4. Process with Orchestrator
    try:
        if orchestrator is None:
             raise HTTPException(status_code=503, detail="Models are not loaded. Please contact administrator.")
        
        result = await orchestrator.analyze_report(str(file_path))
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # 5. Cleanup (optional: keep files for history? The request says extraction only)
        # For this requirement, we clean up.
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    from app.config import HOST, PORT
    logger.info(f"Starting server on {HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT)

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
from typing import Optional

from models import Job, JobStatus
from ai_processor import process_video

load_dotenv()

app = FastAPI(title="SafeEye API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "safeye")

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Ensure upload directories exist
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "SafeEye API", "version": "1.0.0"}


@app.post("/upload_video")
async def upload_video(
    request: Request,
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    photo: Optional[UploadFile] = File(None)
):
    """Upload video and optional photo, returns job_id"""
    if not video.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Invalid video format")
    
    job_id = str(uuid.uuid4())
    
    # Save video file
    video_path = os.path.join(UPLOAD_DIR, f"{job_id}_{video.filename}")
    with open(video_path, "wb") as f:
        content = await video.read()
        f.write(content)
    
    # Save photo if provided
    photo_path = None
    if photo:
        if not photo.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Invalid photo format")
        photo_path = os.path.join(UPLOAD_DIR, f"{job_id}_{photo.filename}")
        with open(photo_path, "wb") as f:
            content = await photo.read()
            f.write(content)
    
    # Create job record
    job = {
        "_id": job_id,
        "status": JobStatus.PENDING,
        "video_filename": video.filename,
        "video_path": video_path,
        "photo_path": photo_path,
        "created_at": datetime.utcnow().isoformat(),
        "results": None
    }
    
    await db.jobs.insert_one(job)
    
    # Start background processing
    background_tasks.add_task(process_video_job, job_id, video_path, photo_path)
    
    return {"job_id": job_id, "status": "pending"}


async def process_video_job(job_id: str, video_path: str, photo_path: Optional[str]):
    """Background task to process video"""
    try:
        # Update status to processing
        await db.jobs.update_one(
            {"_id": job_id},
            {"$set": {"status": JobStatus.PROCESSING}}
        )
        
        # Process video
        results = await process_video(video_path, photo_path, job_id)
        
        # Update job with results
        await db.jobs.update_one(
            {"_id": job_id},
            {"$set": {
                "status": JobStatus.COMPLETED,
                "results": results,
                "completed_at": datetime.utcnow().isoformat()
            }}
        )
    except Exception as e:
        await db.jobs.update_one(
            {"_id": job_id},
            {"$set": {
                "status": JobStatus.FAILED,
                "error": str(e)
            }}
        )


@app.post("/process/{job_id}")
async def trigger_process(job_id: str, background_tasks: BackgroundTasks):
    """Manually trigger processing for a job"""
    job = await db.jobs.find_one({"_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["status"] == JobStatus.PROCESSING:
        return {"message": "Job already processing"}
    
    background_tasks.add_task(
        process_video_job,
        job_id,
        job["video_path"],
        job.get("photo_path")
    )
    
    return {"message": "Processing started"}


@app.get("/results/{job_id}")
async def get_results(job_id: str):
    """Get detection results for a job"""
    job = await db.jobs.find_one({"_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Convert ObjectId to string for JSON serialization
    job["_id"] = str(job["_id"])
    
    return {
        "job_id": job_id,
        "status": job["status"],
        "results": job.get("results"),
        "created_at": job.get("created_at"),
        "completed_at": job.get("completed_at"),
        "error": job.get("error")
    }


@app.get("/history")
async def get_history(limit: int = 50, skip: int = 0):
    """Get history of all jobs"""
    cursor = db.jobs.find().sort("created_at", -1).skip(skip).limit(limit)
    jobs = await cursor.to_list(length=limit)
    
    # Convert ObjectIds to strings
    for job in jobs:
        job["_id"] = str(job["_id"])
    
    total = await db.jobs.count_documents({})
    
    return {
        "jobs": jobs,
        "total": total,
        "limit": limit,
        "skip": skip
    }


@app.get("/processed/{filename}")
async def get_processed_video(filename: str):
    """Serve processed video files"""
    file_path = os.path.join(PROCESSED_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4")
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        await client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


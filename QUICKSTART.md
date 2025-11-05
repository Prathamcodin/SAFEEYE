# SafeEye - Quick Start Guide (Windows)

## Step-by-Step Instructions

### Method 1: Using Docker Compose (Easiest - Recommended)

**Prerequisites:** Docker Desktop installed and running

1. **Open PowerShell or Command Prompt** in the project directory

2. **Start all services:**
   ```powershell
   docker-compose up -d
   ```
   This will start MongoDB, Backend, and Frontend automatically.

3. **Wait for services to start** (about 1-2 minutes)

4. **Open your browser** and go to: `http://localhost:3000`

5. **To stop all services:**
   ```powershell
   docker-compose down
   ```

---

### Method 2: Manual Setup (More Control)

#### Step 1: Install Prerequisites

1. **Python 3.11+** - Download from [python.org](https://www.python.org/downloads/)
2. **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
3. **MongoDB** - Choose one:
   - **Option A:** Install MongoDB locally from [mongodb.com](https://www.mongodb.com/try/download/community)
   - **Option B:** Use Docker: `docker run -d -p 27017:27017 --name mongodb mongo:latest`
   - **Option C:** Use free MongoDB Atlas cloud (no installation needed)

#### Step 2: Start MongoDB

**If using local MongoDB:**
- Open MongoDB Compass or start MongoDB service
- Or run: `mongod` in a terminal

**If using Docker:**
```powershell
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**If using MongoDB Atlas:**
- Create account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Get your connection string (looks like: `mongodb+srv://user:pass@cluster.mongodb.net/`)

#### Step 3: Start Backend

1. **Open PowerShell** in the `backend` folder

2. **Run the startup script:**
   ```powershell
   .\start.bat
   ```
   
   Or manually:
   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create .env file (if not exists)
   if not exist .env (
       echo MONGODB_URL=mongodb://localhost:27017 > .env
       echo DATABASE_NAME=safeye >> .env
   )
   
   # Start server
   uvicorn main:app --reload --port 8000
   ```

3. **Wait for:** `Application startup complete` message
4. **Backend is running at:** `http://localhost:8000`
5. **API docs available at:** `http://localhost:8000/docs`

#### Step 4: Start Frontend

1. **Open a NEW PowerShell** window in the `frontend` folder

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Create environment file:**
   ```powershell
   echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
   ```

4. **Start development server:**
   ```powershell
   npm run dev
   ```

5. **Wait for:** `Ready on http://localhost:3000`
6. **Frontend is running at:** `http://localhost:3000`

---

## How to Use SafeEye

### 1. Upload a Video

1. Open `http://localhost:3000` in your browser
2. Click **"Upload Video"** button
3. Click on the video upload area and select a CCTV video file (.mp4, .avi, .mov, .mkv)
4. (Optional) Click on the photo upload area and select a suspect photo (.jpg, .png)
5. Click **"Analyze Video"** button
6. Wait for upload to complete (progress bar will show)

### 2. View Results

1. After upload, you'll be redirected to the results page
2. **If processing:** You'll see a "Processing Video" message. The page will auto-refresh every 3 seconds.
3. **When complete:** You'll see:
   - **Stats cards:** Total detections, theft suspects, duration, suspect matched
   - **Video player:** Processed video with bounding boxes drawn on detected persons
   - **Detection list:** All detections with timestamps, person IDs, confidence scores
   - **Export button:** Download JSON report

### 3. View Dashboard

1. Click **"Dashboard"** in the navigation or go to `http://localhost:3000/dashboard`
2. View all your analyzed videos:
   - Total videos analyzed
   - Completed/Processing/Failed counts
   - Total detections across all videos
   - List of all jobs with status and timestamps
3. Click on any job to view its results

### 4. Export Reports

1. On any results page, click **"Export JSON"** button
2. A JSON file will download with:
   - All detection data
   - Timestamps
   - Bounding boxes
   - Confidence scores
   - Summary statistics

---

## Troubleshooting

### Backend won't start

**Problem:** `ModuleNotFoundError` or import errors
**Solution:** 
```powershell
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Problem:** MongoDB connection error
**Solution:** 
- Check if MongoDB is running: `docker ps` (if using Docker)
- Verify MongoDB URL in `backend/.env` file
- For Atlas, make sure your IP is whitelisted

### Frontend won't start

**Problem:** `npm install` fails
**Solution:**
```powershell
cd frontend
npm cache clean --force
npm install
```

**Problem:** Can't connect to backend
**Solution:**
- Check `frontend/.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Make sure backend is running on port 8000
- Check browser console for CORS errors

### Video processing fails

**Problem:** YOLOv8 model download fails
**Solution:** 
- Check internet connection (model downloads automatically on first run)
- Model file: `~/.ultralytics/yolov8n.pt` (~6MB)

**Problem:** Processing is very slow
**Solution:**
- This is normal for CPU-only processing
- Videos process frame-by-frame
- Consider shorter test videos (< 1 minute) for testing

### Video won't play

**Problem:** Video player shows "No video"
**Solution:**
- Check if processed video exists in `backend/processed/` folder
- Check browser console for errors
- Verify backend is serving files at `/processed/{filename}` endpoint

---

## Testing with Sample Video

1. **Get a test video:**
   - Use any CCTV footage you have
   - Or download a sample video from the internet
   - Make sure it's in .mp4 format

2. **Upload and test:**
   - Go to upload page
   - Select your video
   - Click "Analyze Video"
   - Wait for processing (may take several minutes depending on video length)

3. **Check results:**
   - View detected persons
   - Check timestamps
   - Verify bounding boxes on video

---

## API Testing (Optional)

You can test the API directly using curl or Postman:

```powershell
# Health check
curl http://localhost:8000/health

# Upload video (replace paths)
curl -X POST http://localhost:8000/upload_video `
  -F "video=@C:\path\to\your\video.mp4" `
  -F "photo=@C:\path\to\suspect.jpg"

# Get results (replace job_id)
curl http://localhost:8000/results/{job_id}

# Get history
curl http://localhost:8000/history
```

Or use the interactive API docs at: `http://localhost:8000/docs`

---

## Next Steps

- **Add more AI models:** See `DEVELOPMENT.md` for integrating DeepSORT and torchreid
- **Deploy to cloud:** Use docker-compose.yml with cloud MongoDB
- **Customize detection:** Modify `backend/ai_processor.py` for better theft detection
- **Add authentication:** Implement user login/signup
- **Cloud storage:** Use AWS S3 for video storage

---

## Need Help?

- Check `README.md` for detailed documentation
- Check `QUICKSTART.md` for detailed usage guide
- Check `DEVELOPMENT.md` for development notes
- Check API docs at `hdocsttp://localhost:8000/` when backend is running
- Check browser console (F12) for frontend errors
- Check backend terminal for processing logs


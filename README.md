# SafeEye - AI Theft Detection Platform

<div align="center">

![SafeEye Logo](https://img.shields.io/badge/SafeEye-AI%20Theft%20Detection-blue?style=for-the-badge&logo=shield-check)

**Advanced AI-powered theft detection platform for shopkeepers**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🎯 Features

- **🎥 Smart Video Analysis** - Upload CCTV footage and get AI-powered person detection
- **🔄 Person Tracking** - DeepSORT integration for advanced multi-person tracking
- **🔍 Person Re-identification** - Match suspects across video frames using photo uploads
- **🚨 Theft Detection** - AI-powered suspicious activity detection with timestamps
- **📊 Dashboard** - Comprehensive analytics and job history
- **📥 Export Reports** - Download detailed JSON reports with all detections
- **🎨 Modern UI** - Beautiful, responsive web interface built with Next.js and TailwindCSS

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/safeye.git
cd safeye

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

#### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (local or cloud)

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URL

# Run backend
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run frontend
npm run dev
```

#### MongoDB Setup

```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or use MongoDB Atlas (cloud)
# Create account at https://www.mongodb.com/cloud/atlas
```

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Detailed setup instructions
- **[Development Guide](DEVELOPMENT.md)** - Development and contribution guidelines
- **[Project Overview](PROJECT_OVERVIEW.md)** - Architecture and technical details
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when backend is running)

## 🏗️ Architecture

```
SafeEye/
├── backend/          # FastAPI Python backend
│   ├── main.py       # API endpoints
│   ├── ai_processor.py  # YOLOv8, tracking, ReID
│   └── models.py     # Data models
├── frontend/         # Next.js TypeScript frontend
│   ├── pages/        # Next.js pages
│   ├── components/   # React components
│   └── styles/      # TailwindCSS styles
└── docker-compose.yml  # Full stack deployment
```

## 🛠️ Tech Stack

- **Frontend**: Next.js 14, TypeScript, TailwindCSS, Lucide Icons
- **Backend**: FastAPI, Python 3.11+, Motor (async MongoDB)
- **AI/ML**: YOLOv8, DeepSORT, Person ReID
- **Database**: MongoDB
- **Deployment**: Docker, Docker Compose

## 📡 API Endpoints

- `POST /upload_video` - Upload video and optional photo
- `POST /process/{job_id}` - Manually trigger processing
- `GET /results/{job_id}` - Get detection results
- `GET /history` - Get job history
- `GET /health` - Health check
- `GET /processed/{filename}` - Serve processed videos

## 🎨 Screenshots

<details>
<summary>Click to view screenshots</summary>

- Home page with hero section
- Upload page with drag-and-drop
- Dashboard with analytics
- Results page with video player and detections

</details>

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [YOLOv8](https://github.com/ultralytics/ultralytics) for person detection
- [DeepSORT](https://github.com/nwojke/deep_sort) for object tracking
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing Python framework
- [Next.js](https://nextjs.org/) for the React framework

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/safeye/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/safeye/discussions)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/safeye&type=Date)](https://star-history.com/#yourusername/safeye&Date)

---

<div align="center">

**Made with ❤️ for shopkeepers and security professionals**

[⬆ Back to Top](#safeye---ai-theft-detection-platform)

</div>

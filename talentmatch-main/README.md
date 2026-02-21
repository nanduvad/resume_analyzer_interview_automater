TalentMatch - AI-Powered Recruitment Platform
<img width="1366" height="768" alt="2 (2)" src="https://github.com/user-attachments/assets/86cd5f36-d181-4c53-a490-60e86ed017f5" />
<img width="1366" height="768" alt="3 (2)" src="https://github.com/user-attachments/assets/f23064c6-39cd-4de6-a525-946d558b2e64" />
<img width="1366" height="768" alt="4 (2)" src="https://github.com/user-attachments/assets/a68c0105-b154-4d44-aa43-790b6fc96683" />
<img width="1366" height="768" alt="1 (2)" src="https://github.com/user-attachments/assets/122251bb-3d9b-49ba-839c-f70afa82dcc8" />


TalentMatch is a modern, AI-powered recruitment platform that intelligently matches candidates to job descriptions using semantic similarity and machine learning.

🚀 Features
Core Functionality
AI Job Analysis - Parse and extract key skills from job descriptions

Smart Candidate Matching - Semantic similarity matching using vector embeddings

Candidate Management - Upload and store candidate profiles

Interview Question Generation - AI-powered, context-aware interview questions

Real-time Ranking - Live candidate ranking with similarity scores

Technical Features
Full-Stack Application - React frontend with Flask backend

Vector Similarity Search - Advanced matching using embeddings

Responsive Design - Mobile-friendly Tailwind CSS interface

RESTful API - Clean API architecture for extensibility

🛠 Tech Stack
Frontend
React 18 - Modern React with hooks

React Router - Client-side routing

Tailwind CSS - Utility-first CSS framework

Framer Motion - Smooth animations

Vite - Fast build tool and dev server

Backend
Flask - Python web framework

Pinecone - Vector database for similarity search

OpenAI Embeddings - Text embedding generation

Python-dotenv - Environment configuration

📦 Installation
Prerequisites
Node.js 16+ and npm

Python 3.8+

Pinecone account (optional - fallback to in-memory store)

Backend Setup
Navigate to backend directory

bash
cd talentmatch/backend
Install Python dependencies

bash
pip install -r requirements.txt
Set up environment variables

bash
cp .env.example .env
Edit .env with your credentials:

env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_environment
OPENAI_API_KEY=your_openai_api_key
DEBUG=True
Start the Flask server

bash
python -m backend.app
Server runs on http://localhost:5000

Frontend Setup
Navigate to project root

bash
cd talentmatch
Install dependencies

bash
npm install
Start development server

bash
npm run dev
Application runs on http://localhost:5173

🎯 Usage
Basic Workflow
Access the Application

Open http://localhost:5173 in your browser

Click "Try it now" to access the dashboard

Analyze Job Description

Paste a job description in the text area

Click "Analyze" to extract skills and requirements

Upload Candidates

Drag & drop resume files or paste candidate names

System automatically processes and stores candidates

View Matches

See real-time candidate rankings with similarity scores

Scores range from 0-100% based on semantic match

Generate Questions

Click "Generate" to create interview questions

Questions are tailored to job requirements and candidate skills

API Endpoints
Jobs
POST /jobs/analyze - Analyze job description

GET /jobs/ - Get jobs endpoint info

Candidates
POST /candidates/upload - Upload multiple candidates

POST /candidates/add - Add single candidate

GET /candidates/debug - Debug stored candidates

Questions
POST /questions/generate - Generate interview questions

POST /questions/submit - Submit and evaluate answers

<img width="509" height="713" alt="Tree" src="https://github.com/user-attachments/assets/44af85b1-1c74-42b5-b16c-945c9a14ea7c" />


env
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=us-east-1
OPENAI_API_KEY=your_openai_key
DEBUG=True
Frontend (vite.config.js)

javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:5000'
    }
  }
})
🚀 Deployment
Development
bash
# Backend
cd backend && 
.

# Frontend  
cd talentmatch && npm run dev
Production Build
bash
# Build frontend
npm run build

# Serve with nginx or similar
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
For support and questions:

Check the Issues page

Create a new issue with detailed description

🏆 Acknowledgments
OpenAI for embedding models

Pinecone for vector database infrastructure

React and Flask communities

Tailwind CSS for styling system

<div align="center">
Built with ❤️ for better hiring experiences

Report Bug · Request Feature

</div>

## 📋 Project Overview


## 🏗️ TECH STACK
```
Project: talentmatch
Frontend: React
  Build: Vite
  Language: TypeScript
  CSS: Tailwind
  Orchestration: docker-compose
```

## 📁 PROJECT STRUCTURE
```
.
./.vscode
./backend
./backend/config
./backend/database
./backend/models
./backend/routes
./backend/src
./backend/tests
./backend/utils
./backups
./backups/pre-typescript-migration
./config
./config/environments
./config/production
```

## 🔑 KEY FILES
```
backend/app.py
dist/index.html
index.html
src/App.tsx
src/index.css
src/main.jsx
src/main.tsx
venv/Lib/site-packages/dotenv/main.py
venv/Lib/site-packages/flask/app.py
venv/Lib/site-packages/flask/sansio/app.py
```

## 📦 DEPENDENCIES
```
Frontend Dependencies:
@auth0/auth0-react framer-motion react react-dom react-router-dom 
```

## 🔍 DETECTED FEATURES
```
✅ Auth: backend/production_auth.py
✅ Auth: backend/routes/auth.py
✅ Auth: config/production/oauth_config.py
✅ API: backend/routes/api.py
✅ API: src/lib/api.ts
✅ API: src/types/api.ts
✅ docker-compose ready
```

## 📊 QUICK STATS
```
Files (source):
2243
```

## 🚀 GETTING STARTED
```
# Install dependencies
npm install

# Available scripts:
npm run build
npm run dev
npm run preview
npm run type-check
npm run type-check:watch

# Start with Docker
docker-compose up
```

## 📝 COMMON NEXT STEPS
```
1. Check .env.example or .env for configuration
2. Run npm install / pip install
3. Start development server
4. Check README.md for project-specific instructions
```

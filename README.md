# 🎙️ CAstPod — AI-Powered Learning Platform

> Transform static textbooks into engaging AI-powered learning podcasts.

CAstPod converts academic PDFs into two-person conversational podcasts (Student + Mentor), synchronized with diagrams, summaries, flashcards, and quizzes — making learning accessible and engaging.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Processing** | Extract text & images from any academic PDF |
| 🎙️ **Podcast Generation** | AI-generated Student/Mentor conversation script |
| 🔊 **Audio Synthesis** | ElevenLabs TTS with distinct voices per character |
| 📝 **Summary & Cheat Sheet** | Concise AI-generated study aids |
| 🃏 **Flashcards** | Interactive flip-card quiz cards |
| ❓ **MCQ Quiz** | 5-10 auto-generated questions with scoring |
| 💬 **Doubt Clearing** | Ask questions about the material, get AI answers |
| 🎯 **Difficulty Modes** | Kids (story-like), Student (balanced), Exam (concise) |
| 🔐 **User Auth** | JWT-based login/signup with session persistence |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite |
| Backend | FastAPI (Python) |
| Database | MongoDB (via Motor async driver) |
| Auth | JWT (python-jose + passlib/bcrypt) |
| AI | Google Gemini API |
| Audio | ElevenLabs TTS |
| PDF | PyMuPDF |

---

## 📁 Project Structure

```
CAstPod/
├── backend/             # FastAPI application
│   ├── main.py          # App entry point
│   ├── config.py        # Environment config
│   ├── routers/         # API route handlers
│   ├── services/        # Business logic
│   ├── models/          # Pydantic schemas
│   └── uploads/         # PDF & audio file storage
│
├── frontend/            # React application
│   └── src/
│       ├── pages/       # Login, Signup, Dashboard, Upload, PodcastPlayer
│       ├── components/  # AudioPlayer, TranscriptView, QuizSection, etc.
│       ├── contexts/    # AuthContext (JWT state management)
│       └── services/    # API wrapper (Axios + JWT interceptors)
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** and **pip**
- **Node.js 18+** and **npm**
- **MongoDB** (local install or [MongoDB Atlas](https://cloud.mongodb.com) free cluster)
- API Keys: [Google Gemini](https://aistudio.google.com) and [ElevenLabs](https://elevenlabs.io) (optional for dev)

### 1. Clone & Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env         # Windows
# cp .env.example .env          # macOS/Linux

# Edit .env with your keys:
# - MONGODB_URL (default: mongodb://localhost:27017)
# - GEMINI_API_KEY (required for AI features)
# - ELEVENLABS_API_KEY (optional — MOCK_AUDIO=true skips real audio)
# - JWT_SECRET (change for production!)
```

### 2. Start Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Verify at: **http://localhost:8000/docs** (Swagger UI)

### 3. Setup & Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

---

## 🔑 Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|---|---|---|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGODB_DB_NAME` | Database name | `castpod` |
| `JWT_SECRET` | Secret key for JWT signing | `dev-secret-...` |
| `GEMINI_API_KEY` | Google Gemini API key | — |
| `ELEVENLABS_API_KEY` | ElevenLabs API key | — |
| `MOCK_AUDIO` | Skip real TTS (for dev) | `true` |

### Frontend (`frontend/.env`)

| Variable | Description | Default |
|---|---|---|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

---

## 🎮 Usage Flow

1. **Sign Up** — Create an account
2. **Upload PDF** — Drag-and-drop your academic PDF
3. **Choose Mode** — Kids 🎈 / Student 📚 / Exam 🎯
4. **Wait** — AI processes content (1-3 minutes)
5. **Listen** — Play the podcast with transcript bubbles
6. **Study** — Explore Summary, Cheat Sheet, Flashcards, Diagrams
7. **Test** — Take the auto-generated MCQ quiz
8. **Ask** — Clear doubts with the AI chat feature
9. **Revisit** — All sessions saved on your dashboard

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Create account |
| `POST` | `/api/auth/login` | Login, get JWT |
| `GET` | `/api/auth/me` | Get current user |
| `POST` | `/api/upload-pdf` | Upload PDF + generate session |
| `GET` | `/api/sessions` | List user sessions |
| `GET` | `/api/sessions/{id}` | Get session details |
| `POST` | `/api/ask-question` | Ask doubt about a session |

---

## 📄 License

MIT — Built for learning.

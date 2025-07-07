# Agentic Interview Bot

## 🚀 Overview
A next-generation, agentic job interview simulator with adaptive questions, real-time voice conversation, and scalable architecture.

## 👨‍💻 Features
- Adaptive question selection via LangGraph
- Semantic answer scoring with Pinecone
- Real-time voice chat with Whisper + ElevenLabs
- WebSocket real-time data
- Docker Compose support

## 🛠 Tech Stack
- FastAPI + LangGraph
- Streamlit frontend
- Whisper STT
- ElevenLabs TTS
- Pinecone vector DB
- Docker Compose

## ⚙️ Running Locally

```bash
git clone <your-repo>
cd <your-repo>
cp .env
docker-compose up --build

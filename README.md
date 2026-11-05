# 🎙️ Nexus AI — Real-Time Conversational Voice AI Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Deepgram](https://img.shields.io/badge/Voice_Agent-Deepgram_Nova--2_%26_Aura-13EF95?style=for-the-badge&logo=deepgram&logoColor=black)](https://deepgram.com/)
[![Groq](https://img.shields.io/badge/LLM_Inference-Groq_LPU-F55036?style=for-the-badge&logo=fastapi&logoColor=white)](https://groq.com/)
[![WebSockets](https://img.shields.io/badge/Streaming-WebSockets_(flask--sock)-010101?style=for-the-badge&logo=socketdotio&logoColor=white)](https://github.com/pallets-eco/flask-sock)
[![Flask](https://img.shields.io/badge/Framework-Flask_3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

Nexus AI is an ultra-low-latency **Real-Time Conversational Voice AI Agent** capable of near-instant voice-to-voice dialogues. Powered by **Deepgram's Voice Agent API** (Nova-2 STT & Aura TTS), **Groq's LPU Inference Engine** (500+ tokens/sec LLM reasoning), and bidirectional **WebSockets** for fluid, full-duplex human-to-AI spoken conversations.

---

## ⚡ Architecture & Low-Latency Pipeline

The system bridges client-side browser microphones directly to cloud inference streams with zero audio file disk buffering:

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 User
    participant Browser as 🌐 Client (Web Audio API)
    participant Server as 🐍 Flask WebSocket (/ws/voice)
    participant Deepgram as ⚡ Deepgram Voice Agent (Nova-2 + Aura)
    participant Groq as 🚀 Groq LPU (Ultra-Fast LLM)

    User->>Browser: Speaks naturally
    Browser->>Server: Streams raw PCM audio chunks via WebSocket
    Server->>Deepgram: Relays audio stream in real time
    Deepgram->>Deepgram: High-accuracy Speech-to-Text (Nova-2 STT)
    Deepgram->>Groq: Sends transcribed prompt for reasoning
    Groq-->>Deepgram: Streams token completion at 500+ tok/sec
    Deepgram->>Deepgram: Synthesizes conversational voice (Aura TTS)
    Deepgram-->>Server: Streams binary audio frames
    Server-->>Browser: Pushes audio frames over WebSocket
    Browser-->>User: Plays audio seamlessly through speakers
```

---

## 🚀 Key Highlights & Capabilities

- **Sub-Second Voice-to-Voice Latency**: Combines Deepgram's streaming STT/TTS with Groq's high-throughput LPU inference to achieve realistic, conversational dialogue speed without awkward pauses.
- **Full-Duplex WebSocket Audio Bridge**: Custom `/ws/voice` gateway built on `flask-sock` handling bidirectional binary audio frames, user transcripts, and agent events.
- **Hybrid Intelligence Architecture**:
  1. **Instant Command Matcher (`/api/command`)**: Token-aware weighted scoring engine matching intents locally against `data/knowledge.json` for zero-latency system navigation (YouTube, Google, navigation).
  2. **Groq LLM Fallback**: Open-ended questions seamlessly route to Groq's high-speed inference engine for deep reasoning.
- **Dynamic Hot-Reloading (`/api/reload`)**: Update and reload the knowledge base JSON at runtime without restarting the Flask daemon.
- **Modern Responsive Web GUI**: Browser interface featuring real-time audio visualization, live user speech transcription, agent response text, and manual text input controls.

---

## 🛠️ Tech Stack & Dependencies

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Speech-to-Text (STT)** | **Deepgram Nova-2** | Real-time streaming speech transcription with domain formatting. |
| **LLM Inference** | **Groq LPU Engine** | Ultra-low latency conversational intelligence. |
| **Text-to-Speech (TTS)** | **Deepgram Aura** | Human-like, natural voice synthesis with zero robotic tone. |
| **Streaming Gateway** | **WebSockets (`flask-sock`)** | Bidirectional binary audio streaming between browser and cloud. |
| **Web Server** | **Flask 3.0** | HTTP REST endpoints and static UI serving. |

---

## 🚀 Quickstart & Setup Guide

### 1. Clone & Setup
```bash
git clone https://github.com/uniqabhishek/Python-Project.git
cd "Python-Project/python/project 2"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the project folder:
```env
DEEPGRAM_API_KEY="your_deepgram_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
```

### 3. Run
```bash
python app.py
```
Open `http://localhost:5000` to interact with your Voice AI Agent!

---

## 👨‍💻 Author

**Abhishek**  
- **GitHub**: [@uniqabhishek](https://github.com/uniqabhishek)  
- **Flagship Project**: [TradeMind AI Workspace](https://uniqabhishek.github.io/Trading-Journal/)

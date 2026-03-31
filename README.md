# WhatsApp AI Chatbot API (FastAPI)

Backend API for WhatsApp automation using Meta Cloud API, built with FastAPI.

## Features
- Send WhatsApp messages via API
- Trigger conversational flows
- Webhook integration for real-time events
- Ready for AI-based automated responses

## Tech Stack
- Python
- FastAPI
- REST APIs
- Webhooks

## Endpoints
- GET /health
- POST /api/send-text
- POST /api/send-flow
- GET/POST /webhook

## Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload

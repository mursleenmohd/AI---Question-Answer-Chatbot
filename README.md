# AI Chatbot

A full-stack conversational AI chatbot built with **Python, FastAPI, LangChain, Groq, Streamlit, and PostgreSQL**.

The project demonstrates how to build an AI-powered application with a separate frontend and backend, structured LLM responses, conversation history, persistent database storage, streaming responses, tool calling, validation, error handling, and logging.

---

## Screenshots

### Chatbot Interface

<img width="1596" height="928" alt="image" src="https://github.com/user-attachments/assets/c4c08052-0f33-4c32-bdc5-6e6751781364" />

### Streaming Response

<img width="1075" height="760" alt="image" src="https://github.com/user-attachments/assets/8f4c5524-8c2c-44b6-9dd5-300d58d4b652" />

### FastAPI Swagger Documentation

<img width="1896" height="978" alt="image" src="https://github.com/user-attachments/assets/79e8e0df-c02d-4077-a683-f5ee2cbedb0b" />

---

## Features

- Conversational AI chatbot
- Streaming AI responses
- Conversation history
- Persistent conversations with PostgreSQL
- LangChain integration
- Groq LLM integration
- Tool calling
- Structured LLM output
- Pydantic validation
- Error handling
- Application logging
- FastAPI REST API
- Streamlit frontend
- Automated testing
- Environment variable configuration

---

## Architecture

```text
                    ┌─────────────────┐
                    │    Streamlit    │
                    │    Frontend     │
                    └────────┬────────┘
                             │
                             │ HTTP / JSON
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │     Backend     │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
             ┌─────────────┐   ┌─────────────┐
             │  LangChain  │   │ PostgreSQL  │
             └──────┬──────┘   └─────────────┘
                    │
                    ▼
              ┌───────────┐
              │   Groq    │
              │    LLM    │
              └───────────┘
```

### Tech Stack & Purpose

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language |
| **FastAPI** | Backend REST API |
| **Streamlit** | Frontend UI |
| **LangChain** | LLM application framework |
| **Groq** | High-performance LLM API |
| **PostgreSQL** | Persistent conversation storage |
| **SQLAlchemy**| Database ORM (Object Relational Mapper) |
| **Pydantic** | Data validation and structured output |
| **Pytest** | Testing framework |
| **Requests** | Frontend ↔ Backend communication |

---

📁 Project Structure

```text
ai-chatbot/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── database_service.py
│   ├── tools.py
│   │
│   ├── routes/
│   │   └── chat.py
│   │
│   ├── services/
│   │   └── llm_service.py
│   │
│   └── schemas/
│       └── chat.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   ├── test_api.py
│   └── test_tools.py
│
├── .env
├── .gitignore
├── requirements.txt

```

## How It Works

When a user sends a message, the request flows through the system as follows:

```text
User ➔ Streamlit ➔ FastAPI ➔ Load conversation history ➔ LangChain ➔ Groq LLM ➔ Generate response ➔ Save message in PostgreSQL ➔ Return response ➔ Streamlit
```

### Conversation History
The application maintains conversation history smoothly. For example:
- **User:** *What is Python?*
- **AI:** *Python is a programming language...*
- **User:** *Who created it?*
- **AI:** *Python was created by Guido van Rossum...*

The second question seamlessly uses the context from the previous turn.

### Streaming
Instead of generating the entire response and making the user wait (`Generate entire response ➔ Return complete response`), the application streams responses progressively:
```text
Generate token/chunk ➔ Send chunk ➔ Display chunk ➔ Generate next chunk ➔ Display next chunk
```
This reduces perceived latency and makes the interface feel highly responsive.

### Tool Calling
The project includes an example **calculator tool**. The LLM can intelligently determine when a calculation requires this tool.
- Supported operations: *Addition, Subtraction, Multiplication, Division*
- The tool logic is decoupled completely from the main LLM orchestration.

### Structured Output
The application leverages Pydantic models to format AI responses into deterministic JSON shapes:
```json
{
    "answer": "Python is a programming language...",
    "topic": "Python",
    "difficulty": "beginner"
}
```

### Validation
Incoming API requests are strictly validated using Pydantic. Empty messages (`""`) are systematically rejected, while well-formed payloads (`"What is FastAPI?"`) pass seamlessly, keeping bad data away from your LLM compute.

### Error Handling
The backend gracefully catches exceptions (Invalid requests, LLM API failures, Database issues, Connection drops) using FastAPI exception handlers. It responds with clean HTTP error responses rather than leaking internal code traces to the client.

### Logging
The backend includes verbose application logging for easy health checks and debugging:
- `INFO | Chat request received`
- `INFO | LLM response generated successfully`

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/mursleenmohd/AI---Question-Answer-Chatbot.git
cd ai-chatbot
```

### 2. Create a Virtual Environment

#### Windows:
```bash
python -m venv myenv
.venv\Scripts\activate
```

#### macOS / Linux:
```bash
python3 -m venv myenv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root. A sample blueprint is provided in `.env.example`.

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=openai/gpt-oss-120b

# Database Configuration
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/ai_chatbot

# App Configurations
API_HOST=127.0.0.1
API_PORT=8000
```
> **Security Warning:** Do not commit the `.env` file to GitHub. Ensure it is explicitly ignored in your `.gitignore`. Never expose `GROQ_API_KEY` or `DATABASE_PASSWORD` in public view or screenshots.

---

## PostgreSQL Setup

1. Create a PostgreSQL database named `ai_chatbot`:
   ```sql
   CREATE DATABASE ai_chatbot;
   ```
2. The data relationships are designed dynamically:
   ```text
   Conversation
        │
        ├── Message (1)
        ├── Message (2)
        └── Message (3)
   ```
   Each unique conversation session stores multiple messaging sequences.

---

## Running the Application

### Running the Backend
From the project root directory, launch the API server:
```bash
uvicorn backend.main:app --reload
```
- The backend API will live at: `http://127.0.0.1:8000`
- Interactive OpenAPI Swagger documentation can be accessed at: `http://127.0.0.1:8000/docs`

### Running the Frontend
Open another terminal, ensure your virtual environment is active, and run:
```bash
streamlit run frontend/app.py
```
- The Streamlit client will spin up automatically in your default web browser.

---

## API Endpoints

### 1. Create Conversation
- **Endpoint:** `POST /conversations`
- **Description:** Creates a new session ID for chat persistence.
- **Response:**
  ```json
  { "conversation_id": 1 }
  ```

### 2. Chat
- **Endpoint:** `POST /chat`
- **Description:** Generates a structured JSON response.
- **Payload:**
  ```json
  { "message": "What is Python?", "conversation_id": 1 }
  ```
- **Response:**
  ```json
  {
      "conversation_id": 1,
      "answer": "Python is a programming language...",
      "topic": "Python",
      "difficulty": "beginner"
  }
  ```

### 3. Streaming Chat
- **Endpoint:** `POST /chat/stream`
- **Description:** Streams response chunks dynamically over the network.

---

## Testing

The codebase includes an automated unit-test suite targeting validation, calculation tools, and endpoint contracts. Execute tests cleanly using:
```bash
pytest
```

---

## Learning Goals

This repository serves as a portfolio blueprint to understand production-grade LLM applications:
- Production REST API structures with **FastAPI**
- Prompt orchestration, tools, and state manipulation with **LangChain**
- Multi-turn relational memory storage using **PostgreSQL & SQLAlchemy**
- Low-latency interactive user experience using streaming tokens

---

## Future Improvements

- [ ] User authentication and session isolation
- [ ] Multi-conversation history panel management
- [ ] Text-search index across old chat histories
- [ ] UI/UX overhaul with custom CSS and markdown themes
- [ ] Database schema migrations tracking with **Alembic**

---

## Author

**Mursleen**
Built as a portfolio project to learn and demonstrate modern AI application development.

---

## Project Highlights

```text
FastAPI + LangChain + Groq + Streamlit + PostgreSQL + Tool Calling + Streaming + Structured Output
```
A complete full-stack conversational AI application.



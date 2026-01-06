# AI Intake Assistant

An intelligent healthcare intake assistant that conducts natural conversations with patients while progressively filling out their demographic information form. The assistant behaves like a human intake specialist rather than a scripted chatbot, allowing users to speak freely, answer questions out of order, and correct themselves naturally.

## Features

- **Natural Conversation**: AI assistant conducts friendly, human-like conversations
- **Progressive Form Filling**: Form updates automatically as information is gathered
- **Flexible Input**: Users can provide information in any order
- **Graceful Corrections**: Handles corrections and clarifications naturally
- **Real-time Updates**: Form fields highlight when updated
- **Multi-Provider LLM Support**: Works with OpenAI, Anthropic Claude, and extensible to other providers
- **Split-Screen UI**: Chat interface (60%) and form display (40%) side by side

## Project Structure

```
AI-Intake-Assist/
├── backend/                 # Python FastAPI backend
│   ├── api/                # API endpoints
│   ├── services/           # Business logic services
│   ├── providers/          # LLM provider implementations
│   ├── models/             # Pydantic data models
│   ├── prompts/            # System prompts for AI
│   ├── storage/            # In-memory session storage
│   ├── app.py             # FastAPI application entry
│   ├── config.py          # Configuration management
│   └── requirements.txt   # Python dependencies
│
├── frontend/               # Vanilla HTML/CSS/JS frontend
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript modules
│   │   └── modules/       # Modular components
│   └── index.html         # Main HTML file
│
├── .env.example           # Environment variables template
└── .gitignore            # Git ignore rules
```

## Prerequisites

- Python 3.8+
- Node.js (for serving frontend) or Python's built-in HTTP server
- API key from OpenAI or Anthropic

## Setup Instructions

### 1. Clone the Repository

```bash
cd "C:\Users\Shreya B\Documents\GitHub\AI-Intake-Assist"
```

### 2. Backend Setup

#### Create Python Virtual Environment

```bash
cd backend
python -m venv venv
```

#### Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cd ..
   copy .env.example .env
   ```

2. Edit `.env` file with your settings:

   **For OpenAI:**
   ```env
   LLM_PROVIDER=openai
   MODEL_NAME=gpt-4-turbo-preview
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   ```

   **For Anthropic Claude:**
   ```env
   LLM_PROVIDER=anthropic
   MODEL_NAME=claude-3-sonnet-20240229
   ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here
   ```

### 3. Frontend Setup

No build step required for vanilla JavaScript!

### 4. Running the Application

#### Start Backend Server

**Terminal 1:**
```bash
cd backend
venv\Scripts\activate  # Activate virtual environment if not already active
python app.py
```

The backend API will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

#### Start Frontend Server

**Terminal 2:**
```bash
cd frontend
python -m http.server 3000
```

**Alternative (if you have Node.js):**
```bash
npx serve -p 3000
```

The frontend will be available at: `http://localhost:3000`

## Usage

1. Open your browser to `http://localhost:3000`
2. The AI assistant will greet you and start the conversation
3. Respond naturally - you can provide information in any order
4. Watch the form fill automatically on the right side
5. Correct any mistakes by simply telling the assistant
6. Continue until all fields are complete

### Example Conversation

```
Assistant: Hi! I'm here to help you get checked in today. To get started, could you tell me your name?

You: Sure, I'm John Doe
Assistant: Great! And what's your date of birth?

You: March 15, 1985. Also my phone is 555-0123

# Zen AI Meditation App

An AI-powered meditation application that provides personalized meditation experiences based on user input and mood analysis.

## Features

- Interactive quiz to understand user's current state
- AI-generated meditation guidance
- Voice synthesis using ElevenLabs API
- Background music generation
- Mobile-first Streamlit interface

## Project Structure

```
zen_ai/
├── backend/
│   ├── app.py              # FastAPI main application
│   ├── agents/             # AI agent implementations
│   ├── settings.py         # Configuration settings
│   └── utils/             # Utility functions
├── frontend/
│   └── app.py             # Streamlit frontend
├── voice_output/          # Generated voice files
└── music_output/          # Generated music files
```

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd zen-ai-meditation
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

5. Start the backend server:
   ```bash
   uvicorn zen_ai.backend.app:app --reload
   ```

6. Start the frontend:
   ```bash
   streamlit run zen_ai/frontend/app.py
   ```

## API Keys Required

- ElevenLabs API key for voice synthesis
- (Future) Suno API key for music generation

## Development

- Backend: FastAPI
- Frontend: Streamlit
- Voice: ElevenLabs API
- Music: (Planned) Suno API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

# This is a test comment for verification. 
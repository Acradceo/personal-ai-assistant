# Personal AI Assistant 🤖

Your free, powerful AI personal assistant that runs on your phone with zero cost.

## Features
- 💬 AI Chat Interface (powered by Mistral 7B via Ollama)
- 🔧 GitHub Integration (automate tasks)
- 📝 Note Taking & Task Management
- 💻 Code Analysis & Suggestions
- 🔒 100% Private (runs locally)
- 📱 Mobile-First Design (Android optimized)

## Tech Stack
- **Backend**: Python Flask + LangChain
- **LLM**: Ollama (Mistral 7B) - Free & Open Source
- **Frontend**: React Native / Web Interface
- **Hosting**: GitHub Codespaces (180 free hours/month)
- **Cost**: $0 (Completely Free)

## Quick Start

### Prerequisites
- Android phone or browser
- GitHub account (for Codespaces)
- 5 minutes of setup time

### Setup Instructions

#### Step 1: Set Up Backend on GitHub Codespaces

1. Fork this repository
2. Go to GitHub Codespaces
3. Create a new Codespace from this repo
4. In the terminal, run:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend will start on `http://localhost:5000`

#### Step 2: Access on Your Android Phone

1. Find your Codespace URL (shown in terminal)
2. Open the frontend URL in your Android browser
3. Start chatting!

## Project Structure
```
personal-ai-assistant/
├── backend/
│   ├── app.py              # Flask server
│   ├── requirements.txt     # Python dependencies
│   ├── config.py          # Configuration
│   ├── models/
│   │   ├── chat.py        # Chat logic
│   │   ├── github.py      # GitHub integration
│   │   └── tasks.py       # Task management
│   └── utils/
│       ├── ollama.py      # Ollama LLM integration
│       └── logger.py      # Logging
├── frontend/
│   ├── index.html         # Main UI
│   ├── styles.css         # Mobile-optimized styles
│   ├── app.js             # JavaScript logic
│   └── assets/
│       └── icon.png       # App icon
├── docs/
│   ├── SETUP.md          # Detailed setup guide
│   ├── API.md            # API documentation
│   └── TROUBLESHOOTING.md # Common issues
└── .github/
    └── workflows/
        └── deploy.yml     # Auto-deploy workflow
```

## Skills Your AI Has

### 1. Chat & Conversation
- Natural language understanding
- Context-aware responses
- Multi-turn conversations

### 2. GitHub Integration
- Create issues/PRs
- Analyze code
- Generate documentation
- Fetch repos and data

### 3. Task Management
- Create & manage tasks
- Set reminders
- Track progress

### 4. Code Assistant
- Code analysis
- Bug detection
- Performance suggestions
- Refactoring help

### 5. Personal Notes
- Save notes
- Search notes
- Auto-organize

## System Requirements

**Server Side (Codespaces):**
- 4GB RAM (free tier)
- 2GB disk space
- Internet connection

**Client Side (Android):**
- Android 8.0+
- 50MB storage
- Internet connection
- Any browser (Chrome, Firefox, etc.)

## How It Works

1. **You type** → Message sent to backend API
2. **Backend processes** → LangChain + Ollama processes your request
3. **Ollama LLM responds** → Mistral 7B generates response
4. **Response displayed** → Shows on your phone in real-time

## Cost Breakdown
- Ollama LLM: FREE (open source)
- GitHub Codespaces: 180 hours/month FREE
- Frontend: FREE (static HTML/CSS/JS)
- Total: $0

## Privacy & Security
- ✅ All data stays private (runs in your Codespace)
- ✅ No third-party APIs needed
- ✅ No data collection
- ✅ Open source (audit the code)

## Contributing
Feel free to fork, modify, and improve!

## Roadmap
- [ ] Voice input/output
- [ ] Offline mode
- [ ] Database for notes
- [ ] Custom skill plugins
- [ ] Native Android app
- [ ] Multi-user support

## Troubleshooting

**Q: Connection refused?**
A: Make sure backend is running and Codespace is active

**Q: Slow responses?**
A: First request loads the model (~30s), subsequent requests are faster

**Q: Can't find Codespace URL?**
A: Check the terminal output or GitHub Codespaces dashboard

## Support
Open an issue on GitHub for any problems!

## License
MIT License - Free to use and modify

---

**Made with ❤️ for Acradceo**

Start building with your AI assistant now! 🚀
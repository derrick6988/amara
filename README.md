# 🤖 Amara: Emotionally Intelligent AI Assistant

An AI bot with **full emotional intelligence** and **intellectual capabilities**. Amara combines emotional awareness, empathetic responses, and deep problem-solving to create meaningful human-AI interactions.

## ✨ Features

- **Emotional Intelligence**: Detects and responds to user emotions (joy, sadness, anger, curiosity, etc.)
- **Empathetic Responses**: Generates context-aware, emotionally aware replies
- **Deep Analysis**: Intellectual problem-solving with structured analysis
- **Web Search**: Search the web with emotional context
- **GitHub Integration**: View and manage GitHub issues with understanding
- **Conversation Memory**: Learns from interactions and maintains conversation context
- **Multi-LLM Support**: Works with OpenAI, Ollama, or other providers
- **Interactive CLI**: Natural conversation interface with special commands

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ 
- Ollama (for local LLM) OR OpenAI API key
- git

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/derrick6988/amara.git
cd amara

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and preferences

# Run the bot
python main_enhanced.py
```

### Option 3: Docker

```bash
# Build the Docker image
docker build -t amara .

# Run with Ollama
docker run -it --network host amara

# Or with OpenAI API
docker run -it -e OPENAI_API_KEY=your_key amara
```

## 🎮 Usage

### Interactive Session

```bash
python main_enhanced.py
```

Commands:
- **`personality`** - Show Amara's personality profile
- **`state`** - Display current emotional and intellectual state
- **`search <query>`** - Search the web with emotional awareness
- **`think <topic>`** - Deep intellectual analysis of a topic
- **`reset`** - Reset conversation while preserving learning
- **`exit`** - Exit the bot
- Or just **chat naturally!**

### Example Interaction

```
========================================================================
🤖 Enhanced AI Bot - With Full Emotional Intelligence & Intellect
========================================================================

Bot Personality Overview:
Amara: a warm, witty, and empathetic assistant centered on community uplift, accuracy, and privacy.

[curious] You: How does machine learning work?

Bot [curious]:
Machine learning is a fascinating approach to AI! It's about creating algorithms that improve through experience rather than explicit programming...

[Emotional Context: Empathy actively engaged]
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
# GitHub token (optional, for GitHub features)
GITHUB_TOKEN=your_github_token_here

# OpenAI API key (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here

# Ollama settings (if using local LLM)
OLLAMA_URL=http://localhost:11434

# LLM Provider: 'openai' or 'ollama'
LLM_PROVIDER=ollama

# Model name
LLM_MODEL=mistral

# Server port (for future web service)
PORT=3000
```

### Running with Different LLM Providers

**Local Ollama (recommended for privacy):**
```bash
# Terminal 1: Start Ollama server
ollama serve

# Terminal 2: Pull a model
ollama pull mistral

# Terminal 3: Run Amara
LLM_PROVIDER=ollama python main_enhanced.py
```

**OpenAI:**
```bash
OPENAI_API_KEY=sk-... LLM_PROVIDER=openai LLM_MODEL=gpt-4o-mini python main_enhanced.py
```

## 🏗️ Architecture

```
amara/
  ├── emotions.py           Emotional intelligence system
  │   ├── EmotionType       Enum of supported emotions
  │   ├── EmotionalState    Current emotional state tracking
  │   ├── EmotionProcessor  Detects emotions in text
  │   ├── EmpathyEngine     Generates empathetic responses
  │   ├── IntelligenceCore  Problem analysis and learning
  │   └── PersonalityCore   Bot personality traits
  │
  ├── main_enhanced.py      Main bot implementation
  │   ├── EnhancedAIBot     Core bot class
  │   ├── WebSearchEngine   Web search capabilities
  │   ├── GitHubAssistant   GitHub integration
  │   └── interactive_session() CLI interface
  │
  ├── ollama.py             LLM provider abstraction
  │   ├── _openai_chat()    OpenAI provider
  │   └── _ollama_chat()    Ollama provider
  │
  ├── requirements.txt      Python dependencies
  ├── Dockerfile            Container setup
  ├── .env.example          Environment template
  └── test/                 Test suite
      └── test_emotions.py  Emotion detection tests
```

### How It Works

1. **User Input** → Emotional Analysis (EmotionProcessor detects mood/sentiment)
2. **Emotion Adaptation** → Bot adjusts its own emotional state to match user needs
3. **Empathetic Response** → EmpathyEngine generates contextual acknowledgment
4. **Intellectual Analysis** → IntelligenceCore performs structured problem analysis
5. **Response Generation** → LLM generates response with system prompt including emotional state
6. **Learning** → Bot stores interaction for future learning

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest test/ -v

# Run with coverage
pytest test/ --cov=. --cov-report=html

# Run specific test
pytest test/test_emotions.py::test_detects_joy -v
```

## 📦 Dependencies

- **requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management
- **duckduckgo-search** - Web search engine
- **PyGithub** - GitHub API client
- **openai** - OpenAI API (optional, if using OpenAI)
- **ollama** - Ollama client (optional, if using Ollama locally)
- **pytest** - Testing framework

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure tests pass:
```bash
pytest test/ -v
```

## 🛠️ Development

### Running Tests on Every Push

Tests automatically run via GitHub Actions. Check `.github/workflows/python-tests.yml` for the configuration.

### Local Development

```bash
# Install development dependencies
pip install -r requirements.txt pytest

# Create a feature branch
git checkout -b feature/your-feature

# Make changes, then test
pytest test/ -v

# Push and create a PR
git push origin feature/your-feature
```

## 📋 Future Roadmap

- [ ] Web interface (Flask/FastAPI)
- [ ] Database persistence for conversation history
- [ ] Advanced personality customization
- [ ] Multi-user support with authentication
- [ ] Voice input/output (speech-to-text, text-to-speech)
- [ ] Custom emotion training
- [ ] Plugin system for extended capabilities
- [ ] Deployment guides (AWS, Heroku, DigitalOcean)

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

If you have questions or encounter issues:

1. Check the [GitHub Issues](https://github.com/derrick6988/amara/issues)
2. Review the documentation above
3. Create a new issue with a clear description

## 🌟 Acknowledgments

Amara is built with emotional intelligence at its core, designed to demonstrate how AI can be both intellectually capable and emotionally aware. Special thanks to the open-source community for the amazing tools and libraries that make this possible.

---

**Made with 💙 by derrick6988**

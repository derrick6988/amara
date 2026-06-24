#!/bin/bash

set -e

echo "🤖 Amara AI Bot - Setup Script"
echo "=============================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
MIN_VERSION="3.11"

if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "❌ Python 3.11 or higher is required. You have Python $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✅ Virtual environment created"
echo ""

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Setup environment file
if [ ! -f .env ]; then
    echo "⚙️  Setting up environment configuration..."
    cp .env.example .env
    echo "✅ Created .env file (edit it with your API keys)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "=============================="
echo "✅ Setup Complete!"
echo "=============================="
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Edit .env with your configuration:"
echo "   - For Ollama (local): Set LLM_PROVIDER=ollama"
echo "   - For OpenAI: Set OPENAI_API_KEY and LLM_PROVIDER=openai"
echo "   - For GitHub: Set GITHUB_TOKEN (optional)"
echo ""
echo "2. If using Ollama locally:"
echo "   - Install Ollama from https://ollama.ai"
echo "   - Run: ollama pull mistral"
echo "   - In another terminal: ollama serve"
echo ""
echo "3. Run Amara:"
echo "   source venv/bin/activate  # Activate virtual environment"
echo "   python main_enhanced.py"
echo ""
echo "🚀 Good luck with Amara!"

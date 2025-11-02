# Legal Document Verification Agent

AI-powered agent for legal operations clerks to automatically verify documents for compliance, renewal dates, obligations, and risks.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- OpenAI API key or Anthropic API key

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Add your API keys to .env.local
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
uvicorn app.main:app --reload
```

## 📋 Features

- ✅ **Document Scanning**: Upload and process PDF/Word documents
- 📅 **Renewal Date Detection**: Automatically extract and track renewal deadlines
- 📜 **Obligation Tracking**: Identify contractual commitments and requirements
- ⚖️ **Compliance Verification**: Check against regulatory requirements
- 🎯 **Risk Assessment**: Highlight compliance gaps and calculate risk scores
- 👤 **Human-in-the-Loop**: Collaborative review with AI agent
- 📊 **Interactive Reports**: Exportable verification reports

## 🏗️ Architecture

Built with:
- **Frontend**: Next.js 15 + React + TypeScript + CopilotKit
- **Backend**: FastAPI + LangGraph + LangChain
- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **Protocol**: AG-UI (Agent-User Interaction)

See [architecture.md](./architecture.md) for detailed design.

## 📖 Documentation

- [Architecture Overview](./architecture.md)
- [Setup Guide](./docs/setup.md) _(coming soon)_
- [User Guide](./docs/user-guide.md) _(coming soon)_
- [API Reference](./docs/api.md) _(coming soon)_

## 🔧 Project Status

🚧 **Under Active Development**

Current Phase: Foundation Setup

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please read the contributing guidelines first.

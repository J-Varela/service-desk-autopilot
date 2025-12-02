# Service Desk Autopilot

An AI-powered service desk automation system that uses multi-agent architecture to intelligently handle IT support requests, automate common tasks, and streamline help desk operations.

## 📊 Presentation

**[View Project Presentation Slides](./docs/Presentation%20-%20Service-desk%20Autopilot%20AI%20%20.pdf)**

## 🌟 Overview

Service Desk Autopilot is an intelligent automation platform designed to:
- **Triage** incoming support requests automatically
- **Execute** common IT tasks through automated runbooks
- **Escalate** complex issues to human agents when needed
- **Provide** self-service capabilities through natural language understanding
- **Audit** all actions for compliance and tracking

## 🏗️ Architecture

The system uses a multi-agent orchestration pattern where specialized agents handle different aspects of the service desk workflow:

### Core Agents

- **Triage Agent**: Analyzes and categorizes incoming requests
- **Planner Agent**: Creates execution plans for complex tasks
- **Knowledge Agent**: Retrieves relevant information and documentation
- **Runbook Executor Agent**: Executes automated procedures
- **Clarification Agent**: Gathers additional information when needed
- **Enrichment Agent**: Enhances requests with context and metadata
- **Safety Agent**: Validates operations for security and compliance
- **Escalation Agent**: Routes complex issues to human operators

### Components

```
service-desk-autopilot/
├── frontend/                # Web UI dashboard
│   ├── index.html          # Main HTML interface
│   ├── script.js           # Frontend logic
│   └── styles.css          # UI styling
├── backend/
│   ├── agents/              # Specialized AI agents
│   ├── config/              # Configuration and settings
│   ├── data/                # Training and test datasets
│   ├── docs/                # Architecture documentation
│   ├── models/              # Data models and schemas
│   ├── orchestrator/        # Agent coordination and routing
│   ├── runbooks/            # Automated task procedures
│   ├── services/            # Integration services
│   └── utils/               # Utilities and helpers
└── serviceEnv/              # Python virtual environment
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment support
- Access to required APIs (Azure OpenAI, GitHub Models, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd service-desk-autopilot
   ```

2. **Activate the virtual environment**
   ```powershell
   # Windows PowerShell
   .\serviceEnv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the `backend` directory:
   ```env
   # AI Model Configuration
   AZURE_OPENAI_ENDPOINT=your-endpoint
   AZURE_OPENAI_API_KEY=your-api-key
   GITHUB_TOKEN=your-github-token
   
   # Service Configuration
   TICKETING_SYSTEM_URL=your-ticketing-url
   DIRECTORY_SERVICE_URL=your-directory-url
   ```

5. **Run the application**
   ```bash
   cd backend
   python -m orchestrator.main
   ```

## 📋 Available Runbooks

Automated procedures for common IT tasks:

- **Password Reset**: Securely reset user passwords
- **Account Status Check**: Verify account status and permissions
- **PTO Balance Lookup**: Check employee vacation balances

## 🔧 Services

The system integrates with various enterprise services:

- **Directory Service**: User account management and authentication
- **HR Service**: Employee information and benefits
- **Ticketing Service**: Incident and request tracking
- **Audit Log Service**: Compliance and activity logging

## 💻 Usage

### Web UI Dashboard

The easiest way to interact with Service Desk Autopilot is through the web interface:

1. **Start the backend server**
   ```powershell
   .\serviceEnv\Scripts\Activate.ps1
   uvicorn backend.orchestrator.main:app --reload
   ```

2. **Open the web UI**
   - Navigate to `frontend/index.html` in your browser
   - Or visit `http://localhost:8000/docs` for API documentation

3. **Start chatting**
   - Enter your user ID (e.g., `jv-123`)
   - Type your request in natural language
   - Watch the agent pipeline execute in real-time

**Features:**
- 💬 Interactive chat interface
- 📊 Real-time agent activity visualization
- 🔍 Live execution logs
- ✅ Connection status monitoring

### CLI Client

For command-line usage:

```powershell
python cli_client.py
```

### API Endpoints

The orchestrator exposes REST API endpoints:

**POST** `/chat` - Submit a support request
```json
{
  "user_id": "jv-123",
  "message": "I need to reset my password"
}
```

**GET** `/health` - Check API status
```json
{
  "status": "ok",
  "environment": "development",
  "azure_configured": true
}
```

### Example Request

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "user_id": "jv-123",
        "message": "I need to reset my password"
    }
)

print(response.json()['reply'])
print(response.json()['activity_log'])
```

## 🧪 Testing

The project includes test datasets in `backend/data/`:
- `train.csv`: Training data for model fine-tuning
- `test.csv`: Test cases for validation
- `HRDataset_v14.csv`: HR information for testing integrations

## 📊 Data Models

Key data structures:

- **Chat**: Conversation and message handling
- **Intent**: Request classification and understanding
- **Plan**: Multi-step task orchestration
- **Runbook**: Automated procedure definitions
- **Escalation**: Routing rules and criteria

## 🔒 Security

- All operations are validated by the Safety Agent
- Audit logging for compliance tracking
- Role-based access control
- Secure credential management

## 🛠️ Development

### Adding New Agents

1. Create agent class in `backend/agents/`
2. Inherit from `BaseAgent`
3. Implement required methods
4. Register in agent router

### Creating Custom Runbooks

1. Define runbook in `backend/runbooks/`
2. Add metadata to `config/runbook_catalog.json`
3. Implement execution logic
4. Add validation and rollback procedures

## 📝 Configuration

Edit `backend/config/settings.py` to customize:
- Agent behavior and thresholds
- API endpoints and timeouts
- Logging levels
- Runbook parameters

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

[Add your license information here]

## 🐛 Troubleshooting

### Common Issues

**Virtual environment not activating**
- Ensure execution policy allows scripts: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**API connection errors**
- Verify environment variables are set correctly
- Check network connectivity to external services

**Agent not responding**
- Review logs in the console output
- Verify model endpoints are accessible

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Contact the development team
- Review documentation in `backend/docs/`

## 🎯 Roadmap

- [ ] Enhanced natural language understanding
- [ ] Additional runbook templates
- [x] Web-based dashboard ✨
- [ ] Integration with more ticketing systems
- [ ] Advanced analytics and reporting
- [ ] Multi-language support

---

Built with ❤️ for IT automation

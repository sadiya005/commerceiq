# CommerceIQ Production Architecture

## System Flow

User
↓
FastAPI
↓
CommerceIQ Application
↓
Business Logic
↓
Business Tools / Agent
↓
Data + Models
↓
Groq API
↓
Response

## Main Components

- FastAPI: API layer
- Business Logic: Customer, product, order and revenue analysis
- Tools: Structured business functions available to the agent
- Agent: Multi-step reasoning and tool selection
- Data: Processed CommerceIQ datasets
- Models: Classical ML, transformer and LLM components
- Groq API: Hosted LLM inference
- Docker: Application containerization
- AWS: Production deployment infrastructure

## Production Principles

- Keep API keys outside source code.
- Separate application logic from notebooks.
- Validate inputs and handle errors.
- Reuse tested business functions.
- Log important application events.
- Keep model and API configuration centralized.
- Do not claim components as deployed unless they are actually deployed.

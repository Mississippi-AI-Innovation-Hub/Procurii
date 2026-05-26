# Mississippi ITS Procurement Assistant

## Overview

This repository contains the code and supporting documentation for a Mississippi Artificial Intelligence Innovation Hub Proof of Concept focused on procurement knowledge retrieval and conversational assistance.

The project explored whether an AI-enabled assistant using Amazon Bedrock Agents could improve access to procurement guidance, reduce reliance on siloed institutional knowledge, and support more consistent responses to procurement-related questions within the Mississippi Department of Information Technology Services (ITS) Procurement Services Division.

The Proof of Concept demonstrates feasibility within a sandbox environment and is not intended to represent a production-ready system.

---

## Agency Problem

The ITS Procurement Services Division experienced operational inefficiencies caused by:

- Siloed institutional knowledge
- Staffing transitions and retirements
- Difficult-to-navigate procurement documentation
- Inconsistent response workflows

This project explored whether conversational AI and retrieval-enabled workflows could improve information accessibility and response consistency.

---

## PoC Scope and Demonstrated Capabilities

This repository demonstrates:

- Conversational procurement assistance
- Amazon Bedrock Agent integration
- Retrieval-based response generation
- Citation-aware responses
- Streamlit-based chatbot interface
- Session-based conversational continuity
- AWS-hosted sandbox workflows

Capabilities demonstrated include:

- Natural language procurement question answering
- Source citation display
- Retrieval-backed responses
- Multi-message session handling
- Suggested prompts and guided interaction
- Debug and validation tooling for response integrity

---

## Architecture Overview

The system uses a Streamlit frontend connected to an Amazon Bedrock Agent Runtime backend.

### High-Level Workflow

1. User submits a procurement-related question
2. Streamlit frontend sends request to Bedrock Agent Runtime
3. Bedrock Agent retrieves relevant procurement information
4. Agent generates contextual response
5. Citations and references are returned
6. Frontend displays response and source materials

### Core Components

- **Frontend/UI:** Streamlit
- **AI Runtime:** Amazon Bedrock Agents
- **Cloud SDK:** boto3
- **Environment Management:** python-dotenv
- **Session Handling:** Streamlit session state
- **Citation Rendering:** Custom sidebar citation display

---

## Repository Structure

```text
README.md                 Project overview and documentation
app.py                    Main Streamlit application
requirements.txt          Python dependencies
docs/                     Supporting project documentation
docs/images/              Architecture diagrams and screenshots
demos/                    Demo assets and sample prompts
retrieval/                Retrieval-related placeholder components
prompts/                  Prompt examples and templates
evaluation/               Evaluation notes and testing materials
infra/                    Infrastructure-related notes
tests/                    Testing utilities and future test cases
data/sample/              Placeholder or synthetic sample data
```

---

## Setup

### Prerequisites

- Python 3.10+
- AWS Account with Bedrock access
- Configured Bedrock Agent
- AWS credentials or IAM access
- pip package manager

---

### Clone Repository

```bash
git clone https://github.com/MaverickDSmith/procurii-chatbot.git
cd procurii-chatbot
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file using `.env.example`.

Required configuration values include:

```env
AGENT_ID=
AGENT_ALIAS_ID=
AWS_REGION=
```

Optional credentials:

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

---

### Run Application

```bash
streamlit run app.py
```

---

## Configuration

The application supports configuration through:

- `.env`
- Streamlit secrets
- IAM role credentials
- AWS CLI profiles

Environment configuration includes:

- Bedrock Agent ID
- Bedrock Alias ID
- AWS Region
- Optional AWS credentials

---

## Data Notes

This repository does not contain real ITS procurement data or protected agency information.

Any included data, screenshots, prompts, or examples are intended for demonstration purposes only and should be considered placeholder or public-safe materials.

---

## Usage

After launching the application:

1. Open the Streamlit interface
2. Submit a procurement-related question
3. Review generated responses
4. Expand citations in the sidebar to inspect referenced materials

Example questions:

- "How do I submit a procurement request?"
- "What are the procurement guidelines?"
- "What is the approval process for purchases?"

---

## Testing and Evaluation

The Proof of Concept was evaluated through:

- Manual testing
- Retrieval validation
- Citation verification
- Sandbox demonstrations
- UI interaction testing

Observed outcomes included:

- Moderate-to-high retrieval relevance
- Stable Bedrock Agent communication
- Successful citation rendering
- Positive usability feedback

---

## Limitations

This project was developed as a limited Proof of Concept and is not production-ready.

Known limitations include:

- Sandbox-only deployment
- Limited testing coverage
- Dependence on source document quality
- No production ITS integrations
- Simplified security and operational controls
- Prototype conversational workflows

---

## Disclaimer

This repository contains code and supporting materials developed as part of a Mississippi Artificial Intelligence Innovation Hub Proof of Concept project.

The contents are provided for prototype demonstration purposes only. They are not production ready and may include simplified workflows, incomplete security guardrails, placeholder integrations, or reduced controls appropriate only for a Proof-of-Concept environment.

This repository should not be used with production data or deployed into production environments without additional security review, governance approval, testing, and operational hardening.

---

## License

MIT License

---

## Contributors

- Cameron Cummings
- Nicole Milla Monterola
- Ava Grace Noe
- Ander Talley
- Cedric Roberson
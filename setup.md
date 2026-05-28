# Setup Instructions

## Prerequisites

The following are required:

- Python 3.10+
- AWS account with Bedrock access
- Configured Bedrock Agent
- pip package manager

---

## Clone Repository

```bash
git clone https://github.com/MaverickDSmith/procurii-chatbot.git
cd procurii-chatbot
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Copy `.env.example` to `.env`.

Required variables:

```env
AGENT_ID=
AGENT_ALIAS_ID=
AWS_REGION=
```

Optional variables:

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

---

## Launch Application

```bash
streamlit run app.py
```

---

## Access Interface

After startup, Streamlit will provide a local URL in the terminal, typically:

```text
http://localhost:8501
```

Open the URL in a browser to interact with the chatbot.
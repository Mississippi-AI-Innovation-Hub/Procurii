# Architecture Overview
<img width="333" height="250" alt="8db47c46-f393-4c0d-b6f6-b61a1be864ad" src="https://github.com/user-attachments/assets/f43ccd3f-895a-4a46-8df0-2465d865beef" />


## Summary

The Mississippi ITS Procurement Assistant is a Streamlit-based conversational interface connected to Amazon Bedrock Agent Runtime services.

The system was developed as a Proof of Concept to evaluate whether AI-enabled conversational workflows could improve access to procurement guidance and reduce dependency on siloed institutional knowledge.

---

## System Components

### Frontend Interface

The frontend is built using Streamlit and provides:

- Conversational chatbot interface
- Suggested prompts
- Session continuity
- Citation sidebar display
- Debug and validation controls

---

### AI Backend

The application communicates with Amazon Bedrock Agent Runtime using boto3.

The Bedrock Agent is responsible for:

- Interpreting user questions
- Retrieving relevant procurement information
- Generating contextual responses
- Returning citation metadata

---

### Citation Handling

The application extracts citation metadata from Bedrock responses and renders source references in a dedicated sidebar.

Citation functionality includes:

- Source labeling
- Expandable citation text
- Retrieval reference display
- Citation numbering

---

### Session Management

Session continuity is maintained using Streamlit session state and UUID-based session identifiers.

---

## High-Level Workflow

1. User submits procurement question
2. Streamlit frontend sends request to Bedrock Agent Runtime
3. Bedrock Agent retrieves relevant information
4. Agent generates response with citations
5. Application renders response and sources

---

## Environment

This project was tested within a sandbox Proof-of-Concept environment and was not deployed as a production system.

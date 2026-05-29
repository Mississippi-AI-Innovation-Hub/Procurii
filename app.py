import streamlit as st
import boto3
import os
import uuid
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()

load_dotenv()

def get_config_value(key: str, default=None):
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

AGENT_ID = get_config_value("AGENT_ID")
AGENT_ALIAS_ID = get_config_value("AGENT_ALIAS_ID")
AWS_REGION = get_config_value("AWS_REGION", "us-east-1")
AWS_SESSION_TOKEN= get_config_value("AWS_SESSION_TOKEN")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None

def invoke_bedrock_agent(prompt: str) -> dict:
    if not AGENT_ID or not AGENT_ALIAS_ID:
        return {
            "text": "Demo mode is active. Please configure AGENT_ID and AGENT_ALIAS_ID to connect to Amazon Bedrock.",
            "citations": []
        }

    try:
        client = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

        response = client.invoke_agent(
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=st.session_state.session_id,
            inputText=prompt
        )

        chunks = []
        citations = []

        for event in response.get("completion", []):
            if "chunk" in event:
                chunk = event["chunk"]
                if "bytes" in chunk:
                    chunks.append(chunk["bytes"].decode("utf-8"))

                if "attribution" in chunk:
                    citations.append(chunk["attribution"])

        return {
            "text": "".join(chunks).strip() or "I did not receive a response from the agent.",
            "citations": citations
        }

    except ClientError as e:
        return {
            "text": f"AWS Bedrock error: {e.response['Error'].get('Message', str(e))}",
            "citations": []
        }
    except Exception as e:
        return {
            "text": f"Unexpected error while calling Bedrock: {str(e)}",
            "citations": []
        }


def insert_citation_markers(content: str, citations: list) -> str:
    # Simple fallback marker behavior.
    # You can make this smarter later if your citation metadata includes spans.
    if not citations:
        return content

    marker_text = " ".join(f"[{idx + 1}]" for idx in range(len(citations)))
    return f"{content}\n\n{marker_text}"


def display_citation_sidebar(citations: list):
    st.markdown("### 📚 Sources")

    for idx, citation in enumerate(citations, start=1):
        with st.expander(f"Source {idx}"):
            st.markdown(f"<div class='citation-text'>{citation}</div>", unsafe_allow_html=True)

# UI
# Custom CSS to center the title and caption, and style citations
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .main-caption {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 1rem;
    }
    /* Citation sidebar styling */
    .citation-text {
        font-size: 0.9rem;
        line-height: 1.5;
        color: #333;
    }
    .citation-source {
        font-size: 0.85rem;
        color: #666;
    }
    </style>
    <div class="main-title">📋 Mississippi ITS Procurement Assistant</div>
    <div class="main-caption">Your AI-powered guide for procurement questions and guidance</div>
""", unsafe_allow_html=True)
st.divider()

# Configuration check
if not AGENT_ID or not AGENT_ALIAS_ID:
    st.warning("⚠️ Please configure your Agent ID and Agent Alias ID in the environment variables or Streamlit secrets.")
    st.info("""
    **Configuration needed:**
    - AGENT_ID
    - AGENT_ALIAS_ID
    - AWS_REGION (optional, defaults to us-east-1)
    - AWS_ACCESS_KEY_ID (optional, if not using IAM role)
    - AWS_SECRET_ACCESS_KEY (optional, if not using IAM role)
    """)
    st.caption("Demo mode active: Bedrock credentials are not configured locally.")
  #  st.stop()
  

# Sidebar for controls (without configuration details)
with st.sidebar:
    st.header("Mississippi ITS")
    st.markdown("**Procurement Office**")
    st.divider()

    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.divider()

    # Debug mode toggle (can be enabled for troubleshooting)
    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = False

    # Show debug toggle in an expander to keep UI clean
    with st.expander("⚙️ Advanced Settings"):
        st.session_state.debug_mode = st.checkbox(
            "Enable Debug Mode",
            value=st.session_state.debug_mode,
            help="Shows detailed logging in terminal for troubleshooting response issues"
        )
        if st.session_state.debug_mode:
            st.caption("⚠️ Debug output will appear in your terminal/console")

    st.divider()
    st.caption("Powered by AI • Built with Streamlit and Amazon Bedrock")

# Suggested questions for new conversations
SUGGESTED_QUESTIONS = [
    "What can you do?",
    "How do I submit a procurement request?",
    "What are the procurement guidelines?",
    "What is the approval process for purchases?",
    "What are the vendor requirements?",
    "How do I check the status of my procurement request?"
]

# Display suggested questions if no messages yet
if len(st.session_state.messages) == 0:
    st.markdown("### 💡 Suggested Questions")
    st.markdown("Get started by asking one of these common questions:")

    # Create columns for better layout
    cols = st.columns(2)
    for idx, question in enumerate(SUGGESTED_QUESTIONS):
        col = cols[idx % 2]
        with col:
            if st.button(question, key=f"suggested_{idx}", use_container_width=True):
                # Store the selected question to process it
                st.session_state.selected_question = question
                st.rerun()

    st.divider()

# Handle selected question from suggested questions
if hasattr(st.session_state, 'selected_question') and st.session_state.selected_question:
    prompt = st.session_state.selected_question
    st.session_state.selected_question = None  # Clear the selected question

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get agent response
    with st.spinner("Thinking..."):
        response = invoke_bedrock_agent(prompt)

    # Add assistant response to chat history with citations
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["text"],
        "citations": response.get("citations", [])
    })
    st.rerun()

# Create main layout: content area on left, citation sidebar on right
col_main, col_sidebar = st.columns([7, 3])

with col_main:
    # Display chat messages
    for msg_idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            content = message["content"]

            # Check for potential issues with assistant responses
            if message["role"] == "assistant":
                # Validate response quality
                if len(content) < 20:
                    st.warning("⚠️ This response seems unusually short. There may have been an issue.")

                # Check if response starts mid-sentence
                if content and not content[0].isupper() and content[0] not in ['(', '[', '"', "'", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    st.info("ℹ️ Note: This response may have been truncated at the beginning.")

                # Add citation markers if this is an assistant message with citations
                if message.get("citations"):
                    content = insert_citation_markers(content, message["citations"])

            st.markdown(content)

with col_sidebar:
    # Display citations for the most recent assistant message with citations
    st.markdown("---")

    # Find the last assistant message with citations
    last_cited_message = None
    for message in reversed(st.session_state.messages):
        if (message["role"] == "assistant" and
            "citations" in message and
            len(message.get("citations", [])) > 0):
            last_cited_message = message
            break

    if last_cited_message:
        display_citation_sidebar(last_cited_message["citations"])

        # Debug mode: Show raw citation data
        if st.session_state.get("debug_mode", False):
            with st.expander("🔧 Debug: Raw Citation Data"):
                st.json(last_cited_message["citations"])
    else:
        st.markdown("### 📚 Sources")
        st.markdown("*Citations will appear here*")

# Chat input
if prompt := st.chat_input("Ask about procurement processes, guidelines, or requirements..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get agent response
    with st.spinner("Thinking..."):
        response = invoke_bedrock_agent(prompt)

    # Add assistant response to chat history with citations
    st.session_state.messages.append({
        "role": "assistant",
        "content": response["text"],
        "citations": response.get("citations", [])
    })

    # Rerun to update the display with the new message
    st.rerun()
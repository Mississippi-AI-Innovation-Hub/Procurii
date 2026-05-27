import streamlit as st
import boto3
import os
import uuid
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Mississippi ITS Procurement Assistant",
    page_icon="📋",
    layout="wide"  # Use wide layout for better citation sidebar
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

def validate_response_integrity(text, original_length):
    """Validate that the response hasn't been corrupted or truncated"""
    issues = []

    # Check if text is suspiciously short
    if len(text) < 10 and original_length > 10:
        issues.append("Response was significantly shortened during processing")

    # Check if response starts mid-sentence (common truncation indicator)
    if text and not text[0].isupper() and text[0] not in ['(', '[', '"', "'"]:
        issues.append("Response appears to start mid-sentence")

    # Check for incomplete sentences at the end
    if text and text[-1] not in ['.', '!', '?', ')', ']', '"', "'"]:
        # This is actually common and OK, so we'll just note it
        pass

    return issues

def cleanup_response_text(text):
    """Clean up response text by removing unwanted characters and phrases"""
    import re

    # Store original for validation
    original_text = text
    original_length = len(text)

    # Remove literal \n strings (not actual newlines)
    text = text.replace('\\n', '\n')

    # Remove other escape sequences that might appear as literal text
    text = text.replace('\\t', ' ')
    text = text.replace('\\r', '')

    # Remove phrases that shouldn't be in the final output
    unwanted_phrases = [
        r'This is outlined in the search results\.?',
        r'This is also outlined in the search results\.?',
        r'This is mentioned in the search results\.?',
        r'This is also mentioned in the search results\.?',
        r'As mentioned in the search results\.?',
        r'According to the search results\.?',
        r'The search results indicate\.?',
        r'Based on the search results\.?',
        r'As shown in the search results\.?',
        r'As outlined in the search results\.?',
        r'As stated in the search results\.?',
        r'This is outlined in the table in the search results\.?',
        r'This is also outlined in the table in the search results\.?',
        r'This information is found in the search results\.?',
        r'This can be found in the search results\.?',
        r'[Tt]his is (?:also )?(?:outlined|mentioned|stated|found|shown) in (?:the )?(?:table in )?(?:the )?search results\.?',
    ]

    for phrase in unwanted_phrases:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)

    # Clean up multiple spaces
    text = re.sub(r' +', ' ', text)

    # Clean up multiple newlines (more than 2 in a row)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove trailing/leading whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    cleaned_text = text.strip()

    # Validate integrity
    if st.session_state.get("debug_mode", False):
        issues = validate_response_integrity(cleaned_text, original_length)
        if issues:
            print(f"⚠️ Response validation issues: {issues}")
            print(f"Original length: {original_length}, Final length: {len(cleaned_text)}")
            print(f"First 100 chars of original: {original_text[:100]}")
            print(f"First 100 chars of cleaned: {cleaned_text[:100]}")

    return cleaned_text

def insert_citation_markers(text, citations):
    """Insert numbered citation markers [1], [2], etc. into the text"""
    # For now, append citation markers at the end of sentences
    # In a more sophisticated version, we'd use citation span data from Bedrock
    if not citations or len(citations) == 0:
        return text

    # Simple approach: add all citation numbers at the end
    citation_count = sum(len(c.get('retrievedReferences', [])) for c in citations)
    if citation_count > 0:
        markers = ' '.join([f'[{i+1}]' for i in range(citation_count)])
        # Add markers at the end if not already present
        if not any(f'[{i+1}]' in text for i in range(citation_count)):
            text = f"{text} {markers}"

    return text

def display_citation_sidebar(citations):
    """Display citations in a right sidebar panel"""
    if not citations or len(citations) == 0:
        st.markdown("*No citations available*")
        return

    st.markdown("### 📚 Sources")
    st.caption("Referenced documents")
    st.markdown("---")

    citation_num = 1
    for citation in citations:
        retrieved_references = citation.get('retrievedReferences', [])

        for reference in retrieved_references:
            location = reference.get('location', {})
            content = reference.get('content', {})

            # Try to extract text from different possible fields
            text = None
            if 'text' in content and content['text']:
                text = content['text'].strip()
            elif 'content' in content and content['content']:
                text = content['content'].strip()

            # Debug mode: Log when text is not found
            if st.session_state.get("debug_mode", False) and not text:
                print(f"Citation {citation_num} has no text. Content structure: {content.keys()}")

            # Skip this citation if there's no actual text content
            if not text or text == '':
                continue

            # Get source location info
            s3_location = location.get('s3Location', {})
            uri = s3_location.get('uri', 'Unknown source')
            source_name = uri.split('/')[-1] if '/' in uri else uri

            # Display numbered citation with consistent, smaller sizing
            st.markdown(f"**[{citation_num}]** {source_name}")
            with st.expander("📖 View source text", expanded=False):
                st.caption(f"Source: {uri}")
                st.markdown(f"<div style='font-size: 0.9rem; line-height: 1.4;'>{text}</div>",
                           unsafe_allow_html=True)
            st.divider()

            citation_num += 1

    # If no valid citations were found after filtering
    if citation_num == 1:
        st.markdown("*No citation text available*")


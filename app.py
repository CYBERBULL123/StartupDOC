import streamlit as st
from backend.gemini import query_gemini  # Import the Gemini function
from backend.langchain import generate_startup_document  # Import LangChain function
import base64

# Function to create a downloadable link
def create_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()  # Encode content to base64
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Document</a>'

# App Title and Description
st.set_page_config(page_title="Startup Automation Tool", layout="centered")
st.markdown(
    """
    <h1 style="text-align:center; color:#4CAF50;">🚀 Startup Automation Tool</h1>
    <p style="text-align:center; font-size:16px; color:#555;">
    Streamline your startup journey with AI-powered document generation.<br>
    Create Business Plans, Funding Proposals, Pitch Decks, and Investor Materials in just a few clicks!
    </p>
    <hr style="border: 1px solid #ddd;">
    """,
    unsafe_allow_html=True,
)

# Dropdown for Document Type
st.markdown("<h3 style='color:#333;'>Select the Document Type</h3>", unsafe_allow_html=True)
doc_type = st.selectbox(
    "",
    ["Business Plan", "Funding Proposal", "Pitch Deck", "Investor Materials"],
    index=0,
)

# Input Fields
st.markdown("<h3 style='color:#333;'>Provide Your Startup Details</h3>", unsafe_allow_html=True)

fields = {
    "Business Plan": [
        {"label": "Business Name", "type": "text", "key": "business_name"},
        {"label": "Market Data", "type": "textarea", "key": "market_data"},
        {"label": "Financial Data", "type": "textarea", "key": "financial_data"},
    ],
    "Funding Proposal": [
        {"label": "Business Name", "type": "text", "key": "business_name"},
        {"label": "Investment Opportunity", "type": "textarea", "key": "investment_opportunity"},
        {"label": "Capital Needed (in USD)", "type": "number", "key": "capital_needed", "default": 1000},
    ],
    "Pitch Deck": [
        {"label": "Business Name", "type": "text", "key": "business_name"},
        {"label": "Business Idea", "type": "textarea", "key": "business_idea"},
        {"label": "Team Vision", "type": "textarea", "key": "team_vision"},
    ],
    "Investor Materials": [
        {"label": "Business Name", "type": "text", "key": "business_name"},
        {"label": "Investment Opportunity", "type": "textarea", "key": "investment_opportunity"},
        {"label": "Team Background", "type": "textarea", "key": "team_background"},
        {"label": "Financial Forecast", "type": "textarea", "key": "financial_forecast"},
    ],
}

user_inputs = {}
for field in fields[doc_type]:
    if field["type"] == "text":
        user_inputs[field["key"]] = st.text_input(field["label"])
    elif field["type"] == "textarea":
        user_inputs[field["key"]] = st.text_area(field["label"])
    elif field["type"] == "number":
        user_inputs[field["key"]] = st.number_input(field["label"], min_value=0, value=field.get("default", 0))

# AI Settings
st.markdown("<h3 style='color:#333;'>AI Settings</h3>", unsafe_allow_html=True)
ai_engine = st.radio("Choose AI Engine", ["Gemini", "LangChain"], horizontal=True, index=1)
response_language = st.selectbox("Response Language", ["English", "Hindi", "Spanish"], index=0)
response_tone = st.radio("Response Tone", ["Formal", "Neutral", "Casual"], horizontal=True, index=0)

# Generate Button
if st.button("Generate Document"):
    if all(user_inputs.values()):
        # Build context and prompt
        context = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in user_inputs.items()])
        prompt = f"Generate a {doc_type.lower()} based on the following details:\n{context}"

        # Generate content
        if ai_engine == "Gemini":
            doc_content = query_gemini(context, prompt)
        else:
            doc_content = generate_startup_document(
                query=doc_type,
                document_type=doc_type.lower().replace(" ", "_"),
                language=response_language,
                tone=response_tone.lower(),
            )

        # Display Generated Content
        st.markdown("<h3 style='color:#333;'>Generated Document</h3>", unsafe_allow_html=True)
        st.markdown(f"### {doc_type}", unsafe_allow_html=True)
        st.markdown(doc_content, unsafe_allow_html=True)

        # Add Download Button
        download_link = create_download_link(doc_content, f"{doc_type.replace(' ', '_')}.txt")
        st.markdown(download_link, unsafe_allow_html=True)
    else:
        st.error("Please fill in all the required fields.")

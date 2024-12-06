import streamlit as st
from backend.gemini import query_gemini  # Import the Gemini function
from backend.langchain import craft_prompt  # Import LangChain function
import base64
import time


# App Configuration
st.set_page_config(page_title="🚀 Startup Automation Tool", layout="wide", page_icon="🌟")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    </style>
    """,
    unsafe_allow_html=True,
)

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Load the CSS file
load_css("ui/style.css")

# Function to create a downloadable link
def create_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Document</a>'

# Initialize Session State for Generated Responses
if "generated_docs" not in st.session_state:
    st.session_state["generated_docs"] = []


# App Header
st.markdown(
    """
    <h1 style="text-align:center; color:#4CAF50;">🚀 Startup Automation Tool</h1>
    <p style="text-align:center; font-size:16px; color:#b3ac29;">
    Streamline your startup journey with <b>AI-powered document generation</b>.<br>
    Create <span style="color:#FF5733;">Business Plans</span>, <span style="color:#33A1FF;">Funding Proposals</span>, 
    <span style="color:#8D33FF;">Pitch Decks</span>, and <span style="color:#FFC300;">Investor Materials</span> in just a few clicks!
    </p>
    <hr style="border: 1px solid #ddd;">
    """,
    unsafe_allow_html=True,
)

# Dropdown for Document Type
st.markdown("<h3 style='color:#b3ac29;'>📑 Select the Document Type</h3>", unsafe_allow_html=True)
doc_type = st.selectbox(
    "",
    ["Business Plan", "Funding Proposal", "Pitch Deck", "Investor Materials"],
    index=0,
)

# Input Fields Configuration
fields = {
    "Business Plan": [
        {"label": "🏢 Business Name", "type": "text", "key": "business_name"},
        {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
         "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"]},
        {"label": "📊 Market Data", "type": "section", "key": "market_data"},
        {"label": "💰 Financial Data", "type": "section", "key": "financial_data"},
    ],
    "Funding Proposal": [
        {"label": "🏢 Business Name", "type": "text", "key": "business_name"},
        {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
         "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"]},
        {"label": "📈 Investment Opportunity", "type": "textarea", "key": "investment_opportunity"},
        {"label": "💵 Capital Needed (in USD)", "type": "number", "key": "capital_needed", "default": 1000},
    ],
    "Pitch Deck": [
        {"label": "🏢 Business Name", "type": "text", "key": "business_name"},
        {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
         "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"]},
        {"label": "💡 Business Idea", "type": "textarea", "key": "business_idea"},
        {"label": "🎯 Team Vision", "type": "textarea", "key": "team_vision"},
    ],
    "Investor Materials": [
        {"label": "🏢 Business Name", "type": "text", "key": "business_name"},
        {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
         "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"]},
        {"label": "📈 Investment Opportunity", "type": "textarea", "key": "investment_opportunity"},
        {"label": "👥 Team Background", "type": "textarea", "key": "team_background"},
        {"label": "📉 Financial Forecast", "type": "textarea", "key": "financial_forecast"},
    ],
}

# Collect User Inputs
st.markdown("<h3 style='color:#b3ac29;'>📝 Provide Your Startup Details</h3>", unsafe_allow_html=True)
user_inputs = {}
for field in fields[doc_type]:
    if field["type"] == "text":
        user_inputs[field["key"]] = st.text_input(field["label"])
    elif field["type"] == "textarea":
        user_inputs[field["key"]] = st.text_area(field["label"])
    elif field["type"] == "number":
        user_inputs[field["key"]] = st.number_input(
            field["label"], min_value=0, value=field.get("default", 0)
        )
    elif field["type"] == "select":
        user_inputs[field["key"]] = st.selectbox(field["label"], field["options"])
    elif field["type"] == "section":
        with st.expander(field["label"]):
            if field["key"] == "market_data":
                user_inputs["target_market"] = st.text_area("🌍 Target Market")
                user_inputs["competitors"] = st.text_area("📊 Competitors")
                user_inputs["market_trends"] = st.text_area("📈 Market Trends")
            elif field["key"] == "financial_data":
                user_inputs["revenue_model"] = st.text_area("💵 Revenue Model")
                user_inputs["cost_structure"] = st.text_area("💰 Cost Structure")
                user_inputs["funding_needed"] = st.number_input("📉 Funding Needed (in USD)", min_value=0)

# AI Settings
st.markdown("<h3 style='color:#b3ac29;'>🎨 Customization</h3>", unsafe_allow_html=True)
response_language = st.selectbox("🌐 Response Language", ["English", "Hindi", "Spanish"], index=0)
response_tone = st.radio(
    "🗣️ Response Tone",
    ["Formal", "Neutral", "Casual", "Professional", "Friendly", "Inspirational", "Serious"],
    horizontal=True,
    index=0  # Default to Formal
)


# Generate Document Button
if st.button("✨ Generate Document"):
    if all(user_inputs.values()):  # Validate all required inputs
        # Build context and prompt
        context = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in user_inputs.items()])
        prompt = craft_prompt(
            query=doc_type,
            document_type=doc_type.lower().replace(" ", "_"),
            language=response_language,
            tone=response_tone.lower(),
        )

        # Spinner and Progress Bar
        with st.spinner("⚙️ Generating your document... Please wait!"):
            progress = st.progress(0)
            for i in range(1, 101):
                time.sleep(0.01)
                progress.progress(i)

        # Query Gemini AI
        doc_content = query_gemini(context, prompt)


        # Save and Display Results
        if doc_content:
            st.session_state["generated_docs"].append({"type": doc_type, "content": doc_content})
            st.markdown("<h3 style='color:#b3ac29;'>📄 Generated Document</h3>", unsafe_allow_html=True)
            st.markdown(f"### {doc_type}", unsafe_allow_html=True)
            st.markdown(doc_content, unsafe_allow_html=True)
            download_link = create_download_link(doc_content, f"{doc_type.replace(' ', '_')}.txt")
            st.markdown(download_link, unsafe_allow_html=True)
        else:
            st.error("❌ Failed to generate the document. Please try again.")
    else:
        st.error("⚠️ Please fill in all the required fields.")

# Display Previously Generated Documents
if st.session_state["generated_docs"]:
    st.markdown("<h3 style='color:#b3ac29;'>📂 Previous Documents</h3>", unsafe_allow_html=True)
    for i, doc in enumerate(st.session_state["generated_docs"]):
        with st.expander(f"📑 {doc['type']} - Document {i + 1}"):
            st.markdown(doc["content"], unsafe_allow_html=True)

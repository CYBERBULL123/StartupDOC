import streamlit as st
from backend.gemini import query_gemini  # Import the Gemini function
from backend.langchain import generate_startup_document  # Import LangChain function

# App Title and Description
st.set_page_config(page_title="Startup Automation Tool", layout="wide")
st.title("🚀 Startup Automation Tool")
st.write("""
A one-stop solution for automating your startup documentation needs. 
Generate Business Plans, Funding Proposals, Pitch Decks, and Investor Materials effortlessly using Gemini AI and LangChain.
""")

# Sidebar for Settings
st.sidebar.header("Settings")
ai_engine = st.sidebar.radio("Choose AI Engine", ["Gemini", "LangChain"], index=1)
response_language = st.sidebar.selectbox("Response Language", ["English", "Hindi", "Spanish"], index=0)
response_tone = st.sidebar.radio("Response Tone", ["Formal", "Neutral", "Casual"], index=0)

# Tabs for Document Generation
tabs = {
    "Business Plan": {
        "fields": [
            {"label": "Business Name", "type": "text", "key": "business_name"},
            {"label": "Market Data", "type": "textarea", "key": "market_data"},
            {"label": "Financial Data", "type": "textarea", "key": "financial_data"},
        ],
        "prompt": "Generate a comprehensive business plan.",
    },
    "Funding Proposal": {
        "fields": [
            {"label": "Business Name", "type": "text", "key": "business_name"},
            {"label": "Investment Opportunity", "type": "textarea", "key": "investment_opportunity"},
            {"label": "Capital Needed (in USD)", "type": "number", "key": "capital_needed", "default": 1000},
        ],
        "prompt": "Generate a funding proposal.",
    },
    "Pitch Deck": {
        "fields": [
            {"label": "Business Name", "type": "text", "key": "business_name"},
            {"label": "Business Idea", "type": "textarea", "key": "business_idea"},
            {"label": "Team Vision", "type": "textarea", "key": "team_vision"},
        ],
        "prompt": "Generate a pitch deck.",
    },
    "Investor Materials": {
        "fields": [
            {"label": "Business Name", "type": "text", "key": "business_name"},
            {"label": "Investment Opportunity", "type": "textarea", "key": "investment_opportunity"},
            {"label": "Team Background", "type": "textarea", "key": "team_background"},
            {"label": "Financial Forecast", "type": "textarea", "key": "financial_forecast"},
        ],
        "prompt": "Generate investor materials.",
    },
}

# Create Tabs
selected_tab = st.selectbox("Choose a Document Type", list(tabs.keys()))
tab_details = tabs[selected_tab]

# Input Form
st.header(f"Generate {selected_tab}")
with st.form(key=f"{selected_tab}_form"):
    user_inputs = {}
    for field in tab_details["fields"]:
        if field["type"] == "text":
            user_inputs[field["key"]] = st.text_input(field["label"])
        elif field["type"] == "textarea":
            user_inputs[field["key"]] = st.text_area(field["label"])
        elif field["type"] == "number":
            user_inputs[field["key"]] = st.number_input(field["label"], min_value=0, value=field.get("default", 0))
    
    submit_button = st.form_submit_button("Generate")

# Document Generation
if submit_button:
    if all(user_inputs.values()):
        # Build the context and prompt
        context = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in user_inputs.items()])
        prompt = tab_details["prompt"]
        
        st.subheader(f"Generated {selected_tab}")
        
        if ai_engine == "Gemini":
            # Use Gemini API
            doc_content = query_gemini(context, prompt)
        else:
            # Use LangChain
            doc_content = generate_startup_document(
                query=selected_tab,
                document_type=selected_tab.lower().replace(" ", "_"),
                language=response_language,
                tone=response_tone.lower()
            )
        
        st.text_area(f"{selected_tab} Content", doc_content, height=300)
    else:
        st.error("Please fill in all the required fields.")

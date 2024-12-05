import streamlit as st
from backend.gemini import query_gemini  # Import the function from your gemini.py script
from backend.langchain import generate_startup_prompt, create_startup_document_chain  # Import LangChain functions

# Streamlit UI for the startup tool
st.title('Startup Automation Tool with Gemini AI and LangChain')

# Create Tabs for different sections
tabs = ['Business Plan', 'Funding Proposal', 'Pitch Deck', 'Investor Materials']
selected_tab = st.selectbox('Select Section', tabs)

# Function to handle generating documents using Gemini
def generate_document_from_gemini(context, prompt):
    response = query_gemini(context, prompt)
    return response

# Function to handle LangChain document generation
def generate_document_from_langchain(query, document_type, language, tone):
    doc_content = create_startup_document_chain(query, document_type, language, tone)
    return doc_content

# Business Plan Section
if selected_tab == "Business Plan":
    with st.form(key='business_plan_form'):
        st.header('Enter Your Startup Information for Business Plan')

        business_name = st.text_input("Business Name")
        market_data = st.text_area("Market Data")
        financial_data = st.text_area("Financial Data")
        
        submit_button = st.form_submit_button("Generate Business Plan")

    if submit_button:
        if business_name and market_data and financial_data:
            input_data = {
                'business_name': business_name,
                'market_data': market_data,
                'financial_data': financial_data
            }
            
            # Context and prompt for the AI model (Gemini or LangChain)
            context = f"Business Name: {business_name}\nMarket Data: {market_data}\nFinancial Data: {financial_data}\n"
            prompt = "Generate a detailed business plan based on the above information."
            
            # Optionally, you can switch between Gemini or LangChain by uncommenting the appropriate block:
            
            # Use Gemini for the response
            # doc_content = generate_document_from_gemini(context, prompt)
            
            # Use LangChain for the response
            doc_content = generate_document_from_langchain(f"Business Plan for {business_name}", "business_plan", "English", "formal")
            
            # Display generated content
            st.subheader("Generated Business Plan:")
            st.text_area("Business Plan", doc_content, height=300)

# Funding Proposal Section
elif selected_tab == "Funding Proposal":
    with st.form(key='funding_proposal_form'):
        st.header('Enter Your Startup Information for Funding Proposal')

        business_name = st.text_input("Business Name")
        investment_opportunity = st.text_area("Investment Opportunity")
        capital_needed = st.number_input("Capital Needed", min_value=1000)
        
        submit_button = st.form_submit_button("Generate Funding Proposal")

    if submit_button:
        if business_name and investment_opportunity and capital_needed:
            input_data = {
                'business_name': business_name,
                'investment_opportunity': investment_opportunity,
                'capital_needed': capital_needed
            }
            
            # Context and prompt for the AI model (Gemini or LangChain)
            context = f"Business Name: {business_name}\nInvestment Opportunity: {investment_opportunity}\nCapital Needed: {capital_needed}\n"
            prompt = "Generate a funding proposal for the above business information."
            
            # Optionally, switch between Gemini or LangChain:
            # doc_content = generate_document_from_gemini(context, prompt)
            doc_content = generate_document_from_langchain(f"Funding Proposal for {business_name}", "funding_proposal", "English", "formal")
            
            # Display generated content
            st.subheader("Generated Funding Proposal:")
            st.text_area("Funding Proposal", doc_content, height=300)

# Pitch Deck Section
elif selected_tab == "Pitch Deck":
    with st.form(key='pitch_deck_form'):
        st.header('Enter Your Startup Information for Pitch Deck')

        business_name = st.text_input("Business Name")
        business_idea = st.text_area("Business Idea")
        team_vision = st.text_area("Team & Vision")
        
        submit_button = st.form_submit_button("Generate Pitch Deck")

    if submit_button:
        if business_name and business_idea and team_vision:
            input_data = {
                'business_name': business_name,
                'business_idea': business_idea,
                'team_vision': team_vision
            }
            
            # Context and prompt for the AI model (Gemini or LangChain)
            context = f"Business Name: {business_name}\nBusiness Idea: {business_idea}\nTeam & Vision: {team_vision}\n"
            prompt = "Generate a pitch deck based on the above information."
            
            # Optionally, switch between Gemini or LangChain:
            # doc_content = generate_document_from_gemini(context, prompt)
            doc_content = generate_document_from_langchain(f"Pitch Deck for {business_name}", "pitch_deck", "English", "formal")
            
            # Display generated content
            st.subheader("Generated Pitch Deck:")
            st.text_area("Pitch Deck", doc_content, height=300)

# Investor Materials Section
elif selected_tab == "Investor Materials":
    with st.form(key='investor_materials_form'):
        st.header('Enter Your Startup Information for Investor Materials')

        business_name = st.text_input("Business Name")
        investment_opportunity = st.text_area("Investment Opportunity")
        team_background = st.text_area("Team Background")
        financial_forecast = st.text_area("Financial Forecast")
        
        submit_button = st.form_submit_button("Generate Investor Materials")

    if submit_button:
        if business_name and investment_opportunity and team_background and financial_forecast:
            input_data = {
                'business_name': business_name,
                'investment_opportunity': investment_opportunity,
                'team_background': team_background,
                'financial_forecast': financial_forecast
            }
            
            # Context and prompt for the AI model (Gemini or LangChain)
            context = f"Business Name: {business_name}\nInvestment Opportunity: {investment_opportunity}\nTeam Background: {team_background}\nFinancial Forecast: {financial_forecast}\n"
            prompt = "Generate investor materials based on the above information."
            
            # Optionally, switch between Gemini or LangChain:
            # doc_content = generate_document_from_gemini(context, prompt)
            doc_content = generate_document_from_langchain(f"Investor Materials for {business_name}", "investor_materials", "English", "formal")
            
            # Display generated content
            st.subheader("Generated Investor Materials:")
            st.text_area("Investor Materials", doc_content, height=300)

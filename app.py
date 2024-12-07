import streamlit as st
from backend.gemini import query_gemini  # Import the Gemini function
from backend.langchain import craft_prompt  # Import LangChain function
import base64
import time


# App Configuration
st.set_page_config(page_title="🚀 Startup Automation Tool", layout="wide", page_icon="🌟")

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Load the CSS file
load_css("ui/style.css")

# Functions to handle main app and project info
def show_main_app():
    st.session_state.show_info = False
    st.rerun()

def show_project_info():
    st.session_state.show_info = True
    st.rerun()


# Function to create a downloadable link
def create_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Document</a>'

# Initialize Session State for Generated Responses and `show_info`
if "generated_docs" not in st.session_state:
    st.session_state["generated_docs"] = []

# Initialize the show_info attribute if it doesn't exist
if "show_info" not in st.session_state:
    st.session_state.show_info = True

if st.session_state.show_info:
    st.markdown("""
        # 🚀 Effortlessly Build Your Startup Docs
        ---------
        
        #### ***🔑 Key Features***
        
        The Startup Automation Tool is here to make your startup journey easier and faster. With just a few clicks, automate important tasks like creating business plans, funding proposals, and pitch decks. Here’s what it can do for you:
        - **Business Plans:** Generate a detailed plan for your startup's future, vision, and growth. 📑
        - **Funding Proposals:** Quickly create documents that attract investors and partners. 💸
        - **Pitch Decks:** Turn your business idea into a compelling presentation for investors. 🎤
        - **Investor Materials:** Craft documents that highlight what matters most to investors. 📈
       
        ----------
        #### ***💡 How It Works***
        
        Our tool is easy to use and walks you through the entire process:
        1. **Enter Your Details:** Share your startup’s goals, market, and vision. 📝
        2. **Choose What You Need:** Select the document you need—whether it's a business plan, funding proposal, or pitch deck. 📄
        3. **Automated Creation:** The tool instantly generates your document based on your input. 🚀
        4. **Customization Options:** You can fine-tune the document to match your style, tone, and audience. 🎨
        5. **Ready to Go:** Download your document in a professional format, ready for presentations or investment meetings. 📥
         
        ------------
        #### ***⚙️ Simple & Smart Technology***
        
        The Startup Automation Tool uses smart technology behind the scenes to ensure your documents are:
        - **Tailored to Your Business:** It understands the unique details of your startup and creates documents that fit your specific needs. 📊
        - **Investor-Ready:** The documents highlight the key information investors care about, making your startup more attractive to potential partners. 💼
        - **Efficient & Fast:** What would normally take hours or days to create, is done in just a few minutes. ⏱️
       
        -------------
        #### ***🌟 Why Choose Our Tool?***
        
        1. **Saves Time:** No need to spend hours writing and formatting documents. Our tool does the hard work for you. ⏳
        2. **Easy to Use:** You don’t need to be a tech expert to use it—just follow simple steps and get the results you need. 🖥️
        3. **High-Quality Results:** Get professional-grade business documents that look polished and impress investors. 💼
        4. **Comprehensive:** Whether you're just starting or preparing to pitch to investors, this tool has everything you need. 📈

        #### ***🔥 Get Started Now!***
        
        Ready to simplify your startup journey? Click below to start generating your business documents today! 🎉
        """)

    if st.button("Click me"):
        show_main_app()

else:
    # App Header
    st.markdown(
    """
    # Startup Automation Tool 🚀
    Streamline your startup journey with AI-powered document generation.
    Create ***Business Plans***, ***Funding Proposals***, ***Pitch Decks***, and ***Investor Materials*** in just a few clicks!
    """
    )

    # Define the mapping of document names to keys for templates
    doc_templates = {
        "business_plan": "Business Plan 🏢",
        "funding_proposal": "Funding Proposal 💼",
        "pitch_deck": "Pitch Deck 🎯",
        "investor_materials": "Investor Materials 📈",
        "technical_documentation": "Technical Documentation 📘",
        "project_proposal": "Project Proposal 🏗️",
        "investment_memorandum": "Investment Memorandum 💡",
        "shareholder_update": "Shareholder Update 📊",
    }

    # Dropdown for Document Type with Emojis
    st.markdown("### 📑 Select the Document Type")
    doc_type = st.selectbox(
        "",
        list(doc_templates.values()),  # Use the values from doc_templates dictionary
        index=0,
    )


    # Function to get the corresponding template key based on the selected document type
    def get_template_key(doc_type):
        for key, value in doc_templates.items():
            if value == doc_type:
                return key
        return None  


    # Input Fields Configuration with Enhanced Data
    fields = {
        "Business Plan 🏢": [
            {"label": "🏢 Business Name", "type": "text", "key": "business_name", "placeholder": "Enter your business name"},
            {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
                "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"], "default": "IT"},
            {"label": "💰 Financial Data", "type": "section", "key": "financial_data"},
            {"label": "🌍 Target Market", "type": "textarea", "key": "target_market", "placeholder": "Describe your target market"},
            {"label": "📊 Competitors", "type": "textarea", "key": "competitors", "placeholder": "Who are your competitors?"},
            {"label": "📈 Market Trends", "type": "textarea", "key": "market_trends", "placeholder": "What are the current market trends?"},
        ],
        "Funding Proposal 💼": [
            {"label": "🏢 Business Name", "type": "text", "key": "business_name", "placeholder": "Enter your business name"},
            {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
                "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"], "default": "IT"},
            {"label": "📈 Investment Opportunity", "type": "textarea", "key": "investment_opportunity", "placeholder": "Describe the investment opportunity"},
            {"label": "💵 Capital Needed (in USD)", "type": "number", "key": "capital_needed", "default": 1000},
            {"label": "📊 Revenue Projections", "type": "textarea", "key": "revenue_projections", "placeholder": "Provide a 3-5 year revenue projection"},
        ],
        "Pitch Deck 🎯": [
            {"label": "🏢 Business Name", "type": "text", "key": "business_name", "placeholder": "Enter your business name"},
            {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
                "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"], "default": "IT"},
            {"label": "💡 Business Idea", "type": "textarea", "key": "business_idea", "placeholder": "What is your business idea?"},
            {"label": "🎯 Team Vision", "type": "textarea", "key": "team_vision", "placeholder": "What is your team's vision for the business?"},
            {"label": "🚀 Market Opportunity", "type": "textarea", "key": "market_opportunity", "placeholder": "What market opportunity are you addressing?"},
        ],
        "Investor Materials 📈": [
            {"label": "🏢 Business Name", "type": "text", "key": "business_name", "placeholder": "Enter your business name"},
            {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
                "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"], "default": "IT"},
            {"label": "📈 Investment Opportunity", "type": "textarea", "key": "investment_opportunity", "placeholder": "Describe the investment opportunity"},
            {"label": "👥 Team Background", "type": "textarea", "key": "team_background", "placeholder": "Describe the background of your team members"},
            {"label": "📉 Financial Forecast", "type": "textarea", "key": "financial_forecast", "placeholder": "Provide your 3-5 year financial forecast"},
        ],
        "Technical Documentation 📘": [
            {"label": "📘 Documentation Title", "type": "text", "key": "doc_title", "placeholder": "Enter the title of your documentation"},
            {"label": "🛠️ Key Features", "type": "textarea", "key": "key_features", "placeholder": "Describe the key features of your product"},
            {"label": "📜 Use Cases", "type": "textarea", "key": "use_cases", "placeholder": "Provide a list of use cases for your product"},
            {"label": "📊 Technical Specifications", "type": "textarea", "key": "technical_specs", "placeholder": "Describe the technical specifications of your product"},
        ],
        "Project Proposal 🏗️": [
            {"label": "🏗️ Project Name", "type": "text", "key": "project_name", "placeholder": "Enter your project name"},
            {"label": "🔎 Project Description", "type": "textarea", "key": "project_description", "placeholder": "Describe your project"},
            {"label": "🎯 Goals and Objectives", "type": "textarea", "key": "goals", "placeholder": "What are your project goals?"},
            {"label": "📆 Timeline", "type": "textarea", "key": "timeline", "placeholder": "Provide the project timeline"},
            {"label": "📊 Market Data", "type": "section", "key": "market_data"},
            {"label": "💵 Capital Needed (in USD)", "type": "number", "key": "capital_needed", "default": 1000},
        ],
        "Investment Memorandum 💡": [
            {"label": "🏢 Business Name", "type": "text", "key": "business_name", "placeholder": "Enter your business name"},
            {"label": "💼 Startup Domain", "type": "select", "key": "startup_domain", 
                "options": ["IT", "EdTech", "Consumer Goods", "FinTech", "Healthcare", "Other"], "default": "IT"},
            {"label": "📈 Investment Highlights", "type": "textarea", "key": "investment_highlights", "placeholder": "Highlight your investment opportunities"},
            {"label": "📊 Market Opportunity", "type": "textarea", "key": "market_opportunity", "placeholder": "Describe the market opportunity"},
            {"label": "📉 Risk Analysis", "type": "textarea", "key": "risk_analysis", "placeholder": "Describe the risks associated with this investment"},
        ],
        "Shareholder Update 📊": [
            {"label": "🏢 Business Name", "type": "text", "key": "business_name", "placeholder": "Enter your business name"},
            {"label": "📊 Business Progress Overview", "type": "textarea", "key": "progress_overview", "placeholder": "Provide an overview of business progress"},
            {"label": "✅ Key Achievements", "type": "textarea", "key": "achievements", "placeholder": "List key achievements"},
            {"label": "🎯 Upcoming Goals", "type": "textarea", "key": "upcoming_goals", "placeholder": "Describe your upcoming goals"},
            {"label": "📉 Challenges", "type": "textarea", "key": "challenges", "placeholder": "List current challenges faced by the business"},
        ],
    }

    fields_to_render = fields.get(doc_type, [])

    # Collect User Inputs
    st.markdown("### 📝 Provide Your Details")
    user_inputs = {}
    for field in fields_to_render:
        if field["type"] == "text":
            user_inputs[field["key"]] = st.text_input(field["label"], placeholder=field.get("placeholder", ""))
        elif field["type"] == "textarea":
            user_inputs[field["key"]] = st.text_area(field["label"], placeholder=field.get("placeholder", ""))
        elif field["type"] == "number":
            user_inputs[field["key"]] = st.number_input(
                field["label"], min_value=0, value=field.get("default", 0)
            )
        elif field["type"] == "select":
            # Ensure that the index is valid by finding the default's position in the options
            default_value = field.get("default", field["options"][0])  # Default to the first option if not specified
            index = field["options"].index(default_value)  # Get index of default value in options
            user_inputs[field["key"]] = st.selectbox(field["label"], field["options"], index=index)
        elif field["type"] == "section":
            with st.expander(field["label"]):
                if field["key"] == "market_data":
                    user_inputs["target_market"] = st.text_area("🌍 Target Market", placeholder="Enter the target market details")
                    user_inputs["competitors"] = st.text_area("📊 Competitors", placeholder="List your competitors")
                    user_inputs["market_trends"] = st.text_area("📈 Market Trends", placeholder="Describe market trends")
                elif field["key"] == "financial_data":
                    user_inputs["revenue_model"] = st.text_area("💵 Revenue Model", placeholder="Describe the revenue model")
                    user_inputs["cost_structure"] = st.text_area("💰 Cost Structure", placeholder="Describe the cost structure")
                    user_inputs["funding_needed"] = st.number_input("📉 Funding Needed (in USD)", min_value=0)


    # AI Settings
    st.markdown("### 🎨 Customization")
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
            doc_key = get_template_key(doc_type)
            
            # Build context and prompt
            context = "\n".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in user_inputs.items()])
            prompt = craft_prompt(
                query=doc_type,
                document_type=doc_key,
                language=response_language,
                tone=response_tone.lower(),
            )

            # Spinner, Countdown, and Progress Bar
            countdown_time = 20  # Simulated countdown time in seconds
            with st.spinner("⚙️ Generating your document... Please wait!"):
                progress = st.progress(0)
                
                for i in range(1, 101):
                    time.sleep(countdown_time / 100)  # Simulate the time taken to generate
                    progress.progress(i)

                # Query Gemini AI
                doc_content = query_gemini(context, prompt)


            # Save and Display Results

            if doc_content:
                st.session_state["generated_docs"].append({"type": doc_type, "content": doc_content})
                st.markdown("### 📄 Generated Document")
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

                # Generate and display the download link for each previously generated document
                previous_download_link = create_download_link(doc["content"], f"{doc['type'].replace(' ', '_')}_Document_{i + 1}.txt")
                st.markdown(previous_download_link, unsafe_allow_html=True)

# Footer Section
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 18px; color: #555;">
        Developed by 🤠 <strong>Aditya Pandey</strong>
    </div>
    """,unsafe_allow_html=True
)

# Social Media Links in Footer
st.markdown(
    """
    <style>
        .footer {
            margin-top: 20px;
            text-align: center;
        }
        .social-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 10px;
        }
        .social-link {
            text-decoration: none;
            font-size: 16px;
            color: #0073e6;
            font-weight: bold;
            border: 2px solid #0073e6;
            border-radius: 5px;
            padding: 5px 10px;
            transition: all 0.3s ease-in-out;
        }
        .social-link:hover {
            background-color: #0073e6;
            color: white;
        }
        .emoji {
            margin-right: 5px;
        }
    </style>
    <div class="footer">
        <div class="social-container">
            <a href="https://www.linkedin.com/in/aditya-pandey-896109224" class="social-link">
                <span class="emoji">🔗</span>LinkedIn
            </a>
            <a href="https://aadi-web-1.onrender.com/" class="social-link">
                <span class="emoji">🌐</span>Website
            </a>
            <a href="https://github.com/CYBERBULL123" class="social-link">
                <span class="emoji">🐙</span>GitHub
            </a>
            <a href="https://cyberbull.medium.com/" class="social-link">
                <span class="emoji">✍️</span>Blog
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True
)

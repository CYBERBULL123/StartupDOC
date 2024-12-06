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
        
        ***🔑 Key Features***
        
        The Startup Automation Tool is here to make your startup journey easier and faster. With just a few clicks, automate important tasks like creating business plans, funding proposals, and pitch decks. Here’s what it can do for you:
        - **Business Plans:** Generate a detailed plan for your startup's future, vision, and growth. 📑
        - **Funding Proposals:** Quickly create documents that attract investors and partners. 💸
        - **Pitch Decks:** Turn your business idea into a compelling presentation for investors. 🎤
        - **Investor Materials:** Craft documents that highlight what matters most to investors. 📈

        ***💡 How It Works***
        
        Our tool is easy to use and walks you through the entire process:
        1. **Enter Your Details:** Share your startup’s goals, market, and vision. 📝
        2. **Choose What You Need:** Select the document you need—whether it's a business plan, funding proposal, or pitch deck. 📄
        3. **Automated Creation:** The tool instantly generates your document based on your input. 🚀
        4. **Customization Options:** You can fine-tune the document to match your style, tone, and audience. 🎨
        5. **Ready to Go:** Download your document in a professional format, ready for presentations or investment meetings. 📥

        ***⚙️ Simple & Smart Technology***
        
        The Startup Automation Tool uses smart technology behind the scenes to ensure your documents are:
        - **Tailored to Your Business:** It understands the unique details of your startup and creates documents that fit your specific needs. 📊
        - **Investor-Ready:** The documents highlight the key information investors care about, making your startup more attractive to potential partners. 💼
        - **Efficient & Fast:** What would normally take hours or days to create, is done in just a few minutes. ⏱️

        ***🌟 Why Choose Our Tool?***
        
        1. **Saves Time:** No need to spend hours writing and formatting documents. Our tool does the hard work for you. ⏳
        2. **Easy to Use:** You don’t need to be a tech expert to use it—just follow simple steps and get the results you need. 🖥️
        3. **High-Quality Results:** Get professional-grade business documents that look polished and impress investors. 💼
        4. **Comprehensive:** Whether you're just starting or preparing to pitch to investors, this tool has everything you need. 📈

        ***🔥 Get Started Now!***
        
        Ready to simplify your startup journey? Click below to start generating your business documents today! 🎉
        """)

    if st.button("Click me"):
        show_main_app()

else:
    # App Header
    st.markdown(
    """
    # Startup Automation Tool
    Streamline your startup journey with AI-powered document generation.
    Create ***Business Plans***, ***Funding Proposals***, ***Pitch Decks***, and ***Investor Materials*** in just a few clicks!
    """
    )

    # Dropdown for Document Type
    st.markdown("### 📑 Select the Document Type")
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
    st.markdown("### 📝 Provide Your Startup Details")
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
                st.success("🚀 Document generated successfully!")
                st.markdown(create_download_link(doc_content, f"{doc_type}_Document.txt"), unsafe_allow_html=True)
            else:
                st.error("❌ Error generating document. Please try again.")
        else:
            st.warning("⚠️ Please fill in all the required fields.")

# Add a footer (optional)
st.markdown("---")
st.write("Developed by 🤠 (Aditya Pandey)")

# Links
linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
website_url = "https://aadi-web-1.onrender.com/"
github_url = "https://github.com/CYBERBULL123"
medium_url = "https://cyberbull.medium.com/"

# Footer with responsive design and fixed at the bottom
st.markdown(
    """
    <style>
    .social-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px; /* Space between items */
        padding: 10px;
    }
    .social-link {
        text-decoration: none;
        font-size: max(18px, 1vw); /* Ensures text stays a good size */
        transition: transform 0.2s ease-in-out;
        color: black; /* Default link color */
    }
    .social-link:hover {
        transform: scale(1.2); /* Hover effect to enlarge */
        color: red; /* Change color on hover */
    }
    .emoji {
        font-size: max(24px, 2vw); /* Ensures emojis remain large enough */
        margin-right: 8px; /* Space between emoji and text */
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
                <span class="emoji">✍️</span>Medium Blog
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True
) 

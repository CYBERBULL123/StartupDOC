from langchain.prompts import PromptTemplate


def generate_prompt_template(document_type, tone):
    """
    Generate a dynamic and optimized prompt template based on document type and tone.

    Args:
        document_type (str): The type of document to generate (e.g., Business Plan, Funding Proposal, etc.).
        tone (str): The tone of the response (Formal, Casual, etc.).

    Returns:
        PromptTemplate: A LangChain prompt template for dynamic LLM inputs.
    """
    # Define tone styles for more nuanced prompt generation
    tone_styles = {
        "Formal": "Adopt a formal, highly professional tone with a focus on structure, precision, and clarity.",
        "Neutral": "Use a neutral tone, ensuring clear and balanced information without emotional bias or excessive detail.",
        "Casual": "Provide a conversational and approachable tone, using simple language while ensuring clarity.",
        "Professional": "Emphasize clear, concise, and structured language with a focus on professionalism and detailed insights.",
        "Friendly": "Adopt a warm, approachable tone that engages readers with simplicity and empathy.",
        "Inspirational": "Use motivating language to evoke enthusiasm and confidence in the reader.",
        "Serious": "Maintain a straightforward, serious tone, conveying critical information with emphasis on logic and results."
    }

    # Document templates with improved structure and effectiveness
    templates = {
        "business_plan": """
            Create a comprehensive business plan with the following sections:
            1. **Executive Summary**: Briefly summarize the company, its mission, and vision. Include key highlights of the business.
            2. **Market Analysis**: Analyze the target market, including key trends, customer needs, and competitor landscape.
            3. **Product/Service Overview**: Describe the product or service, its features, and unique selling points.
            4. **Marketing and Sales Strategies**: Explain how the business plans to attract customers, sales strategies, and marketing channels.
            5. **Financial Projections**: Provide projections for revenue, expenses, profit margins, and break-even analysis.
            6. **Operational Plan**: Outline the daily operations, production methods, and key partnerships.

            **Role**: The business strategist is responsible for ensuring a robust and comprehensive plan with clear data and market insight.
            Ensure clarity, conciseness, and a logical flow throughout the document.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
        "funding_proposal": """
            Draft a compelling funding proposal that includes the following sections:
            1. **Executive Summary**: Provide a high-level overview of the business, including the investment opportunity.
            2. **Problem Statement and Market Opportunity**: Define the problem your product/service solves and outline the market size and demand.
            3. **Proposed Solution/Business Case**: Clearly present your solution and why it is the best option available.
            4. **Funding Requirements and Allocation Plan**: Detail how much funding is needed, how it will be used, and the expected outcomes.
            5. **Financial Projections and Return on Investment (ROI)**: Project the financial performance and explain how investors will benefit.
            6. **Risk Assessment and Mitigation Strategies**: Identify potential risks and outline strategies for mitigating them.

            **Role**: The investment analyst should focus on presenting the funding opportunity clearly, using data-driven insights and strategic rationale to address investor concerns.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
        "pitch_deck": """
            Create a visually compelling and concise pitch deck with the following sections:
            1. **Introduction and Vision**: Start with a brief introduction and your company’s vision.
            2. **Problem and Solution**: Explain the problem you're solving and present your solution clearly.
            3. **Market Opportunity and Competitive Landscape**: Provide insights into the market size, growth, and competitors.
            4. **Business Model and Revenue Streams**: Define how your company will make money and why your model is sustainable.
            5. **Financial Projections and Milestones**: Share your financial projections and key business milestones.
            6. **Ask and Call to Action**: Specify the funding needed and what you are seeking from potential investors.

            **Role**: The presentation designer is responsible for ensuring a visually engaging presentation that resonates with investors.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
        "technical_documentation": """
            Write a comprehensive technical document that covers the following areas:
            1. **System Overview and Architecture**: Provide a high-level description of the system architecture, including components and how they interact.
            2. **Setup and Installation Instructions**: Clearly explain how to set up the system, including dependencies, configuration, and installation steps.
            3. **Features and Functionalities**: Describe the system’s features and how each one works.
            4. **API Documentation (if applicable)**: Provide detailed API endpoints, request/response formats, and usage examples.
            5. **Troubleshooting Guide and FAQs**: List common issues and their solutions, along with frequently asked questions.

            **Role**: The technical writer or engineer should ensure the document is clear, detailed, and accessible for developers and users alike.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
        "project_proposal": """
            Create a comprehensive project proposal with the following sections:
            1. **Executive Summary**: Briefly introduce the project and summarize the expected benefits.
            2. **Project Objectives and Scope**: Clearly outline the project’s goals, objectives, and the scope of work.
            3. **Methodology and Timeline**: Describe the approach, methodology, and timeline for executing the project.
            4. **Budget and Resource Requirements**: Specify the resources, budget, and timelines needed for successful project completion.
            5. **Expected Outcomes and Impact**: Outline the expected outcomes and how they will impact stakeholders and the community.

            **Role**: The project manager or coordinator must ensure the proposal is thorough, with a clear plan for execution, risk management, and alignment to business goals.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
        "investor_materials": """
            Prepare detailed investor materials that include:
            1. **Overview of the Investment Opportunity**: Present an overview of the business opportunity, highlighting key value propositions.
            2. **Market Size and Growth Potential**: Provide a detailed analysis of the market size, trends, and potential for growth.
            3. **Financial Projections and ROI**: Share financial projections, expected returns, and any relevant financial metrics.
            4. **Risk Assessment and Mitigation Strategies**: Address potential risks and outline strategies to mitigate them.
            5. **Key Investment Highlights and Benefits**: Emphasize the key selling points for investors and the benefits they will gain.

            **Role**: The investment consultant or financial analyst must create clear, compelling materials that address investor needs and mitigate concerns.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
        "investment_memorandum": """
            Write a compelling investment memorandum with the following sections:
            1. **Business Overview and Vision**: Introduce the company and its vision for the future.
            2. **Investment Highlights and Unique Selling Proposition (USP)**: Clearly articulate what makes the business unique and why it's a worthwhile investment.
            3. **Market Opportunity and Competitive Advantage**: Define the market opportunity, how the business stands out, and its competitive advantage.
            4. **Financial Metrics and Projections**: Provide detailed financial data, growth projections, and key financial indicators.
            5. **Risk Analysis and Mitigation Plans**: Outline potential risks to the business and how they will be mitigated.

            **Role**: The corporate strategist should focus on creating a convincing, data-driven narrative that positions the company as a viable, high-potential investment.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
        "shareholder_update": """
            Draft a shareholder update document with the following sections:
            1. **Business Performance Overview**: Summarize the company’s performance since the last update, including key metrics.
            2. **Key Achievements and Milestones**: Highlight significant achievements and progress toward goals.
            3. **Financial Performance and Key Metrics**: Provide financial data such as revenue, expenses, and profit margins.
            4. **Upcoming Goals and Future Plans**: Outline the company’s plans and goals for the upcoming quarter/year.
            5. **Risk Assessment and Challenges**: Identify any challenges or risks the company is facing and how they will be addressed.

            **Role**: The executive or communication officer must ensure transparency and keep shareholders informed about the company’s performance and outlook.

            Tone: {tone}
            Query: {query}
            Language: {language}
        """,
    }

    # Fallback to neutral tone style if the specified tone is not found
    tone_style = tone_styles.get(tone, tone_styles["Neutral"])

    # Fetch the template based on document type
    template = templates.get(document_type.lower(), templates["business_plan"])

    return PromptTemplate(
        input_variables=["query", "language", "tone"],
        template=template.strip()
    )


def craft_prompt(query, document_type, language, tone):
    """
    Craft a prompt for the Gemini LLM using LangChain.

    Args:
        query (str): The user's input or topic.
        document_type (str): The type of document (e.g., Business Plan, Funding Proposal).
        language (str): Language for the response.
        tone (str): The tone of the response (e.g., Formal, Casual).

    Returns:
        str: The crafted prompt.
    """
    prompt_template = generate_prompt_template(document_type, tone)
    return prompt_template.format(query=query, language=language, tone=tone)

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain


def generate_prompt_template(document_type, tone):
    """
    Generate a dynamic prompt template based on document type and tone.

    Args:
        document_type (str): The type of document to generate (e.g., Business Plan, Funding Proposal, etc.).
        tone (str): The tone of the response (Formal, Casual, etc.).

    Returns:
        PromptTemplate: A LangChain prompt template for dynamic LLM inputs.
    """
    templates = {
        "business_plan": {
            "neutral": """
                You are a business strategist in {language}. Generate a business plan for the query.
                Tone: {tone}
                Query: {query}
                
                Sections:
                1. Market Analysis
                2. Product/Service Overview
                3. Financial Projections
                Provide detailed insights for each section.
            """,
            "formal": """
                You are an expert business consultant in {language}. Develop a structured business plan.
                Tone: {tone}
                Query: {query}
                
                The plan should include:
                1. Market Research
                2. Competitive Analysis
                3. Financial Metrics
                Make the content professional and data-driven.
            """,
            "casual": """
                You are a creative business consultant in {language}. Create a user-friendly business plan.
                Tone: {tone}
                Query: {query}
                
                Focus on:
                - Market Trends
                - Product/Service Insights
                - Financial Potential
                Use a conversational style.
            """,
        },
        "funding_proposal": {
            "neutral": """
                You are a financial advisor in {language}. Generate a funding proposal for the query.
                Tone: {tone}
                Query: {query}
                
                Include:
                1. Funding Requirements
                2. Use of Funds
                3. ROI Projections
                Make it clear and investor-focused.
            """,
            "formal": """
                You are an experienced finance expert in {language}. Create a detailed funding proposal.
                Tone: {tone}
                Query: {query}
                
                Highlight:
                1. Funding Needs
                2. Investment Returns
                3. Risk Analysis
                Use professional language to engage investors.
            """,
            "casual": """
                You are a startup mentor in {language}. Develop a relaxed yet impactful funding proposal.
                Tone: {tone}
                Query: {query}
                
                Key Points:
                - Why funding is needed
                - How funds will be used
                - Potential for growth and returns
                Use an approachable tone.
            """,
        },
        # Add other document types (pitch_deck, investor_materials, etc.) as needed.
    }

    # Default to neutral tone if specific tone is not found
    document_templates = templates.get(document_type.lower(), templates["business_plan"])
    template = document_templates.get(tone.lower(), document_templates["neutral"])

    return PromptTemplate(
        input_variables=["query", "language", "tone"],
        template=template.strip()
    )


def create_document_chain(llm, document_type, tone="neutral"):
    """
    Create an LLMChain for generating startup documents dynamically.

    Args:
        llm (LLM): The LLM instance for generating content.
        document_type (str): The type of document (e.g., Business Plan, Funding Proposal).
        tone (str): The tone of the response (Formal, Casual, Neutral).

    Returns:
        LLMChain: A LangChain object configured with the dynamic prompt template.
    """
    prompt_template = generate_prompt_template(document_type, tone)
    return LLMChain(llm=llm, prompt=prompt_template)


def generate_startup_document(llm, query, document_type, language, tone):
    """
    Generate a startup-related document based on user inputs.

    Args:
        llm (LLM): The LLM instance for generating content.
        query (str): The user's input or topic.
        document_type (str): Type of document to generate (e.g., Business Plan, Funding Proposal).
        language (str): Language for the response (English, Hindi, etc.).
        tone (str): The tone of the response (Formal, Casual, etc.).

    Returns:
        str: The generated document text.
    """
    chain = create_document_chain(llm, document_type, tone)
    return chain.run(query=query, language=language, tone=tone)


def build_sequential_chain(llm, tasks):
    """
    Build a sequential chain for complex workflows (e.g., generating multiple sections).

    Args:
        llm (LLM): The LLM instance for generating content.
        tasks (list): A list of dictionaries defining tasks (e.g., [{"type": "business_plan", "tone": "formal"}]).

    Returns:
        SimpleSequentialChain: A LangChain object to process tasks sequentially.
    """
    chains = []
    for task in tasks:
        document_type = task.get("type", "business_plan")
        tone = task.get("tone", "neutral")
        chain = create_document_chain(llm, document_type, tone)
        chains.append(chain)

    return SimpleSequentialChain(chains=chains)

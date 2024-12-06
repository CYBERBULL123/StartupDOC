from langchain.prompts import PromptTemplate


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
                Generate a business plan in {language}.
                Tone: {tone}
                Query: {query}
                
                Sections:
                1. Market Analysis
                2. Product/Service Overview
                3. Financial Projections
                Provide detailed insights for each section.
            """,
            "formal": """
                Develop a structured business plan in {language}.
                Tone: {tone}
                Query: {query}
                
                Include:
                1. Market Research
                2. Competitive Analysis
                3. Financial Metrics
                Use professional language and structure.
            """,
            "casual": """
                Create a casual and user-friendly business plan in {language}.
                Tone: {tone}
                Query: {query}
                
                Highlight:
                - Market Trends
                - Product/Service Insights
                - Financial Potential
                Use a conversational style.
            """,
        },
        # Add templates for other document types (e.g., funding_proposal, pitch_deck).
    }

    # Fallback to neutral tone if the specified tone is not found
    document_templates = templates.get(document_type.lower(), templates["business_plan"])
    template = document_templates.get(tone.lower(), document_templates["neutral"])

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

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def generate_startup_prompt(query, document_type, language, tone):
    """
    Generate dynamic prompts for startup automation based on user inputs.
    
    Args:
        query (str): The user input or topic related to the startup.
        document_type (str): Type of document being generated (Business Plan, Funding Proposal, etc.).
        language (str): The language for the response (English, Hindi, etc.).
        tone (str): The tone of the response (Formal, Casual, etc.).
    
    Returns:
        PromptTemplate: The generated prompt template for LLM generation.
    """
    
    # Define template structures for various document types
    document_templates = {
        "business_plan": {
            "neutral": """
                You are a professional business strategist in {language}. 
                Respond to the user's query in a {tone} tone and generate a comprehensive business plan.
                Query: {query}
                The business plan should include sections like Market Analysis, Product/Service Overview, and Financial Projections.
                Provide detailed insights and actionable steps for each section.
            """,
            "formal": """
                You are an experienced business consultant in {language}. 
                Respond in a formal tone and develop a structured business plan based on the provided information.
                Query: {query}
                The business plan should cover all necessary components such as Market Research, Competitive Analysis, Product Overview, and Financial Forecast.
                Include strategic recommendations and long-term objectives.
            """,
            "casual": """
                You are a creative business consultant in {language}. 
                Respond in a friendly, casual tone and help create a detailed yet easy-to-understand business plan.
                Query: {query}
                The business plan should focus on making the content approachable yet insightful. Include market insights, product idea, and financial outlook.
            """
        },
        "funding_proposal": {
            "neutral": """
                You are an expert in business finance in {language}. 
                Respond in a neutral tone to generate a funding proposal for the user's startup.
                Query: {query}
                The proposal should outline the funding requirements, use of funds, and return on investment for potential investors.
                Provide a structured, clear proposal with financial projections and growth potential.
            """,
            "formal": """
                You are a seasoned finance expert in {language}. 
                Respond in a formal tone and generate a comprehensive funding proposal.
                Query: {query}
                The proposal should include detailed financial metrics, funding requirements, ROI projections, and risk analysis.
                Provide precise, formal language that investors can trust.
            """,
            "casual": """
                You are a financial advisor in {language}. 
                Respond in a relaxed and approachable tone to create an engaging funding proposal.
                Query: {query}
                Focus on making the proposal simple yet impactful, highlighting funding needs, the potential for returns, and a roadmap for growth.
            """
        },
        "pitch_deck": {
            "neutral": """
                You are a creative business strategist in {language}. 
                Respond in a neutral tone and develop a compelling pitch deck for the user's startup.
                Query: {query}
                The pitch deck should present the business idea, market opportunity, team overview, and financial forecast.
                Keep the content concise and impactful, focusing on what potential investors would find most compelling.
            """,
            "formal": """
                You are an experienced business presenter in {language}. 
                Respond in a formal tone and create a professional pitch deck.
                Query: {query}
                The pitch deck should include sections on the problem, solution, market analysis, competition, team, and financials.
                Present a clear, polished narrative that convinces investors to take action.
            """,
            "casual": """
                You are an engaging pitch creator in {language}. 
                Respond in a friendly, conversational tone to develop a creative pitch deck.
                Query: {query}
                Make the pitch deck visually appealing and straightforward. Focus on clarity and engagement to impress investors.
            """
        },
        "investor_materials": {
            "neutral": """
                You are an investment consultant in {language}. 
                Respond in a neutral tone to develop detailed investor materials for the user's startup.
                Query: {query}
                The materials should focus on the company's value proposition, team, market potential, and financial forecast. 
                Keep the content balanced and professional, presenting the startup as a great investment opportunity.
            """,
            "formal": """
                You are an investment banker in {language}. 
                Respond in a formal tone and generate highly professional investor materials.
                Query: {query}
                Provide a structured, detailed document that highlights key financial metrics, the startup's growth potential, and risk analysis.
            """,
            "casual": """
                You are a startup advisor in {language}. 
                Respond in a casual, friendly tone to create investor materials.
                Query: {query}
                Focus on simplifying the complex financial and business details in an engaging way. Ensure that potential investors can easily understand the startup's potential.
            """
        }
    }

    # Select the correct template based on document type and tone
    template = document_templates.get(document_type.lower(), document_templates["business_plan"]).get(tone.lower(), document_templates[document_type.lower()]["neutral"])

    # Create the PromptTemplate object with dynamic input variables
    prompt = PromptTemplate(
        input_variables=["query", "language", "tone"],
        template=template.strip()  # Removes extra spaces/lines
    )

    return prompt

def create_startup_document_chain(query, document_type, language, tone, llm):
    """
    Create a chain that generates a document for a startup based on user inputs.
    
    Args:
        query (str): The user's input.
        document_type (str): Type of document to generate (Business Plan, Funding Proposal, etc.).
        language (str): The language of the response (English, Hindi, etc.).
        tone (str): The tone of the response (Formal, Casual, etc.).
        llm (LLM): The LLM instance used to generate content.
    
    Returns:
        str: The generated document.
    """
    
    # Generate the dynamic prompt using the input data
    prompt = generate_startup_prompt(query, document_type, language, tone)

    # Create the chain with the LLM and the generated prompt
    chain = LLMChain(llm=llm, prompt=prompt)

    # Generate the document by running the chain
    generated_document = chain.run(query=query, language=language, tone=tone)

    return generated_document

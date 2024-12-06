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
    tone_styles = {
        "Formal": "Use precise, professional language with a structured format.",
        "Neutral": "Provide clear and balanced information without emotional bias.",
        "Casual": "Use a conversational tone with simple and engaging language.",
        "Professional": "Focus on clarity and professionalism with detailed insights.",
        "Friendly": "Adopt a warm and approachable tone to connect with readers.",
        "Inspirational": "Use motivational language to inspire confidence and action.",
        "Serious": "Convey information in a straightforward and no-nonsense manner."
    }


    templates = {
        "business_plan": {
            "neutral": """
                Generate a comprehensive business plan in {language}.
                Tone: {tone}
                Query: {query}

                Sections to include:
                1. Executive Summary
                2. Market Analysis
                3. Product/Service Overview
                4. Marketing and Sales Strategies
                5. Financial Projections
                6. Operational Plan
                Provide structured and insightful details for each section.
            """,
            "formal": """
                Develop a meticulously structured business plan in {language}.
                Tone: {tone}
                Query: {query}

                Include the following:
                1. Executive Summary
                2. Detailed Market Research and Trends
                3. Competitive Analysis
                4. Product/Service Value Proposition
                5. Financial Metrics and Projections
                6. Organizational Structure and Operational Plan
                Use formal language and ensure a professional structure.
            """,
            "casual": """
                Create an easy-to-understand business plan in {language}.
                Tone: {tone}
                Query: {query}

                Highlight:
                - Overview of the Market and Key Trends
                - Product/Service Features and Benefits
                - Simplified Financial Outlook
                - Practical Sales and Marketing Tips
                Use a conversational and approachable tone.
            """,
        },
        "funding_proposal": {
            "neutral": """
                Draft a detailed funding proposal in {language}.
                Tone: {tone}
                Query: {query}

                Include the following sections:
                1. Executive Summary
                2. Problem Statement
                3. Proposed Solution/Business Case
                4. Funding Requirements
                5. Financial Projections
                6. ROI for Investors
                Provide clear and persuasive content tailored for potential investors.
            """,
            "formal": """
                Create a professionally written funding proposal in {language}.
                Tone: {tone}
                Query: {query}

                Ensure inclusion of:
                1. Concise Executive Summary
                2. Problem and Market Opportunity Analysis
                3. Proposed Solution or Innovation
                4. Detailed Funding Request with Use of Funds
                5. Financial Projections (e.g., ROI, Break-even Analysis)
                6. Competitive Edge and Risk Mitigation
                Maintain a professional tone and provide convincing arguments for funding.
            """,
            "casual": """
                Write a straightforward funding proposal in {language}.
                Tone: {tone}
                Query: {query}

                Cover these points:
                - Brief Overview of the Problem and Solution
                - Funding Needs and Potential Impact
                - Simple Financial Expectations (e.g., expected growth, profits)
                Use a friendly tone that engages non-experts.
            """,
        },
        "pitch_deck": {
            "neutral": """
                Prepare a concise and impactful pitch deck in {language}.
                Tone: {tone}
                Query: {query}

                Slides to include:
                1. Introduction
                2. Problem and Solution
                3. Market Opportunity
                4. Business Model
                5. Competitive Analysis
                6. Financial Highlights
                7. Call to Action
                Use clear and visually engaging content.
            """,
            "formal": """
                Develop a highly professional pitch deck in {language}.
                Tone: {tone}
                Query: {query}

                Include slides for:
                1. Executive Overview
                2. Market Challenges and Strategic Solutions
                3. Target Market and Demographics
                4. Revenue Model and Streams
                5. Financial Metrics (Projections, Profit Margins, etc.)
                6. Competitive Differentiators
                7. Closing with Key Asks and Next Steps
                Maintain clarity and professionalism in content and design.
            """,
            "casual": """
                Design a visually appealing and easy-to-follow pitch deck in {language}.
                Tone: {tone}
                Query: {query}

                Include:
                - Key Problems and Solutions
                - Market Size and Opportunity
                - Revenue Streams in Simple Terms
                - Highlights of Financial Potential
                - Clear Call-to-Action for Investors
                Use a friendly tone and keep it engaging.
            """,
        },
        "technical_documentation": {
            "neutral": """
                Create detailed technical documentation in {language}.
                Tone: {tone}
                Query: {query}

                Sections:
                1. Overview of the Technology/System
                2. Installation and Setup Instructions
                3. Features and Functionalities
                4. API References (if applicable)
                5. Troubleshooting and FAQs
                Ensure clarity and technical accuracy.
            """,
            "formal": """
                Develop comprehensive technical documentation in {language}.
                Tone: {tone}
                Query: {query}

                Include:
                1. Introduction and Scope
                2. System Architecture and Design Overview
                3. Installation/Deployment Steps
                4. Technical Features and Use Cases
                5. Detailed API References or Modules
                6. Maintenance and Troubleshooting Guide
                7. Appendices and Glossary
                Use precise, technical language and a structured format.
            """,
            "casual": """
                Write simple and user-friendly technical documentation in {language}.
                Tone: {tone}
                Query: {query}

                Focus on:
                - What the system/software does
                - How to install and use it
                - Key features explained in plain language
                - Common issues and how to fix them
                Use simple terms for better accessibility.
            """,
        },
        "project_proposal": {
            "neutral": """
                Draft a project proposal in {language}.
                Tone: {tone}
                Query: {query}

                Key sections:
                1. Project Objective
                2. Scope and Deliverables
                3. Methodology and Timeline
                4. Budget and Resource Requirements
                5. Expected Outcomes and Impact
                Ensure clarity and a persuasive structure.
            """,
            "formal": """
                Write a formal project proposal in {language}.
                Tone: {tone}
                Query: {query}

                Structure:
                1. Executive Summary
                2. Objectives and Goals
                3. Approach and Timeline
                4. Budget Breakdown and Resource Allocation
                5. Anticipated Benefits and Impact Analysis
                6. Conclusion and Next Steps
                Keep the tone professional and concise.
            """,
            "casual": """
                Create a simple project proposal in {language}.
                Tone: {tone}
                Query: {query}

                Outline:
                - What is the project and why it matters
                - Key steps to achieve it
                - Budget and time estimates
                - Expected results and benefits
                Use a conversational tone that is easy to follow.
            """,
        },
        "investor_materials": {
            "neutral": """
                Prepare a comprehensive set of investor materials in {language}.
                Tone: {tone}
                Query: {query}

                Include:
                1. Investment Opportunity Overview
                2. Key Metrics (Market Size, Revenue Potential, Growth Rates)
                3. Financial Projections and Returns
                4. Risk Assessment and Mitigation Strategies
                5. Call-to-Action (Investment Ask and Benefits)
                Ensure a balance between detail and readability to engage investors effectively.
            """,
            "formal": """
                Develop a professional set of investor materials in {language}.
                Tone: {tone}
                Query: {query}

                Key sections:
                1. Executive Summary of the Opportunity
                2. Market Opportunity and Strategic Positioning
                3. Financial Projections (Cash Flow, ROI, Exit Strategy)
                4. Competitive Landscape Analysis
                5. Risk Management Framework
                6. Investment Terms and Use of Funds
                Use a structured approach to present a compelling case for investment.
            """,
            "casual": """
                Create an engaging and easy-to-digest set of investor materials in {language}.
                Tone: {tone}
                Query: {query}

                Cover these key points:
                - What makes this opportunity exciting
                - High-level financial outlook (e.g., potential returns)
                - Why now is the right time to invest
                - Any risks and how you plan to handle them
                - Clear investment ask with benefits
                Use an approachable tone that resonates with non-technical audiences.
            """,
        },
        "investment_memorandum": {
            "neutral": """
                Draft an investment memorandum in {language}.
                Tone: {tone}
                Query: {query}

                Structure:
                1. Business Overview
                2. Investment Highlights
                3. Market Opportunity
                4. Financial Performance and Projections
                5. Risk Analysis
                6. Conclusion and Investment Call-to-Action
                Provide concise, well-researched details to appeal to potential investors.
            """,
            "formal": """
                Write a detailed and formal investment memorandum in {language}.
                Tone: {tone}
                Query: {query}

                Include:
                1. Company Background and Vision
                2. Unique Selling Proposition (USP) and Value Creation
                3. Comprehensive Market Analysis
                4. Financial Metrics and Expected Returns
                5. Risks, Assumptions, and Mitigation Plans
                6. Appendix (Supporting Data, Legal Notes)
                Ensure the language is precise, professional, and persuasive.
            """,
            "casual": """
                Create a simple and engaging investment memorandum in {language}.
                Tone: {tone}
                Query: {query}

                Cover:
                - What the company does and why it’s unique
                - Key financial highlights (e.g., revenue potential)
                - Market opportunity in straightforward terms
                - Risks and how they’re being addressed
                - Clear investment benefits
                Use a friendly tone to make it easy to understand.
            """,
        },
        "shareholder_update": {
            "neutral": """
                Prepare a shareholder update document in {language}.
                Tone: {tone}
                Query: {query}

                Suggested sections:
                1. Business Progress Overview
                2. Key Achievements or Milestones
                3. Financial Performance Highlights
                4. Upcoming Goals and Plans
                5. Challenges and Risk Updates
                Maintain clarity and provide actionable insights for stakeholders.
            """,
            "formal": """
                Draft a formal shareholder update in {language}.
                Tone: {tone}
                Query: {query}

                Include:
                1. Summary of Business Activities
                2. Financial Performance (KPIs, Revenue, Expenses)
                3. Strategic Initiatives and Progress
                4. Future Roadmap and Priorities
                5. Risk Assessment and Adjustments
                Use professional and structured language to ensure credibility.
            """,
            "casual": """
                Write a casual shareholder update in {language}.
                Tone: {tone}
                Query: {query}

                Outline:
                - What’s new and exciting in the business
                - Recent achievements in simple terms
                - How the finances are doing (big picture)
                - What’s coming next
                - Any challenges and how they’ll be tackled
                Use an informal, engaging style to connect with stakeholders.
            """,
        },
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

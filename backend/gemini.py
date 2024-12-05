import os
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
import streamlit as st

# Configure API Key
gemini_key = st.secrets["api_keys"]["gemini"]
os.environ["GOOGLE_API_KEY"] = gemini_key
genai.configure(api_key=gemini_key)


# Function to query Gemini model
def query_gemini(context, prompt, image=None):
    """
    Query the Gemini model with a given context and prompt, optionally including an image.

    Args:
        context (str): Context for the prompt.
        prompt (str): User prompt to generate content.
        image (str, optional): Path to an image file for multimodal inputs.

    Returns:
        str: Generated content from the Gemini model or None if an error occurs.
    """
    try:
        # Choose the Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro-latest')

        # Generate content based on whether an image is included
        if image:
            response = model.generate_content([context + prompt, image])
        else:
            response = model.generate_content(context + prompt)

        # Parse response
        if hasattr(response, 'candidates') and response.candidates:
            return ' '.join(part.text for part in response.candidates[0].content.parts)
        else:
            return "Unexpected response format from Gemini API."
    except GoogleAPIError as e:
        return f"An error occurred while querying the Gemini API: {e}"

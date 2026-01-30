from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv()


def llm_model():
    API_KEY=os.getenv("LLM_KEY")
    
    prompt_temp = ChatPromptTemplate.from_template(
        """
    You are a JSON generator.

    Extract the following fields from the visiting card text:
    name, designation,email,phone,company-name,address,website-name.

    Visiting card text:{details}

    STRICT RULES:
    - Output MUST be valid JSON
    - Output MUST start with '{{' and end with '}}'
    - DO NOT include explanations, comments, markdown, or code blocks
    - DO NOT include any text before or after the JSON
    - Phone must be a string (not an array)
    - If a field is missing, use null

    Return JSON only.
    """
    )
    if API_KEY:
        llm=ChatOpenAI(
            model="meta-llama/llama-3-8b-instruct",
            temperature=0,
            openai_api_key=API_KEY,
            openai_api_base="https://openrouter.ai/api/v1"
        )
    else:
        print("api key not found")
    
    model_chain=prompt_temp|llm|StrOutputParser()
    
    return model_chain
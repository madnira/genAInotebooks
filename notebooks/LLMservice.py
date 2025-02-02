import google, googleapiclient
import google.generativeai as genai
import os , jinja2, logging
from dotenv import load_dotenv

# Definign logging configuration
logging.basicConfig(filename='code_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables and API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Function for calling the LLM model
def LLMcall(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    logging.info("LLM response generated")
    return response.text
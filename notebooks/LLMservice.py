# Import all libraries
from flask import Flask , request , jsonify
import google, googleapiclient
import google.generativeai as genai
import os , jinja2, logging
from dotenv import load_dotenv

# Definign logging configuration
logging.basicConfig(filename='code_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Inititating flsak app
app = Flask(__name__)

# Load environment variables and API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Function for calling the LLM model
@app.route("/llmcall", methods=["POST"])
def LLMcall():
    model = genai.GenerativeModel("gemini-1.5-flash")
    data = request.get_json()
    prompt = data.get("prompt")
    response = model.generate_content(prompt)
    logging.info("LLM response generated")
    return jsonify({"response": f"{response.text}"})

# Default healthcheck function

@app.route("/health", methods=["GET"])
def healthcheck():
    return "<p>LLM as aservice is up and running</p>"



if __name__ == '__main__':
    app.run(debug=True, port=5050)
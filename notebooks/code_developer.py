# Import all libraries
from flask import Flask , request , jsonify
import google, googleapiclient
import google.generativeai as genai
import os , jinja2, logging
import requests
from dotenv import load_dotenv
import json

from LLMservice import LLMcall


# Definign logging configuration
logging.basicConfig(filename='code_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Inititating flsak app
app = Flask(__name__)


# Load prompt templates
env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
code_prompt = env.get_template('prompts/coding_prompt.j2')
filename_prompt = env.get_template('prompts/sumarize_filename.j2')

LLMurl = "http://127.0.0.1:5050/llmcall"


# Function for coding
def code(topic, language, code_prompt):
    try:
        if topic is None or language is None:
            logging.error("Either of topic or language is missing")
            return jsonify({"error": "Both topic and language are required"}), 400
        elif language not in ['python', 'java', 'c']:
            logging.error("Language not supported. Supported languages are C, Java and Python only")
            return jsonify({"error": "Language not supported. Supported languages are C, Java and Python only"}), 400
        else:
            logging.info("Code generation started")
            prompt = code_prompt.render(topic=topic, language=language)
            logging.info(f"Code Prompt - {prompt}")
            code_response = LLMcall(prompt)

            #model = genai.GenerativeModel("gemini-1.5-flash")
            #code_response = model.generate_content(prompt)
            logging.info("Code generation completed")
            return code_response

    except Exception as e:
        logging.info(f"An unexpected error occurred: {str(e)}")

# Function for creating filename from topic
def filename(topic, filename_prompt):
    try:
        if topic is None or filename is None:
            logging.error("Topic or Filename is missing")
            return jsonify({"error": "Both topic and filename are required"}), 400
        else:
            logging.info("Filename generation started")
            prompt = filename_prompt.render(topic=topic)
            filename_response = LLMcall(prompt)
            logging.info("Filename generation completed")
            return filename_response.strip()

    except Exception as e:
        logging.info(f"An unexpected error occurred: {str(e)}")

# function for generatig the code
@app.route("/code", methods=["POST"])
def generate_code():
    """
    This function expects to recieve data in a JSON payload in format :
    {
        "topic": "<TOPIC on which the code to be generated>",
        "language": "< programming LANGUAGE with options - C, Java and Python only"
    }
    """
    data = request.get_json()
    topic = data.get("topic")
    language = data.get("language")
    logging.info(f"Received data: {data}")

    try:
        if data is None:
            logging.error("Data is missing")
            return jsonify({"error": "Data is missing"}), 400
        else:
            #code_response = code(topic, language, code_prompt)
            rendered_code_prompt = code_prompt.render(topic=topic, language=language)
            code_payload = {"prompt": rendered_code_prompt}
            code_response_payload = requests.post(LLMurl, json=code_payload)
            
            code_response = code_response_payload.json()["generated_text"]          

            if code_response is None:
                return jsonify({"error": "Code generation failed"}), 500
            else:
                #code_filename = filename(topic, filename_prompt)
                rendered_filename_prompt = filename_prompt.render(topic=topic)
                filename_payload = {"prompt": rendered_filename_prompt}
                code_filename_payload = requests.post(LLMurl, json=filename_payload)
                
                code_filename = code_filename_payload.json()["generated_text"]



                if code_filename is None:
                    return jsonify({"error": "Filename generation failed"}), 500
                

            # Save the file
            output_dir = 'output_files'
            file = os.path.join(output_dir, f"{code_filename}.html") 
            # save in a file
            with open(file, "w") as f:
                f.write(code_response)
                logging.info("File saved successfully")

            return jsonify({"message": "File saved successfully)"})


    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500





# Default healthcheck function
@app.route("/health", methods=["GET"])
def healthcheck():
    return "<p>Code develper app service is Up and running</p>"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Route to serve the index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/isc')
def isc():
    return render_template('isc.html')


# API route to handle chat requests
@app.route('/api', methods=["GET","POST"])
def chat_api():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"response": "Message cannot be empty."}), 400

        # Check if API key is properly loaded
        if not os.getenv('OPENAI_API_KEY'):
            print("API key not found!")
            return jsonify({"response": "API key not configured."}), 500

        # Use OpenAI API to generate a response
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            # Extract the AI's response
            ai_response = response.choices[0].message.content
            return jsonify({"response": ai_response})
        except Exception as api_error:
            print(f"OpenAI API error: {api_error}")
            return jsonify({"response": f"OpenAI API error: {str(api_error)}"}), 500

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"response": f"Server error: {str(e)}"}), 500
    
    

if __name__ == '__main__':
    print("🚀 Starting Flask app...")
    app.run(debug=True)

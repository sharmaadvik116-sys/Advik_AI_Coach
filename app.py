import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env locally.
# On Render, these values will come from Render's
# Environment Variables settings.
load_dotenv()


# --------------------------------------------------
# Flask application
# --------------------------------------------------

app = Flask(__name__)

# Allow the Advik-Olympiad GitHub Pages website
# to communicate with this backend.
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://sharmaadvik116-sys.github.io"
            ]
        }
    }
)


# --------------------------------------------------
# OpenAI configuration
# --------------------------------------------------

api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("REMOTE_SENSING_VECTOR_STORE_ID")


if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not configured."
    )


if not vector_store_id:
    raise RuntimeError(
        "REMOTE_SENSING_VECTOR_STORE_ID is not configured."
    )


client = OpenAI(
    api_key=api_key
)


# --------------------------------------------------
# AI Coach instructions
# --------------------------------------------------

coach_instructions = """
You are Advik's AI Coach for Science Olympiad Remote Sensing.

Your job is to help a middle-school student learn Remote Sensing.

Use the Remote Sensing knowledge base available through file search
whenever it is relevant.

Teaching style:

1. Explain concepts clearly and simply.
2. Use step-by-step reasoning for calculations.
3. Do not immediately give the answer when the student asks
   for a practice question unless they specifically ask for the answer.
4. When the student gives an incorrect answer:
   - clearly say that it is incorrect,
   - explain exactly where the mistake happened,
   - show the correct method,
   - then give a similar practice question.
5. When the student is confused, explain the concept in a simpler way.
6. Remember the conversation so follow-up questions such as
   "what about this one?" or "give me another one" make sense.
7. Encourage the student to try problems independently.
8. Keep explanations appropriate for a middle-school Science Olympiad student.
9. When calculations are involved, show the formula and the steps.
10. Do not claim that information comes from the Science Olympiad
    rules unless the information is actually supported by the
    available knowledge base.
11. If the knowledge base does not contain enough information to
    answer a specialized Remote Sensing question, say so clearly
    rather than inventing a rule or fact.
"""


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(silent=True) or {}


        question = data.get(
            "question",
            ""
        ).strip()


        history = data.get(
            "history",
            []
        )


        if not question:

            return jsonify({
                "error": "Please enter a question."
            }), 400


        # ------------------------------------------
        # Validate conversation history
        # ------------------------------------------

        clean_history = []


        if isinstance(history, list):

            for message in history:

                if not isinstance(message, dict):
                    continue


                role = message.get("role")
                content = message.get("content")


                if role not in ["user", "assistant"]:
                    continue


                if not isinstance(content, str):
                    continue


                content = content.strip()


                if not content:
                    continue


                clean_history.append({
                    "role": role,
                    "content": content
                })


        # ------------------------------------------
        # Add the current question
        # ------------------------------------------

        clean_history.append({
            "role": "user",
            "content": question
        })


        # ------------------------------------------
        # Ask OpenAI
        # ------------------------------------------

        response = client.responses.create(

            model="gpt-5",

            instructions=coach_instructions,

            input=clean_history,

            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [
                        vector_store_id
                    ]
                }
            ]
        )


        answer = response.output_text


        if not answer:

            answer = (
                "I could not generate an answer. "
                "Please try asking the question again."
            )


        return jsonify({
            "answer": answer
        })


    except Exception as error:

        print(
            "AI Coach error:",
            repr(error)
        )


        return jsonify({
            "error": (
                "The AI Coach encountered an error. "
                "Please try again."
            )
        }), 500


# --------------------------------------------------
# Production server
# --------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
import os

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env locally.
# On Render, these values come from Render Environment Variables.
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
vector_store_id = os.getenv(
    "REMOTE_SENSING_VECTOR_STORE_ID"
)


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
# AI Coach base instructions
# --------------------------------------------------

coach_instructions = """
You are Advik's AI Coach for Science Olympiad Remote Sensing.

Your job is to help a middle-school student learn Remote Sensing.

Use the Remote Sensing knowledge base available through file search
whenever it is relevant.

General teaching style:

1. Explain concepts clearly and simply.
2. Use step-by-step reasoning for calculations.
3. Encourage Advik to think through problems independently.
4. When Advik is confused, explain the concept in a simpler way.
5. Remember the conversation so follow-up questions make sense.
6. Keep explanations appropriate for a middle-school Science Olympiad student.
7. When calculations are involved, show the formula and the steps.
8. Do not invent information that is not supported by the available
   Remote Sensing knowledge base.
9. Do not claim that information comes from the Science Olympiad
   rules unless the information is actually supported by the
   available knowledge base.
10. If the knowledge base does not contain enough information to
    answer a specialized Remote Sensing question, say so clearly
    rather than inventing a rule or fact.
"""


# --------------------------------------------------
# Study Mode instructions
# --------------------------------------------------

mode_instructions = {

    "explain": """
STUDY MODE: EXPLAIN

Explain the student's requested Remote Sensing concept clearly.

Use:
- simple language,
- short sections,
- important definitions,
- examples when helpful,
- step-by-step explanations for calculations.

After explaining, ask a short check-for-understanding question
when appropriate.
""",


    "practice": """
STUDY MODE: PRACTICE

Give Advik a Remote Sensing practice problem based on the topic
he asks about.

Do NOT immediately give the answer.

Let Advik attempt the problem first.

If he provides an answer:
- determine whether it is correct,
- explain the reasoning,
- if incorrect, identify the mistake,
- show the correct method,
- then give a similar practice question.
""",


    "quiz": """
STUDY MODE: QUIZ

Act like a Science Olympiad quiz coach.

Give one question at a time.

Do NOT reveal the answer immediately.

Wait for Advik's response.

After he answers:
- tell him whether the answer is correct,
- explain why,
- identify the important concept,
- then provide the next question.

Use a mixture of:
- multiple choice,
- short answer,
- calculations,
- concept questions,

when appropriate to the topic.
""",


    "correct": """
STUDY MODE: CORRECT MY ANSWER

Focus on understanding Advik's mistake.

When Advik provides an answer:
1. State whether the answer is correct or incorrect.
2. Explain exactly where the reasoning went wrong if incorrect.
3. Explain the correct thought process.
4. Show the correct calculation when applicable.
5. Give one similar question so Advik can try again.

Do not simply provide the answer without explaining the reasoning.
""",


    "calculation": """
STUDY MODE: CALCULATION HELP

Help Advik solve Remote Sensing calculations step by step.

Use this structure when appropriate:

1. What information is given?
2. What are we trying to find?
3. What formula should we use?
4. Substitute the values.
5. Calculate the result.
6. Check the units.
7. Explain what the answer means.

Encourage Advik to perform the calculation himself when possible.
""",


    "image": """
STUDY MODE: IMAGE INTERPRETATION

Help Advik practice interpreting Remote Sensing images,
maps, and displays.

Focus on observations such as:
- color,
- brightness,
- patterns,
- texture,
- shape,
- location,
- scale,
- spatial resolution,
- spectral information,
- thermal information,
- radar information,
- elevation information,

when relevant to the available knowledge base.

If an actual image has not been provided, do not pretend that
you can see one. Instead, explain what features Advik should look
for or provide a text-based interpretation practice question.
"""
}


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json(
            silent=True
        ) or {}


        # ------------------------------------------
        # Get current question
        # ------------------------------------------

        question = data.get(
            "question",
            ""
        ).strip()


        # ------------------------------------------
        # Get conversation history
        # ------------------------------------------

        history = data.get(
            "history",
            []
        )


        # ------------------------------------------
        # Get Study Mode
        # ------------------------------------------

        mode = data.get(
            "mode",
            "explain"
        )


        if mode not in mode_instructions:

            mode = "explain"


        # ------------------------------------------
        # Validate question
        # ------------------------------------------

        if not question:

            return jsonify({
                "error": "Please enter a question."
            }), 400


        # ------------------------------------------
        # Validate conversation history
        # ------------------------------------------

        clean_history = []


        if isinstance(
            history,
            list
        ):

            for message in history:

                if not isinstance(
                    message,
                    dict
                ):
                    continue


                role = message.get(
                    "role"
                )


                content = message.get(
                    "content"
                )


                if role not in [
                    "user",
                    "assistant"
                ]:
                    continue


                if not isinstance(
                    content,
                    str
                ):
                    continue


                content = content.strip()


                if not content:
                    continue


                clean_history.append({
                    "role": role,
                    "content": content
                })


        # ------------------------------------------
        # Add current question
        # ------------------------------------------

        clean_history.append({
            "role": "user",
            "content": question
        })


        # ------------------------------------------
        # Combine base instructions
        # with selected Study Mode
        # ------------------------------------------

        selected_mode_instructions = (
            mode_instructions[mode]
        )


        final_instructions = (
            coach_instructions
            + "\n\n"
            + selected_mode_instructions
        )


        # ------------------------------------------
        # Ask OpenAI
        # ------------------------------------------

        response = client.responses.create(

            model="gpt-5",

            instructions=final_instructions,

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


        # ------------------------------------------
        # Get answer
        # ------------------------------------------

        answer = response.output_text


        if not answer:

            answer = (
                "I could not generate an answer. "
                "Please try asking the question again."
            )


        # ------------------------------------------
        # Return answer
        # ------------------------------------------

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
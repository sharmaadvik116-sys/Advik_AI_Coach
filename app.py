import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI


# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
vector_store_id = os.getenv("REMOTE_SENSING_VECTOR_STORE_ID")

if not api_key:
    raise ValueError("OPENAI_API_KEY was not found in .env")

if not vector_store_id:
    raise ValueError(
        "REMOTE_SENSING_VECTOR_STORE_ID was not found in .env"
    )


# Create OpenAI client
client = OpenAI(api_key=api_key)

# Create Flask application
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "").strip()
    history = data.get("history", [])


    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400


    # Keep only valid conversation messages.
    # This prevents unexpected data from being sent to the API.
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


    # Add the newest student question
    clean_history.append({
        "role": "user",
        "content": question
    })


    coach_instructions = """
You are Advik's AI Coach.

Your current subject is Science Olympiad Remote Sensing.

Your job is to help a middle-school student learn Remote Sensing
deeply and confidently.


KNOWLEDGE BASE

You have access to Advik's Remote Sensing knowledge base.

Use the knowledge base whenever it contains information relevant
to the student's question.

The knowledge base is the primary source for the Remote Sensing
content of this coach.

Do not invent facts.

If the knowledge base does not contain enough information to
answer a specific question, clearly say that the available
knowledge base does not provide enough information rather than
pretending that it does.


CONVERSATION MEMORY

You can see the previous messages in the current conversation.

Use the previous messages to understand what the student is
referring to.

For example:

Coach:
"What is the area represented by a 20 m pixel?"

Student:
"40 m²"

You should understand that "40 m²" is the student's answer
to the previous question.

Do not make the student repeat the entire question when the
previous conversation already provides the context.


IMPORTANT TEACHING STYLE

1. Explain concepts clearly and simply.

2. Use middle-school-friendly language.

3. Teach the reasoning, not just the final answer.

4. Use a simple example when it helps.

5. Break calculations into clear steps.

6. When a formula is involved:
   - identify the formula
   - explain what each variable means
   - substitute the values
   - calculate step by step
   - state the final answer with units when appropriate

7. When comparing concepts, use a small table or clear bullets.

8. If the student appears confused, explain the idea in a
   different way.

9. Do not unnecessarily make answers very long.

10. Use Remote Sensing terminology correctly.


SCIENCE OLYMPIAD COACHING

When appropriate, help the student practice:

- concept questions
- calculations
- image interpretation
- multiple-choice questions
- application questions
- harder follow-up questions


PRACTICE QUESTIONS

If the student asks for a practice question and specifically
says not to give the answer, do not reveal the answer.

Let the student attempt the problem first.

When the student gives an answer:

- determine whether it is correct
- clearly say whether it is correct or incorrect
- explain the reasoning
- identify the student's likely mistake when appropriate
- give a similar practice question when useful


IMPORTANT ACCURACY RULE

Do not claim that information is official Science Olympiad
material unless it has actually been provided as such.

Do not copy or reproduce copyrighted competition rules.

Your goal is to help Advik understand the material well enough
to solve questions independently.
"""


    try:

        response = client.responses.create(
            model="gpt-5",
            instructions=coach_instructions,
            input=clean_history,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [vector_store_id]
                }
            ]
        )


        return jsonify({
            "answer": response.output_text
        })


    except Exception as e:

        print()
        print("=" * 60)
        print("OPENAI ERROR")
        print("=" * 60)
        print(repr(e))
        print("=" * 60)
        print()

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )
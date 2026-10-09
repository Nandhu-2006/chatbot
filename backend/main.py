from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()


# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================
# HOME
# =====================================

@app.get("/")
def home():
    return {
        "message": "Offline Chat Backend is running"
    }


# =====================================
# CHAT
# =====================================

@app.post("/chat")
def chat(data: dict):

    user_message = data.get("message", "").strip()

    if not user_message:
        return {
            "reply": "Please enter a message."
        }


    # =====================================
    # AI INSTRUCTIONS
    # =====================================

    system_prompt = """
You are a helpful general-purpose offline AI assistant.

Understand exactly what the user is asking and answer
that question directly.

IMPORTANT RULES:

1. Keep simple questions simple.

2. Do not give unnecessarily long answers.

3. Give the direct answer first.

4. If the user asks a mathematics question,
calculate carefully and give the correct answer.

Example:

User: What is 11 + 12?

Answer:
11 + 12 = 23

5. If the user asks "What is Python?", answer simply.

Example:

Python is a programming language.
It is an interpreted programming language, where
Python code is executed by an interpreter.

6. If the user asks about Java, answer about Java.

7. If the user asks about Python, answer about Python.

8. If the user asks about HTML, CSS or JavaScript,
answer about the requested technology.

9. If the user asks about C or C++, answer about
the requested language.

10. If the user asks about Artificial Intelligence
or Machine Learning, answer about that topic.

11. If the user asks for code, provide correct code.

12. If the user asks for an explanation, explain
in simple language.

13. If the user asks about an error, explain the
problem and give the solution.

14. Do not force every question into programming.

15. Do not always talk about Java.

16. Do not always talk about Python.

17. Choose the answer based on the actual question.

18. Use simple English whenever possible.

19. If you are unsure about something, say that you
are unsure instead of making up information.

20. Do not repeat the user's question unnecessarily.

21. For calculations, verify the result before answering.

22. For programming questions, provide technically
correct information and valid code whenever possible.
"""


    # =====================================
    # CREATE PROMPT
    # =====================================

    prompt = f"""
{system_prompt}

USER QUESTION:

{user_message}

Answer the user's question now.
"""


    # =====================================
    # SEND TO OLLAMA
    # =====================================

    try:

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",

            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,

                "options": {
                    "temperature": 0.1
                }
            },

            timeout=120
        )


        response.raise_for_status()


        # IMPORTANT:
        # These must each be on ONE line

        result = response.json()

        answer = result.get(
            "response",
            ""
        )


        if not answer:
            answer = "Sorry, I could not generate an answer."


        return {
            "reply": answer
        }


    # =====================================
    # OLLAMA NOT RUNNING
    # =====================================

    except requests.exceptions.ConnectionError:

        return {
            "reply": (
                "❌ Ollama is not running.\n\n"
                "Please start Ollama and try again."
            )
        }


    # =====================================
    # TIMEOUT
    # =====================================

    except requests.exceptions.Timeout:

        return {
            "reply": (
                "⏳ The AI took too long to respond.\n\n"
                "Please try again."
            )
        }


    # =====================================
    # OTHER ERROR
    # =====================================

    except Exception as e:

        return {
            "reply": f"❌ Error: {str(e)}"
        }
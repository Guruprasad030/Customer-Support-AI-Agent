import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class CustomerSupportBot:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(history=[])

        self.system_prompt = """
You are a professional AI Customer Support Assistant.

Rules:
- Be polite and professional.
- Answer customer questions clearly.
- If you don't know the answer, say:
  "I'm sorry, I don't have that information. Please contact our support team."
- Never make up information.
- Keep answers concise.
"""

    def ask(self, question):
        try:
            prompt = f"""
{self.system_prompt}

Customer:
{question}

Assistant:
"""

            response = self.chat.send_message(prompt)

            return response.text

        except Exception as e:
            return f"Error: {str(e)}"

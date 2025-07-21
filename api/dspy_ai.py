import dspy
from dotenv import load_dotenv
import google.generativeai as genai
import os
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")
lm = dspy.LM("gemini/gemini-2.5-flash", api_key=api_key)
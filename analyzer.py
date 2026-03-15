from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_logs(logs):

    try:

        # Limit log size to avoid free-tier token limits
        logs = logs[:1500]

        prompt = f"""
You are an expert Site Reliability Engineer.

Analyze the following system logs and provide a structured incident report.

Return the response exactly in this format:

ROOT CAUSE:
(Explain the main issue)

SEVERITY:
Low / Medium / High / Critical

AFFECTED COMPONENT:
Which system component is impacted

RECOMMENDED FIX:
Steps to resolve the issue

INCIDENT SUMMARY:
Short explanation for engineers

Logs:
{logs}
"""

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text
        else:
            return "AI analysis returned an empty response."

    except Exception as e:
        return f"AI analysis failed: {str(e)}"

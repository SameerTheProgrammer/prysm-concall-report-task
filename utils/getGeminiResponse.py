from config.aiModel import client
from constants.index import constants

# Define the prompt template
def build_analyze_concall_report_prompt(transcript: str) -> dict:
    return {
        "system": """
You are a professional financial analyst. Analyze the following earnings conference call transcript and provide structured insights:

1. Summary: Summarize the key points discussed in bullet format.
2. Insights: List important financial, strategic, and operational insights.
3. Risks: Mention any risks, concerns, or red flags raised.
4. Opportunities: Highlight potential areas of future growth or opportunity.
5. Tone Analysis:
   - Sentiment (positive, neutral, negative)
   - Repeated phrases or themes
   - Key focus areas

Respond in a well-structured, readable format with clear section headings.
""",
        "user": f"""Transcript:
\"\"\"
{transcript}
\"\"\"
"""
    }

# Analyze the transcript using AI model
def analyze_concall_report(transcript: str):
    prompt = build_analyze_concall_report_prompt(transcript)
    response = client.chat.completions.create(
        model=constants["AI_MODEL"],
        messages=[
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]}
        ]
    )
    return response.choices[0].message

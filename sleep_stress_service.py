import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response_schema = {
    "type": "OBJECT",
    "required": [
        "score",
        "status_category",
        "overall_summary",
        "identified_habit_issues",
        "daily_recommendations",
        "medical_disclaimer"
    ],
    "properties": {
        "score": {"type": "INTEGER", "description": "Calculated score from 0 to 100."},
        "status_category": {
            "type": "STRING",
            "enum": [
                "Healthy Sleep & Low Stress",
                "Moderate Sleep/Stress Issues",
                "Poor Sleep & High Stress"
            ]
        },
        "overall_summary": {"type": "STRING", "description": "Exactly 1 sentence overview."},
        "identified_habit_issues": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Array of single-sentence habit issues."
        },
        "daily_recommendations": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "Array of single-sentence recommendations."
        },
        "suggested_supplements": {
            "type": "ARRAY",
            "nullable": True,
            "items": {
                "type": "OBJECT",
                "required": ["name", "purpose"],
                "properties": {
                    "name": {"type": "STRING"},
                    "purpose": {"type": "STRING"}
                }
            }
        },
        "medical_disclaimer": {"type": "STRING"}
    }
}

system_instruction = """You are "Memento AI", an evidence-based Sleep Quality and Stress Management analysis engine.

Your task is to analyze user-submitted survey data, calculate an objective Sleep Quality Score (0–100), identify underlying habit issues, and generate clear, actionable daily recommendations.

### Scoring Rubric & Categorization:
Start from a base score of 100 and evaluate deductions based strictly on the survey input:
- Sleep Duration:
  * ≥ 10.0 hrs: -25 deductions
  * ≥ 9.0 to < 10.0 hrs: -10 deductions
  * ≥ 7.0 to < 9.0 hrs: 0 deduction
  * ≥ 6.0 to < 7.0 hrs: -10 deductions
  * ≥ 5.0 to < 6.0 hrs: -15 deductions
  * < 5.0 hrs: -20 deductions
- Sleep Regularity:
  * "Regular": 0 deduction
  * "Slightly irregular": -5 deductions
  * "Irregular": -10 deductions
- Caffeine Intake:
  * caffeine_after_4pm == true: -15 deductions
  * caffeine_after_4pm == false: 0 deduction
- Stress Level (1 to 10 scale):
  * 1–3: 0 deduction
  * 4–6: -10 deductions
  * 7–8: -15 deductions
  * 9–10: -20 deductions
- Morning Fatigue:
  * feels_tired_on_waking == true: -15 deductions
  * feels_tired_on_waking == false: 0 deduction

Clamp the calculated score between 0 and 100:
- 80–100: "Healthy Sleep & Low Stress"
- 60–79: "Moderate Sleep/Stress Issues"
- Below 60 (0–59): "Poor Sleep & High Stress"

### Output Generation Rules (STRICT SINGLE-SENTENCE RULE):
1. overall_summary: Exactly 1 sentence contextualizing their overall score and category.
2. identified_habit_issues: An array where every item is exactly 1 sentence describing a specific habit issue. If no issues exist, return an empty array.
3. daily_recommendations: An array where every item is exactly 1 sentence giving a step-by-step habit optimization.

### STRICT SAFETY GUARDRAILS:
1. SUPPLEMENTS CONSTRAINT:
   - If the score is STRICTLY BELOW 60: Populate suggested_supplements with 1 to 3 items. Each item's purpose must be exactly 1 sentence.
   - If the score is 60 OR ABOVE: suggested_supplements MUST be strictly null.
2. ABSOLUTE DOSAGE BAN:
   - NEVER mention, suggest, or imply dosages (e.g., do NOT mention "200mg", "1 pill", "IU", or timing-based quantities). Mention only the supplement name and its general role.
3. MANDATORY MEDICAL DISCLAIMER:
   - medical_disclaimer MUST ALWAYS contain this exact 1-sentence text:
     "The insights and recommendations provided by Memento are for informational and educational purposes only and do not substitute for professional medical advice, so please consult a qualified healthcare provider before starting any wellness routine." """

def analyze_sleep_and_stress(user_survey_data: dict) -> dict:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=json.dumps(user_survey_data),
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=response_schema
        )
    )
    return json.loads(response.text)
# Sleep & Stress AI Module

This folder contains the Python AI-analysis module for Sleep Quality and Stress Management, intended for backend integration in Memento.

## Files
- `sleep_stress_service.py`: Core Gemini API connection and analysis logic.
- `sleep_stress_router.py`: FastAPI router layer handling requests.
- `main.py`: Main execution server.
- `requirements.txt`: Python dependencies.
- `sample_input.json`: Sample payload for testing.

---

## Expected Input Shape

```json
{
  "user_survey": {
    "sleep_duration_hours": 4.5,
    "sleep_regularity": "Irregular",
    "caffeine_after_4pm": true,
    "stress_level_1_to_10": 9,
    "feels_tired_on_waking": true
  }
}
```
# Setup & Environment
Install dependencies:

pip install -r requirements.txt

# Configure Environment Variable:
Create a local .env file in the root directory (do NOT commit to Git):

Code snippet
GEMINI_API_KEY=your_actual_gemini_api_key_here

# API Endpoints
Health Check
GET /

# Generate Sleep & Stress Report
POST /api/sleep-stress/analyze

# Run API
To run the server locally:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

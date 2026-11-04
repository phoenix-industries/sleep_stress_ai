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

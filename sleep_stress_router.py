from fastapi import APIRouter, HTTPException, Body
from services.sleep_stress_service import analyze_sleep_and_stress

router = APIRouter(prefix="/api/sleep-stress", tags=["Sleep & Stress Analysis"])

@router.post("/analyze")
async def analyze_survey(payload: dict = Body(...)):
    try:
        survey_data = payload.get("user_survey", payload)
        
        if not survey_data or not isinstance(survey_data, dict):
            raise HTTPException(status_code=400, detail="Invalid survey payload provided.")
        
        analysis_result = analyze_sleep_and_stress(survey_data)
        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Analysis Error: {str(e)}")
# ai_care_gap.py - AI service for care gap identification
from typing import List, Dict
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# Import our dependencies
from .main import get_current_active_user, User
from .care_coordination import CareActivity

# Define router
router = APIRouter()

# Load our pre-trained model (placeholder - you'll need to train this)
try:
    model = joblib.load('care_gap_model.pkl')
except:
    # Placeholder model - replace with actual trained model
    model = IsolationForest(n_estimators=100, contamination=0.01)
    model.fit(np.random.randn(100, 5))  # Random data for placeholder

# Data model for AI analysis request
class CareGapAnalysisRequest(BaseModel):
    patient_id: str
    care_history: List[CareActivity]
    patient_demographics: Dict
    current_medications: List[str]

# Analyze care gaps using AI
@router.post("/analyze-care-gaps")
async def analyze_care_gaps(request: CareGapAnalysisRequest,
                           current_user: User = Depends(get_current_active_user)):
    # Check permissions
    if current_user.role not in ["care_coordinator", "provider", "ai_service"]:
        raise HTTPException(status_code=403, detail="Not authorized to perform analysis")
    
    # Extract features from care history
    features = []
    for activity in request.care_history:
        features.append([
            1 if activity.status == "completed" else 0,
            (datetime.now() - activity.due_date).days,
            1 if activity.assignee else 0,
            len(activity.description),
            1 if activity.title.lower().find("follow-up") != -1 else 0
        ])
    
    # If no features, return empty
    if not features:
        return {"gaps": [], "recommendations": []}
    
    # Convert to numpy array
    X = np.array(features)
    
    # Analyze with our model
    anomalies = model.predict(X)
    
    # Identify care gaps
    care_gaps = []
    recommendations = []
    for i, anomaly in enumerate(anomalies):
        if anomaly == -1:  # -1 indicates anomaly in Isolation Forest
            activity = request.care_history[i]
            care_gaps.append({
                "activity_id": activity.id,
                "title": activity.title,
                "status": activity.status,
                "due_date": activity.due_date,
                "days_overdue": (datetime.now() - activity.due_date).days
            })
            
            # Generate recommendation based on activity type
            if "follow-up" in activity.title.lower():
                recommendations.append(f"Schedule follow-up for {activity.title}")
            elif "medication" in activity.title.lower():
                recommendations.append(f"Review medication regimen for {activity.title}")
            else:
                recommendations.append(f"Address unresolved {activity.title}")
    
    # Add demographic-based recommendations
    if request.patient_demographics.get("age", 0) > 65:
        recommendations.append("Consider geriatric care coordination")
    
    if "hypertension" in request.current_medications:
        recommendations.append("Monitor blood pressure regularly")
    
    return {
        "patient_id": request.patient_id,
        "care_gaps": care_gaps,
        "recommendations": list(set(recommendations)),  # Remove duplicates
        "analysis_date": datetime.now()
    }
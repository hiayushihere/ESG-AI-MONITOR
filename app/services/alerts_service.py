from app.models.models import DailyMetric

def get_risk_status(company_id):
    # Fetch last 2 metrics to compare
    recent = DailyMetric.query.filter_by(company_id=company_id).order_by(DailyMetric.date.desc()).limit(2).all()
    
    if not recent:
        return {"level": "Stable", "message": "No risk data available.", "color": "#64748B"}

    current = recent[0]
    
    # If we have a previous day, calculate the spike
    if len(recent) > 1:
        prev = recent[1]
        spike = current.risk_score - prev.risk_score
        if spike > 25:
            return {"level": "CRITICAL", "message": f"Risk surged by {int(spike)} pts!", "color": "#E11D48"}

    # Absolute thresholds
    if current.risk_score > 70:
        return {"level": "HIGH RISK", "message": "Negative sentiment dominating.", "color": "#E11D48"}
    elif current.risk_score > 40:
        return {"level": "ELEVATED", "message": "Increased negative signals.", "color": "#D97706"}
    
    return {"level": "STABLE", "message": "Normal market sentiment.", "color": "#10B981"}
from ..ai_service import generate_recommendation
from ..models import Recommendation

def create_recommendation(db, user_id, planner, request_data, image_path=None):
    result = generate_recommendation(planner, request_data, image_path)
    row = Recommendation(
        user_id=user_id, planner=planner, budget=float(request_data["budget"]),
        request_json=request_data, result_json=result
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, **result}

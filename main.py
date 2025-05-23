from fastapi import FastAPI, HTTPException
from src.models.schemas import *
from src.services.velocity_service import compare_with_last_session
from src.services.cluster_service import categorize_clusters
from src.services.scoring_service import evaluate_session

app = FastAPI()

@app.get("/health")
def basic_health_check():
    return {
        "status": "ok",
        "message": "API funcionando"
    }

@app.post("/velocity/compare-last")
def velocity_endpoint(new_session: SessionInput):
    try:
        result = compare_with_last_session(new_session)
        return {"status": "ok", "message": "Comparison successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cluster/categorize")
def cluster_endpoint(user_id: int):
    try:
        print(user_id)
        result = categorize_clusters(user_id)
        return {
            "status": "ok",
            "message": "Clustering successful",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/geo/score-val")
def scoring_endpoint(payload: ScoreRequest):
    try:
        result = evaluate_session(payload.session, payload.zones)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ATS Resume Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # for local dev; later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ATSRequest(BaseModel):
    job_description: str
    resume_text: str

class ATSResponse(BaseModel):
    score: int
    matched_keywords: list[str]
    missing_keywords: list[str]

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/ats-score", response_model=ATSResponse)
def ats_score(payload: ATSRequest):
    jd_words = set(
        w.lower() for w in payload.job_description.split() if len(w) > 2
    )
    resume_words = set(
        w.lower() for w in payload.resume_text.split() if len(w) > 2
    )

    matched = sorted(jd_words & resume_words)
    missing = sorted(jd_words - resume_words)

    score = 0
    if jd_words:
        score = round(len(matched) / len(jd_words) * 100)

    return ATSResponse(
        score=score,
        matched_keywords=matched,
        missing_keywords=missing,
    )

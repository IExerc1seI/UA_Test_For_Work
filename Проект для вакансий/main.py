from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
import uvicorn
from fastapi.responses import RedirectResponse
from schemas import JobSearchRequest 


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Job Aggregator API")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/jobs", response_model=list[schemas.WorkInDB])
def get_jobs(
    skip: int = Query(0, ge=0, description="Скільки записів пропустити"),
    limit: int = Query(10, ge=1, le=1000, description="Скільки записів повернути"),
    db: Session = Depends(get_db)
):
    job = db.query(models.Work).offset(skip).limit(limit).all()
    return job

@app.get("/jobs/{id}", response_model=schemas.WorkInDB)
def get_id_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Work).filter(models.Work.id == job_id).first()  
    if job is None:
        raise HTTPException(status_code=404, detail="Car not found")  
    return job

@app.post("/job/search", response_model=list[schemas.WorkInDB])
def search_jobs(payload: JobSearchRequest, db: Session = Depends(get_db)):
    query = db.query(models.Work)

    if payload.keyword:
        keyword = f"%{payload.keyword.lower()}%"
        query = query.filter(
            models.Work.title.ilike(keyword) | 
            models.Work.description.ilike(keyword)
        )

    if payload.City:
        query = query.filter(models.Work.City.ilike(f"%{payload.City}%"))

    if payload.Work_name:
        query = query.filter(models.Work.Work_name.ilike(f"%{payload.Work_name}%"))

    if payload.Salary:
        query = query.filter(models.Work.Salary <= payload.Salary)

    return query.all()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    
from fastapi import FastAPI
from pydantic import BaseModel
from retrival.retrieve import RetrivalPhase
from client.rqqueue import queue

app = FastAPI()

class User(BaseModel):
    query:str

@app.get('/')
def Home():
    return "Welcome from home"


@app.post("/userQuery")

def UserQuery(user:User):
  Query=user.query

  #job = queue.enqueue(RetrivalPhase , Query)
  return RetrivalPhase(Query=Query)


@app.get('/job/{job_id}')
def get_result(job_id: str):
    job = queue.fetch_job(job_id)
    if job is None:
        return {"job_id": job_id, "error": "Job not found"}

    job.refresh()  # fetch latest status/result

    if job.is_finished:
        return {"job_id": job_id, "status": "finished", "result": job.result}

    if job.is_failed:
        return {"job_id": job_id, "status": "failed", "error": job.exc_info}

    return {"job_id": job_id, "status": "processing"}



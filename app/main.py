from fastapi import FastAPI
from app.router import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=f"Daily Diet planner API",
    version="v1"
)

app.include_router(router, prefix=f"/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return {"message": f"Welcome to Daily Diet planner APIs."}
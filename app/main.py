from fastapi import FastAPI
from app.routes import github, slack

app = FastAPI()

app.include_router(github.router)
app.include_router(slack.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI project!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
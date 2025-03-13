from fastapi import FastAPI
from app.routes import github, slack
from fastapi.middleware.cors import CORSMiddleware  # 추가된 임포트


app = FastAPI()

# 🚀 CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 모든 도메인 허용 (보안 필요 시 특정 도메인으로 제한)
    allow_credentials=True,
    allow_methods=["*"],  # 🔥 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 🔥 모든 헤더 허용
)



app.include_router(github.router)
app.include_router(slack.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI project!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
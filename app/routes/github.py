# app/routes/github.py
import logging  # 로깅 모듈 추가
from fastapi import APIRouter, Request
from app.services.slack_service import send_slack_message

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/github")
async def github_webhook(request: Request):
    data = await request.json()
    
    logger.info("Received GitHub webhook data: %s", data)  # 수신된 데이터 로깅

    if data.get("action") == "opened":
        pr_title = data["pull_request"]["title"]
        pr_url = data["pull_request"]["html_url"]
        pr_author = data["pull_request"]["user"]["login"]

        logger.info("Processing PR: %s by %s", pr_title, pr_author)  # PR 처리 로깅

        # Slack 메시지 전송
        await send_slack_message(pr_title, pr_url, pr_author)

    return {"message": "Received"}
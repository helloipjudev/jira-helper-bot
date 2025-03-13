# app/routes/github.py
from fastapi import APIRouter, Request
from app.services.slack_service import send_slack_message

router = APIRouter()

@router.post("/github")
async def github_webhook(request: Request):
    data = await request.json()

    if data.get("action") == "opened":
        pr_title = data["pull_request"]["title"]
        pr_url = data["pull_request"]["html_url"]
        pr_author = data["pull_request"]["user"]["login"]

        # Slack 메시지 전송
        await send_slack_message(pr_title, pr_url, pr_author)

    return {"message": "Received"}
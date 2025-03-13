import httpx
from app.config import SLACK_WEBHOOK_URL

async def send_slack_message(pr_title: str, pr_url: str, pr_author: str):
    payload = {
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"📢 *새로운 PR이 생성되었습니다!*"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f"🔗 *PR 제목:* {pr_title}\n👤 *작성자:* {pr_author}\n🔗 *PR 링크:* <{pr_url}>" }},
            {"type": "actions", "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "헬로입주 티켓 생성"},
                    "action_id": "create_jira_ticket",
                    "value": f"{pr_title}||{pr_url}||{pr_author}||IPJU",
                    "url": "https://port-0-jira-helper-bot-1272llx1jee5l.sel5.cloudtype.app/jira/create-ticket"  # 👈 FastAPI 엔드포인트로 요청 보내기
                },
                {
                "type": "button",
                "text": {"type": "plain_text", "text": "파트너스 티켓 생성"},
                "action_id": "create_jira_ticket",
                "value": f"{pr_title}||{pr_url}||{pr_author}||PTN",
                "url": "https://port-0-jira-helper-bot-1272llx1jee5l.sel5.cloudtype.app/jira/create-ticket"
                }
            ]}
        ]
    }
    async with httpx.AsyncClient() as client:
        await client.post(SLACK_WEBHOOK_URL, json=payload)



        
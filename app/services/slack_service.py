import requests
import json
import os
from config import settings 
import logging  # 로깅 모듈 추가

# 로깅 설정
logging.basicConfig(level=logging.INFO)  # 로그 레벨 설정
logger = logging.getLogger(__name__)  # 로거 인스턴스 생성

print()

async def send_slack_message(pr_title: str, pr_author: str, pr_url: str):
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "📢 *새로운 PR이 생성되었습니다!*"}
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"🔗 *PR 제목:* {pr_title}\n👤 *작성자:* {pr_author}\n🔗 *PR 링크:* <{pr_url}>"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "헬로입주 티켓 생성"},
                        "style": "primary",
                        "action_id": "create_jira_ticket_helloipju",
                        "value": f"{pr_title}||{pr_url}||{pr_author}||IPJU",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "파트너스 티켓 생성"},
                        "style": "danger",
                        "action_id": "create_jira_ticket_partners",
                        "value": f"{pr_title}||{pr_url}||{pr_author}||PTN",
                    }
                ]
            }
        ]
    }
    logger.info(f"🚀  {settings.SLACK_WEBHOOK_URL}")
    response = requests.post(settings.SLACK_WEBHOOK_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Slack 메시지 전송 성공!")
    else:
        print(f"❌ Slack 메시지 전송 실패! 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")

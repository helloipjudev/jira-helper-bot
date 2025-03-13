import requests
import json
import os
from dotenv import load_dotenv



load_dotenv()  # .env 파일 로드

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_message(pr_title: str, pr_author: str, pr_url: str):
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
                        "url": "https://port-0-jira-helper-bot-1272llx1jee5l.sel5.cloudtype.app/jira/create-ticket"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "파트너스 티켓 생성"},
                        "style": "danger",
                        "action_id": "create_jira_ticket_partners",
                        "value": f"{pr_title}||{pr_url}||{pr_author}||PTN",
                        "url": "https://port-0-jira-helper-bot-1272llx1jee5l.sel5.cloudtype.app/jira/create-ticket"
                    }
                ]
            }
        ]
    }

    response = requests.post("SLACK_WEBHOOK_URL", headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Slack 메시지 전송 성공!")
    else:
        print(f"❌ Slack 메시지 전송 실패! 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")

# 테스트 실행
if __name__ == "__main__":
    send_slack_pr_notification(
        pr_title="🚀 새 기능 추가: AI 챗봇 업그레이드",
        pr_author="PotatoArtie",
        pr_url="https://github.com/helloipjudev/apis/pull/725"
    )
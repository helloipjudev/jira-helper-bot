import httpx
import logging
import base64
from app.config import JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Basic Auth 헤더 생성
def get_jira_auth_header():
    auth_string = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    return {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }

# JIRA 티켓 생성 함수
async def create_jira_ticket(title: str, description: str, project_key: str):
    if not JIRA_DOMAIN:
        raise ValueError("JIRA_DOMAIN이 설정되지 않았습니다!")

    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
    headers = get_jira_auth_header()

    # 📌 JIRA API에서 요구하는 올바른 `description` 형식 적용
    description_content = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": description
                    }
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": title,
            "description": description_content,
            "issuetype": {"name": "Task"}
        }
    }

    logger.info(f"Jira API 요청 시작: {url}")
    logger.info(f"요청 Payload: {payload}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            jira_key = response.json().get("key")
            logger.info(f"Jira 티켓 생성 성공: {jira_key}")
            return jira_key
        else:
            logger.error(f"Jira 티켓 생성 실패! 상태 코드: {response.status_code}, 응답: {response.text}")
            raise Exception(f"Jira API 요청 실패: {response.text}")
    except httpx.ConnectError:
        logger.error("JIRA 서버에 연결할 수 없습니다. JIRA_DOMAIN 값을 확인하세요!")
        raise Exception("JIRA 서버 연결 실패! JIRA_DOMAIN 확인 필요")
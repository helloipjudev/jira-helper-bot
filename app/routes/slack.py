from fastapi import APIRouter, Request, Form
import json
from app.services.jira_service import create_jira_ticket
from app.services.slack_service import send_slack_message

router = APIRouter()


@router.post("/jira/create-ticket")
async def create_ticket(request: Request, payload: str = Form(...)):
    """Slack에서 버튼 클릭 시 JIRA 티켓을 생성하는 API"""

    data = json.loads(payload)

    # 📌 버튼 클릭 데이터 확인
    if "actions" in data:
        action = data["actions"][0]  # 첫 번째 액션을 가져옴

        if action["action_id"] == "create_jira_ticket":
            # 📌 버튼 value에서 데이터 추출 (title, pr_url, assignee)
            pr_data = action["value"].split("||")
            pr_title = pr_data[0]   # 제목
            pr_url = pr_data[1]     # PR 링크
            assignee = pr_data[2]   # 작성자 (Assignee)

            # 📌 JIRA 티켓 생성 API 호출
            jira_ticket_id = await create_jira_ticket(
                title=pr_title, 
                description=f"PR URL: {pr_url}",
                project_key={pr_data[3]},
                assignee=assignee  # 👈 Assignee 자동 등록
            )

            return {"message": f"✅ JIRA 티켓 생성 완료: {jira_ticket_id}"}

    return {"message": "✅ Slack 버튼 클릭 처리 완료"}
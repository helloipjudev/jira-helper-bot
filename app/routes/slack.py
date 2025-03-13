from fastapi import APIRouter, Request, Form
import json
from app.services.jira_service import create_jira_ticket
from app.services.slack_service import send_slack_message

router = APIRouter()

@router.post("/jira/create-ticket")
async def create_ticket(title: str, description: str, project_key: str):
    jira_ticket_id = await create_jira_ticket(title, description, project_key)
    
    if jira_ticket_id:
        return {"message": "Jira 티켓이 성공적으로 생성되었습니다!", "jira_ticket_id": jira_ticket_id}
    else:
        return {"error": "Jira 티켓 생성 실패"}
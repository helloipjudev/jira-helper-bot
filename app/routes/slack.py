from fastapi import APIRouter, Request, Form, Depends
import json
from app.services.jira_service import create_jira_ticket
import logging  # 로깅 모듈 추가

# 로깅 설정
logging.basicConfig(level=logging.INFO)  # 로그 레벨 설정
logger = logging.getLogger(__name__)  # 로거 인스턴스 생성

router = APIRouter()

@router.post("/jira/create-ticket")
async def create_ticket(request: Request):
    """Slack에서 버튼 클릭 시 JIRA 티켓을 생성하는 API"""

    logger.info("🔄 JIRA 티켓 생성 요청 시작")  # 요청 시작 로깅

    try:
        # 📌 Slack에서 보낸 요청 데이터 확인
        if request.headers.get("content-type") == "application/json":
            data = await request.json()  # JSON 요청 처리
        else:
            form_data = await request.form()  # Form 요청 처리
            payload = form_data.get("payload")
            data = json.loads(payload) if payload else {}

        logger.info("📌 Slack 버튼 클릭 데이터: %s", json.dumps(data, indent=2))  # 로그 출력

        # 📌 버튼 클릭 데이터 확인
        if "actions" in data:
            action = data["actions"][0]  # 첫 번째 액션을 가져옴
            logger.info("📌 버튼 클릭: %s", action)  # 로그 출력

            if action["action_id"] in ["create_jira_ticket_helloipju", "create_jira_ticket_partners"]:
                pr_data = action["value"].split("||")
                pr_title = pr_data[0]   # 제목
                pr_url = pr_data[1]     # PR 링크
                assignee = pr_data[2]   # 작성자
                project_key = pr_data[3]  # 프로젝트 키 (IPJU 또는 PTN)

                logger.info("🔹 PR 제목: %s, 🔗 PR 링크: %s, 👤 담당자: %s, 📌 프로젝트: %s", 
                            pr_title, pr_url, assignee, project_key)  # 로그 출력

                # 📌 JIRA 티켓 생성 API 호출
                jira_ticket_id = await create_jira_ticket(
                    title=pr_title, 
                    description=f"PR URL: {pr_url}",
                    project_key=project_key,
                    assignee=assignee  
                )

                logger.info("✅ JIRA 티켓 생성 완료: %s", jira_ticket_id)  # 티켓 생성 완료 로깅
                return {"message": f"✅ JIRA 티켓 생성 완료: {jira_ticket_id}"}

        return {"message": "⚠️ 잘못된 요청입니다."}

    except Exception as e:
        logger.error("❌ JIRA 생성 중 오류 발생: %s", str(e))  # 오류 로그 출력
        return {"error": "JIRA 티켓 생성 실패", "detail": str(e)}

    finally:
        logger.info("🔄 JIRA 티켓 생성 요청 종료")  # 요청 종료 로깅
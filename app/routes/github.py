import logging
import json
import os
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, Header

from app.services.slack_service import send_slack_message

# 로깅 설정 (DEBUG 레벨 활성화)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

# 📌 환경 변수에서 GitHub Webhook Secret 가져오기
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")


def verify_signature(request_body: bytes, signature_header: str):
    """GitHub Webhook Signature 검증"""
    if not GITHUB_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="❌ GITHUB_WEBHOOK_SECRET이 설정되지 않았습니다!")

    try:
        # GitHub 서명 생성 (HMAC SHA-256)
        secret = bytes(GITHUB_WEBHOOK_SECRET, "utf-8")
        expected_signature = "sha256=" + hmac.new(secret, request_body, hashlib.sha256).hexdigest()

        # GitHub이 보낸 서명과 비교
        if not hmac.compare_digest(expected_signature, signature_header):
            raise HTTPException(status_code=403, detail="🚨 Signature 검증 실패! Webhook 요청이 위조되었을 수 있음.")
    except Exception as e:
        logger.exception("❌ 서명 검증 중 오류 발생!")
        raise HTTPException(status_code=500, detail=f"❌ 서명 검증 오류: {str(e)}")


@router.post("/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None)  # GitHub에서 보낸 서명 헤더 가져오기
):
    """GitHub Webhook 엔드포인트 (서명 검증 및 JSON 파싱)"""

    try:
        # 요청 본문 가져오기
        body = await request.body()
        logger.debug(f"📥 요청 본문 (x_hub_signature_256): {x_hub_signature_256}")
        logger.debug(f"📥 요청 본문 (Raw Body): {body}")

        # 📌 서명 검증
        if x_hub_signature_256:
            verify_signature(body, x_hub_signature_256)
        else:
            raise HTTPException(status_code=400, detail="❌ X-Hub-Signature-256 헤더가 없습니다!")

        # 📌 JSON 데이터 로깅 및 파싱
        try:
            data = json.loads(body)
            logger.debug(f"📦 JSON 파싱 결과: {data}")
        except json.JSONDecodeError as e:
            logger.exception("❌ JSON 파싱 오류 발생!")
            raise HTTPException(status_code=400, detail=f"❌ JSON 파싱 오류: {str(e)}")

        # 📌 PR 이벤트 처리
        if data.get("action") == "opened":
            try:
                pr_title = data["pull_request"]["title"]
                pr_url = data["pull_request"]["html_url"]
                pr_author = data["pull_request"]["user"]["login"]

                logger.info(f"🚀 PR 처리 중: {pr_title} by {pr_author}")

                # Slack 메시지 전송
                await send_slack_message(pr_title, pr_url, pr_author)

            except KeyError as e:
                logger.exception("❌ PR 데이터에서 필요한 키가 없습니다!")
                raise HTTPException(status_code=400, detail=f"❌ PR 데이터 오류: {str(e)}")

        return {"message": "✅ GitHub Webhook 요청 수신 완료!"}

    except Exception as e:
        logger.exception("🔥 서버 내부 오류 발생!")
        raise HTTPException(status_code=500, detail=f"🔥 서버 오류: {str(e)}")
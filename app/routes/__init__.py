from .github import router as github_router
from .slack import router as slack_router

# 필요한 경우 라우터를 한 번에 가져올 수 있습니다.
routers = [github_router, slack_router]
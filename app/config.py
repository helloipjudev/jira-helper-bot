import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv(override=True)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_HELLO_IPJU_KEY = os.getenv("JIRA_PROJECT_HELLO_IPJU_KEY")
JIRA_PROJECT_PARTNER_KEY = os.getenv("JIRA_PROJECT_PARTNER_KEY")




class Settings(BaseSettings):
    SLACK_WEBHOOK_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

# 설정 객체 생성
settings = Settings()
